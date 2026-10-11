import { jsx, jsxs } from 'react/jsx-runtime'
import { useEffect, useState } from 'react'

const ID = 'skill-review-receipt'

function SkillReviewPane({ ctx }) {
  const [items, setItems] = useState([])
  const [selected, setSelected] = useState([])
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  async function refresh() {
    setLoading(true)
    setError('')
    try {
      const data = await ctx.rest('/queue')
      const next = Array.isArray(data?.items) ? data.items : []
      setItems(next)
      setSelected(next.map(item => item.id))
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { void refresh() }, [])

  const chosen = items.filter(item => selected.includes(item.id))
  const request = { ids: chosen.map(item => item.id) }
  const button = 'rounded-md border border-(--ui-border) px-2.5 py-1.5 text-xs hover:bg-(--ui-surface-hover) disabled:opacity-50'
  const small = 'text-xs text-(--ui-text-tertiary)'

  async function copyReceipt() {
    if (!chosen.length) return
    setBusy(true); setError(''); setNotice('')
    try {
      const result = await ctx.rest('/receipt', { method: 'POST', body: request })
      const ok = await ctx.os.writeClipboard(result.markdown)
      if (!ok) throw new Error('剪贴板写入失败')
      setNotice(`已复制 ${chosen.length} 条建议的回执，可粘贴到 GPT 继续讨论。`)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally { setBusy(false) }
  }

  async function exportReceipt() {
    if (!chosen.length) return
    setBusy(true); setError(''); setNotice('')
    try {
      const result = await ctx.rest('/export', { method: 'POST', body: request })
      setNotice(`回执已保存：${result.path}`)
      await ctx.os.revealPath(result.path)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally { setBusy(false) }
  }

  return jsxs('div', { className: 'flex h-full min-h-0 flex-col gap-3 overflow-hidden p-3 text-sm', children: [
    jsxs('div', { className: 'flex items-start justify-between gap-2', children: [
      jsxs('div', { children: [jsx('div', { className: 'font-semibold', children: 'Skill 建议回执' }), jsx('div', { className: small, children: `${items.length} 条待审建议 · 只读整理` })] }),
      jsx('button', { className: button, type: 'button', onClick: () => void refresh(), disabled: loading || busy, children: '刷新' })
    ]}),
    jsx('div', { className: 'flex flex-wrap gap-2', children: [
      jsx('button', { className: button, type: 'button', onClick: () => setSelected(items.map(item => item.id)), disabled: !items.length || busy, children: '全选' }),
      jsx('button', { className: button, type: 'button', onClick: () => setSelected([]), disabled: !selected.length || busy, children: '清空' }),
      jsx('button', { className: button, type: 'button', onClick: () => void copyReceipt(), disabled: !chosen.length || busy, children: busy ? '处理中…' : '复制回执' }),
      jsx('button', { className: button, type: 'button', onClick: () => void exportReceipt(), disabled: !chosen.length || busy, children: '导出 Markdown' })
    ]}),
    notice ? jsx('div', { className: 'rounded-md bg-(--ui-surface-raised) p-2 text-xs', children: notice }) : null,
    error ? jsx('div', { className: 'rounded-md border border-red-500/30 p-2 text-xs text-red-500', children: error }) : null,
    loading ? jsx('div', { className: small, children: '正在读取本地待审队列…' }) : null,
    !loading && items.length === 0 ? jsx('div', { className: small, children: '当前没有待审 Skill 建议。' }) : null,
    jsxs('div', { className: 'min-h-0 flex-1 space-y-2 overflow-y-auto', children: items.map(item => jsxs('article', { className: 'rounded-lg border border-(--ui-border) p-2.5', children: [
      jsxs('label', { className: 'flex cursor-pointer items-start gap-2', children: [
        jsx('input', { type: 'checkbox', checked: selected.includes(item.id), onChange: event => setSelected(old => event.target.checked ? [...old, item.id] : old.filter(id => id !== item.id)) }),
        jsxs('span', { className: 'min-w-0 flex-1', children: [
          jsx('span', { className: 'block font-medium', children: item.summary || '未提供摘要' }),
          jsx('span', { className: `mt-1 block ${small}`, children: `${item.operations?.length ?? 0} 项操作 · ${item.origin} · ${item.id}` })
        ]})
      ]}),
      item.operations?.length ? jsxs('details', { className: 'mt-2 pl-5', children: [
        jsx('summary', { className: `${small} cursor-pointer`, children: `查看建议内容（${item.operations.length}）` }),
        jsxs('div', { className: 'mt-2 space-y-2', children: item.operations.map((op, index) => jsxs('div', { className: 'rounded bg-(--ui-surface-raised) p-2', children: [
          jsx('div', { className: 'font-medium', children: `${index + 1}. ${op.action} · ${op.name} / ${op.file_path}` }),
          op.old_string ? jsx('pre', { className: 'mt-2 max-h-40 overflow-auto whitespace-pre-wrap break-words text-xs', children: `原文：\n${op.old_string}\n\n建议替换：\n${op.new_string}` }) : null,
          op.content ? jsx('pre', { className: 'mt-2 max-h-48 overflow-auto whitespace-pre-wrap break-words text-xs', children: op.content }) : null
        ]}, `${item.id}-${index}`)) })
      ] }) : null
    ]}, item.id)) }),
    jsx('div', { className: `${small} border-t border-(--ui-border) pt-2`, children: '复制和导出只整理当前选择的队列内容，不会修改待审记录或 Skill 文件。' })
  ]})
}

export default {
  id: ID,
  name: 'Skill 建议回执',
  description: '只读查看待审 Skill 建议，复制或导出供人工讨论的 Markdown 回执。',
  defaultEnabled: true,
  register(ctx) {
    ctx.register({
      id: 'pane',
      area: 'panes',
      title: 'Skill 建议回执',
      data: { placement: 'right', width: '380px' },
      render: () => jsx(SkillReviewPane, { ctx })
    })
  }
}
