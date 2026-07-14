---
name: autonomous-build-loop
description: Drives a whole feature from a short prompt to merge-ready with minimal supervision — derives a machine-checkable done-contract, plans and executes tasks in a build→test→verify cycle, and persists all state to files on disk so the work survives context compaction and resumes cleanly in a fresh session. Use when asked to autonomously build or implement a feature/ticket end-to-end, run an unattended build loop, drive a plan to completion across sessions, or "just build X" with little hand-holding. Composes your set's requirements, planning, test-authoring, review, verification, debugging, and git-hygiene workflows by capability per phase instead of duplicating them; stops for the human at every irreversible action.
---

# Autonomous Build Loop

A loop that **drives a feature from prompt to merge-ready on its own** — it plans, builds, tests, and verifies in cycles, keeps its state in files so a fresh session resumes exactly where the last stopped, and pauses for you only at irreversible actions. It *orchestrates* your other workflows when they exist and *falls back* to built-in procedures when they don't — so it composes in a rich harness and still runs standalone in a bare one. Its own machinery (contract, state, cycle, checker, retry, checkpoint) needs nothing beyond a shell, git, and file access.

**Link by capability, not by name.** Each phase below names a *capability* ("a planning workflow", "a verification workflow"). Invoke whatever skill in your current set provides it — discover it from the available skill descriptions at runtime. Names drift between projects; capabilities don't. If your set lacks one, use the built-in fallback for that phase ([REFERENCE.md](REFERENCE.md) → Standalone fallbacks) — the loop is self-sufficient and requires no other skill installed.

**Bind capabilities → skills at the orchestrator, then pass names down.** A capability phrase does not self-fire. Resolve it once, up front, where you (the orchestrator) can see the full skill list, then bake the concrete `invoke <name>` into each dispatched agent's prompt. A subagent silently skips a vague "use a planning workflow"; it won't skip a named instruction. If nothing matches, do the step inline.

## When to use

A multi-step feature or ticket you want driven end-to-end from a short prompt. **Not** a trivial one-file change (just make it) and **not** vague/unspecced work (spec it first — the loop refuses to start without a checkable contract). Needs the ability to write files; a subagent/parallel-dispatch tool makes the checker far stronger (single-context is the fallback).

## Setup — once per task

1. **Spec.** Invoke your set's requirements-interrogation / idea-validation capability until the goal is unambiguous. Do not proceed on assumptions.
2. **Contract.** Turn the spec into a **machine-checkable done-list**: every item backed by a command with an exit code (`pnpm test`, `tsc --noEmit`, a demoable acceptance check). Reject any item you can't express as a check — a vague goal can never halt the loop. Your test-planning capability feeds this.
3. **State.** Scaffold `docs/loop/<slug>/` deterministically with `scripts/init.sh <slug>` — it stamps out `contract.md`, `plan.md`, `journal.md` (schemas in [REFERENCE.md](REFERENCE.md)) and refuses to clobber an existing loop. Fill `plan.md` via your planning capability: an orientation header (goal, key paths, build/test commands) plus ordered, self-contained tasks each carrying a status (`todo|doing|done|blocked`). Use your checkpoint/handoff capability to write that header — it's the self-contained orientation a fresh agent reads first.

## One cycle — repeat until the contract is green

1. **Read state.** Re-read `plan.md` and the tail of `journal.md` from disk. Trust the files, not memory or session-start context.
2. **Pick** the next unblocked task.
3. **Build.** Invoke the capability-right skill(s) for it (the domain workflow for the area; functional-core principles). Author tests first: red → green.
4. **Commit.** One local commit per task. Reversible, so allowed without asking.
5. **Check** — run `scripts/check.sh <slug>` (executes the contract's declared commands, pass/fail per item) or dispatch a fresh-context subagent to review. Deterministic execution *or* fresh eyes — never self-grade in the working context.
6. **Record.** Append the measured result to `journal.md`; flip the task's status in `plan.md`.
7. **On failure**, log the error *and the contract line it broke*; route to your debugging capability; retry bounded (≤3), each retry carrying the error forward — never re-run the same failing prompt verbatim. Still failing → escalate to the human.
8. **Gate.** Contract fully green → stop, summarize, refresh the `plan.md` header for handoff. Otherwise → next cycle.
9. **Irreversible boundary** — push, open a PR, deploy, delete, publish, post comments → **STOP and ask.** Autonomy budget is not approval budget.

## Non-obvious policy — why this loop, not a naive one

- **L1 — The contract must be exit-code-checkable.** "Improve X" can't halt; "`test` exits 0" can. No un-checkable done-items.
- **L2 — Check in fresh context.** An agent grading its own work in the same window brings the same blind spots in; verification needs fresh eyes or a deterministic command.
- **L3 — Autonomy ≠ approval.** Run unattended through reversible actions; stop at every irreversible/outward one. Inherit the project's approval boundary — don't invent a looser one.
- **L4 — State lives on disk, not the transcript.** Anything only in context is gone at the first compaction. Read-at-start, write-each-cycle.
- **L5 — Retries carry the error, are bounded, and escalate.** A verbatim re-prompt loops forever; three informed attempts then a human.
- **L6 — Every cycle logs a measured result.** An unmeasured "done" is a vibe. `journal.md` records the check output, not a claim.
- **L7 — The plan is a hypothesis; the code wins.** When execution contradicts a plan step, stop, note it in `journal.md`, and re-derive — don't force a step you can see is wrong.

## Capabilities by phase

Prefer the matching skill in your set (by its description). If none exists, use that phase's built-in fallback in [REFERENCE.md](REFERENCE.md) — the loop runs fully standalone.

| Phase | Capability to invoke |
|---|---|
| Spec | requirements interrogation; idea validation |
| Contract | test-case planning; design-spec (its contract section) |
| Plan / state | task planning & breakdown; checkpoint/handoff (writes the orientation header) |
| Per-task research | codebase research (trace the code paths the task touches) |
| Build | the domain workflow for the area; functional-core / immutability principles |
| Test | test-first authoring (write the failing test before the code) |
| Check | verification — run the gates, evidence over claims; formal verification for provable invariants |
| On failure | systematic debugging (root cause before patch) |
| Pre-handoff | git-history hygiene — linearize commits / distribute fixups; leak audit before any publish |
| Recurrence | feed repeated failures back into your design-spec and test-planning workflows |

## What the loop hands to the human, never loops on

Product/UX judgment ("should this exist at all?"), anything not expressible as an exit-code check, and every irreversible action. Surface these as decisions; don't spin on them.

See [REFERENCE.md](REFERENCE.md) for the state-file schemas, the contract format with examples, the resume protocol, the checker-dispatch mechanics, and the failure-mode catalog.
