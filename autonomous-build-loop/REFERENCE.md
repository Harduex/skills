# Autonomous Build Loop — Reference

Depth for the loop in [SKILL.md](SKILL.md). Everything here is capability-based — adapt the mechanics to whatever file, subagent, and skill primitives your harness provides.

## State files — the durable memory

Under `docs/loop/<slug>/`: one continuation note, one contract, and one file per task. Plus a git-ignored journal under `.loop/<slug>/`. They are the loop's memory; the transcript is not. Read them at the start of every cycle; write them at the end of every cycle.

The shape has one governing idea: **finished work leaves the tree.** A task's file is deleted in the very commit that completes it, so the directory only ever holds current and future work, while git history keeps every instruction that was ever executed — recoverable with `git show <commit>^:docs/loop/<slug>/<file>`. The note stays short because it is not an archive, and a fresh session's first read is never a graveyard of completed tasks.

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

### `CHECKPOINT.md` — the continuation note (rewritten every cycle)

The one file a new session reads first. It names exactly one current task and carries only what cannot be re-derived.

```md
# Checkpoint — <feature>   (slug: <slug>)

**Status:** in-progress            <!-- ready | in-progress | waiting-human | done -->
**Current task:** `docs/loop/<slug>/002-widgets-endpoint.md`

## Orientation
- Goal: <one paragraph — what and why>
- Branch: <branch-name>
- Key paths: `<path>` — <role>; `<path>` — <role>
- Build / run / test: `<cmd>` · `<cmd>`
- Contract: `docs/loop/<slug>/contract.md`

## Last completed
- Task 001 — Widget model + migration.

## Last verification
- Task 001: `pnpm test` → PASS (42 tests); `pnpm tsc --noEmit` → PASS; migration applied and rolled back cleanly.

## Locked decisions
- [D2] New widgets default to `status="draft"` — mirrors gadgets. Settled; do not re-open.

## Known blockers
- none

## Next action
Read task 002, invoke the capabilities it names, and implement only that task.
```

It is a **state description, not a log**: what is true now, what was actually measured, what must not be re-decided, what to do next. Narrative history belongs to git; failure detail belongs to the journal. A checkpoint can never contain its own commit SHA — it is written before that commit exists — so use `git log -1` when the exact hash is needed.

### `NNN-<task>.md` — one file per task (written ahead, deleted on completion)

Each slice is an executable brief that stands alone: an agent with zero prior context reads the note, then this file, and can work. Give each one a status, the contract rows it must turn green, the capabilities to invoke, its goal, its **allowed scope** (the files it may touch), the invariants to preserve, a test-first checklist, acceptance criteria, and required verification. If a slice needs three paragraphs of caveats to be executable, it is several tasks — split it before dispatch. Size them so one slice is one reviewable capability: a reviewer could approve it and reject the next.

**The completion commit is atomic.** When every acceptance item is verified:

```bash
git add <implementation and tests> docs/loop/<slug>/CHECKPOINT.md
git rm docs/loop/<slug>/002-widgets-endpoint.md
git commit -m "feat(002): <the capability, imperative>"
```

One commit carries implementation, tests, the advanced note, and the retired slice. Never a second "checkpoint commit" — the state update *is* part of completing the work, and a separate commit lets the two drift. If the task is not fully verified, the slice stays and the pointer does not move.

**Human gate.** When a task needs a decision or evidence only a person can supply, set `Status: waiting-human`, write the exact decision or evidence needed, commit the prototype/evidence **keeping** the slice, and leave the pointer alone. The person records their answer in the note; the task's eventual completion commit records the durable decision, retires the slice, and advances the pointer.

**Recovery.** Pointer names an existing slice → continue it. Pointer names a missing slice with a clean tree → the completion commit landed but the pointer didn't advance, or the pointer was hand-edited: read `git log -- docs/loop/<slug>/CHECKPOINT.md`, restore the intended pointer, then work. Uncommitted changes with the pointer still on a slice → the last session stopped mid-task; reconcile against that slice rather than advancing.

