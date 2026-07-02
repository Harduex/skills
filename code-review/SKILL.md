---
name: code-review
description: Reviews code changes for correctness, security, test coverage, and design quality, producing severity-tagged findings. Supports local changes, specific commits, or GitLab merge requests. Use when user requests a code review, asks to review a diff, branch, commits, or MR — or asks to post, publish, or clean up review findings as inline MR comments. Never pushes to remote; never posts comments without user approval.
---

# Code Review

**NEVER push, force-push, or write to any remote/origin branch. All remote operations are read-only.**

**Core rule: read full files, not just diffs, and catalog the sibling patterns before judging new code (Step 2). A diff-only review is pattern matching, and sibling asymmetry is the defect class it reliably misses.**

## Step 0: Ask the user what to review

When invoked, **always ask the user** which review mode they want before proceeding:

> What would you like me to review?
>
> 1. **Local changes** — unstaged, staged, or full branch diff against main
> 2. **Specific commits** — one or more commit SHAs or a range
> 3. **GitLab merge request** — review an MR by URL or number
>
> (Or describe what you'd like reviewed and I'll figure it out.)

Wait for the user's answer. If the user already specified what to review when invoking the skill, skip the question and infer the mode. Then proceed based on their choice:

### Mode 1: Local changes
- Run `git status` and `git branch --show-current` to orient
- **Unstaged**: `git diff`
- **Staged**: `git diff --cached`
- **Full branch diff**: `git diff main...HEAD` and `git log main..HEAD --oneline`

### Mode 2: Specific commits
- Ask for the SHA(s) or range (e.g. `abc123`, `abc123..def456`, `HEAD~3..HEAD`)
- Use `git show <sha>` for single commits or `git diff <range>` for ranges
- Use `git log --oneline <range>` to understand the sequence of changes

### Mode 3: GitLab merge request
- Accept a full URL or just a MR number (e.g. `!142`)
- Use `glab mr view <number>` to read the MR description and metadata
- Use `glab mr diff <number>` to get the diff
- Fetch the source branch locally if needed: `git fetch origin <branch>` (read-only fetch only)
- Review against the MR's target branch, not just main
- Fetch the existing MR discussion **before** reviewing: `glab mr note list <iid>` (the REST `/discussions` endpoint misses GitLab Duo notes). Build an exclusion list — do not re-report findings already raised in the comments — and use the thread to learn intent and decisions already made

## Step 0.5: Scope large reviews into modules

**Do not attempt a single full-diff review across a large branch.** Attention thins, real issues get missed, and the review degenerates into pattern matching. Before executing, assess the size of the change and split if it's too big to hold in one pass.

### When to split

Rough thresholds — split if **any** apply:
- More than ~20 changed files
- More than ~5 commits, especially if they span clearly different concerns
- The diff spans multiple layers (data, server, client, tests, infra) that can be reviewed independently

### How to split

Derive the logical modules **from the actual diff**, not from a fixed list — the right modules depend on the feature. Read the file paths, commit messages, and dependency graph to identify the natural seams the change creates. A small feature may need only 2 modules; a sprawling refactor may split into 7. Modules don't have to match folder structure — group by the concern each set of changes implements.

Propose the modular plan to the user **before** starting:

> This branch touches N files across M commits. From the diff, the logical modules look like:
> 1. <module derived from the diff>
> 2. <module derived from the diff>
> 3. <module derived from the diff>
>
> Want me to review each in turn, or do you have a different split in mind?

Wait for confirmation, then review each module in its own pass. Findings stay grouped by module so the user can act on them incrementally.

### Optional prep: rebase into self-contained commits

If the existing commits don't already align with logical modules (e.g. a "WIP" commit spans multiple concerns, or fixup commits are scattered), offer to rebase the branch first so each commit **is** a self-contained module. Then review per commit using **Mode 2**.

Pattern:
```bash
# stage related changes for one logical module
git add <files for module A>
git commit --fixup=<target-commit-for-module-A>

# repeat for each module, then autosquash
GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash <base>^
```

This produces a clean per-commit history that is also easier for human reviewers. The user must approve any rebase that rewrites already-pushed commits. After rebase, the branch needs a force-push — **never run that yourself**, the user pushes.

### Cross-module concerns

Some issues span modules (a data-layer change the client depends on, a contract that affects both ends of a request). Note them during the module they originate in, and re-verify when reviewing the dependent module. Do **not** create a separate "cross-cutting" pass — it duplicates the per-module work.

