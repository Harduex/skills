# Changelog

## v1.8.1

- **`general-coding-standards`: new rule M6 — reuse the codebase's existing vocabulary
  of operations.** The reuse habit fires on nouns (a component, a hook, a registry) and
  lets multi-token expressions through: inline arithmetic reads as code being written,
  not as a dependency being added. Searching by name cannot close the gap, because the
  helper's name is what the author does not know yet — so the rule says to enumerate the
  shared utility modules' exports and read the list. Hooked into author mode, the M-band
  review sweep, and the self-check. Sibling mirroring (M4) is named as a carrier rather
  than a guard: a sibling older than the helper hands over the pre-helper idiom.
- **`distribute-fixups`: corrected the verification baseline.** The skill recorded HEAD
  before the fixup commits, then demanded an empty diff against it — impossible for
  uncommitted changes, since that commit predates the very changes being distributed. A
  check that can never pass teaches the reader to wave it through. The baseline is now
  the tip of the fixup stack, whose tree is the end state the rebase must reproduce.

## v1.8.0

- **New skill: `write-handoff-doc`** (delivery-lifecycle bundle). Converts an internal
  artifact — a design spec, a shipped branch or feature, an API contract — into a
  self-contained external handoff document another team can act on with zero internal
  context. Encodes the proven format (dateline with a conscious status, one-paragraph
  "short version", task-ordered sections, rule/cost and their-reaction tables,
  define-by-negation, their-side open items), the audience filter (storage is not
  contract; no decision IDs, tickets, or internal paths; verify every claim and link,
  hedge what isn't pinned), and the publish lifecycle (repo file is the source of
  truth; published copies sync back as deltas with medium artifacts stripped).
  Cold-tested on a real spec; the tester's eight reported gaps are folded in.

## v1.7.5

- **code-review resolves GitLab Duo's bare note-id citations.** Duo points at its own earlier
  comments as `#887738`, and GitLab auto-links merge-request and issue refs but not note ids —
  so the citation renders as dead text and a human sent to look at one finds nothing on the
  page. The reference now says to resolve the id through the notes API and hand over the
  `#note_<id>` anchor URL, which does open the comment.
- **The report bar no longer claims its calibration is local.** The findings table cited "this
  project's review history", which resolves to whatever repo the reader is in — asserting a
  14-session review history they never had. A model reading the table as locally measured
  would hand its absolutes ("zero were ever fixed") back as facts about the reader's own team,
  so the attribution now names it for what it is: one team's sample.

## v1.7.4

- **write-a-skill now teaches the current Agent Skills standards.** The skill knew two
  frontmatter fields and nothing about testing, so it could not answer what the spec now
  defines: six portable fields with hard name constraints (lowercase/hyphens, must match the
  directory name), ~15 Claude Code extensions (invocation control, subagent execution, tool
  grants, path scoping), and the hard upload error claude.ai / the Skills API raise on any
  non-spec field. SKILL.md now carries the name/description constraints, the
  never-summarize-the-workflow description rule, and a baseline-first test-and-retest
  authoring process; a new REFERENCE.md holds the field tables, portability rules, string
  substitutions and dynamic context injection, the no-prompt bundled-script pattern,
  progressive disclosure patterns, testing methodology, and anti-patterns. A subagent
  application test passed all three scenarios and its gap report drove four clarifications,
  including sandbox-only baselines for side-effectful workflows.

## v1.7.3

- **functional-programming now carries a full, citable rule set.** The skill stated the
  Data > Calculations > Actions triad and functional core / mutable shell, but was silent on
  everything in between: where a function belongs, what to do with near-identical functions and
  hand-written loops, how data crosses trust boundaries, and how async code goes wrong.
  REFERENCE.md now defines 51 rules in seven bands with stable IDs for review citations —
  C classify, A improve actions, I immutability disciplines, D stratified design, F refactorings &
  functional tools, T timelines, R architecture — each band with one worked TypeScript example,
  plus an expanded anti-patterns table. SKILL.md gains the "actions spread" rationale, names
  core/shell as the onion architecture, and routes into the bands; its description now also
  triggers on layers, abstraction barriers, duplicated functions, and race conditions. Subagent
  application tests shaped the final rules: T9 added (threshold effects edge-trigger on the
  before/after transition), the queue example hardened so a failed job cannot strand queued ones,
  and C3 tightened so a deterministic in-place mutator no longer qualifies as a calculation.

