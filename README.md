# Agent Trace Reporter

`Agent Trace Reporter` is a local-first CLI tool that converts AI coding session logs into weekly Markdown reports.

## Why This Exists

AI coding work often lives in local session traces, not only in final commits. Prompts contain task context, execution boundaries, debugging paths, failed attempts, constraint changes, and final decisions.

Agent Trace Reporter turns those local traces into weekly Markdown reports grouped by week, project, and device. The goal is to make AI coding work searchable, reviewable, and reusable without uploading private logs.

This project is useful for prompt reuse, workflow review, failure analysis, and building a personal data layer around AI-assisted development. This public repository contains only fictional sample data.

## What It Does

- Parses Claude Code JSONL logs.
- Parses Codex JSONL logs.
- Filters system messages and keeps real user requests.
- Groups messages by ISO week, project, and device.
- Infers project names from `cwd`.
- Generates Markdown weekly reports.
- Outputs project statistics and frequent keywords.

## Quick Start

This repository does not contain any real session logs. The commands below read only the fictional data under `samples/`.

```bash
python claude_weekly_summary.py --device sample --input-dir samples/claude-code --output-dir sample-reports --week 2026-W15
python codex_weekly_summary.py --device sample --input-dir samples/codex --output-dir sample-reports --week 2026-W15
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Sample Output

- [Claude Code sample report](sample-reports/2026-W15/cc-sample.md)
- [Codex sample report](sample-reports/2026-W15/cd-sample.md)

## What This Demonstrates

This repository demonstrates:

- Local review tooling for AI coding workflows.
- Agent trace parsing and structuring.
- Data preparation for failure analysis.
- Local data processing boundaries.
- Developer-tool design tradeoffs and privacy boundaries.

## Privacy Boundary

- **Local-first**: the tool processes local files only.
- **No upload**: it does not upload session logs.
- **No real logs in public repo**: this public repository does not include real Claude Code or Codex session records.
- **Sample data only**: `samples/` and `sample-reports/` contain only fictional content.
- **Disposable generated reports**: the default output directory, `reports/`, is ignored by `.gitignore` and can be deleted at any time.

See [docs/privacy-boundary.md](docs/privacy-boundary.md) for more detail.

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

Arguments:

- `--input-dir`: JSONL input directory. The demo uses `samples/`.
- `--output-dir`: Markdown output directory. Defaults to `reports/`.
- `--device`: device label. Allowed values are `sample`, `air`, and `pro`.
- `--week`: ISO week, such as `2026-W15`.
- `--all`: generates reports for every week found in the input data.

## License

MIT License. See [LICENSE](LICENSE).
