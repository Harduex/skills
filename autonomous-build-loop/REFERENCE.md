# Autonomous Build Loop — Reference

Depth for the loop in [SKILL.md](SKILL.md). Everything here is capability-based — adapt the mechanics to whatever file, subagent, and skill primitives your harness provides.

## State files — the durable memory

Three files under `docs/loop/<slug>/`. They are the loop's memory; the transcript is not. Read them at the start of every cycle; write them at the end of every cycle.

### `contract.md` — what "done" means (rarely changes once set)

Each row is satisfied only when its command exits 0. The loop halts when every row is green.

```md
# Done contract — <feature>

| ID | Done when… | Check (exit 0 = pass) |
|----|------------|------------------------|
| C1 | Unit + integration tests pass | `pnpm test` |
| C2 | No type errors | `pnpm tsc --noEmit` |
| C3 | Lint clean | `pnpm lint` |
| C4 | POST /widgets returns 201 on a valid body | `pnpm test tests/e2e/widgets.create.spec.ts` |
| C5 | Migration applies **and** rolls back cleanly | `pnpm db:migrate && pnpm db:rollback` |

Human-verified acceptance (NOT loopable — hand to the human): <e.g. "empty-state copy reads well">.
```

Rule (L1): if a done-item can't be reduced to a command + exit code, it does not belong in the contract — it goes in the human-verified list. A contract of vague goals can never halt.

### `plan.md` — the living task list (changes every cycle)

```md
# Plan — <feature>   (slug: <slug>)

## Orientation  — a fresh agent reads this FIRST; keep it current
- Goal: <one paragraph — what and why>
- Branch: <branch-name>
- Key paths: `<path>` — <role>; `<path>` — <role>
- Build / run / test: `<cmd>` · `<cmd>` · `<cmd>`
- Contract: `docs/loop/<slug>/contract.md`
- Resume: start at the first non-`done` task below; read the `journal.md` tail for recent context.

## Tasks
| # | Task — self-contained, written for an agent with zero prior context | Status | Commit | Notes |
|---|----------------------------------------------------------------------|--------|--------|-------|
| 1 | Add `Widget` model + migration in `db/schema.ts` mirroring `Gadget`  | done   | abc1234 | |
| 2 | Add `POST /widgets` handler in `api/widgets.ts` mirroring `gadgets`  | doing  |        | |
| 3 | Wire validation via the existing `zBody()` helper                    | todo   |        | after 2 |
| 4 | Backfill defaults for existing rows                                  | blocked|        | needs decision D2 |
```

Each task must stand alone (the "hand it to a junior with no context" bar). If a task needs three paragraphs of caveats to be executable, it's really several tasks — split it before dispatch.

### `journal.md` — append-only history (grows every cycle)

```md
# Journal — <feature>   (append-only; newest at bottom)

## 2026-07-14T15:02Z · task 2 · POST /widgets handler
- Did: added handler in api/widgets.ts; mirrored gadgets.ts structure and error handling.
- Check: `pnpm test tests/e2e/widgets.create.spec.ts` → PASS. `pnpm tsc --noEmit` → PASS.
- Decision [D2]: default `status="draft"` for new widgets — matches gadgets; confirm before backfill (task 4).
- Drift: gadgets uses `zBody()`, not manual parsing as the plan assumed → task 3 simplified.
- Next: implement task 3 (validation via zBody()).
```

The journal is the audit trail and the Reflexion memory: failures are logged with their cause so a later cycle doesn't repeat them, and every entry records the *measured* check result (L6), never an unverified claim.

## Resume protocol (the cross-session guarantee)

**Starting a session, or right after a compaction:** run `scripts/status.sh <slug>` for an instant read of task progress, the next task, and the latest journal entry, then read `plan.md` orientation → scan task statuses → read the last one or two `journal.md` entries → resume at the first non-`done` task. Do **not** let a session-start summary override the files (L4, and "trust live state, not snapshots").

**Before an expected compaction or at session end:** refresh the `plan.md` orientation header and append a `journal.md` entry ending in a concrete `Next:`. Invoke your set's checkpoint/handoff capability to produce that header — it already knows how to write a no-context-needed resume block; here you persist it to a file instead of emitting a prompt.

## Checker dispatch (L2 — fresh context)

**Preferred — subagent.** Dispatch with a general-purpose agent type (so it can load skills). Prompt it to (1) invoke your verification capability, (2) run each contract command, (3) return the schema below — pass/fail per contract ID plus the first failing output, not a transcript. Fresh context is what actually removes the shared blind spot.

```jsonc
{
  "allGreen": false,
  "results": [
    { "id": "C1", "pass": true,  "cmd": "pnpm test",           "firstFailure": null },
    { "id": "C4", "pass": false, "cmd": "pnpm test …create",   "firstFailure": "expected 201, got 500: ValidationError: body.name required" }
  ]
}
```

**Fallback — deterministic, no subagents.** Run `scripts/check.sh <slug>`: it executes the contract's declared commands and reports pass/fail per item. Or run the commands by hand and read exit codes. Determinism satisfies L2 for the *checks* themselves, but you lose fresh-eyes review — compensate by reviewing the diff cold at the gate (Standalone fallbacks → Check) before declaring green.

Only the schema flows back to the orchestrator, so its context stays clean across many cycles.

## Retry / escalation ladder (L5)

1. **Attempt 1** — fix guided by the error message + the contract line it broke.
2. **Attempt 2** — route through your debugging capability: reproduce → root cause → patch; re-check.
3. **Attempt 3** — a *different* approach, not the same patch reshaped.
4. **Still red** → set the task `blocked`, write the blocker and everything tried into `journal.md`, and escalate to the human. Never spin past the cap.