## v1.7.2

- **Slice numbering is stated to be the execution order.** The skill said tasks are "ordered so
  dependencies flow forward" but never that the filename number *is* that order, that the note's
  pointer must agree with it, or how to insert a task that must run before existing ones — enough
  silence to justify appending an unblocker at the end and explaining the mismatch away in the
  note. Inserting now means renumbering, with its four parts named (files, each slice's own `git rm`
  target, cross-references between slices, numbers quoted in the note and contract) plus the
  verification that catches a partial pass: every slice retires itself, every forward reference
  moves forward, no slice references itself. Bare numbers in prose are flagged as the ones that
  survive renumbering and then point at the wrong task.

## v1.7.1

- **Finished runs are closed out, not left in the tree.** The paper-trail convention was defined
  for slices only: a completed slice left in its completion commit, but the run itself had no
  close-out, so finished `docs/loop/<slug>/` directories accumulated and each kept a
  `CHECKPOINT.md` — several notes claiming to be current, which is the exact L10 hazard the skill
  exists to prevent. Closing out is now ordered and explicit: graduate the durable decisions,
  **hand over any still-open human-verified item** (machine-green is not finished — a pending host
  gate must not vanish with the note), `git rm -r` the directory in one commit, repoint or remove
  the instruction-file line, and delete the ignored journal. A paused run keeps everything.
  `status.sh` with no argument now names each run's note and warns when more than one exists.
- **A scaffolded loop must be made discoverable, and the skill now says so.** Setup covered
  creating the state but never telling the repo where it is, so a perfectly scaffolded native run
  could stay invisible: a fresh session reads the instruction file, finds no mention of the note,
  and the resume guarantee depends on luck. Native mode now requires one line in the repo's
  agent instruction file naming the note as a first read — exactly one target, repointed rather
  than appended when a finished run is replaced, and untouched in adopted mode, where the repo
  already points where it wants. `init.sh` prints the instruction file it found and the line to
  add, or says none exists.
- **The adopt/native reader no longer loses a note's pointer to its own prose.** It took the
  first line containing "current" and searched only that line plus two more; the note template's
  guidance comment says "keep it current", so a freshly generated `CHECKPOINT.md` reported
  `slice: (none named)` while the pointer sat three lines further down — failing on the exact
  shape `init.sh` writes. Every line naming the current item is now a candidate, examined with
  its two following lines, and the first window that actually holds a path wins; a backticked
  token must look like a filename before it counts, so prose in backticks is not mistaken for a
  pointer.

## v1.7.0

- **`autonomous-build-loop` scaffolds a continuation note and disposable task slices by
  default.** Its own state was a `plan.md` task table plus a committed journal, so the pattern
  it could only *borrow* from a host repo — one durable note naming a single current task,
  per-task files that leave the tree when finished, and the paper trail kept by git history —
  was unavailable whenever the loop stood up its own state. `init.sh` now stamps
  `CHECKPOINT.md` (status, current task, orientation, last verification, locked decisions,
  blockers, next action), `contract.md`, the first `NNN-*.md` slice, and a journal under
  `.loop/<slug>/` hidden by a self-ignoring `.gitignore` — failures and retries survive a
  compaction without entering history. A completed slice is deleted in the same commit that
  advances the note: one atomic commit, never a separate state commit, because a stop between
  the two leaves the pointer lying about what is done. Unverified work keeps its slice and its
  pointer; a judgment gate parks the note at `waiting-human` with the evidence needed.
- **One reader for both shapes.** `status.sh` reports the note's status fields, the current
  slice and whether its file still exists, the remaining queue, tree cleanliness, the history
  of retired slices, and the journal tail — native and adopted state now go through the same
  code path, since they are the same shape. Runs scaffolded in the `plan.md` shape are still
  read in that shape, so an in-flight loop keeps resuming with nothing to migrate.
- **Adopt mode tolerates foreign note shapes, and is loud when it cannot.** The reader only
  understood this skill's own notation, so pointing it at a note using YAML frontmatter or
  `## Heading` sections produced a plausible, entirely empty report — which reads as "nothing in
  progress" rather than "I could not parse this". It now accepts four field notations, finds the
  pointer on the naming line or the two after, reports unnumbered work files instead of a bare
  `0`, and prints `shape: UNRECOGNISED` with an instruction to read the note directly. Also
  fixes an mawk portability bug: `#{2,3}` never matched, because mawk has no interval
  expressions.
