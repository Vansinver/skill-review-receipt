# Skill Review Receipt

**把 AI 提出的 Skill 修改变成可读、可复制、可带走的审核回执。**

> Status: Alpha · 当前提供 Hermes 适配器。通用导入和其他工具适配器尚未实现。

## 为什么做它

AI 助手有时会在会话后提出新增或修改 Skill。提案不等于值得长期保留：它可能只适用于一次对话、与现有内容重复，或带来额外维护成本。这个插件把 Hermes 已暂存的 Skill 写入整理成审核材料，方便用户自己判断，或带到另一个 AI 工具继续讨论。

它只读取 Hermes 的待审队列。面板没有批准、拒绝或写入 Skill 的操作。

## 当前功能

- 在 Hermes Desktop 面板查看待审 Skill 写入。
- 选择建议并展开查看具体内容。
- 复制 Markdown 回执，或导出到 `HERMES_HOME/reports/skill-reviews/`。
- 回执列出来源编号、时间、摘要、变更内容和供后续讨论的问题。

## 安装

需要 Hermes CLI 和支持桌面插件的 Hermes Desktop。当前 Alpha 尚未验证完整的 Hermes 版本兼容范围。

```bash
hermes plugins install Vansinver/skill-review-receipt
```

安装时按提示启用插件，再重启 Hermes gateway；桌面端重新加载后，在面板中打开 **Skill 建议回执**。如面板未出现，请检查 `hermes plugins list` 和 Hermes Desktop 插件加载提示。

> 桌面插件的发现方式会随 Hermes 版本变化。若此安装方式在你的版本中不可用，请提交脱敏后的版本信息和错误提示。

## 数据与权限

- 插件没有云端服务，不会自行把队列内容发送到第三方。
- 插件读取当前 Hermes 后端的 `pending/skills/` 队列；连接远程后端时，队列和导出文件位于远程环境。
- 复制或导出的回执可能包含候选 Skill 的具体文本。分享前请检查并删去个人信息、内部路径和秘密。
- Hermes 后端插件以 Hermes 当前用户权限运行。只从信任的来源安装，并先检查代码。
- 插件不会启用 background review，也不会修改写入审批配置。

## 产品边界

当前版本只接 Hermes 已有的待审写入队列，不负责生成建议，也不是跨工具 Skill 管理器。其他 AI 工具即使没有插件入口，也可以在后续通过通用回执格式和人工粘贴/导入接入；这部分尚未实现。

## 路线

1. **0.1 — Hermes 回执适配器**：只读面板、复制和 Markdown 导出。
2. **0.2 — 通用回执导入**：粘贴或导入其他 AI 工具导出的 Markdown/JSON。
3. **后续 — 审核证据**：探索重复候选识别、经历来源和有无 Skill 的对照评估。
4. **后续 — 其他适配器**：按用户需求添加，不预设每个 AI 都有插件入口。

## 相关项目

本项目不宣称首创 Skill 演化或审批流程。相邻项目与本项目的定位边界记录在 [docs/RELATED_WORK.md](docs/RELATED_WORK.md)。

## License

[MIT License](LICENSE)。
