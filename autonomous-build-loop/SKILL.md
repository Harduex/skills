---
name: autonomous-build-loop
description: Drives a whole feature from a short prompt to merge-ready with minimal supervision — derives a machine-checkable done-contract, plans and executes tasks in a build→test→verify cycle, and persists all state to files on disk so the work survives context compaction and resumes cleanly in a fresh session. Use when asked to autonomously build or implement a feature/ticket end-to-end, run an unattended build loop, drive a plan to completion across sessions, or "just build X" with little hand-holding. Composes your set's requirements, planning, test-authoring, review, verification, debugging, and git-hygiene workflows by capability per phase instead of duplicating them; stops for the human at every irreversible action.
---

# Autonomous Build Loop

Operate at a principal-engineer altitude: correctness and reversibility over speed, evidence over confidence, and the smallest change that satisfies the contract. Every rule below is that stance made checkable.

A loop that **drives a feature from prompt to merge-ready on its own** — it plans, builds, tests, and verifies in cycles, keeps its state in files so a fresh session resumes exactly where the last stopped, and pauses for you only at irreversible actions. It *orchestrates* your other workflows when they exist and *falls back* to built-in procedures when they don't — so it composes in a rich harness and still runs standalone in a bare one. Its own machinery (contract, state, cycle, checker, retry, checkpoint) needs nothing beyond a shell, git, and file access.

**Link by capability, not by name.** Each phase below names a *capability* ("a planning workflow", "a verification workflow"). Invoke whatever skill in your current set provides it — discover it from the available skill descriptions at runtime. Names drift between projects; capabilities don't. If your set lacks one, use the built-in fallback for that phase ([REFERENCE.md](REFERENCE.md) → Standalone fallbacks) — the loop is self-sufficient and requires no other skill installed.

**Bind capabilities → skills at the orchestrator, then pass names down.** A capability phrase does not self-fire. Resolve it once, up front, where you (the orchestrator) can see the full skill list, then bake the concrete `invoke <name>` into each dispatched agent's prompt. A subagent silently skips a vague "use a planning workflow"; it won't skip a named instruction. If nothing matches, do the step inline.

**Scripts stay in the skill; only state goes in the repo.** The three helper scripts ship *inside this skill* under `scripts/`. Invoke each by its path under this skill's base directory — written `$SKILL/scripts/…` below, where `$SKILL` is the directory the harness prints when the skill loads — with your working directory at the repo root. They write only to `docs/loop/<slug>/`, and nothing at all when bound to a substrate the repo already owns. **Never copy them into the project**: the containment boundary is the whole point — the tooling lives in the skill, and only the *state* is committed to the repo's `docs/`.

## When to use

A multi-step feature or ticket you want driven end-to-end from a short prompt. **Not** a trivial one-file change (just make it) and **not** vague/unspecced work (spec it first — the loop refuses to start without a checkable contract). Needs the ability to write files; a subagent/parallel-dispatch tool makes the checker far stronger (single-context is the fallback).

## Setup — once per task