### `.loop/<slug>/journal.md` — ephemeral history (git-ignored)

```md
# Journal — <feature>   (ephemeral, git-ignored; newest at bottom)

## 2026-07-14T15:02Z · task 2 · POST /widgets handler
- Did: added handler in api/widgets.ts; mirrored gadgets.ts structure and error handling.
- Check: `pnpm test tests/e2e/widgets.create.spec.ts` → PASS. `pnpm tsc --noEmit` → PASS.
- Attempt 1 failed: validation ran after the handler body; zBody() must wrap the route, not the payload.
- Drift: gadgets uses `zBody()`, not manual parsing as the plan assumed → task 3 simplified.
- Next: implement task 3 (validation via zBody()).
```

This is the Reflexion memory: failures with their cause so a later cycle doesn't repeat them, and the *measured* check result every cycle (L6), never an unverified claim. It is deliberately **not** committed — `init.sh` writes `.loop/.gitignore` containing `*`, so the directory is invisible to git without editing the repo's own ignore file. Durable outcomes graduate to the note; the rest dies with the branch. Keeping failed attempts out of history is the point: the audit trail records what was done, the journal records what was tried.

## State substrates — native and adopted (L10)

The files above are one *encoding* of four state roles. A repo that already runs its own continuation convention encodes the same roles under its own names — bind to it rather than standing up a second ledger beside it. The shapes match closely because the native shape *is* this pattern; adopted mode mostly means different filenames and someone else's commit rules.

| Role | Native | Typical adopted |
|---|---|---|
| Orientation — what a fresh session reads first | `CHECKPOINT.md` header | the repo's durable continuation note |
| Ledger — the units of work and their status | `NNN-*.md` slices + the note's pointer | per-unit work slices + a pointer to the current one |
| History — what was tried and measured | git history of retired slices + the note's verification section; failures in the ignored journal | version history of retired slices + the note's verification section |
| Contract — what "done" means, as commands | `contract.md` | the current slice's acceptance items over repo-wide gate commands |

**Making the loop discoverable (native mode).** Scaffolding the state is half the job; the repo has to *say* where it is. The instruction file agents read first — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or whatever this project uses — must name the note as a first read, e.g. a "Start here" line pointing at `docs/loop/<slug>/CHECKPOINT.md` and stating that it names the one current task. Without that line the loop is invisible to the next session and to every other tool, and the resume protocol below has nothing to latch onto. Three rules: exactly one target, so a repo never advertises two notes (L10); repoint rather than append when a finished run's note is being replaced; and in adopted mode change nothing — the repo already points where it wants. `init.sh` prints the file it found and the line to add. If the repo has no instruction file, create a minimal one whose only job is that pointer.

**Older native runs.** Loops scaffolded before this shape use a `plan.md` task table with a committed `journal.md`. `status.sh <slug>` still reads them, so an in-flight loop keeps resuming untouched — the two encodings coexist and no migration is required to finish a run.

**Resolve the mode in this order — first match wins.** Precedence, not a guess: a repo can declare a convention *whose target is the loop's own state*, and that is still native.

1. `docs/loop/<slug>/` already exists for this feature → **native**. Stop; a live loop is never re-bound mid-run.
2. The instruction file's "read this first" target lives inside `docs/loop/` → **native**. Stop.
3. It names a distinct continuation note, and per-unit work slices exist alongside it → **adopted**.
4. Anything else — no instruction file, an unreachable target, a note with no slices → **ask once**, then proceed. Never infer a substrate from a filename alone.

**How far the adaptation goes.** The *binding* is done by you, from the repo's own files, so it stretches to any convention that names a current unit of work — including ones with no per-task files at all (a checklist, an issue tracker, a board). The *scripts* are narrower: `status.sh --adopt` recognises status fields written as `**Key:** value`, YAML frontmatter, `## Key` + its first line, or plain `Key: value`, and finds the current-item pointer on the line naming it or the two lines after. When it recognises neither, it prints `shape: UNRECOGNISED` and tells you to read the note yourself — an empty report must never read as "nothing in progress". Anything past that, read the files directly; the script is a convenience, never the source of truth.

