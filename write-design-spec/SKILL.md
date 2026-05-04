---
name: write-design-spec
description: Authors concise, reviewable design specs for features and systems. Enforces a fixed structure (TL;DR, ASCII architecture, contract, decisions table, failure-modes table, out of scope) and an assertive, contract-first style. Use when writing a new design doc, rewriting an existing one, or reviewing a spec for shape and clarity.
---

# Writing Design Specs

A design spec describes the *shape* of a solution — contracts, decisions, tradeoffs, non-goals. Not implementation, not background, not narrative. **A reader who only reads the TL;DR must understand ~90% of the design.** Everything below the TL;DR is elaboration.

## Required structure

Use these sections, in this order. Skip a section only if it would genuinely be empty.

1. **Title + frontmatter lines** — `**Date:** YYYY-MM-DD` and `**Scope:** <one sentence stating what is in scope and who it is for>`. No table of contents, version history, author block, or status badges.
2. **TL;DR** — one paragraph, 5–10 sentences. Must contain, in any order: what the thing is, the core mechanism, the key tradeoff, the access/security model in one line, and what is *not* in scope. If you cannot compress to one paragraph, the design is not ready.
3. **Architecture** — one ASCII box-and-arrow diagram in a fenced block (monospace renders everywhere — PRs, terminals, plain editors). Underneath it, one short sentence that defines the design **by negation**: e.g. *"One endpoint. No preflight, no token, no server-side manifest, no queue."*
4. **The contract** — exact request shape, exact response headers/body, exact error codes (`400 empty_selection`, `404 nothing_to_download`). Use real codebase identifiers (table names, column names, role names, types, endpoints). Not "the API returns an error" — name the code and the wire format.
5. **Resolution / flow** — numbered list. Each step states what happens *and* which security or correctness invariant it enforces (auth gate, type filter, headers-not-yet-written guard, etc.).
6. **Key decisions** — markdown table with columns `# | Decision | Why`. Each *Why* cell is self-contained: it includes the tradeoff with numbers when possible (e.g. *"DEFLATE buys ~1% size at 5–10× CPU. STORED skips that."*) and would convince a skeptical reviewer on its own, without context from elsewhere in the doc.
7. **Failure modes** — markdown table with columns `When | Where | Result`. Every failure the system can hit, mapped to its handler. Cover adversarial inputs (forged requests, race conditions, partial inputs) — not just happy-path errors. End with one sentence on what state survives a failure (typically: none).
8. **Out of scope** — bulleted list. Explicit non-goals, deferred items ("v2"), and *deliberate* omissions (rate limiting, resumable downloads, reporting skipped items). This bounds the review and prevents scope drift in implementation.

## Style rules

- **Assertive prose.** Write what *is*, not what *should be*. "The frontend submits via a hidden form" — not "the frontend could/should submit". Strike *may*, *might*, *we should consider*, *in the future perhaps*.
- **State the threat model.** Any spec touching a boundary answers three questions: what does the backend trust, what does it independently verify, what does a hand-crafted/forged request hit? Make this explicit, not implicit.
- **Numbers in tradeoffs.** When a decision rests on cost or performance, put the number in the *Why* cell. "Tens of KB per request", "~1% size at 5–10× CPU", "30-minute gateway timeout".
- **Use codebase identifiers.** Real names from the actual code: `global_admin_role`, not `userRole`; `nodeUuids`, not `ids`; `payment-service`, not "the backend service".
- **Define by negation.** Somewhere in the spec, list what it explicitly does *not* do. Half the value of the doc is fencing off what the design has chosen to skip.
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
4. Sweep the doc (and the surrounding research/RFC if any) for everything the design deliberately *doesn't* do; consolidate into **Out of scope**.
5. Strip implementation detail: pseudo-code, library APIs, internal ordering, retry policies. Leave the contract, the invariants, and the *why*.
6. Replace any rich diagram with an ASCII box-and-arrow if it can carry the same information. Keep the rich one only if removing it loses meaning.

## Review checklist

- [ ] Date + Scope lines at the top, nothing else above the TL;DR
- [ ] TL;DR is one paragraph and reads as a complete summary on its own
- [ ] ASCII architecture diagram followed by a define-by-negation sentence
- [ ] Exact request / response / error contracts using real codebase names
- [ ] Threat model stated: what is trusted, what is independently verified, what a forged request hits
- [ ] `# | Decision | Why` table where each *Why* is self-contained and includes numbers where relevant
- [ ] `When | Where | Result` failure-modes table covering adversarial inputs and race conditions
- [ ] Out-of-scope section enumerating deferred items *and* deliberate omissions
- [ ] No hedging language, no implementation minutiae, no future-tense speculation, no estimates or owners
