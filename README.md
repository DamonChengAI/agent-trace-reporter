# Agent Trace Reporter

Agent Trace Reporter 是一个 local-first CLI 工具，用于把 AI Coding session logs 转换成按周聚合的 Markdown 复盘报告。

Agent Trace Reporter is a local-first CLI tool that converts AI coding session logs into weekly Markdown reports.

## 为什么做这个项目

AI Coding 的关键产出经常分散在 Claude Code / Codex 的本地 session trace 里：需求澄清、调试路径、失败尝试、约束变化和最终决策都可能只存在于对话记录中。

这个项目把这些 trace 转换成按周、项目和设备聚合的 Markdown 报告，用于个人复盘、面试展示和开发者工具产品思考。它不上传本地日志，公开仓库只包含虚构 sample data。

## 它能做什么

- 解析 Claude Code JSONL logs
- 解析 Codex JSONL logs
- 过滤系统消息，只保留真实用户请求
- 按 ISO week、project、device 聚合
- 根据 `cwd` 推断项目名
- 生成 Markdown 周报
- 输出项目统计和高频关键词

## Quick Start

本仓库不包含任何真实 session log。下面的命令只读取 `samples/` 里的虚构数据。

```bash
python claude_weekly_summary.py --device sample --input-dir samples/claude-code --output-dir sample-reports --week 2026-W15
python codex_weekly_summary.py --device sample --input-dir samples/codex --output-dir sample-reports --week 2026-W15
```

运行测试：

```bash
python -m unittest discover -s tests
```

## Sample Output

- [Claude Code sample report](sample-reports/2026-W15/cc-sample.md)
- [Codex sample report](sample-reports/2026-W15/cd-sample.md)

## Privacy Boundary

- local-first：工具只处理本地文件。
- no upload：不会上传 session log。
- no real logs in public repo：公开仓库不包含真实 Claude Code / Codex 会话记录。
- sample data only：`samples/` 和 `sample-reports/` 只包含虚构内容。
- generated reports are disposable：默认输出目录 `reports/` 被 `.gitignore` 忽略，用户可以随时删除。

更多说明见 [docs/privacy-boundary.md](docs/privacy-boundary.md)。

## Interview Relevance

这个仓库用于展示：

- AI Coding workflow 的本地复盘能力
- Agent Trace 解析和结构化能力
- failure analysis 的数据准备思路
- local data processing 的工程边界
- 面向开发者工具的产品判断和隐私设计

## CLI Usage

Claude Code:

```bash
python claude_weekly_summary.py --device sample --input-dir samples/claude-code --output-dir sample-reports --week 2026-W15
python claude_weekly_summary.py --device sample --input-dir samples/claude-code --output-dir sample-reports --all
```

Codex:

```bash
python codex_weekly_summary.py --device sample --input-dir samples/codex --output-dir sample-reports --week 2026-W15
python codex_weekly_summary.py --device sample --input-dir samples/codex --output-dir sample-reports --all
```

参数：

- `--input-dir`：JSONL 输入目录，demo 使用 `samples/`
- `--output-dir`：Markdown 输出目录，默认 `reports/`
- `--device`：设备标签，允许 `sample`、`air`、`pro`
- `--week`：指定 ISO week，例如 `2026-W15`
- `--all`：生成输入数据里的所有周

## English Version

Agent Trace Reporter is a local-first CLI tool that turns AI coding session logs into weekly Markdown reports.

Why it exists: AI coding work often lives inside session traces rather than final commits alone. Requirements, debugging steps, failed attempts, and product decisions are scattered across local logs. This project structures those traces into a weekly review grouped by week, project, and device.

What it does:

- parses Claude Code JSONL logs
- parses Codex JSONL logs
- filters system messages
- groups messages by ISO week, project, and device
- generates Markdown reports
- extracts project stats and frequent keywords

Privacy model:

- local-first processing
- no upload
- no real logs in this public repository
- sample data only
- disposable local reports

