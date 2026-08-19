---
name: write-handoff-doc
description: Converts an internal artifact — a design spec, a shipped branch or feature, an API or data contract — into a self-contained handoff document an external team can read fast and act on without any internal context. Use when handing a contract, integration guide, or feature description to another team or company, when asked for a handoff document, a client-facing explainer, or a doc to publish outside the repo (Google Doc, wiki, PDF), when converting a spec into something reviewable by people without codebase access, or when folding a published copy's review edits back into the repo source.
---

# Writing External Handoff Documents

A handoff document is a **projection** of an internal artifact for a reader who cannot change the design and will never operate your internals: everything they must implement or obey, nothing about how you store, decide, or track things. It must read fast — a reviewer decides from the first paragraph — and survive being read with zero context.

If a design-spec capability exists in your set, it owns the internal artifact (decisions, rejected alternatives, architecture); this skill owns the external projection derived from it. The repo file is the source of truth; the published copy (Google Doc, wiki) is a paste of it.

## The audience filter — the non-negotiable

Include only what the reader can act on; cut everything whose audience is your own team:

- Internal storage, schema, roles, migrations. **Storage is not contract**: expose the wire/interface shape, never where a field happens to live — lifting a stored blob's key to a typed top-level field is the norm, not duplication.
- Decision IDs, ticket keys, team history, internal file paths, review threads.
- Your side's open work and internal revisit-triggers ("add pagination the day X disproves the bound"). Keep **their** open items; for yours state only the user-visible effect ("until then, X is simply null").

**Verify every claim against live code before writing it, and every URL by fetching it.** An invented field name or a dead link handed to an external team is this skill's core failure mode. A detail that is genuinely not pinned yet gets an explicit hedge ("the exact fields will be in the <living reference>") — never a fabricated name. Refinements the exemplars settled:

- **A proposal handoff has no live code** — there the internal spec's contract is the verification baseline, and the dateline's "proposal" status carries that caveat once for the whole document; don't re-hedge every field.
- **Null semantics or formats the source doesn't pin get one collective hedge** under the example block, never per-field guesses.
- **Say where requests go** — the host/base URL, or an explicit "delivered separately / same base as <sibling doc>" — never a silent assumption.
- **Sibling external docs may be referenced by title**; attach the link only once its published URL is verified to resolve.

## Format

Full annotated skeleton in [REFERENCE.md](REFERENCE.md). The shape:

1. **Title** — "The <thing> for <audience>" or "How <thing> works in <system>".
2. **Italic dateline** — last-updated date (the handoff's own last edit, not the internal source's date); status (*agreed proposal, ready for review* vs *describes what exists today*); a supersedes-link when replacing a published predecessor; "field names are final unless this review changes them" when true.
3. **One intro paragraph** — what the thing is, who the doc is for, what it covers, what becomes the living reference later. No Background/Motivation/History sections, ever.
4. **`## The short version`** — one paragraph carrying ~90% of the content; a reader who stops here can decide. This is the one licensed long paragraph.
5. **Middle sections ordered by the reader's tasks** in order of first need (an API reads: authenticate → read → identify → write → offline/replay rules → domain conventions) — never by your architecture.
6. **`## What it deliberately does not do`** — define by negation; each bullet says what to do instead where one exists.
7. **`## Open items on <their> side`** — only theirs, only actionable, each with the user-visible effect until it lands.

Rendering rules:

- **Bold-led paragraphs**: the claim first, elaboration after ("**Polling is cheap.** …").
- **Enumerable facts are tables**: an annotated JSON/example block for shapes; `Rule | Cost of ignoring it` for conventions you don't enforce; an error/edge table with a *their-reaction* column — the column is the invariant, the placement is free (its own late section for a multi-route contract; folded into the task section for a single small surface).
- **One analogy** for the single hardest concept — not more.

## Prose

**Before writing any prose, invoke your set's controlled-language / writing-standards capability** (in this catalog: `general-standards`) and follow its own routing for documents. Capability mentions don't self-fire: actually invoke the capability rather than working from a summary of it. That capability owns these rules and decides which of its references a document author needs; this skill neither restates them nor names its files. The short-version paragraph is the stated exception to paragraph caps. On top of that standard, the rules this genre keeps re-learning:

- **Define a term inline at first use the moment it could be misread** ("across threads — between different root comments — any order"). If the author pauses on a sentence, an external reviewer will too: fix the sentence, don't plan to explain it in review.
- **Pair every data rule with its UI action and the field that triggers it** — what to do with the data + what to show the user + which response field says which. A data rule alone ("keep your cache") reads as contradicting the UX until the pairing is explicit.
- **Redundancy across homes is deliberate.** Contract sections, the conventions table, and the error table each serve a reader who jumped straight there — keep each home complete; cut only same-home duplication. Reading speed comes from structure, not from squeezing words.

## Lifecycle

1. Write or update the repo file next to its internal source, named `<topic>-handoff.md` (or the project's docs convention); commit.
2. Publish by pasting. **Never rewrite a previously published predecessor whose review comments anchor to its text** — publish a new doc and mark the old one superseded (with a link) only after its threads close.
3. Fold review edits back as a delta: fetch the live published text, diff against the repo file, apply the substantive changes, and **skip publish-medium artifacts** — page-break headings, escaped punctuation, table-alignment noise, lost code-fence languages, curly quotes. Fix grammar slips on the way and flag them back so both copies stay identical.
4. Any repo-file change → re-paste to the published copy. The two never drift silently.

## Checklist

- [ ] Writing-standards capability invoked before writing, and its document rules applied
- [ ] Every technical claim verified against live code/data; every link fetched and resolving
- [ ] No internal storage, roles, decision IDs, tickets, or team history anywhere
- [ ] The short version alone is decision-sufficient
- [ ] Sections ordered by the reader's tasks, not your architecture
- [ ] Every unenforced convention carries its cost of ignoring
- [ ] Define-by-negation section present
- [ ] Open items are theirs only, each with the user-visible effect
- [ ] Unpinned details hedged explicitly, never invented
- [ ] Published copy is a paste of the repo source; medium artifacts stripped on every sync back