1. **Bind the state substrate — before scaffolding anything.** The loop runs on four state roles: *orientation*, *task ledger*, *history*, *contract*. Resolve where each one lives, once, in this order: (a) a loop state directory already exists for this feature → **native**, stop; (b) the repo's agent instruction file points a new session at a continuation note that lives *inside* that state directory → **native**, stop; (c) it points at a distinct continuation note plus per-unit work slices → **adopted** — bind the four roles to those files, obey that convention's commit and cleanup rules, and scaffold nothing; (d) ambiguous → ask, once. Two continuation notes is not redundancy, it is a coin flip at every session start (L10). Role mapping, discovery probe, and adopted-mode invariants: [REFERENCE.md](REFERENCE.md) → *State substrates*.
2. **Spec.** Invoke your set's requirements-interrogation / idea-validation capability until the goal is unambiguous. Do not proceed on assumptions.
3. **Contract.** Turn the spec into a **machine-checkable done-list**: every item backed by a command with an exit code (`pnpm test`, `tsc --noEmit`, a demoable acceptance check). Reject any item you can't express as a check — a vague goal can never halt the loop. Your test-planning capability feeds this. For a **bug-fix** item, the contract also names its **baseline repro** — the observable failure to demonstrate on the unchanged code — so "done" is a red→green transition, not just a green check (L9).
4. **State.** *Native:* scaffold `docs/loop/<slug>/` deterministically with `$SKILL/scripts/init.sh <slug>` — it stamps out `contract.md`, `plan.md`, `journal.md` (schemas in [REFERENCE.md](REFERENCE.md)) and refuses to clobber an existing loop. Fill `plan.md` via your planning capability: an orientation header (goal, key paths, build/test commands) plus ordered, self-contained tasks each carrying a status (`todo|doing|done|blocked`). *Adopted:* the files already exist — write no parallel ones. Fill only what the substrate leaves undeclared (usually the contract's gate commands) in its own idiom, and keep the loop's working notes ephemeral and version-ignored. Either way, use your checkpoint/handoff capability to write the orientation — file-backed, not as a paste-in prompt; it's the self-contained orientation a fresh agent reads first.

## One cycle — repeat until the contract is green

1. **Read state.** Re-read the bound orientation and ledger, plus the tail of the bound history, from disk. Trust the files, not memory or session-start context.
2. **Pick** the next unblocked task. A substrate whose units are session-sized holds more than one cycle: work its sub-steps (its own checklist is the sub-ledger) and never mint a new unit of work to track them.
3. **Build.** Invoke the capability-right skill(s) for it (the domain workflow for the area; functional-core principles). Author tests first: red → green. For a bug fix, first reproduce the failure on the *unchanged* baseline (confirm it's red for the right reason) before touching code — otherwise you can't tell a real fix from a no-op (L9).
4. **Commit.** One local commit per task. Reversible, so allowed without asking. Where the substrate declares its own granularity, follow it exactly — e.g. one atomic completion commit carrying implementation, tests, the advanced continuation note, and removal of the finished slice, with no separate state commit.
5. **Check** — run `$SKILL/scripts/check.sh <slug>` (executes the contract's declared commands, pass/fail per item; `--gates <path>` when the gate table lives in the substrate) or dispatch a fresh-context subagent to review. Deterministic execution *or* fresh eyes — never self-grade in the working context. A "pre-existing / not caused by this change" verdict — yours or the checker's — is only as trustworthy as its scope: it holds only if *every* change on the branch touching the affected surface was examined (L9).
6. **Record.** Append the measured result to the bound history; flip the unit's status in the bound ledger.
7. **On failure**, log the error *and the contract line it broke*; route to your debugging capability; retry bounded (≤3), each retry carrying the error forward — never re-run the same failing prompt verbatim. Still failing → escalate to the human.
8. **Gate.** Contract fully green → stop, summarize, refresh the orientation for handoff. Otherwise → next cycle. A **judgment gate** is separate from both: a decision that is cheap and reversible but not yours to make (which prototype wins, which wording ships) is not a blocked task — enter the substrate's human-gate state if it declares one (record the exact decision or evidence needed, commit the evidence *without* retiring the slice, leave the pointer where it is), otherwise stop and ask.
9. **Irreversible boundary** — push, open a PR, deploy, delete, publish, post comments → **STOP and ask.** Autonomy budget is not approval budget.

## Non-obvious policy — why this loop, not a naive one

- **L1 — The contract must be exit-code-checkable.** "Improve X" can't halt; "`test` exits 0" can. No un-checkable done-items.
- **L2 — Check in fresh context.** An agent grading its own work in the same window brings the same blind spots in; verification needs fresh eyes or a deterministic command.
- **L3 — Autonomy ≠ approval.** Run unattended through reversible actions; stop at every irreversible/outward one. Inherit the project's approval boundary — don't invent a looser one.
- **L4 — State lives on disk, not the transcript.** Anything only in context is gone at the first compaction. Read-at-start, write-each-cycle.
- **L5 — Retries carry the error, are bounded, and escalate.** A verbatim re-prompt loops forever; three informed attempts then a human.
- **L6 — Every cycle logs a measured result.** An unmeasured "done" is a vibe. `journal.md` records the check output, not a claim.
- **L7 — The plan is a hypothesis; the code wins.** When execution contradicts a plan step, stop, note it in `journal.md`, and re-derive — don't force a step you can see is wrong.
- **L8 — The harness is editable, but evolving it is a reasoned, human-gated act.** Improve the instruction files, skills, and memory the loop runs on when the journal shows a *recurring, reusable* gap — never on a one-off, never silently, never without the human's go-ahead. Durable harness edits are irreversible-class (L3).
- **L9 — A fix is verified only against a demonstrated baseline.** For a bug fix, reproduce the failure *before* the change (red for the right reason), then show it gone *after* (green). An after-state check alone can "fix" a bug that never existed, or hide that the change itself *caused* the symptom — both look green. When a human reports "it works on the reference/baseline build," that is an empirical before/after; trust it over static-diff reasoning and re-open the diagnosis.
- **L10 — One source of truth for state.** Bind to the repo's continuation convention where it declares one; scaffold the loop's own files only where it doesn't. Two ledgers drift inside a single session, and the next session reads the wrong one. The substrate's commit and cleanup discipline outranks this skill's defaults — but where it deliberately keeps no record of *failed* attempts, keep the loop's own ephemeral, version-ignored journal anyway: a committed audit trail and a Reflexion memory are different artifacts, and L5/L8 run on the second one.

## Capabilities by phase

Prefer the matching skill in your set (by its description). If none exists, use that phase's built-in fallback in [REFERENCE.md](REFERENCE.md) — the loop runs fully standalone.

| Phase | Capability to invoke |
|---|---|
| Spec | requirements interrogation; idea validation |
| Contract | test-case planning; design-spec (its contract section) |
| Plan / state | task planning & breakdown; checkpoint/handoff (writes the orientation, file-backed) |
| Per-task research | codebase research (trace the code paths the task touches) |
| Build | the domain workflow for the area; functional-core / immutability principles |
| Test | test-first authoring (write the failing test before the code) |
| Check | verification — run the gates, evidence over claims; formal verification for provable invariants |
| On failure | systematic debugging (root cause before patch) |
| Pre-handoff | git-history hygiene — linearize commits / distribute fixups; leak audit before any publish |
| Recurrence | feed repeated failures back into your design-spec and test-planning workflows |
| Harness evolution | lessons-capture / instruction-file optimization; skill authoring & workflow extraction — see *Evolving the harness* |

## Evolving the harness (self-improvement)

The loop may improve the harness it runs on — instruction files, skills, memory — but only for a real, observed reason, and never silently. Signals accumulate in `journal.md` as you work; act on those, don't invent them.

**Trigger only when the journal shows a durable, reusable gap** — the same correction or mistake recurred across cycles; you found a convention the instruction files don't capture; a multi-step workflow emerged that no existing skill covers; or a skill you invoked was wrong, stale, or missing the pitfall you just hit. **Do not** act on a one-off preference, anything already documented, or speculation ("might help later"). One occurrence is a journal note, not a harness change (L8).

**When a trigger fires, propose — never auto-apply.** Harness edits are durable and outward-facing, so they sit behind the same human gate as any irreversible action (L3/L8). Surface a clear proposal: *what* you learned, *why* it recurs (cite the journal cycles), *which home* it belongs in, and a one-line summary of the change. On the go-ahead, apply it via the right capability, commit it in its proper repo, and log the outcome in `journal.md`. Route by capability: a project convention → your lessons-capture / instruction-file capability; a reusable workflow → your skill-authoring / workflow-extraction capability; a stale skill → edit that skill. The run's working state stays wherever it is bound; durable lessons graduate *out* to where future sessions will read them. Mechanics: [REFERENCE.md](REFERENCE.md) → *Evolving the harness*.

## What the loop hands to the human, never loops on

Product/UX judgment ("should this exist at all?"), anything not expressible as an exit-code check, every irreversible action, and every harness-evolution proposal (L8 — surfaced with a reason, never auto-applied). Surface these as decisions; don't spin on them.

See [REFERENCE.md](REFERENCE.md) for the state-file schemas, the contract format with examples, state substrates (native vs adopted), the resume protocol, the checker-dispatch mechanics, and the failure-mode catalog.
