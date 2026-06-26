---
name: analyze-agent-sessions
description: Use when reconstructing or documenting how something was built across past Claude Code agent sessions — mine the ~/.claude/projects transcripts (JSONL) for a feature, branch, or Jira ticket spanning many sessions and repos to produce an implementation workflow, a postmortem, a timeline, or a catalogue of where the agent went wrong and the human had to redirect. Also when asked to extract a reusable process from prior work, audit agent session activity, or (optionally) tally token/cost usage across sessions.
---

# Analyze Agent Sessions

Mine past Claude Code transcripts to reconstruct what actually happened across many sessions — then synthesize it into a documented workflow, postmortem, or timeline. Core moves: **discover the relevant transcripts, render them cheaply, fan out one subagent per phase, and anchor everything to git ground truth.** Transcripts alone are incomplete — always reconcile against commits.

Bundled helpers (hand these to every subagent by path; never re-read raw JSONL):
- `scripts/index_sessions.py <files…>` — chronological index: `ts | short-id | gitBranch | user-turns | first real message`.
- `scripts/render_session.py <file>` — one transcript → grep-friendly text (full turns, tool calls as one-liners, results/thinking truncated).

## When to use

- "Document the whole workflow of building X so I can reuse it" / postmortem / timeline of a feature.
- Find where the agent went wrong and the human had to redirect, across a feature's sessions.
- Extract a reusable process, or audit session activity, for a branch / Jira ticket spanning many sessions and repos.

When NOT to use: a single recent session (just read it); questions answerable from git history or docs alone.

## Workflow

### 1. Negotiate the deliverable (don't assume)
Where the output lives (a `maui-skills` skill / a project `docs/` doc / a personal note) and the focus (process-only, code-only, or **process as the spine + concrete changes**). Use your question tool.

### 2. Discover transcripts across every involved repo
Claude Code stores one folder per working directory under `~/.claude/projects/`, named by replacing `/` with `-` in the absolute path (`/home/me/proj` → `-home-me-proj`). Enumerate, then rank by relevance and apply a noise floor:
```bash
ls -1 ~/.claude/projects/                              # find the repo slugs (incl. the parent path)
D=~/.claude/projects
grep -c -iE "<JIRA>|\b<keyword>\b" "$D"/<slug>/*.jsonl | awk -F: '$2>=20{print $1}' > files.txt
python3 scripts/index_sessions.py $(cat files.txt)     # chronological, branch-keyed index
```
The **branch name is usually the strongest discriminator** (e.g. every relevant session has `br=<feature-branch>`); the Jira code and keyword rank candidates; `≥20` hits drops incidental mentions.

### 3. Partition curated sessions into phases
From the index, hand-pick the genuinely-relevant sessions and group them by phase/sub-feature (research, backend, UI, viewer, tests, MR reviews, regressions, wrap-up…). Assign each phase its specific session ids.

### 4. Fan out one subagent per phase
**REQUIRED SUB-SKILL for the fan-out:** superpowers:dispatching-parallel-agents. Keep the orchestrator's context clean — subagents do the reading. Give every agent an identical contract: the `render_session.py` path, its session ids, "render-then-grep, never `cat` raw JSONL," "ignore unrelated tangents," and this fixed output schema (cap ~350 lines, "never invent; cite session id + timestamp"):
```
## Sessions            (ids covered)
## What was accomplished
## Workflow / process
## Corrections & misses  ← PRIORITY. Per item:
   [nit|bug|regression|wrong-approach|missed-requirement] title
   • agent did … • why wrong … • how the human caught it (verbatim quote ≤25w) • resolution • session+ts
## Decisions / pivots
## Memorable user quotes
```
The "where the agent went wrong" thread is the priority — it is the reusable signal, not a feature changelog. Each agent greps its rendered file for friction:
```bash
grep -niE "no,|not |wrong|actually|revert|don'?t|instead|you missed|forgot|that'?s not|recheck|why did you|incorrect|mistake|broke|regression|undo|hold on|not what|misunderstood|should(n'?t| be)|hallucin" rendered.txt
```

### 5. Anchor to git ground truth, then reconcile
In **every** repo: `git log --reverse <base>..<branch>` and `git diff --stat <base>...<branch>`. Recover design/planning docs deleted from the branch tip straight from history: `git show <sha>:path`. Cross-check session dates against commit/ADR dates — if work predates the captured sessions, back-fill that phase from git rather than pretending the transcripts are complete.

### 6. Reduce into one document
Stitch the per-phase reports + git history into a chronological **spine** (a Phase | When | What | Skills table), then distill cross-cuts: a reusable playbook, plan→as-built pivots, a correction catalogue (recurring patterns / headline regressions / smaller misses), "what the human had to supply," harness improvements, and a copy/paste checklist. Append a session index citing ids + key SHAs. Show the draft; offer to promote it to a skill or render an Artifact.

## Pitfalls

- **Never `cat` raw JSONL** (~1MB+ each) — route through `render_session.py`. Smoke-test the renderer on one session (`wc -l`/`wc -c`) before fanning out.
- **`isSidechain` is unreliable** (uniformly false in some CC versions) — you can't use it to separate subagent traffic. Detect subagents via `Agent`/`Task` tool calls and the returning `task-notification` user turns.
- **Skip harness/meta first messages** (`<command-name>`, `Base directory for this skill`, `Caveat:`, `[Request interrupted`, lines `<15` chars) when reading a session's topic — both helper scripts already do.
- **Sessions interleave unrelated work** — instruct every subagent to ignore non-topic tangents; expect (and surface) a mis-scoped session.
- **Transcripts are incomplete** — earlier planning/design often predates the captured sessions. Git is ground truth; reconcile.
- **Live sessions are still being rewritten/compacted** — order/topic of the in-progress session can look off; analyze completed sessions.

## Optional: usage & cost metrics

Not part of the base reconstruction. If asked for token/cost/volume, add a pass over assistant entries' `usage.input_tokens`/`output_tokens`, or shell out to `ccusage`. **Dedupe by `message.id` first** — resume/fork/compact rewrite entries (~2× double-count); summing raw lines inflates totals.