**Discovery probe (adopted).** Read the repo's agent instruction file → follow its first "read this before working" pointer → read the note and the slice it names as current → `git status` and `git log -1` to see whether the last session stopped mid-slice. That is the whole binding; re-derive it each session (it costs three reads) rather than caching it in a file the repo did not ask for.

**Adopted-mode invariants.**
- **Write nothing the repo did not already define.** No `docs/loop/` beside a bound substrate, no extra note, no second ledger. If a role has no home there, the loop's own copy of it stays ephemeral and version-ignored.
- **Obey its lifecycle verbatim** — commit granularity, whether a finished slice is retired or marked, whether the history lives in commits rather than a file, and any human-gate state it defines.
- **Reconcile before advancing.** Uncommitted changes with the pointer still on a slice means the last session stopped mid-slice: finish or unwind that slice; never advance the pointer to make the tree look clean.
- **Keep an ephemeral journal.** A substrate that keeps only *durable decisions* keeps no record of failed attempts, so L5 (retries carry the error) and L8 (a gap that recurred ≥2 cycles) lose their evidence at the first compaction. Write it to an ignored path, mirror only durable outcomes into the note, and let it die with the branch.
- **Sub-cycles, not new units.** Session-sized slices hold several cycles. Drive the slice's own checklist as the sub-ledger; never add a unit of work to the substrate to track your own cycles.

**Contract binding.** Where the substrate states acceptance per slice, the gate *commands* are usually repo-wide and stable (the build/test/sanitizer entry points). Declare them once in a gate table the repo owns, in the `| Cn | done when… | \`cmd\` |` shape this skill's checker already parses, and point `check.sh --gates <path>` at it — the contract stays on disk (L4) instead of being re-derived into a command line each session. Two rules when writing that table: a gate that cannot pass in this environment (an uninstalled tool) belongs in the human-verified list, not as a permanently red row; and a gate that needs an environment prefix to pass must carry it in the row.

## Resume protocol (the cross-session guarantee)

**Starting a session, or right after a compaction:** run `$SKILL/scripts/status.sh <slug>` for an instant read of the note's status, the current slice, how many slices remain, whether the tree is clean, and the journal tail — then read the note, read the slice it names, and reconcile any uncommitted changes against that slice before touching anything. Do **not** let a session-start summary override the files (L4, and "trust live state, not snapshots"). Bound to a substrate, the same sequence runs against it via `$SKILL/scripts/status.sh --adopt <note> [slice-dir]`.

**Before an expected compaction or at session end:** refresh the note (status, last verification, next action) and append a journal entry ending in a concrete `Next:`. Invoke your set's checkpoint/handoff capability to produce that header — it already knows how to write a no-context-needed resume block; ask it for the file-backed form so it lands in the file instead of the transcript, and when bound to a substrate, in that note's existing sections rather than a shape of your own.

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

**Fallback — deterministic, no subagents.** Run `$SKILL/scripts/check.sh <slug>` (or `check.sh --gates <path>` against a substrate-owned gate table): it executes the contract's declared commands and reports pass/fail per item. Or run the commands by hand and read exit codes. Determinism satisfies L2 for the *checks* themselves, but you lose fresh-eyes review — compensate by reviewing the diff cold at the gate (Standalone fallbacks → Check) before declaring green.

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
- **Check.** Run `$SKILL/scripts/check.sh <slug>` (or every contract command by hand) and show the output. Then review the diff cold for correctness/security (auth boundaries, injection, data loss), state and concurrency (cancellation, re-entry, races), error/degrade paths, and symmetry with siblings. With subagents, review in a fresh agent; without, review as a distinct pass after re-reading the diff from scratch.
- **Debug (on a failing check).** Reproduce reliably; form one hypothesis; instrument to confirm or refute it rather than guess-patching; fix the root cause, not the symptom; re-run the check.
- **Git hygiene (pre-handoff).** One logical change per commit; each commit builds green on its own; no add-then-remove churn; imperative subject lines stating the why. Never push without explicit approval.
- **Leak check (pre-publish).** Scan the diff (and history, on a first publish) for secrets, tokens, PII, and machine-local paths. Publishing is irreversible regardless → it goes through the human checkpoint (L3).

