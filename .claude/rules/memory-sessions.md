# Session History

Substantive work completed per session.

<!-- Claude: add an entry here when completing meaningful work. One bullet per session is enough. No permission needed. -->

## 2026-04-30

- Reviewed README.md with Backend Architect agent; rewrote database schema and API endpoints section — added `round_exclusions` table, per-bet multiplier, `scheduled_start`/`scheduled_end`, commitment hash, full token ledger, CHECK constraints, FK ON DELETE rules, and 14 missing API endpoints.
- Created `CLAUDE.md` with project overview, architecture, bet lifecycle, and command templates.
- Added session logging: `.claude/scripts/log-session.py` + Stop hook in `.claude/settings.json`.
- Added auto-memory system: `.claude/rules/memory-*.md` files + reflect-nudge Stop hook.