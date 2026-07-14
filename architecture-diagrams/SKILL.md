---
name: architecture-diagrams
description: Create consistent, readable architecture, system, and flow diagrams using C4 conventions rendered in ASCII (for specs, RFCs, design docs, READMEs, PRs). Use when drawing or editing an architecture / system / context / container diagram, a request/response or sequence flow (who-calls-whom-in-what-order), a box-and-arrow diagram in a markdown doc, or when a diagram is too wide for a review pane or its boxes/arrows are misaligned. Encodes the C4 element and relationship conventions and bundles a generator with three layouts — SEQ (an RFC-style sequence ladder, the default for flows), LR (side-by-side), and TB (stacked) — so alignment and width are computed, never hand-counted.
---

# Architecture Diagrams (C4, ASCII-first)

Model with **C4** ([c4model.com](https://c4model.com)); render in **ASCII** by default — it diffs cleanly and shows up correctly everywhere (specs, PRs, terminals, plain editors).

## Choosing a layout (do this first)

**ASCII is the default for every shape.** The bundled generator automates three layouts — `"LR"` (owning systems side by side), `"TB"` (systems stacked down the page), and `"SEQ"` (an RFC-style ladder: boxes across the top, lifelines down the page, one horizontal labeled arrow per message in time order — how OAuth RFC 6749 and the SIP call-flow RFCs draw multi-party flows in 72 columns). The other ASCII shapes you draw by hand using the conventions below. Match the *layout to the topology of the story* — don't bend the architecture to fit the tool:

| If the story is… | Draw it as | Notes |
|---|---|---|
| a request/response flow — *who calls whom, in what order* (most design-spec diagrams) | **the generator, `ORIENTATION = "SEQ"`** | labels stack in time instead of widening gaps, so width barely grows with edge count; returns and skip-level calls are ordinary arrows. The default for flows |
| static structure across 2–3 owning systems with short labels | **the generator, `ORIENTATION = "LR"`** | width grows with every column *and* every label — it stops fitting a review pane fast |
| static structure across 4+ systems (no meaningful time order) | **the generator, `ORIENTATION = "TB"`** | width ≈ widest box + longest label, regardless of system count |
| a small hub-and-spoke / C4 **Context** (a system with a few neighbours or actors) | **free-form ASCII**, by hand, using the conventions below | keep it small — radial ASCII stays readable only when the edges are few |
| too large/dense to stay readable in ASCII, **or** it must be interactive / zoomable / a polished export | render **outside ASCII** — Mermaid-C4 / PlantUML-C4 / Structurizr | the *only* reason to leave ASCII |

**Hard width budget: 120 chars.** A diagram wider than a merge-request review pane gets a horizontal scrollbar and reviewers see half of it — the generator and `verify_boxes.py` both flag this. Fix by switching to `"TB"` or shortening labels, never by shipping the scroll.

## The rule for the generated layouts: compute alignment, don't count spaces

When you *are* drawing a generator shape, let it place every box width, gap, arrow, and header — **never hand-align them.** Off-by-one borders and labels overflowing their gap are otherwise guaranteed, and you'll burn turns re-counting. This rule governs *alignment*, not *which diagram to draw* (that's the table above).

[scripts/diagram.py](scripts/diagram.py) — set `ORIENTATION`, edit the `COLUMNS`, `EDGES`, and `SKIP_EDGES` blocks (same config drives both orientations), then:
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
  - return (`←` / `▲`): `receives push from [WebSocket]` (in `"SEQ"` write the source's action instead: `pushes update [WebSocket]` on a leftward arrow)

  Always bracket the `[protocol/tech]`. The arrowhead shows direction; the preposition keeps it readable as text. In `"LR"` keep labels terse — every label widens its gap and the whole diagram; `"TB"` gives each label a full line; `"SEQ"` word-wraps labels above their arrow.
- **Skip-level calls** (a system talks to a non-adjacent one) are `SKIP_EDGES`, routed in a channel below (`"LR"`) or right of (`"TB"`) the boxes. Same subject/preposition rule. In `"SEQ"` there are no skip edges — every message goes in `EDGES` (time-ordered, `{"from": i, "to": j, "label": …}`) and simply draws as a longer arrow.
- **Mark deltas with `(NEW)`** on whatever the current change adds; everything unmarked is reused.
- **One sentence under the diagram defines it by negation** ("No new datastore. No second front door. …") — the same define-by-negation sentence a design spec carries.

## Workflow

**Tiebreaker (apply first, it settles most cases):** if the diagram has *any* request/response, message, or ordering story to tell — anything you'd narrate as "X calls Y, then Y calls Z" — default to `"SEQ"`. Reach for `"LR"` / `"TB"` only for pure box-and-line *structure* with no meaningful time order (a component map, a deployment topology). When a diagram could be read either way, prefer `"SEQ"`: a flow drawn as static structure loses its ordering, but structure drawn as a flow just reads as a short ladder.

1. **Choose the layout and orientation** (tiebreaker above, then the table). If it's not a generator shape, stop here and use the right tool.
2. Pick the C4 level — **Context** (systems + people), **Container** (deployable units; the usual choice for a spec), or **Component** (inside one container). Don't mix levels in one diagram.
3. Map: boundaries → columns, containers → box lines, interactions → `EDGES` (adjacent) and `SKIP_EDGES` (non-adjacent), each with direction + `[protocol]`.
4. Run the generator, eyeball it, and honor the width warning (switch to `"SEQ"` rather than ship a sideways scroll), then patch into the doc.
5. Add the define-by-negation sentence; add a legend only if a label isn't self-evident.

See [SHOWCASE.md](SHOWCASE.md) for a rendered gallery of all four layouts (SEQ, LR, TB stacked/staggered, hand-drawn hub-and-spoke), each with the copy-paste config that produced it — the fastest way to pick a layout and start from a working config. See [REFERENCE.md](REFERENCE.md) for the C4 element cheat-sheet, the full generator config (including `SKIP_EDGES`), and the alignment failure modes this prevents.
