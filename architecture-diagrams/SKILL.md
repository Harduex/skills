---
name: architecture-diagrams
description: Create consistent, readable architecture, system, and flow diagrams using C4 conventions rendered in ASCII (for specs, RFCs, design docs, READMEs, PRs). Use when drawing or editing an architecture / system / context / container diagram, a change-footprint or scope diagram (what a change actually adds), a request/response or sequence flow (who-calls-whom-in-what-order), a box-and-arrow diagram in a markdown doc, when a reviewer says a diagram shows the wrong thing or answers the wrong question, or when a diagram is too wide for a review pane or its boxes/arrows are misaligned. Encodes the C4 element and relationship conventions and bundles a generator with four layouts — FOOTPRINT, SEQ, LR, TB — so alignment and width are computed, never hand-counted.
---

# Architecture Diagrams (C4, ASCII-first)

Model with **C4** ([c4model.com](https://c4model.com)); render in **ASCII** by default — it diffs cleanly and shows up correctly everywhere (specs, PRs, terminals, plain editors).

## Choosing a layout (do this first)

**ASCII is the default for every shape.** The bundled generator automates four layouts; the other ASCII shapes you draw by hand using the conventions below.

**Choose by the reader's first question, not by the topology you happen to be holding.** One system yields a different correct diagram depending on what the section is for — a system that *has* a request/response story is not thereby a diagram *about* that story:

| The reader's first question | Draw it as | Notes |
|---|---|---|
| ***What are we actually building?*** — the change inventory: routes, tables, columns, triggers, functions, settings, and who owns each | **the generator, `ORIENTATION = "FOOTPRINT"`** | one box per owning system, one line per unit of work, at most one connecting arrow per adjacent pair. Small enough to take in at a glance, and it's what a lead wants first from a design doc |
| ***Who calls whom, in what order?*** — a request/response flow | **the generator, `ORIENTATION = "SEQ"`** | an RFC-style ladder (OAuth RFC 6749, SIP call flows): boxes across the top, lifelines down, one labeled arrow per message in time order. Labels stack in time instead of widening gaps, so width barely grows with edge count |
| ***How do the pieces sit relative to each other?*** — static structure, 2–3 owning systems | **the generator, `ORIENTATION = "LR"`** | the classic side-by-side read: each arrow is a sentence in the gap between two boxes. It sizes gaps naturally while the diagram fits, then wraps the labels above their arrows rather than widening — height, not a scrollbar |
| the same, across 4+ systems | **the generator, `ORIENTATION = "TB"`** | width ≈ widest box + longest label, regardless of system count |
| a small hub-and-spoke / C4 **Context** (a system with a few neighbours or actors) | **free-form ASCII**, by hand, using the conventions below | keep it small — radial ASCII stays readable only when the edges are few |
| too large/dense to stay readable in ASCII, **or** it must be interactive / zoomable / a polished export | render **outside ASCII** — Mermaid-C4 / PlantUML-C4 / Structurizr | the *only* reason to leave ASCII |

**Hard width budget: 120 chars.** A diagram wider than a code-review pane gets a horizontal scrollbar and reviewers see half of it — `verify_boxes.py` flags this. `"LR"` and `"FOOTPRINT"` hold the budget themselves by spending height on long labels instead of width, and `"SEQ"` and `"TB"` are width-stable by construction; a warning therefore means the *boxes* are too wide, so shorten the box lines. Never ship the scroll.

## The rule for the generated layouts: compute alignment, don't count spaces

When you *are* drawing a generator shape, let it place every box width, gap, arrow, and header — **never hand-align them.** Off-by-one borders and labels overflowing their gap are otherwise guaranteed, and you'll burn turns re-counting. This rule governs *alignment*, not *which diagram to draw* (that's the table above).

[scripts/diagram.py](scripts/diagram.py) — set `ORIENTATION`, edit the `COLUMNS`, `EDGES`, and `SKIP_EDGES` blocks (one config drives all four layouts), then:
- `python3 scripts/diagram.py` → print the diagram (eyeball it; heed the width warning)
- `python3 scripts/diagram.py path/to/doc.md` → splice it into that file's fenced ``` block (the one whose first line contains the first boundary label)

Copy the script next to the doc you're editing; it's stdlib-only, no dependencies.

## Hand-drawn shapes: verify each box (no generator covers these)

Hub-and-spoke diagrams are drawn by hand — and that's where borders silently go missing. **Don't eyeball it; run the bundled checker** before shipping:

```
python3 scripts/verify_boxes.py doc.md        # lints every fenced diagram in the doc
python3 scripts/verify_boxes.py diagram.txt   # or a raw diagram / piped stdin
```

It flags any box missing a border, a broken side wall, a misaligned corner, or a diagram over the 120-char width budget — the failures hand-drawing (and hand-editing a generated doc) silently ships. Exit 0 = clean. (Generator boxes are correct by construction, and the checker recognises skip-edge routing, so it's safe to run on any diagram.)

## Conventions (apply to every diagram)

- **Each `COLUMNS` entry is one owning system / boundary**, drawn as a bordered box with a guillemet header (above the box in `"LR"`, its first line in `"TB"`); mark externals: `« PROVIDERS — external »`. **The border is the boundary** (C4 system boundary), not a container.
- **Each line inside the box is a container**, tagged with its technology: `api gateway  [Go]`, `database  [Postgres]`. Indent sub-details one space.
- **Arrows = relationships, read as a sentence.** The **left box (`"TB"`: the upper box; `"SEQ"`: the arrow's source) is the subject** and the **preposition points at the partner**:
  - outbound (`→` / `▼`): `forwards token to [HTTPS]`
  - return (`←` / `▲`): `receives push from [WebSocket]` (in `"SEQ"`, where the source is the subject, write the source's action and keep the preposition: `pushes update to [WebSocket]`)

  **Every arrow carries a preposition aimed at the partner** — `to`, `from`, `into`, `against`. This holds in all four layouts, `"FOOTPRINT"` included: a label whose preposition attaches to the protocol or a role instead (`calls the routes on [HTTPS]`, `queries as the customer role [SQL]`) stops being a sentence about two systems and becomes a note about one. Always bracket the `[protocol/tech]`. The arrowhead shows direction; the preposition keeps it readable as text. In `"LR"` a label that outgrows its gap wraps onto the lines below it rather than widening the diagram, so terse labels buy compactness, not correctness; `"TB"` gives each label a full line; `"SEQ"` word-wraps labels above their arrow.
- **Skip-level calls** (a system talks to a non-adjacent one) are `SKIP_EDGES`, routed in a channel below (`"LR"`) or right of (`"TB"`) the boxes. Same subject/preposition rule. In `"SEQ"` there are no skip edges — every message goes in `EDGES` (time-ordered, `{"from": i, "to": j, "label": …}`) and simply draws as a longer arrow.
- **Mark deltas with `(NEW)`** on whatever the current change adds; everything unmarked is reused.
- **In `"FOOTPRINT"` each line is a unit of work, not a container** — a route, column, table, trigger, function, or setting — carrying its count where it has one (`+4 columns`, `×2 functions`). Every line is marked: `(NEW)`, or a `reused` line naming what it leans on. Work you depend on but don't own gets its own boundary box, `« not ours — external owners »`, with the ticket that owns it — so the diagram shows what you must *ask for* alongside what you build. That box takes no arrow; it's a dependency panel, not a hop.
- **A footprint's arrows name the hop, not the messages** — at most one per adjacent pair (`queries as the customer role [SQL]`), never a call-by-call sequence. Arrows are what stop the diagram reading as three stacked shopping lists; a ladder's worth of them is what `"SEQ"` is for.
- **One sentence under the diagram defines it by negation** ("No new datastore. No second front door. …") — the same define-by-negation sentence a design spec carries.

## Workflow

1. **Read the target document first and list its headings.** Two facts about the doc settle the shape before topology gets a vote:
   - **A design doc's first diagram is a `"FOOTPRINT"`.** Under an `Architecture` / `Overview` / `Design` heading the reader has not yet asked how bytes move — they're asking what gets built and who owns it. Answer *that* question there.
   - **If the doc narrates the call sequence in prose, don't draw it twice.** A `Flow` / `Sequence` / `How it works` heading, or numbered steps of the form "the app calls X, then X calls Y", means the ladder is already written and carries more than a diagram can. Draw the `"FOOTPRINT"` instead.

   A doc can carry **two** diagrams: the footprint under `Architecture`, and a `"SEQ"` ladder beside a flow section whose prose doesn't already carry the sequence.
2. **Choose the shape** from the reader's-question table. If it's not a generator shape, stop here and use the right tool.
3. Pick the C4 level — **Context** (systems + people), **Container** (deployable units; the usual choice for a spec), or **Component** (inside one container). Don't mix levels in one diagram. (`"FOOTPRINT"` sits outside this: its lines are units of work, not elements.)
4. Map: boundaries → columns; box lines → containers, or units of work in `"FOOTPRINT"`; interactions → `EDGES` (adjacent) and `SKIP_EDGES` (non-adjacent), each with direction + `[protocol]`.
5. Run the generator, eyeball it, and honor the width warning (switch to `"SEQ"` rather than ship a sideways scroll), then patch into the doc.
6. Add the define-by-negation sentence; add a legend only if a label isn't self-evident.

See [SHOWCASE.md](SHOWCASE.md) for a rendered gallery of every layout (FOOTPRINT, SEQ, LR, TB stacked/staggered, hand-drawn hub-and-spoke), each with the copy-paste config that produced it — the fastest way to pick a layout and start from a working config. See [REFERENCE.md](REFERENCE.md) for the C4 element cheat-sheet, the full generator config (including `SKIP_EDGES`), and the alignment failure modes this prevents.
