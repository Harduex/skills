---
name: save-learned-lessons
description: Capture durable lessons from the current session — user preferences, project conventions, gotchas, and reusable techniques — and route each to its right home (the memory system, project/global CLAUDE.md or AGENTS.md, or an existing/new custom skill). Use when the user wants to save lessons, capture what was learned, or mentions "save learned lessons".
---

# Save Learned Lessons

Review this session and extract the durable lessons worth keeping — things that
help a future session, not one-off details. Look for:

- **Corrections & preferences** the user gave (how they want work done, tools, tone).
- **Project facts & constraints** you discovered that aren't obvious from code or git.
- **Gotchas** — non-obvious failures, footguns, or environment quirks you resolved.
- **Reusable techniques** — an approach that worked and would apply again.

Skip anything already recorded, derivable from code/CLAUDE.md/git, or relevant
only to this one conversation.

For each lesson, pick exactly one destination:

| Lesson type | Destination |
|---|---|
| User preference, feedback, project/reference fact | Your memory system — one file per fact in its documented format, plus a pointer in the memory index |
| Preference that applies to *every* project | Global `~/.claude/CLAUDE.md` |
| Convention specific to *this* project | The project's `CLAUDE.md` / `AGENTS.md` |
| Reusable technique for a domain | The most relevant existing custom skill — update it. Create a new skill only if none fits. |

When a lesson is really a whole repeatable *workflow* that warrants its own skill — not a single fact — use the extract-a-workflow-into-a-skill capability in your set rather than hand-rolling it here.

Before writing, check for an existing entry that already covers the lesson and
update it instead of duplicating.

Then present every proposed change grouped by destination — path plus the exact
text to add or edit — and wait for approval. On approval, apply the changes and
report what changed.