## Evolving the harness (self-improvement)

The loop runs on a harness — instruction files (`AGENTS.md`/`CLAUDE.md`), skills, and memory. It may improve that harness, but under strict discipline (L8): a **real recurring reason**, a **clear proposal**, and the **human's go-ahead** before anything durable is written.

**The signal is the journal, not a hunch.** `journal.md` is the loop's Reflexion memory — every cycle logs what happened and why. Harness evolution reads *that record* for a pattern; it does not invent one from a single cycle.

**Triggers — act only when one is clearly met:**
- The same correction or mistake recurred across ≥2 cycles (the journal shows it twice).
- You discovered a convention the instruction files don't capture and a future task would trip on it.
- A reusable, multi-step workflow emerged that no existing skill covers.
- A skill you invoked was wrong, stale, or missing the exact pitfall you just hit.
- Recurring spec/contract ambiguity points to a missing checklist item.

**Anti-triggers — leave these as a journal note, never a harness edit:**
- A one-off preference or a single occurrence (one correction ≠ a standing rule).
- Anything the instruction files / skills already cover.
- Speculation ("might be useful later") with no observed need in this run.

**Routing — send each learning to the home where future sessions will actually read it:**

| Learning | Home | Capability to invoke | Commit in |
|---|---|---|---|
| Project convention / gotcha / durable preference | instruction file or memory | lessons-capture / instruction-file optimization | the repo that owns the file |
| A reusable workflow no skill covers | a new skill | skill authoring / workflow extraction | your skills repo |
| A skill was wrong / stale / missing a pitfall | that skill | skill authoring | your skills repo |
| Better contract items / test coverage for this domain | this run's `contract.md` + your design-spec/test-planning workflow | test-case planning | `docs/loop/<slug>/` (local, this run) |

**Protocol (propose → gate → apply → record):**
1. **Propose, don't apply.** Surface: *what* you learned, *why* it recurs (cite the journal cycles), *which home* it belongs in, and a one-line diff summary. Harness edits are durable and outward-facing → same human gate as any irreversible action (L3).
2. **Wait for the go-ahead.** No approval → it stays a journal note.
3. **Apply via the routed capability** — don't hand-roll what a skill-authoring or lessons-capture workflow does properly.
4. **Commit it in its proper repo** in the same session (uncommitted harness work is lost work) and **log the outcome** in `journal.md`.

Keep the run's working state where it is bound; durable lessons graduate *out* of it. A loop's state is disposable per-feature scaffolding — the harness is where knowledge lives for the next feature.

## Knobs (defaults, and how to change them)

- **Stop boundary** — default: run to *merge-ready*, human checkpoint at every irreversible action. To allow unattended **draft** PRs, add "open draft PR" to the reversible set; keep merge, deploy, and comment-posting behind the checkpoint regardless.
- **Substrate** — default: subagent checker (above); single-context fallback documented above.
- **State location** — default: committed `docs/loop/<slug>/` (auditable, survives machines) in native mode, the repo's own files when bound to a substrate; the failure journal is always ignored under `.loop/`. Gitignore the whole thing if you don't want loop state in history — you then forfeit cross-machine resume and the completed-task trail.
- **Retiring slices** — default: a completed slice is deleted in its completion commit, leaving it in history only. To keep completed slices in the tree instead, mark them `done` in place; you then own the graveyard and a fresh session pays to read past it.
- **Pass cap** — default ≤3 attempts per task before escalation; raise only with a reason.

## Scripts

