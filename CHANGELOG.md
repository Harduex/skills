# Changelog

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
