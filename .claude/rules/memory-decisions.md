# Project Decisions

Architectural and design decisions made during this project, with dates.

<!-- Claude: update this file immediately when a decision is confirmed. Include date and rationale. No permission needed. -->

## 2026-04-30

- **Multiplier lives on `bets`, not `rounds`** — each player picks their own multiplier; `rounds.max_multiplier` caps it.
- **`round_exclusions` is a first-class table** — mid-round number exclusion is auditable and reversible.
- **Commitment hash scheme** — winning number is pre-generated at round creation; SHA-256(number || secret || round_id) stored in `rounds.commitment_hash` for transparency verification at draw time.
- **`token_grants` as a complete ledger** — includes `balance_before`, `balance_after`, `grant_type`, `note`; negative amounts represent deductions.
- **`min_number` / `max_number` replaces `number_range`** — explicit range boundaries rather than a single ambiguous integer.
- **Session logging via Stop hook** — `.claude/scripts/log-session.py` writes per-session logs to `.claude/log/`.
- **Memory files in `.claude/rules/`** — flat markdown files auto-loaded each session; no RAG or embeddings needed.