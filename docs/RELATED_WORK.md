# 相关项目与定位记录

检索日期：2026-10-11。此页是初步定向检索，不是穷尽式竞品调查。

## 相邻项目

- [skill-evolution](https://github.com/Carlo1911/skill-evolution)：分析近期 Hermes/Claude Code 会话并形成 Skill 提案；默认人工审阅，包含评估门槛。与“会话经历 → 提案 → 人工把关”链路高度相邻。
- [OpenGlasses Skill Self-Evolution](https://github.com/straff2002/OpenGlasses/blob/main/docs/plans/skill-self-evolution.md)：记录了从失败/纠正中提出 Skill，并由 Suggested Skills inbox 批准、编辑或忽略的流程。
- [Skill RSI](https://github.com/justinwetch/Skill-RSI)：Codex 插件方向，比较 Skill 变体的任务表现，并把晋级决策连到具体评估证据。
- [Skill Deck](https://github.com/Hccake/skill-deck)：跨平台 Skill 发现、安装、浏览、更新和 Agent 关联管理。
- [Skill Manager](https://github.com/abubakarsiddik31/skill-manager)：跨工具 Skill 浏览、编辑、启停、安装和安全扫描。
- [Agent Skills 评估指南](https://github.com/agentskills/agentskills/blob/main/docs/skill-creation/evaluating-skills.mdx)：建议将有 Skill 与无 Skill 的运行对照，并记录输出、评分和运行指标。
- [Agent Skills 规范](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx)：规定可携带的 Skill 文件结构；各客户端的发现位置和集成方式仍由具体实现决定。
- [SkillsVote 研究](https://arxiv.org/abs/2605.18401)：讨论 Skill 收集、推荐、演化和证据门控。

## 定位结论

“自动进化 Skill”“审批建议”“管理跨工具 Skill”都已有项目或研究覆盖。单纯再做一个生成器或管理器，差异不足。

本项目当前聚焦在更窄的一层：读取已有待审建议，不应用变更，生成一个可复制、可导出、可交给另一位审阅者讨论的回执。跨工具适配不是已有功能；第一阶段先用人工粘贴/文件导入作为低成本路径，再看用户需求决定是否做自动连接器。

## 公开表述边界

可以说“为 Hermes 待审 Skill 写入提供回执 UI”。目前不应说“第一个”“通用所有 AI 工具”或“自动判断 Skill 是否有用”。
