#!/usr/bin/env python3
"""Generate weekly Markdown reports from Claude Code JSONL logs."""

import argparse
import collections
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys


TOOL_ID = "cc"
TOOL_NAME = "Claude Code"
WEEKDAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

STOP_WORDS = set(
    """
    the a an is are was were be been being have has had do does did will would
    should can could of to in for on with at by from as into through during
    before after above below between out off over under again further then once
    here there when where why how all each every both few more most other some
    such no nor not only own same so than too very and but or if because until
    while about against this that these those i me my we our you your he him
    his she her it its they them their what which who whom much many
    的 了 在 是 我 有 和 就 不 人 都 一个 上 也 很 到 说 要 去 你 会 着 没有
    这 那 这个 那个 什么 怎么 可以 已经 还 因为 所以 但是 如果 对 用 给 从
    需要 应该 可能 进行 通过 使用 关于 问题
    """.split()
)

RE_CHINESE_WORDS = re.compile(r"[\u4e00-\u9fff]{2,6}")
RE_ENGLISH_WORDS = re.compile(r"[a-zA-Z]{3,}")


def extract_text(content):
    """Extract text from Claude Code message.content."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
        return "\n".join(parts)
    return ""


def is_real_user_message(text):
    stripped = (text or "").strip()
    if not stripped:
        return False
    if stripped == "[Request interrupted by user]":
        return False
    if stripped.startswith("# AGENTS.md") or stripped.startswith("# CLAUDE"):
        return False
    if stripped.startswith("/") and len(stripped.split()) <= 2:
        return False
    if stripped.startswith("<") and not stripped.startswith("<http"):
        if re.match(r"^<[a-zA-Z0-9_-]+>.*</[a-zA-Z0-9_-]+>\s*$", stripped, re.DOTALL):
            return False
        if len(stripped) < 200:
            return False
    return True


def parse_timestamp(value):
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def derive_project_name(cwd, fallback="unknown"):
    if cwd:
        name = Path(str(cwd).rstrip("/")).name
        return name or "unknown"
    if fallback:
        name = Path(str(fallback)).stem
        return name or "unknown"
    return "unknown"


def read_jsonl(path):
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def scan_messages(input_dir):
    messages = []
    base = Path(input_dir)
    if not base.is_dir():
        raise FileNotFoundError(f"input directory does not exist: {input_dir}")

    for path in sorted(base.rglob("*.jsonl")):
        for obj in read_jsonl(path):
            if obj.get("type") != "user":
                continue
            message = obj.get("message") or {}
            if message.get("role") != "user":
                continue
            text = extract_text(message.get("content", ""))
            if not is_real_user_message(text):
                continue
            timestamp = parse_timestamp(obj.get("timestamp"))
            if not timestamp:
                continue
            messages.append(
                {
                    "timestamp": timestamp,
                    "project": derive_project_name(obj.get("cwd"), path.parent.name),
                    "text": text.strip(),
                }
            )

    return sorted(messages, key=lambda item: item["timestamp"])


def parse_week_string(value):
    match = re.match(r"^(\d{4})-W(\d{1,2})$", value or "")
    if not match:
        raise ValueError("week must use YYYY-WNN format, for example 2026-W15")
    year, week = int(match.group(1)), int(match.group(2))
    if not 1 <= week <= 53:
        raise ValueError("week number must be between 1 and 53")
    return year, week


def week_start_end(year, week):
    start_date = dt.date.fromisocalendar(year, week, 1)
    start = dt.datetime.combine(start_date, dt.time.min, tzinfo=dt.timezone.utc)
    return start, start + dt.timedelta(days=7)


def week_label(year, week):
    return f"{year}-W{week:02d}"


def current_week():
    today = dt.datetime.now(dt.timezone.utc).date()
    iso = today.isocalendar()
    return iso.year, iso.week


def get_all_weeks(messages):
    return sorted({(item["timestamp"].isocalendar().year, item["timestamp"].isocalendar().week) for item in messages})


def extract_keywords(texts, top_n=12):
    counter = collections.Counter()
    try:
        import jieba  # type: ignore
    except ImportError:
        jieba = None

    for text in texts:
        if jieba:
            words = jieba.lcut(text)
            for word in words:
                normalized = word.strip().lower()
                if len(normalized) >= 2 and normalized not in STOP_WORDS:
                    counter[normalized] += 1
            continue

        for match in RE_CHINESE_WORDS.finditer(text):
            word = match.group()
            if word not in STOP_WORDS:
                counter[word] += 1
        for match in RE_ENGLISH_WORDS.finditer(text):
            word = match.group().lower()
            if word not in STOP_WORDS:
                counter[word] += 1

    return counter.most_common(top_n)


def clean_text(text):
    return re.sub(r"\s+", " ", text.replace("\r", " ").replace("\n", " ")).strip()


def render_markdown(year, week, device, messages):
    start, end = week_start_end(year, week)
    label = week_label(year, week)
    project_counter = collections.Counter(item["project"] for item in messages)
    active_days = {item["timestamp"].date().isoformat() for item in messages}
    all_texts = [item["text"] for item in messages]

    lines = [
        f"# {TOOL_NAME} Weekly Summary - {label}",
        "",
        f"- Source: {TOOL_NAME}",
        f"- Device: {device}",
        f"- Week: {label}",
        f"- Date range: {start.date().isoformat()} to {(end - dt.timedelta(days=1)).date().isoformat()}",
        "",
        "## Overview / 概览",
        "",
        f"- User messages: {len(messages)}",
        f"- Active days: {len(active_days)} / 7",
        f"- Projects: {len(project_counter)}",
        "",
        "## Project Stats / 项目统计",
        "",
        "| Project | Messages | Share | Active Days | Top Keywords |",
        "|---|---:|---:|---:|---|",
    ]

    total = len(messages) or 1
    by_project = collections.defaultdict(list)
    for item in messages:
        by_project[item["project"]].append(item)

    for project, count in project_counter.most_common():
        project_messages = by_project[project]
        days = {item["timestamp"].date().isoformat() for item in project_messages}
        keywords = extract_keywords([item["text"] for item in project_messages], top_n=5)
        keyword_text = ", ".join(word for word, _ in keywords) if keywords else "-"
        lines.append(f"| {project} | {count} | {round(count / total * 100)}% | {len(days)} | {keyword_text} |")

    lines.extend(["", "## Keywords / 高频关键词", ""])
    keywords = extract_keywords(all_texts)
    lines.append(", ".join(f"{word} ({count})" for word, count in keywords) if keywords else "_No keywords extracted._")

    lines.extend(["", "## Messages / 用户消息", ""])
    by_day = collections.defaultdict(list)
    for item in messages:
        by_day[item["timestamp"].date().isoformat()].append(item)

    for offset in range(7):
        current = start + dt.timedelta(days=offset)
        day = current.date().isoformat()
        lines.extend([f"### {day} ({WEEKDAY_NAMES[offset]})", ""])
        day_messages = by_day.get(day, [])
        if not day_messages:
            lines.extend(["_No user messages._", ""])
            continue
        for item in day_messages:
            time_text = item["timestamp"].strftime("%H:%M")
            lines.append(f"- `{time_text}` [{item['project']}] {clean_text(item['text'])}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def save_report(output_dir, year, week, device, content):
    week_dir = Path(output_dir) / week_label(year, week)
    week_dir.mkdir(parents=True, exist_ok=True)
    path = week_dir / f"{TOOL_ID}-{device}.md"
    path.write_text(content, encoding="utf-8")
    return path


def generate_for_week(input_dir, output_dir, device, year, week):
    messages = scan_messages(input_dir)
    start, end = week_start_end(year, week)
    week_messages = [item for item in messages if start <= item["timestamp"] < end]
    if not week_messages:
        return None
    content = render_markdown(year, week, device, week_messages)
    return save_report(output_dir, year, week, device, content)


def build_parser():
    parser = argparse.ArgumentParser(description="Generate weekly reports from Claude Code JSONL logs.")
    parser.add_argument("--input-dir", required=True, help="Directory containing Claude Code JSONL files.")
    parser.add_argument("--output-dir", default="reports", help="Output directory for Markdown reports.")
    parser.add_argument("--device", choices=["sample", "air", "pro"], default="sample", help="Device label.")
    parser.add_argument("--week", help="ISO week, for example 2026-W15.")
    parser.add_argument("--all", action="store_true", help="Generate all weeks found in the input directory.")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.week and args.all:
        parser.error("--week and --all cannot be used together")

    messages = scan_messages(args.input_dir)
    if not messages:
        print("No user messages found.")
        return 1

    if args.all:
        weeks = get_all_weeks(messages)
    elif args.week:
        weeks = [parse_week_string(args.week)]
    else:
        weeks = [current_week()]

    generated = []
    for year, week in weeks:
        start, end = week_start_end(year, week)
        week_messages = [item for item in messages if start <= item["timestamp"] < end]
        if not week_messages:
            continue
        content = render_markdown(year, week, args.device, week_messages)
        generated.append(save_report(args.output_dir, year, week, args.device, content))

    if not generated:
        print("No reports generated for the selected week range.")
        return 0

    for path in generated:
        print(f"Report generated: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