## Execute the review

Follow these steps in order. Do not skip steps.

### 1. Understand intent before judging code

Read commit messages (`git log main..HEAD`) or ask the user what the change is trying to accomplish. A review without understanding intent is just pattern matching.

If the branch, commits, or MR reference a tracker issue (e.g. Jira `CLOUD-1234`), fetch that issue and read its **acceptance criteria** — that is the ground-truth definition of intent, and it lets you check the diff against what was actually asked for (missing ACs are a common defect class the code alone won't reveal).

### 2. Read full files, not just diffs

For every changed file, read the complete file (or at minimum the surrounding function/component). Diffs hide context — you need to understand what the changed code interacts with.

**Context patterns to check:**
- If a component is changed, check the surfaces that consume it for how it's actually used
- If a database migration is changed, verify the down-migration reverses the up-migration in strict LIFO order
- If a typed schema or contract is changed, check the generated type definitions and every call site whose shape depends on the change
- If reactive primitives are changed (effects, hooks, signals, subscriptions), check dependency declarations and cleanup paths
- **If the change introduces a new instance of a category that already has siblings** (e.g. a new entity type beside existing entity types, a new endpoint beside existing endpoints, a new processor beside existing processors), locate the sibling implementations and read them end-to-end before judging the new code. Catalog the sibling patterns first — naming, data shapes, integration points, where each concern lives — so you can spot deviations the new code makes. Asymmetric divergence from established sibling patterns is one of the most common defect classes in any codebase, and the diff alone won't reveal it.

Before reviewing, also read the consuming project's conventions documentation (`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, or equivalent) for project-specific constraints — pinned dependencies, banned framework patterns, architectural boundaries between services, asset and data conventions. The skill encodes review *principles*; the project's own docs encode the *facts* you need to apply them.

### 3. Check test coverage

- Are there tests for the changed behavior in `tests/`? If not, flag it.
- Do existing tests still cover the changed code paths, or have they been invalidated?
- Are the tests testing behavior (good) or implementation details (fragile)?
- Read the test files — do not assume tests are correct just because they exist.

### 4. Run available checks

Discover the project's lint, typecheck, and build commands from its `package.json` scripts, `Makefile`, `justfile`, build config, or equivalent. Run the ones that fit the change scope:
- **Lint** / **Format** — catches stylistic and convention issues
- **Type check** — catches type errors; note any relaxations (e.g. `strict: false`, `strictNullChecks: false` in TypeScript) because those mean the compiler won't catch entire classes of issues you'll need to spot manually
- **Build** — only for changes large enough to risk breakage

Report tool results but focus your review on what tools *cannot* catch.

### 5. Evaluate the change across these dimensions

- **Correctness**: Edge cases, null/undefined handling (no `strictNullChecks`!), race conditions, error propagation, async/await correctness
- **Security**: Injection vectors, auth/authz gaps, secrets in code, unsafe deserialization (see [REFERENCE.md](REFERENCE.md))
- **Design**: Does the change increase or decrease complexity? Is it in the right layer? Does it duplicate existing abstractions?
- **Pattern symmetry**: When the change introduces something new alongside existing siblings, does it follow the conventions those siblings established? Compare across every layer the new code touches — data shapes, naming, schema/type definitions, permissions, request/response shapes, UI placement and styling, error handling, server-vs-client responsibility split. Every divergence should be either deliberate (with a justification you can articulate) or flagged as a bug. Common asymmetry traps: stuffing typed fields into generic JSON blobs when siblings expose them as first-class typed fields; choosing a different pipeline/architecture than equivalent siblings without a clear reason; missing UI affordances that siblings have; reply/derivative endpoints that re-accept fields their parent already supplies; one-off naming when siblings share a convention. When the change mirrors an existing feature, enumerate the analog's surfaces (search its identifier) and diff the change against that list — absent surfaces are findings, not assumptions.
- **Readability**: Would a new team member understand this code without the commit message?
- **Consistency**: Does it follow the conventions the surrounding code already establishes — import paths/aliases, naming, file organization, and the rules the project's lint/format config enforces? Don't manually flag what the formatter or linter already catches; do flag patterns that are consistent across the codebase but not enforced by tooling.

### Project-specific red flags

Project-specific red flags live in the consuming project's conventions documentation (`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, or equivalent), not in this skill. Read that documentation before reviewing — typical contents include pinned dependency versions, banned framework patterns, architectural boundaries between services, asset/data conventions, and any "we tried this and it failed" lore. Apply those red flags during the review alongside the general dimensions above.

## Deliver findings

Structure every finding as:

```
**[F1] [SEVERITY] file_path:line_number — Short title**
Description of the issue and why it matters.
Suggested fix (if you have one).
```

Prefix each finding with a short stable ID (`F1`, `F2`, …) so the user can answer by id and ask follow-up questions about a specific finding without re-quoting it.

Severity levels:
- **BLOCKER** — Must fix before merge. Bugs, security issues, data loss risk.
- **ISSUE** — Should fix. Design problems, missing tests, unclear logic.
- **SUGGESTION** — Optional improvement. Better naming, simpler approach, minor readability.
- **NITPICK** — Take it or leave it. Style, formatting, personal preference.
- **PRAISE** — Highlight good work. Elegant solution, solid test, good refactoring.

### Rules for good feedback

- Frame critiques as questions: "Would it be clearer if..." not "This is wrong."
- Every BLOCKER and ISSUE must include a concrete suggestion or code sketch.
- Include at least one PRAISE if the change has any merit. Do not fabricate praise.
- Do not flag things the linter already catches — just report the lint results.

## Publishing findings as MR comments

Only when the user asks — and **never post anything the user hasn't seen and approved**. MR comments are outward-facing; a flood of them reads as spam and is unpleasant to clean up.

1. **Triage first.** Do not propose every finding from the report — re-filter with senior judgment down to the findings genuinely worth an inline comment (real bugs, data integrity, user-visible defects). Drop speculative findings (no repro, low confidence), nitpicks, hygiene items, and likely-intentional design tradeoffs. A handful of sharp comments lands better than full coverage. Re-fetch the MR discussion right before drafting — the thread may have grown since the review — and drop any finding already raised there by anyone (human, Duo, or a previous Claude pass): never duplicate an existing comment.
2. **Keep each comment short.** 2–5 sentences: what's wrong, why it matters, concrete fix. No essays, no evidence dumps — the reviewer has the code right there.
3. **Show drafts, then wait.** Present every draft with its anchor (`file:line` plus the code on that line). Apply the user's corrections and re-show what changed. Post only after an explicit go-ahead, and only the approved set.
4. **Verify after posting** — never trust the POST alone; see the verification paragraph below. Report the verified anchors back to the user.

**Convention:** every Claude-authored comment starts with the line `🤖 **Claude review · <SEVERITY>**`. It identifies machine-authored comments at a glance and doubles as the cleanup key (delete by sweeping `/notes` for bodies starting with the marker).

**Mechanics live in [REFERENCE.md](REFERENCE.md#publishing-mechanics-gitlab):** anchor verification against the fetched MR `head_sha` (never the local tree), the nested-JSON POST (`glab api -f` silently drops `position`), post-verification (`DiffNote` + non-null position), and replying to GitLab Duo threads. Follow them exactly — wrong anchors post "successfully" as misplaced noise.

## Acting on review feedback

When you implement a finding from a reviewer — human or automated:

- **A suggested fix is a hypothesis, not an instruction — and can be worse than the bug.** Verify its full effect before applying, *including the rollback / undo path*. Automated reviewers especially reason without full context (they may not see function bodies, lockfiles, or the data model), so a confidently-worded fix — e.g. a destructive schema change that doesn't cleanly reverse — can introduce a new defect while "addressing" the finding.
- **Scope the fix to exactly what was asked; don't generalize a narrow comment.** "Tighten the permissions on these two fields" means those two fields — not the whole permission set. Over-applying a scoped instruction to adjacent code is a common way to add a regression while resolving a valid comment. When tempted to widen the change, confirm scope with the reviewer first.
- **Check the tool's native capability before scripting around it.** A flaky CLI call gets a documented flag or supported mode — not a hand-rolled retry/backoff loop.

## Finish with a summary

End the review with:

1. **Verdict**: Approve, Request Changes, or Needs Discussion
2. **One-line summary**: What this change does well and what needs attention
3. **Risk assessment**: Low / Medium / High — based on blast radius and confidence in test coverage

For the full security checklist and review psychology guidelines, see [REFERENCE.md](REFERENCE.md).
