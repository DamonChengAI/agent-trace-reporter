# Privacy Boundary / 隐私边界

## 中文

Agent Trace Reporter 的默认边界是 local-first：它处理用户显式传入的本地 JSONL 文件，并在本地生成 Markdown 报告。

本公开仓库只包含虚构 sample data。真实 Claude Code / Codex 会话记录、真实报告、运行日志、真实项目路径、真实 prompt、公司信息、个人隐私和生产凭证都不应该进入 Git。

设计原则：

- 工具只读取 `--input-dir` 指定的本地目录。
- `samples/` 只包含虚构项目和虚构请求。
- `sample-reports/` 由虚构 sample data 生成。
- 默认输出目录 `reports/` 被 `.gitignore` 忽略。
- 用户可以随时删除输出目录，不影响原始 session log。
- 如果后续增加 Web UI，必须继续保留 local-first 模式，或在上传前提供显式确认。

这个仓库的重点不是收集数据，而是展示如何在隐私边界内把 AI Coding trace 转换成可复盘的工程产物。

## English

Agent Trace Reporter is designed as a local-first tool. It reads local JSONL files explicitly provided through `--input-dir` and writes Markdown reports to a local output directory.

This public repository contains sample data only. Real AI coding logs, real reports, runtime logs, local project paths, real prompts, company information, personal information, and production credentials should not be committed.

Principles:

- read only the directory provided through `--input-dir`
- keep public samples fully fictional
- keep generated `reports/` out of Git
- let users delete generated output at any time
- preserve local-first behavior if a Web UI is added later, or require explicit confirmation before upload

