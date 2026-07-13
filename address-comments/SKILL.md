---
name: address-comments
description: "Validates and addresses reviewer feedback on the current branch's merge/pull request — comments fetched from GitLab or GitHub via their CLIs (glab, gh), or pasted into the chat. Use when asked to fetch, read, or check MR/PR review comments, validate whether they are real concerns worth fixing, implement or answer them, reply to review threads, or when the user pastes reviewer comments or a list of feedback items to address. Also for analyzing an MR/PR discussion to recommend a course of action."
---

# Address Review Comments

The receiving side of code review: turn reviewer feedback on a merge/pull request into verified verdicts, scoped fixes, and approved replies. (The authoring side — reviewing someone else's diff — belongs to your set's code-review capability; if your set has a receiving-code-review discipline skill, invoke it alongside this one.)

**Core rule: every comment — human or bot — is a falsifiable hypothesis, not an instruction. Validate its premises against the real code before any verdict, fix, or reply.** Bot reviewers reason without full context (they don't see function bodies, config flags, lockfiles); a confidently-worded suggested fix can introduce the exact bug it claims to prevent. The mirror also holds: your verdicts are proposals — an "invalid" ruling can be flipped by team agreements the repo doesn't record, so let the user overrule without friction.

## Intake modes

1. **Fetched** — comments live on the MR/PR; you fetch them with the forge CLI (default when the user says "the MR/PR comments").
2. **Pasted** — the user pastes comments or a feedback list into the chat (see "Pasted comments" below).
3. **Decision support** — analyze one discussion thread and recommend a course of action, no fixes yet.

## Phase 1 — Locate the MR/PR and baseline

- Detect the forge from `git remote -v` and use its CLI: `glab` (GitLab) or `gh` (GitHub). Trust live state: `git branch --show-current`, never a session-start snapshot or a prior session's assumption. Both CLIs resolve the current branch's MR/PR with no argument (`glab mr view` / `gh pr view`). If the user names a ticket or branch that doesn't match what you find, ask — don't go hunting across repos.
- Before trusting any line anchor, verify the review baseline: compare the MR/PR head SHA against local `HEAD`. If they differ, `git fetch` and read the branch via `git show origin/<branch>:<path>` — never validate a comment against code the reviewer didn't see. Commands: [REFERENCE.md](REFERENCE.md).

## Phase 2 — Fetch and inventory

- **No single endpoint returns every comment kind.** GitLab's REST `/discussions` silently omits bot reviewer notes; GitHub splits feedback across inline review comments, review summaries, and conversation comments. Sweep the forge's full set (per-forge cookbook in [REFERENCE.md](REFERENCE.md)) and reconcile your inventory against the MR/PR's visible comment count before concluding "no comments".
- Inventory every unresolved thread plus general non-threaded notes, honoring any author filter the user gave. Skip system/activity notes. Note per item: author, file:line anchor, resolved state, and the thread/comment ID needed for replying.

## Phase 3 — Validate each comment

- Read the anchored file and every premise the comment relies on (compiler strictness flags, dependency arrays, sibling corpus, the SQL or config it refers to). Suggestion blocks span a line *range* — read the whole range, not just the anchor line.
- **Read the comment's scope exactly.** A comment anchored on one block means that block — widening a narrow ask ("trim these lists" ≠ "trim the whole file") is how valid comments turn into regressions. When tempted to widen, ask first.
- Classify with evidence: `valid` / `valid but latent` / `invalid (state why, with file:line proof)` / `already handled` / `question — answer only, no code change`.

## Phase 4 — Report, then gate

Report **item by item: quote the original comment verbatim, then your verdict, evidence, and proposed action directly beneath it.** A thematic summary or bare table is not acceptable as the primary format. Tag every item with a short stable ID (C1, D1…) so the user can reply by ID. End with a recommendation, then ask which items to act on — include "reply explaining why" as the offered disposition for anything not fixed, and don't bake "drop the invalid ones" into the options: the user may want a harmless fix anyway.

**Nothing is edited before the user picks scope** — unless the opening instruction already authorized fixing (e.g. "apply the valid ones"), in which case fix but still gate everything outward.

## Phase 5 — Fix

- Invoke the relevant domain skills before editing; search for existing helpers before writing new ones; fix in the file the comment anchors to unless there's a stated reason not to.
- One commit per comment/concern (so replies can cite SHAs), following the repo's commit-message convention. At branch close, fold review-fix commits into their originating commits via your set's fixup-distribution capability if the branch convention is linear history.
- Verify by exercising the changed behavior (run the affected tests, drive the flow) — green typecheck/lint is not verification, and note that a root tsconfig often excludes test directories, so a clean `tsc` on test files may have checked nothing.

## Phase 6 — Reply and hand back

- Draft a reply for every thread the user asked to answer: fixed → what changed + commit SHA; not fixed → why; question → the answer. Triage: banners, LGTMs, and already-conceded threads need no reply.
- Show all drafts and **post only after explicit approval — approval to fix is not approval to post.** If replies cite commit SHAs, the push (also approval-gated) must happen first so the SHAs resolve.
- Reply conventions: user-voice threads start with the model name (`<Model>: …`) so authorship is visible; bot threads must *start* with the bot's @-mention (e.g. `@GitLabDuo`) or the bot never sees the reply. Per-forge mechanics and post-verification: [REFERENCE.md](REFERENCE.md).
- **Never mark threads resolved** — that's the reviewer's/author's call. Hand back with threads open, push pending, and a per-ID summary of dispositions.
- No hacky workarounds anywhere in this flow: a `403`/insufficient-scope means the token lacks write scope — tell the user; burst rate-limits mean prefer native CLI subcommands over raw API loops.

## Pasted comments

When the user pastes feedback instead of pointing at an MR/PR, the paste is the authorization boundary and its inline annotations override any prior severity call. Parse each item's contract:

| Paste shape | Contract |
|---|---|
| Plain item ("Fix the vN badge") | Fix it |
| Parenthetical condition ("(only if not symmetric with X)") | Check the condition first; fix only if it holds |
| Question ("why does this return two shapes?") | Explain, don't touch code until asked |
| "Investigate…" + symptom | Root-cause it — never mask the symptom with defensive code |

Pasted items carry no thread anchors: locate the code yourself, keep the paste's own ordering/numbering in your report, and validate exactly as in Phase 3. If the paste references a thread you can access, fetch the authoritative discussion anyway for attribution and full context. Replies usually don't apply (nothing to post to) — verdicts and fixes are the deliverable.

## Decision support

For "should we do this now / postpone / is the reviewer right": fetch the real thread, read the code both sides argue about, and decide on mechanism facts (not effort feelings). Sharpen the user's framing when the evidence warrants it — "decline with a revisit condition" is often truer than "postpone". Draft any thread reply in the user's own voice (they're the participant), double-gated as in Phase 6.