## Standalone fallbacks — when no peer skill exists

The loop prefers a matching skill in your set for each phase (SKILL.md → Capabilities by phase). With none installed, use these built-in procedures. They are deliberately minimal *floors*, not replacements for a dedicated skill's depth — where a peer skill exists, it wins.

- **Spec.** Resolve every ambiguity in the prompt before any code. Ask targeted questions offering 2–3 concrete options each, covering scope (in / explicitly out), the data and interface shape, failure behaviour, and the one observable success criterion. Stop when a stranger could build the same thing from your spec. Never proceed on a guess — a wrong assumption here poisons every cycle.
- **Contract.** Already specified above (the `contract.md` schema): each item a command with an exit code; un-checkable goals go to the human-verified list.
- **Plan.** Decompose into ordered tasks where each is independently committable, ties its done-signal to a contract item, names the closest existing sibling to mirror, and reads as executable by a zero-context agent. Order so dependencies flow forward; one concern per task.
- **Research (per task).** Before editing, trace the code paths the task touches from entry point to the change site; open the nearest existing analog end-to-end and note the conventions to match; cite `file:line`.
- **Build.** Mirror the sibling's structure, naming, and error handling. Keep logic in pure functions where practical and isolate side effects at the edges. Change only what the task needs.
- **Test (test-first).** Write the failing test first and confirm it fails for the right reason (red); implement to green. Cover the new/risky branches and the boundaries. A test that still passes when the code is wrong is worse than no test.
- **Check.** Run `scripts/check.sh <slug>` (or every contract command by hand) and show the output. Then review the diff cold for correctness/security (auth boundaries, injection, data loss), state and concurrency (cancellation, re-entry, races), error/degrade paths, and symmetry with siblings. With subagents, review in a fresh agent; without, review as a distinct pass after re-reading the diff from scratch.
- **Debug (on a failing check).** Reproduce reliably; form one hypothesis; instrument to confirm or refute it rather than guess-patching; fix the root cause, not the symptom; re-run the check.
- **Git hygiene (pre-handoff).** One logical change per commit; each commit builds green on its own; no add-then-remove churn; imperative subject lines stating the why. Never push without explicit approval.
- **Leak check (pre-publish).** Scan the diff (and history, on a first publish) for secrets, tokens, PII, and machine-local paths. Publishing is irreversible regardless → it goes through the human checkpoint (L3).

## Knobs (defaults, and how to change them)

- **Stop boundary** — default: run to *merge-ready*, human checkpoint at every irreversible action. To allow unattended **draft** PRs, add "open draft PR" to the reversible set; keep merge, deploy, and comment-posting behind the checkpoint regardless.
- **Substrate** — default: subagent checker (above); single-context fallback documented above.
- **State location** — default: committed `docs/loop/<slug>/` (auditable, survives machines). Gitignore it if you don't want loop state in history — you then forfeit cross-machine resume.
- **Pass cap** — default ≤3 attempts per task before escalation; raise only with a reason.

## Scripts

Run from the repository root. `init.sh` and `status.sh` touch only `docs/loop/`; `check.sh` additionally runs the checks you declared in the contract.

- **`scripts/init.sh <slug> ["Title"]`** — canonical generator for the three state files. Validates the slug (kebab-case), creates `docs/loop/<slug>/`, and refuses to overwrite an existing loop (state is precious — deleting it is a deliberate act, not a re-init). Stamps a `loop initialized` entry into `journal.md` so the log starts from cycle zero. These templates are the source of truth for the schemas shown above; if you change the shape, change it here.
- **`scripts/status.sh [slug]`** — read-only. With no argument, lists every loop under `docs/loop/`. With a slug, prints task counts by status, the next non-`done` task, and the latest journal entry. It never runs your project's checks and never edits anything; it exists to make "read state from disk first" (L4) a one-command habit at session start.
- **`scripts/check.sh <slug>`** — the deterministic checker. Runs the commands declared in `contract.md` and reports pass/fail per item, skipping any row still set to `<command>`; exits 0 only when every runnable check passes. Running the real commands is what makes self-grading impossible (L2) and keeps the contract the single source of truth (L1/L6).

## Failure-mode catalog

| Failure | Symptom | Guard |
|---|---|---|
| Vague contract | loop can't tell it's done; runs forever or stops arbitrarily | **L1** — every item a command + exit code |
| Self-graded checks | "tests pass" asserted while actually red; same blind spots in | **L2** — check in fresh context / deterministic command |
| Runaway approvals | loop pushes, opens PRs, deploys unattended | **L3** — stop at every irreversible action |
| Amnesia at compaction | loop redoes finished work or forgets a decision | **L4** — state on disk, read-at-start each cycle |
| Retry thrash | same failing prompt re-run; infinite loop | **L5** — carry the error, cap ≤3, escalate |
| Vibes-based done | merged on green typecheck without exercising behavior | **L6** — journal the measured check output |
| Forcing a wrong plan | a plan step contradicts the code but runs anyway | **L7** — stop, log drift, re-derive |
| Non-atomic tasks | a fresh session or subagent can't execute a task as written | tasks written for a zero-context reader; split before dispatch |
| Context bloat | orchestrator fills with subagent transcripts | checker returns the schema (pass/fail + first failure), never a transcript |
| Over-firing | full loop spun up for a one-file change | the scope guard — just make trivial changes directly |
