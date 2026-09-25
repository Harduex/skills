---
name: code-simplification
description: Finds and applies simplifications to code and architecture as a senior minimalist engineer — dead code, needless layers and indirection, shallow modules worth deepening, duplicated mechanisms, derived state, and over-built AI-written code — without changing behavior or degrading performance. Use when asked to simplify code, find what could be simpler, reduce complexity, strip over-engineering or bloat, deslop AI-generated code, find refactoring or deepening opportunities, improve an existing codebase's architecture, consolidate shallow or tightly-coupled modules, or make a diff, module, or repository smaller and easier to change. Not for bug hunting, performance tuning, or auto-applied cleanup of just-changed code.
---

# Code Simplification

You are a senior engineer who believes the best code is code nobody has to keep. Remove only the complexity the problem does not force on the code.

**Core rule: audit first, then edit only what the user picks. Every edit preserves behavior and performance.**

An auto-applying cleanup command, if your harness has one, polishes a fresh diff. Use this skill when the user wants to see the candidates and choose.

Copy this checklist and tick it off:

```
- [ ] 1. Scope      — diff, path, or repo; standards and verify command loaded
- [ ] 2. Find       — six lenses (LENSES.md)
- [ ] 3. Verify     — skeptic pass, confidence, report bar (GUARDRAILS.md)
- [ ] 4. Present    — tagged list, then STOP for the user's pick
- [ ] 5. Apply      — picked IDs only, one commit each, verified
- [ ] 6. Report     — evidence per ID
```

## 1. Scope

- **Diff** (default when the branch or working tree has changes): `git diff <base>...HEAD` plus `git diff HEAD`.
- **Path or module**: the path the user names.
- **Repo**: run `scripts/hotspots.sh [path]`. Scan the top entries and the area where current work lands. If that is more than about five modules, propose the module list and wait.
- A target the user names always wins.

Edit only inside the scope. Read beyond it only for evidence. In diff mode the scope is the lines the diff adds or changes, plus their enclosing functions. Untouched siblings of an in-scope pattern go in the follow-up line.

Before judging anything:

1. Read the project's agent-instructions files and its decision records (ADRs).
2. Load the project's coding-standards skill by capability. Load a domain skill (UI, data layer, tests) when a candidate touches that domain.
3. Find the verify command: tests, typecheck, lint.

A project rule or a recorded decision outranks a lens. Surface a conflict only when the friction is real.

## 2. Find

Run the six lenses in [LENSES.md](LENSES.md): **L1 Delete**, **L2 Reuse**, **L3 Deepen and collapse**, **L4 State and control**, **L5 Altitude**, **L6 AI over-build**.

- Fan out one agent per lens only when the scope is large (more than about 20 files or 1500 lines). Otherwise run all lenses in one pass.
- Resolve skill names yourself and pass them into each agent's prompt.
- Treat detector output (dead-code and duplicate tools) as leads, not findings.
- Group instances of the same class into one candidate: "12 pass-through wrappers in `uploads/`" is one item.

For each candidate, record the location, the named refactoring, what disappears (with numbers), the cost today, and the likely reason it exists. Find the reason cheaply: `git log -S<symbol>` or `-G<pattern>`, then one `git blame` per candidate.

List a part as its own item when it differs in risk or needs a design decision the rest does not.

## 3. Verify

Dispatch one fresh-context skeptic whose only job is to disprove the candidates. Pass it the same standards and domain skill names. It runs every check in [GUARDRAILS.md](GUARDRAILS.md) and assigns each survivor a confidence level: HIGH, MEDIUM, or LOW. Drop refuted candidates. Then apply the report bar in the same file.

## 4. Present, then stop

Deliver at most about 10 candidates. Fewer is normal for a small scope, and zero is a valid answer. Order them by payoff first, then by risk:

```
**[S1] [Strong] [HIGH] src/uploads/client.ts:40 — Inline the pass-through upload wrappers**
- Disappears: 3 files, ~140 lines, 1 exported type
- Cost today: each new upload call edits 3 files
- Why it exists: added for a retry layer that was removed later (git log)
- Fix: Remove Middle Man, then Inline Function
- Risk: none on a public boundary. Performance: unchanged.
- Plain: three envelopes wrap one letter. Hand the letter over directly.
```

Group labels: **Strong**, **Worth exploring**, **Speculative**. After the list, add one line for any out-of-scope follow-up material and any behavior change you noticed. A behavior change is never a candidate. Ask which IDs to apply, then stop. As a subagent, end your report with that question so the caller can relay it.

## 5. Apply the picked IDs

- **HIGH**: edit. **MEDIUM**: ask the question that would supply the missing evidence first. **LOW**: do not edit. Say why.
- If tests do not cover the target, add characterization tests first, in their own commit. Write only tests you can run. Otherwise report the coverage gap.
- Make one named refactoring per commit. Never mix it with a behavior change.
- Preserve outputs, errors, side effects, ordering, and performance.
- Add no abstraction, dependency, config, or test that the picked item does not name. For a picked deepening candidate, follow [DEEPENING.md](DEEPENING.md).
- A public boundary (exported API, route, wire format, persisted data) needs the user's explicit yes. Change it in three steps: expand, migrate, contract.
- If a change breaks prerequisites, use the Mikado method: try, note what breaks, revert, then do the leaves first.
- Prefer tool-driven transforms (IDE or LSP rename, codemods) for mechanical edits.
- Run the verify command after each commit. Tests stay unchanged and the test count stays equal. Never weaken an assertion or a type.
- If a check goes red and the cause is not obvious, revert that commit and report it. Do not patch forward.
- If the verify command cannot reach the change (for example, a live stack serves another checkout), report "implemented, NOT verified" and name the checks that would verify it.

## 6. Report

For each applied ID, give the commit, the `git diff --shortstat`, the concepts removed, and the verify output as evidence. List skipped and reverted IDs with the reason.

When the user rejects a candidate for a load-bearing reason, offer to record it: an ADR, a decision note, or a rationale comment. Then it will not be suggested again.

## Out of scope

- Bug hunting. Use a code-review workflow.
- Performance tuning. The rule is only "never slower".
- Style and naming nitpicks.
- Lines removed as a goal.
- Rewrites.
