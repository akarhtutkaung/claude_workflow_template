#!/usr/bin/env python3
"""
Stop hook: writes a session log to .claude/log/<date>-<session_id>.md
Receives JSON on stdin with session_id and transcript_path.
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

def _parse_transcript(transcript_path: str) -> dict:
    user_messages = []
    tool_calls = []
    assistant_snippets = []

    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg = entry.get("message", {})
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "user":
                if isinstance(content, str) and content.strip():
                    user_messages.append(content.strip()[:300])
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text = block.get("text", "").strip()
                            if text:
                                user_messages.append(text[:300])

            elif role == "assistant":
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict):
                            if block.get("type") == "tool_use":
                                tool_calls.append(block.get("name", "unknown"))
                            elif block.get("type") == "text":
                                text = block.get("text", "").strip()
                                if text:
                                    assistant_snippets.append(text[:300])
                elif isinstance(content, str) and content.strip():
                    assistant_snippets.append(content.strip()[:300])

    return {
        "user_messages": user_messages,
        "tool_calls": tool_calls,
        "assistant_snippets": assistant_snippets,
    }


def extract_summary(transcript_path: str) -> dict:
    """Parse the JSONL transcript, retrying briefly if the file hasn't been flushed yet."""
    empty = {"user_messages": [], "tool_calls": [], "assistant_snippets": []}
    for _ in range(5):
        try:
            result = _parse_transcript(transcript_path)
            if result["user_messages"] or result["assistant_snippets"]:
                return result
            # File exists but has no message content yet — wait and retry
            time.sleep(1)
        except (OSError, IOError):
            time.sleep(1)
    return empty


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        sys.exit(0)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    session_id: str = data.get("session_id", "unknown")
    transcript_path: str = data.get("transcript_path", "")

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S UTC")
    short_id = session_id[:8] if len(session_id) >= 8 else session_id

    # Resolve log directory relative to this script's location
    script_dir = Path(__file__).parent
    log_dir = script_dir.parent / "log"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"{date_str}-{short_id}.md"

    summary = extract_summary(transcript_path) if transcript_path else {}

    user_messages = summary.get("user_messages", [])
    tool_calls = summary.get("tool_calls", [])
    assistant_snippets = summary.get("assistant_snippets", [])

    lines = [
        f"# Session Log",
        f"",
        f"| Field       | Value |",
        f"|-------------|-------|",
        f"| Session ID  | `{session_id}` |",
        f"| Date        | {date_str} |",
        f"| Time        | {time_str} |",
        f"| Transcript  | `{transcript_path or 'n/a'}` |",
        f"",
    ]

    if user_messages:
        lines += ["## User Requests", ""]
        for i, msg in enumerate(user_messages, 1):
            # Collapse newlines for compact display
            compact = " ".join(msg.split())
            lines.append(f"{i}. {compact}")
        lines.append("")

    if tool_calls:
        # Deduplicate while preserving order
        seen = {}
        for t in tool_calls:
            seen[t] = seen.get(t, 0) + 1
        lines += ["## Tools Used", ""]
        for name, count in seen.items():
            lines.append(f"- `{name}` × {count}")
        lines.append("")

    if assistant_snippets:
        lines += ["## Assistant Summary (last response excerpt)", ""]
        # Take the last assistant snippet as the closing summary
        last = assistant_snippets[-1]
        compact = " ".join(last.split())
        lines.append(f"> {compact}")
        lines.append("")

    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()