**These three scripts ship *inside this skill* — they are the containment boundary.** The tooling stays in the skill; only the *state* (`docs/loop/<slug>/`) is written into the repo. Invoke each by its path under this skill's base directory — `$SKILL/scripts/…`, where `$SKILL` is the directory the harness prints when the skill loads — with your working directory at the repo root, so `docs/loop/` resolves against the project. **Never copy them into the project** (that scatters the harness across the repo and forks a second copy that silently drifts from the skill). `init.sh`/`status.sh` touch only `docs/loop/`; `check.sh` additionally runs the checks you declared in the contract.

- **`$SKILL/scripts/init.sh [--force] <slug> ["Title"]`** — canonical generator for the state files: the continuation note, the contract, the first task slice, and the git-ignored journal (plus the `.loop/.gitignore` that hides it). Validates the slug (kebab-case), creates `docs/loop/<slug>/`, and refuses to overwrite an existing loop (state is precious — deleting it is a deliberate act, not a re-init). It also refuses when the repo appears to own a continuation convention already, naming what it found: scaffolding beside a substrate is the L10 failure, and `--force` is the deliberate override for the rare repo that wants both. Stamps a `loop initialized` entry into the journal so the log starts from cycle zero. These templates are the source of truth for the schemas shown above; if you change the shape, change it here.
- **`$SKILL/scripts/status.sh [slug]`** — read-only. With no argument, lists every loop under `docs/loop/`. With a slug, prints the note's status fields, the current slice and whether its file is still present, how many slices remain, whether the tree is clean, the recent history of retired slices, and the journal tail. A run in the older `plan.md` shape is read in that shape instead, so it keeps resuming. `--adopt [note] [slice-dir]` reads a substrate instead: the note's status fields, the slice it names as current, whether that slice's file is present, uncommitted-change count, and the recent slice history from `git log`. It accepts four field notations (bold, YAML frontmatter, headings, plain `Key: value`), counts numbered slices or falls back to reporting the other `.md` files it can see, and prints `shape: UNRECOGNISED` when it can find neither fields nor a pointer. With no path it probes the common note names and prints which one it chose — it guesses out loud rather than silently. It never runs your project's checks and never edits anything; it exists to make "read state from disk first" (L4) a one-command habit at session start.
- **`$SKILL/scripts/check.sh <slug> | --gates <path>`** — the deterministic checker. Runs the commands declared in `contract.md` (or in the substrate-owned gate table given to `--gates`) and reports pass/fail per item, skipping any row still set to `<command>`; exits 0 only when every runnable check passes. Rows are `| <ID> | description | \`command\` |`; the command is the last backticked span on the row. Running the real commands is what makes self-grading impossible (L2) and keeps the contract the single source of truth (L1/L6). Point `--gates` at a file that exists to declare gates — never at a work-slice document whose prose contains backticked commands (`git rm …`), because every command it finds, it runs.

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
| Harness churn | loop rewrites skills / instruction files on a one-off or on speculation | **L8** — a real recurring signal in the journal + a human-gated proposal; one occurrence is a journal note |
| Fix of nothing / self-inflicted symptom | a fix is "verified" by its after-state only — but the bug never existed, or the change itself caused the symptom | **L9** — reproduce the failure on the unchanged baseline first; verify as an A/B (before vs after), and trust a human's baseline/reference A/B over static-diff reasoning |
| Two ledgers | loop state and the repo's own note disagree; the next session resumes from whichever it read | **L10** — bind before scaffolding, first match wins in the precedence order |
| Split completion | the work commits, the note advances in a second commit; a stop between them leaves the pointer lying | one atomic completion commit — implementation, tests, note, retired slice |
| Premature retirement | a slice is deleted while its acceptance items are unproven, so the instructions are gone and "done" is unverifiable | retire only after the gates are measured green; unverified work keeps its slice and its pointer |
| Silent loss of failure memory | bound to a substrate that records only durable decisions, so retries and recurring gaps leave no trace past a compaction | keep the ephemeral, ignored journal even in adopted mode — L5/L8 run on it |
| Gate that can never be green | a contract row needs an uninstalled tool or a missing environment prefix; the loop reads an environmental red as a code failure | environment-blocked items go to the human-verified list; a needed prefix lives in the row |
