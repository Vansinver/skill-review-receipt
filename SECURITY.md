# 安全与隐私说明

Skill Review Receipt 是 Hermes 用户插件。Hermes 后端插件由当前用户进程导入运行，拥有该进程可访问文件和资源的权限；不要把它当作沙箱代码。

## 数据处理

- 读取当前 Hermes profile 的 `pending/skills/*.json`。
- 复制操作把选中的提案内容放入系统剪贴板。
- 导出操作在当前 Hermes 后端的 `reports/skill-reviews/` 中新增 Markdown 文件。
- 插件代码本身不调用外部模型、远端 API 或遥测服务。
- 如果桌面端连接远程 Hermes，后端数据和导出文件在远程主机，不是在本机。

回执可能包含用户数据、项目路径或机密文本。分享前请人工检查和脱敏。

## 不在插件功能里的操作

插件不批准、拒绝、删除或应用待审项；不写入 Skill；不更改 background review、nudge 或 write approval 配置。

## 报告漏洞

公开仓库正式建立后，在此补充维护者的私下安全联系渠道。在此之前，请勿向公开 issue 粘贴真实待审记录或敏感回执。
