---
name: write-design-spec
description: Authors concise, reviewable design specs (written before implementation) and as-built architecture decision records (ADRs, written after a feature ships) for features and systems. Enforces a fixed structure (TL;DR, ASCII architecture, contract, decisions table, failure-modes table, out of scope) and an assertive, contract-first style. Use when writing or rewriting a design doc, reviewing a spec for shape and clarity, or — once a branch/feature is finished and ready to ship, or when the user explicitly asks — converting it into an ADR ("convert branch to ADR"). The spec is the pre-implementation artifact; the ADR is the post-ship record — do not create an ADR mid-task or speculatively.
---

# Writing Design Specs

A design spec describes the *shape* of a solution — contracts, decisions, tradeoffs, non-goals, *and the alternatives that lost*. Not implementation, not background, not narrative. **A reader who only reads the TL;DR must understand ~90% of the design.** Everything below the TL;DR is elaboration.

A spec is the long-lived source of truth for "what we built and why". It is **not** a pre-implementation artifact that gets abandoned the moment code ships. After ship, update the date line to `(as-built: YYYY-MM-DD)`, add a `**Status:** Authoritative.` line, and reconcile any divergence between the spec and the code — the code wins, the spec gets corrected. In a repo with no separate decision log, this *is* the ADR. In a repo that keeps one (e.g. `docs/adrs/`), promote the settled spec into an ADR there with this same structure — see [Converting a shipped branch into an ADR](#converting-a-shipped-branch-into-an-adr).

## Required structure

Use these sections, in this order. Skip a section only if it would genuinely be empty.

1. **Title + frontmatter lines** — `**Date:** YYYY-MM-DD` (add `(as-built: YYYY-MM-DD)` once shipped), `**Scope:** <one sentence stating what is in scope and who it is for>`, and once shipped a `**Status:** Authoritative. <one-line pointer to the implementation path or branch>`. No table of contents, version history, author block, or badges.
2. **TL;DR** — one paragraph, 5–10 sentences. Must contain, in any order: what the thing is, the core mechanism, the key tradeoff, the access/security model in one line, and what is *not* in scope. If you cannot compress to one paragraph, the design is not ready.
3. **Architecture** — one ASCII box-and-arrow diagram in a fenced block (monospace renders everywhere — PRs, terminals, plain editors). If a dedicated diagramming skill is available in your set, build the diagram with it rather than hand-aligning ASCII. Underneath it, one short sentence that defines the design **by negation**: e.g. *"One endpoint. No preflight, no token, no server-side manifest, no queue."*
4. **The contract** — exact request shape, exact response headers/body, exact error codes (`400 empty_selection`, `404 nothing_to_download`). Use real codebase identifiers (table names, column names, role names, types, endpoints). Not "the API returns an error" — name the code and the wire format.
5. **Resolution / flow** — numbered list. Each step states what happens *and* which security or correctness invariant it enforces (auth gate, type filter, headers-not-yet-written guard, etc.).
6. **Key decisions** — markdown table with columns `# | Decision | Why`. Each *Why* cell is self-contained: it includes the tradeoff with numbers when possible (e.g. *"DEFLATE buys ~1% size at 5–10× CPU. STORED skips that."*) and would convince a skeptical reviewer on its own, without context from elsewhere in the doc.
7. **Rejected alternatives** — markdown table with columns `Option | Why rejected`. This is the *decision graveyard* — the options a future reader is most likely to propose without knowing you already considered them. Include the architecture-level rejects (hosting plane, async-job vs streaming, preflight vs single-shot), the library bake-off, and any naming/contract decisions that have a tempting wrong answer. Each *Why rejected* cell must be self-contained, name a concrete failure mode or cost (FD pressure, CPU/byte, blast radius, contract drift), and not require reading any other row. **Omit options nobody would seriously propose** — the table is a defense against re-litigation, not a survey of the option space.
8. **Failure modes** — markdown table with columns `When | Where | Result`. Every failure the system can hit, mapped to its handler. Cover adversarial inputs (forged requests, race conditions, partial inputs) — not just happy-path errors. End with one sentence on what state survives a failure (typically: none).
9. **Analogous feature & parity** — name the closest existing analog to the thing being designed. Enumerate the surfaces the analog touches by searching its identifier across the codebase (UI surfaces, endpoints, schema, permissions, notifications, analytics, tests) — do not enumerate from memory. Then a markdown table with columns `Surface | In scope? | Reason`: every analog surface is either in scope or explicitly out, with a reason. The out-of-scope rows are the deferred-gaps record for follow-up work. Omit the section only when the feature genuinely has no analog — say so in one line instead.
10. **Out of scope** — bulleted list. Explicit non-goals, deferred items ("v2"), and *deliberate* omissions (rate limiting, resumable downloads, reporting skipped items). This bounds the review and prevents scope drift in implementation.

## Style rules

- **Assertive prose.** Write what *is*, not what *should be*. "The frontend submits via a hidden form" — not "the frontend could/should submit". Strike *may*, *might*, *we should consider*, *in the future perhaps*.
- **State the threat model.** Any spec touching a boundary answers three questions: what does the backend trust, what does it independently verify, what does a hand-crafted/forged request hit? Make this explicit, not implicit.
- **Numbers in tradeoffs.** When a decision rests on cost or performance, put the number in the *Why* cell. "Tens of KB per request", "~1% size at 5–10× CPU", "30-minute gateway timeout".
- **Use codebase identifiers.** Real names from the actual code: `global_admin_role`, not `userRole`; `nodeUuids`, not `ids`; `payment-service`, not "the backend service".
- **Mirror existing patterns.** When the design introduces a unit that already has siblings in the codebase — a component beside components, an op beside ops, a migration beside migrations — name, place, and shape it like the closest existing one (its suffix conventions, file location, structure). Any deliberate divergence from a sibling pattern belongs in the Key decisions table with its reason, so the choice is reviewable instead of accidental.
- **Define by negation.** Somewhere in the spec, list what it explicitly does *not* do. Half the value of the doc is fencing off what the design has chosen to skip.
- **Record what you chose against, not just what you chose.** The rejected-alternatives table is load-bearing — it's the artifact that prevents the same architectural debate from re-opening in six months. If a decision didn't have a serious alternative, don't manufacture one; but if it did, the loser belongs in the table with a one-sentence cause-of-death.
- **Push implementation out.** Pseudo-code, library choice rationale, error-handling minutiae, internal call ordering — these belong in the plan, not the spec. When tempted, write *"implementation detail, lives in the plan"* and move on.
- **Symmetric tables.** Every row in `Key decisions` and `Failure modes` has the same shape and depth. If one row needs four sentences and another needs three words, you're mixing levels of abstraction.

## Forbidden

- Mermaid / PlantUML / sequence diagrams as the *primary* diagram. ASCII first; supplemental rich diagrams only if they add something ASCII genuinely cannot show.
- "Background", "Introduction", "Motivation" sections. Lead with TL;DR. The scope line and the TL;DR carry the framing.
- Unstructured prose where a table works. Decisions and failure modes are *always* tables.
- Time estimates, owner assignments, rollout phases, milestone dates. Those belong in the plan/RFC, not the design.
- Speculative future sections ("v2 might…", "we could later…"). Either it is in scope, or it is in *Out of scope*. There is no third state.
- Implementation code beyond a contract type (`{ nodeUuids: string[] }` is fine; a 20-line handler sketch is not).

## Rewriting an existing spec into this shape

1. Write the **TL;DR** first, from scratch, ignoring the existing prose. If you cannot land it in one paragraph, the design has unresolved questions — surface them before continuing.
2. Convert every "we decided / we chose / it was decided" prose paragraph into a row of the **Key decisions** table. For each row, force a numeric or named tradeoff into the *Why* cell.
3. Walk the doc and rewrite every *should/may/could/might* as an assertion — or move it to *Out of scope* if it isn't actually decided.
4. Sweep the doc (and any superseded research / RFC / ADR) for the load-bearing rejected options — the architecture branches not taken, the library that lost the bake-off, the contract field name that was tempting but wrong — and consolidate into **Rejected alternatives**. Then delete the source documents; the spec absorbs their reasoning.
5. Sweep the doc for everything the design deliberately *doesn't* do; consolidate into **Out of scope**.
6. Strip implementation detail: pseudo-code, library APIs, internal ordering, retry policies. Leave the contract, the invariants, and the *why*.
7. Replace any rich diagram with an ASCII box-and-arrow if it can carry the same information. Keep the rich one only if removing it loses meaning.

## Converting a shipped branch into an ADR

An ADR is the **as-built** counterpart of the spec — the spec is written *before* the code, the ADR *after*, and the code is its source of truth. **Gate first:** create an ADR only once the implementation is finished and ready to ship, or when the user explicitly asks. Never spin one up mid-task or speculatively — a half-built feature has no settled architecture to record. If the repo keeps no decision log (no `docs/adrs/` or equivalent), **ask the user** whether to start one and where; create the location only if they want it, rather than inventing a path.

1. **Match the log's format.** Read the most recent `docs/adrs/ADR-NNNN-*.md` and mirror its frontmatter (`**Date:** … (as-built: YYYY-MM-DD)`, `**Status:**`, `**Scope:**`, a linked `**Implementation:**` block) and section order. The new file is `ADR-<next-number>-<slug>.md` (the first in a freshly created log is `ADR-0001`).
2. **Gather the as-built facts** from the shipped branch — exact migration/file paths, contract signatures, role grants, indexes, test paths — and link them. Don't copy a pre-build spec's contract verbatim; verify it against what merged.
3. **Add a `Plan → as-built deltas` table.** Every place the shipped code diverged from the pre-build spec/plan is a row (`Plan | As-built | Why`). This is the highest-value part of an as-built ADR and the thing a plan-only doc cannot capture.
4. **Draw the diagram with the diagramming skill** if one is in your set; mark `(NEW)` on what the branch adds.
5. **Keep rollout out.** Feature flags, percentages, and milestone dates are rollout, not architecture — omit them.
6. **Remove the superseded planning docs.** Once the ADR absorbs them, `git rm` the pre-build design spec / test plan / implementation plan — git history preserves them — and repoint any ADR links off the deleted files. Confirm deletion + commit with the user first.

## Review checklist

- [ ] Date + Scope lines at the top, nothing else above the TL;DR
- [ ] TL;DR is one paragraph and reads as a complete summary on its own
- [ ] ASCII architecture diagram followed by a define-by-negation sentence
- [ ] Exact request / response / error contracts using real codebase names
- [ ] Threat model stated: what is trusted, what is independently verified, what a forged request hits
- [ ] `# | Decision | Why` table where each *Why* is self-contained and includes numbers where relevant
- [ ] New units mirror the closest existing sibling's naming/location/structure, or the divergence is recorded in Key decisions
- [ ] `Option | Why rejected` table covering the architecture branches not taken, the library bake-off, and any contract decisions with a tempting wrong answer — each row self-contained
- [ ] `When | Where | Result` failure-modes table covering adversarial inputs and race conditions
- [ ] Closest analog named, its surfaces enumerated from a codebase search, and a `Surface | In scope? | Reason` parity table (or an explicit one-line "no analog")
- [ ] Out-of-scope section enumerating deferred items *and* deliberate omissions
- [ ] No hedging language, no implementation minutiae, no future-tense speculation, no estimates or owners
- [ ] If shipped: `(as-built: YYYY-MM-DD)` on the date line, `**Status:** Authoritative` line with implementation pointer, and divergence between spec and code reconciled (code wins)
