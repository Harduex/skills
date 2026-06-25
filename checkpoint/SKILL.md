---
name: checkpoint
description: Produces a self-contained handoff prompt capturing the current session's state — goal, decisions, progress, key files, next steps — to paste into a fresh session and continue seamlessly. Use when the context is getting long, before compacting, or when the user wants to continue this work in a new/clean session, or mentions "checkpoint" or "handoff".
---

Write a single self-contained checkpoint prompt that lets a fresh agent — with NONE of this conversation's context — resume exactly where we are. Output it as one fenced code block addressed to the next agent, and nothing else.

Capture only what the next session can't re-derive for itself:

- **Goal** — what we're achieving and why (the bigger picture).
- **State** — what's done, what's in progress right now, what's untouched.
- **Decisions & constraints** — choices already made and their rationale; what's off the table.
- **Key locations** — files/paths (with line refs), the branch, commands to build/run/test, env specifics.
- **Next steps** — the immediate next action(s), in order.
- **Gotchas** — pitfalls, dead ends, and surprises learned this session.
- **Open questions / blockers** — anything awaiting a decision or external input.

Be concrete — real names, paths, values — not vague summaries; point into the code rather than restating it. Drop any section that's genuinely empty instead of padding it. Keep it tight: enough to continue, no replay of the whole history.
