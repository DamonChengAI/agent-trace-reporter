# Design Notes / 设计说明

## 中文

## 为什么按周聚合

AI Coding 的复盘节奏天然适合按周组织。一天太碎，一个月又太长；周维度能把需求推进、调试过程、失败尝试和最终产出放在同一个上下文里。

## 为什么按项目统计

Agent session 往往跨多个项目。按项目聚合可以回答更有价值的问题：本周主要精力投向哪里，哪些项目出现了更多调试和迭代，哪些项目需要后续复盘。

## 为什么保留完整用户消息或可配置截断

用户消息是 AI Coding trace 里最接近真实意图的部分。它包含需求、约束、纠错、验收标准和上下文变化。MVP 默认完整保留 sample 消息；真实使用时可以在公开分享前自行删除或截断输出。

## 为什么过滤系统消息

系统消息和工具上下文通常噪声很高，并且可能包含环境信息。公开 showcase 更应该关注真实用户请求，所以脚本会过滤系统注入、IDE 上下文头部、中断提示和空消息。

## 和 AI Coding / Agent Trace 的关系

这个工具把 Claude Code / Codex 的本地 session trace 转换成可读的 review artifact。它不是 eval 平台，但可以作为 failure analysis、工作流复盘和后续 eval 数据准备的前置层。

## 当前局限

- 不评估代码质量。
- 不分析模型回答质量。
- 不上传云端。
- sample 版本只展示解析和报告生成能力。
- 对真实日志格式的兼容性采用保守策略：优先覆盖常见 JSONL 字段，不承诺覆盖所有历史变体。

## English

Weekly aggregation matches how developer work is usually reviewed. It is compact enough to preserve context and broad enough to capture meaningful progress, failures, and decisions.

Project-level stats matter because AI coding sessions often span multiple codebases. Grouping by project makes the report useful for workflow review instead of becoming a flat chat archive.

User messages are preserved because they contain intent, constraints, corrections, and acceptance criteria. System messages are filtered because they are noisy and may contain environment context.

This project is related to AI Coding and Agent Trace work because it turns raw local traces into reviewable artifacts. It does not evaluate code quality or model answer quality. The sample version demonstrates parsing and report generation only.

