# Claude Workflow Template

A drop-in `.claude/` directory template that gives Claude Code persistent memory, automatic session logging, and a reflection nudge — without any external services or embeddings.

## What's included

```
.claude/
├── rules/
│   ├── memory-profile.md      # Facts about you (role, background)
│   ├── memory-preferences.md  # How you like things done
│   ├── memory-decisions.md    # Architectural decisions with dates
│   └── memory-sessions.md     # Substantive work per session
├── scripts/
│   ├── log-session.py         # Stop hook: writes per-session log
│   └── reflect-nudge.sh       # Stop hook: prompts reflection after fixes/discoveries
├── log/                       # Auto-generated session logs (gitignored)
└── settings.json              # Hook wiring
CLAUDE.md                      # Instructions Claude loads on every session
```

## How it works

**Persistent memory** — The four `rules/` markdown files are loaded into Claude's context at the start of every session via `CLAUDE.md`. Claude is instructed to update them in real time as it learns about you, your preferences, and your decisions — no manual syncing required.

**Session logging** — A `Stop` hook runs `log-session.py` when Claude finishes responding. It parses the session transcript and writes a structured markdown log to `.claude/log/` with user requests, tools used, and the final assistant response.

**Reflect nudge** — A second `Stop` hook runs `reflect-nudge.sh`. If the session contained fixes, workarounds, or discoveries, it surfaces a reminder to run `/reflect` and capture learnings in the project docs.

## Setup

1. Copy the `.claude/` directory and `CLAUDE.md` into your project root.

2. Update the script paths in `.claude/settings.json` to match your project:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /absolute/path/to/.claude/scripts/log-session.py"
          },
          {
            "type": "command",
            "command": "bash /absolute/path/to/.claude/scripts/reflect-nudge.sh"
          }
        ]
      }
    ]
  }
}
```

3. Open the project in Claude Code. The memory files and hooks will be active immediately.

## Customizing the memory files

Each file in `rules/` is plain markdown. Claude writes to them automatically, but you can edit them directly at any time to seed facts, correct stale info, or remove entries that no longer apply.

| File | What to put in it |
|------|-------------------|
| `memory-profile.md` | Your role, tech stack familiarity, team context |
| `memory-preferences.md` | Style rules, tooling preferences, things Claude should avoid |
| `memory-decisions.md` | Key architectural choices and the date they were made |
| `memory-sessions.md` | High-level summary of completed work per session |

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- Python 3 (for `log-session.py`)
- Bash (for `reflect-nudge.sh`)

## License

MIT — see [LICENSE](LICENSE).