- **Release hygiene.** `bump_version.py` writes only `bundles.json`; the per-bundle manifests
  come from `generate_bundles.py`. v1.6.1 was committed with `--check` run in place of the real
  generate, so its four `plugin.json` files still declared 1.6.0 and a marketplace client keyed
  on the manifest version saw no new release. Fixed, and the unpushed v1.6.1 tag was dropped in
  favour of this release.

## v1.6.1

- **`autonomous-build-loop` binds to a repo's own continuation convention instead of
  assuming it owns its state.** The loop scaffolded `docs/loop/<slug>/` unconditionally, so a
  repo already running a checkpoint-and-task-slice convention ended up with two ledgers — its
  instruction file pointing a new session at one and the loop trusting the other. Setup now
  opens by resolving four state roles (orientation, ledger, history, contract) against
  whichever files hold them, native or adopted, in a precedence order rather than by
  inference: a live loop directory wins outright, and a repo whose "read this first" pointer
  targets the loop's own state is still native. New **L10** states the invariant — one source
  of truth, the substrate's commit and cleanup discipline outranking this skill's defaults —
  plus its exception: a substrate that records only durable decisions records no failed
  attempts, so the loop keeps an ephemeral ignored journal, because L5 and L8 read that rather
  than the audit trail. The cycle also separates a **judgment gate** (cheap, reversible, not
  the agent's call) from a blocked task and from the irreversible boundary, and drives
  session-sized slices as several cycles over the slice's own checklist instead of minting
  units of work to track itself.
- **Scripts.** `status.sh --adopt [note] [slice-dir]` reads a repo-owned note — status fields,
  current slice and whether its file is still present, uncommitted-change count, recent slice
  history — and prints which note it probed rather than guessing silently. `check.sh --gates
  <path>` runs a gate table the repo owns, keeping the contract on disk (L4) instead of retyped
  into an argument list each session, and accepts any `<LETTERS><digits>` row ID. `init.sh`
  refuses to scaffold beside a detected convention unless given `--force`.
- **Checker robustness fix.** Each declared check now runs in a subshell with `-u` disabled. A
  contract row that dereferenced an unset variable previously aborted the whole checker
  mid-report — no verdict for that row, no summary line, and an exit code indistinguishable
  from an ordinary failed check.
- **`checkpoint` gained a destination rule.** It mandated a single fenced block "and nothing
  else", which contradicted every caller that needs the same content written into a durable
  file. The paste-in block stays the default; a file-backed request now writes in place,
  preserving the target's existing headings and replacing stale content rather than appending.

## v1.6.0

- **New skill: `investigate-before-asking`** (thinking bundle). Resolves integration
  unknowns about external or unfamiliar systems from researchable artifacts — local
  checkouts, org code hosting, issue trackers, git history, live databases — and crosses
  team boundaries only with the non-inferable residue. Encodes an iron rule proven in the
  extraction session (source locally before remotely; verify the unknown's own premise
  first), an evidence ladder (wire contract > code with live callers > data sample >
  comment > inference) with the dead-code and prod-may-differ traps, a verbatim dispatch
  brief for read-only investigators, a rationalization table, and an output contract of
  per-unknown verdicts plus a minimal owner-addressed ask-list. Projects supply their own
  source map via an optional `ATLAS.md` beside the skill; all cross-skill references are
  capability-based so the skill ports across harnesses.

## v1.5.1

- **`write-design-spec` derives its sections from the reader instead of imposing a fixed
  list.** The skill assumed every document it touched was deciding something, so a document
  describing a shipped system to another team inherited *Rejected alternatives*, *Failure
  modes* and *Out of scope* — sections that argue with a reader who is not contesting
  anything. Two questions now settle the shape: can the reader still change the design, and
  will they operate the system or only understand it. *Out of scope* ("what we chose not to
  build") reframes to *Known limitations* ("what it does not do") when the reader was not
  party to the choice, and *Analogous feature & parity* is named as a builder's scoping
  instrument that never belongs in a document written for a later reader. The full structure
  stays the default for specs and ADRs.
- **Claim-first prose rule.** Lead every paragraph and bullet with its point, explanation
  after — a paragraph that opens with setup makes the reader carry context before they know
  what it is for.
- Reconciled `write-design-spec` drift from its maui-skills counterpart: the Architecture
  section now carries the change-footprint guidance (an inventory of what is being built,
  grouped by owning system, not a sequence ladder), matching what `architecture-diagrams`
  already prescribes for a design doc's first diagram.

## v1.5.0

- **`spec-overview` roots scan-label, then assert.** Comparing the skill's output against
  what the reader actually wanted showed pure-assertion roots scan worse than
  `**Sync** — the phone pulls the scene's entire comment set from GET /…/comments`: the
  bold word is what the eye finds on a re-scan, and the claim after the dash stays
  disagreeable. A label with no claim is still empty.
- **Refusals fold into the part they protect** instead of opening as a dedicated block —
  "no cursor, no tombstone table" under sync, "no change to any existing write function"
  under build cost. The block read as a second TL;DR and stripped each negative of the
  context that makes it checkable.
- **The interface surface is enumerated as its own part** — one line per route/command
  with the real verb and path; it is what another team implements against.
- Compactness rules: one line per child (the spec holds the argument), decision ids cited
  once at the line carrying the decision, open items question-first with the id trailing
  (`— PM call (TBD-E)`), and the title carries path/revision only when the overview
  travels beyond the conversation that named the document.

## v1.4.0

- **`spec-overview` is a briefing, not a review instrument.** It was written around the
  reviewer — "the reader already knows the domain and is scanning for the claim that is
  wrong" — which narrowed it to one of its uses. It produces a one-screen overview carrying
  the decisions; catching up, briefing a teammate, handing work to another team, and
  spotting a wrong claim are all things you can then do with it, and the artifact is
  identical either way.
- The falsifiability rule survives with a new justification: it was "a reviewer must be able
  to disagree", it is now "a line nobody could disagree with is conveying nothing". Same
  test, and it holds whether or not anyone is reviewing.
- **Three format improvements** from running the skill against a real design and comparing
  passes: the title carries provenance (name, path, revision), the deliberate negatives get
  their own opening section rather than being scattered, and root bullets assert instead of
  labelling so a reader can agree or disagree without descending. Open items are enumerated
  by id, including recently closed ones.

## v1.3.1

- **`spec-overview` titles the overview with a heading rather than a bold line.** Every
  root bullet in the format is already bold, so a bold title sat above them looking like a
  bullet that had lost its marker instead of a title. The worked example now opens with a
  heading, and the structure rules say why.

## v1.3.0

- **New `spec-overview` skill** (delivery-lifecycle) — condenses a spec, design doc, RFC,
  or plan into a one-screen bullet overview built for **correction rather than
  comprehension**. The reader already knows the domain and is scanning for the claim that
  is wrong, so the central rule is that every bullet must be falsifiable: if a domain
  reader cannot disagree with a line, it is cut. Vague bullets survive review by saying
  nothing, which is the failure mode the skill exists to prevent.
- Each line is written twice over — plain meaning first so a non-expert grasps the intent,
  then the exact identifier so an expert can check it against the code. Route paths, field
  names, roles, and decision ids are the correction handles. Root bullets follow the
  system's logical parts rather than the document's section order, nesting stays at two
  levels, undecided items come last because that is where corrections concentrate, and the
  document's deliberate negatives lead because negative claims are the easiest to falsify.
- The skill also records the round trip: a challenge to the overview is usually a defect in
  the spec, so it is fixed there and the overview regenerated.

## v1.2.1

- **`architecture-diagrams` picks the diagram by the reader's first question**, not by
  the topology it happens to be holding. The old tiebreaker made `SEQ` unconditional —
  every backend design has some request/response story — so a ladder won even where the
  document's own flow section already narrated the sequence in richer prose. The workflow
  now reads the target document's headings first: a design doc's opening diagram is the
  change footprint, and a doc that narrates the call order in prose does not get that
  order redrawn as a ladder.
- **New `FOOTPRINT` layout** answering "what are we actually building" — one box per
  owning system, one line per unit of work (route, table, column, trigger, function,
  setting) with counts and `(NEW)`/reused marks, a box for work the change depends on but
  does not own, and at most one connecting arrow per adjacent pair naming the hop rather
  than the messages.
- **`LR` no longer outgrows the review pane.** Gap width was previously whatever the
  longest label needed on one line, so width had no ceiling. Gaps are now sized naturally
  while the whole diagram fits 120 chars — anything that already fit renders byte-for-byte
  as before — and past that they share the leftover width while labels wrap onto the lines
  below their arrow. Long labels cost height, never a scrollbar.
- **Every arrow carries a preposition aimed at the partner** in all four layouts; the `SEQ`
  carve-out that dropped it on return arrows is gone.
- **New `scripts/regen_showcase.py`** so the gallery cannot drift from the generator: each
  example declares where its config comes from, and `--check` fails if any rendered block
  no longer matches what the generator produces.

## v1.2.0

- **New skill `general-coding-standards`** (delivery-lifecycle): language-agnostic coding
  standards translated from ASD-STE100 Simplified Technical English (Issue 9).
  40 rules in six banded, stable-ID sections — naming (controlled vocabulary +
  per-project glossary), statements/functions (guards first, one action per
  statement, size triggers), modules, errors/logs (severity + condition +
  consequence), prose (comments, docs, commits), and consistency. Ships a
  starter vocabulary (approved verbs, banned vague words), a review mode with
  rule-ID-tagged findings, and STE-MAPPING.md tracing all 53 rules + 8 general
  recommendations + the dictionary to their coding equivalents — each source
  rule fully paraphrased and page-referenced, no verbatim spec text.

## v1.1.0

- **New skill `filming-verification`** (delivery-lifecycle): record a short,
  caption-annotated screen video that proves a change works, in place of a
  written test report. Covers the film/prose/nothing decision, captioning with
  *measured* values, the ~1.5x readability ceiling (captions dominate the
  runtime, so speeding past it hides the evidence), verifying the film by
  extracting frames before delivering it, and two drivers — a test runner with
  built-in recording, or a browser-automation MCP plus an OS screen recorder
  that can show but not assert.
- `verify-before-done`: added the deliverable policy — chat prose with stable
  IDs (`TC-3`, `F2`) is the default; a file only when a reader outside the
  conversation needs it or the human asked; a film replaces the written report
  and its screenshots.
- `code-review`: findings belong in the conversation, not a report file; offer a
  film once for user-visible changes prose can't settle, never on backend,
  schema, or refactor-only diffs.
- `review-fix-loop`: pass lists and the final summary stay in chat (new **G7**)
  instead of `review-pass-N.md` / `review-final-report.md` — report files
  written for the person you are already talking to get deleted, and writing
  them slows the loop.
- `architecting`: reconciled with the downstream `maui-skills` copy, which had
  drifted — took that copy's more concrete plan-drift paragraph and kept this
  one's stronger interrogation directives, then ordered the design-time rules
  (directives, interrogation, resilience) before the execution-time one (plan
  drift). The two files are now identical.

## v1.0.2

- `address-comments`: corrected the GitLab raw-API reply note — `glab api
  --input -` needs an explicit `-H 'Content-Type: application/json'` (else
  `HTTP 415`); it is usable, not a dead end. Now consistent with the
  `code-review` skill's posting form.

## v1.0.1

- `address-comments`: documented GitLab reply-posting pitfalls in the forge
  mechanics reference — `glab api .../discussions/<id>/notes -f body=@file`
  posts the literal `@path` (unlike `gh`'s `-F`) and `--input -` fails
  `HTTP 415`; use the documented `glab mr note create --reply -m "$(cat …)"`,
  and verify the *stored note body* after posting, not just placement.

## v1.0.0

- Removed the obsolete `continuous-chat-loop` skill (major bump).
- Every skill now belongs to a bundle — no more root-only skills:
  - `set-output-style` → `harness-evolution`.
  - `formal-verification`, `functional-programming`, `site-refiner` →
    `delivery-lifecycle`.

## v0.1.0

- Initial release of the Evolving Harness framework.
- New `using-evolving-harness` router skill: routes non-trivial tasks through
  the gated lifecycle and runs the session-end evolution loop.
- Four plugin bundles generated from `bundles.json`: `harness-evolution`,
  `delivery-lifecycle`, `git-ops`, `thinking`.
- Plugin marketplace `evolving-harness` (`.claude-plugin/marketplace.json`).
- SessionStart hook nudging the router in the `harness-evolution` bundle.
- `scripts/generate_bundles.py` (bundle generator) and
  `scripts/bump_version.py` (release helper); CI validation workflow.
- The flat root catalog remains unchanged and `npx skills add Harduex/skills`
  keeps working.
