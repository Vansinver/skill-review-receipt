from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from hermes_constants import get_hermes_home

router = APIRouter()
_ID_RE = re.compile(r"^[a-fA-F0-9]{1,32}$")


class ReceiptRequest(BaseModel):
    ids: list[str] = Field(default_factory=list, max_length=500)


def _queue_dir() -> Path:
    return get_hermes_home() / "pending" / "skills"


def _records() -> list[dict[str, Any]]:
    root = _queue_dir()
    if not root.is_dir():
        return []
    records: list[dict[str, Any]] = []
    for path in root.glob("*.json"):
        try:
            if path.is_symlink() or path.resolve().parent != root.resolve():
                continue
            record = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(record, dict) or not _ID_RE.fullmatch(str(record.get("id", ""))):
                continue
            record["id"] = str(record["id"])
            records.append(record)
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
    records.sort(key=lambda r: _created_at(r))
    return records


def _created_at(record: dict[str, Any]) -> float:
    try:
        return float(record.get("created_at") or 0)
    except (TypeError, ValueError):
        return 0.0


def _operations(record: dict[str, Any]) -> list[dict[str, Any]]:
    payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
    raw = payload.get("operations") if payload.get("action") == "batch" else [payload]
    result = []
    for op in raw if isinstance(raw, list) else []:
        if not isinstance(op, dict):
            continue
        result.append({
            "action": str(op.get("action") or "unknown"),
            "name": str(op.get("name") or "未命名 Skill"),
            "file_path": str(op.get("file_path") or "SKILL.md"),
            "old_string": str(op.get("old_string") or ""),
            "new_string": str(op.get("new_string") or ""),
            "content": str(op.get("content") or op.get("file_content") or ""),
        })
    return result


def _public_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record["id"],
        "action": str(record.get("action") or ""),
        "summary": str(record.get("summary") or ""),
        "origin": str(record.get("origin") or "unknown"),
        "created_at": _created_at(record),
        "operations": _operations(record),
    }


def _select_records(ids: list[str]) -> list[dict[str, Any]]:
    requested = list(dict.fromkeys(str(item) for item in ids))
    if not requested:
        raise HTTPException(status_code=400, detail="请至少选择一条建议")
    if any(not _ID_RE.fullmatch(item) for item in requested):
        raise HTTPException(status_code=400, detail="建议编号格式无效")
    by_id = {record["id"]: record for record in _records()}
    missing = [item for item in requested if item not in by_id]
    if missing:
        raise HTTPException(status_code=409, detail=f"队列已变化，请刷新后重试：{', '.join(missing)}")
    return [by_id[item] for item in requested]


def _code_block(text: str) -> str:
    longest = max((len(match.group(0)) for match in re.finditer(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{text.rstrip()}\n{fence}" if text else "（空）"


def _build_receipt(records: list[dict[str, Any]]) -> str:
    created = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "# Skill 自进化建议回执", "",
        f"- 生成时间：{created}",
        f"- 建议条数：{len(records)}",
        "- 数据来源：Hermes 本地待审 Skill 写入队列",
        "- 处理状态：仅整理与展示；没有采纳、忽略或写入任何 Skill。", "",
        "> 回执记录系统提出了什么建议，不代表建议有用或应该保留。请结合实际使用频率、重复情况、替代方案和维护成本逐条判断。", "",
        "## 建议清单", "",
    ]
    for index, record in enumerate(records, 1):
        stamp = datetime.fromtimestamp(_created_at(record)).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        operations = _operations(record)
        lines.extend([
            f"### {index}. {record.get('summary') or '未提供摘要'}", "",
            f"- 队列编号：`{record['id']}`",
            f"- 提交时间：{stamp}",
            f"- 来源：{record.get('origin') or 'unknown'}",
            f"- 建议操作：{len(operations)} 项",
        ])
        for op_index, op in enumerate(operations, 1):
            lines.extend(["", f"#### 操作 {op_index}：{op['action']} — `{op['name']}`", f"- 文件：`{op['file_path']}`"])
            if op["action"] == "patch":
                lines.extend(["", "原内容：", _code_block(op["old_string"]), "", "建议替换为：", _code_block(op["new_string"])])
            elif op["content"]:
                lines.extend(["", "建议内容：", _code_block(op["content"])])
            elif op["action"] in {"remove_file", "delete"}:
                lines.extend(["", "这是删除建议；回执没有执行该操作。"])
        lines.append("")
    lines.extend([
        "## 可带去讨论的问题", "", "请逐条评估：",
        "1. 这条建议是否解决了反复出现、且值得复用的问题？",
        "2. 它是否与现有 Skill 重复，或只是一次性对话内容？",
        "3. 建议内容是否准确、范围是否过宽、后续维护成本是否合理？",
        "4. 结论应为保留、合并、暂缓观察还是舍弃？请说明依据。", "",
    ])
    return "\n".join(lines)


@router.get("/queue")
def get_queue() -> dict[str, Any]:
    return {"items": [_public_record(record) for record in _records()]}


@router.post("/receipt")
def preview_receipt(body: ReceiptRequest) -> dict[str, str]:
    return {"markdown": _build_receipt(_select_records(body.ids))}


@router.post("/export")
def export_receipt(body: ReceiptRequest) -> dict[str, str]:
    markdown = _build_receipt(_select_records(body.ids))
    output_dir = get_hermes_home() / "reports" / "skill-reviews"
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    target = output_dir / f"skill-review-receipt-{stamp}.md"
    suffix = 1
    while target.exists():
        target = output_dir / f"skill-review-receipt-{stamp}-{suffix}.md"
        suffix += 1
    temp = target.with_suffix(target.suffix + f".{os.getpid()}.tmp")
    try:
        temp.write_text(markdown, encoding="utf-8", newline="\n")
        temp.replace(target)
    finally:
        if temp.exists():
            temp.unlink()
    return {"markdown": markdown, "path": str(target)}
