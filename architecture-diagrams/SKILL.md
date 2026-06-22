---
name: architecture-diagrams
description: Create consistent, readable architecture and system diagrams using C4 conventions rendered in ASCII (for specs, RFCs, design docs, READMEs, PRs). Use when drawing or editing an architecture / system / context / container diagram, a box-and-arrow diagram in a markdown doc, or when a diagram's boxes or arrows are misaligned. Encodes the C4 element and relationship conventions and bundles a generator for the columnar (swimlane) layout so alignment is computed, never hand-counted.
---

# Architecture Diagrams (C4, ASCII-first)

Model with **C4** ([c4model.com](https://c4model.com)); render in **ASCII** by default — it diffs cleanly and shows up correctly everywhere (specs, PRs, terminals, plain editors).

## Choosing a layout (do this first)

**ASCII is the default for every shape.** The bundled generator only automates **one** of them — the columnar "swimlane" (owning systems left-to-right, the call flow running across them). The other ASCII shapes you draw by hand using the conventions below. Match the *layout to the topology of the story* — don't bend the architecture to fit the columnar tool:

| If the story is… | Draw it as | Notes |
|---|---|---|
| left-to-right flow across 2–5 owning systems (adjacent **or** skip-level calls) | **columnar ASCII** — the generator | what it's built for; alignment is computed for you |
| a sequential call chain (A→B→C→D…) | **vertical ASCII**, by hand | a single column of one width aligns trivially — see REFERENCE |
| a small hub-and-spoke / C4 **Context** (a system with a few neighbours or actors) | **free-form ASCII**, by hand, using the conventions below | keep it small — radial ASCII stays readable only when the edges are few |
| too large/dense to stay readable in ASCII, **or** it must be interactive / zoomable / a polished export | render **outside ASCII** — Mermaid-C4 / PlantUML-C4 / Structurizr | the *only* reason to leave ASCII |

## The rule for the columnar layout: compute alignment, don't count spaces

When you *are* drawing the columnar shape, let the generator place every box width, gap, arrow, and header — **never hand-align them.** Off-by-one borders and labels overflowing their gap are otherwise guaranteed, and you'll burn turns re-counting. This rule governs *alignment*, not *which diagram to draw* (that's the table above).

[scripts/diagram.py](scripts/diagram.py) — edit the `COLUMNS`, `EDGES`, and `SKIP_EDGES` blocks, then:
- `python3 scripts/diagram.py` → print the diagram (eyeball it)
- `python3 scripts/diagram.py path/to/doc.md` → splice it into that file's fenced ``` block (the one whose first line is the first boundary label)

Copy the script next to the doc you're editing; it's stdlib-only, no dependencies.

## Hand-drawn shapes: verify each box (no generator covers these)

Vertical chains and hub-and-spoke are drawn by hand — and that's where borders silently go missing. **Don't eyeball it; run the bundled checker** before shipping:

```
python3 scripts/verify_boxes.py doc.md        # lints every fenced diagram in the doc
python3 scripts/verify_boxes.py diagram.txt   # or a raw diagram / piped stdin
```

It flags any box missing a border, a broken side wall, a misaligned corner, or column-mate boxes of unequal width — the failures hand-drawing silently ships. Exit 0 = clean. (Generator output is correct by construction, and the checker recognises skip-edge routing, so it's safe to run on any diagram.)

## Conventions (apply to every diagram)

- **Each column is one owning system / boundary**, drawn as a bordered box with a guillemet header; mark externals: `« PROVIDERS — external »`. **The border is the boundary** (C4 system boundary), not a container.
- **Each line inside the box is a container**, tagged with its technology: `api gateway  [Go]`, `database  [Postgres]`. Indent sub-details one space.
- **Arrows = relationships, read as a sentence.** The **left box is the subject** and the **preposition points at the partner**:
  - outbound (`→`): `forwards token to [HTTPS]`
  - return (`←`): `receives push from [WebSocket]`

  Always bracket the `[protocol/tech]`. The arrowhead shows direction; the preposition keeps it readable in plain left-to-right text. Keep labels short — a long label widens the whole gap.
- **Skip-level calls** (a system talks to a non-adjacent one) are `SKIP_EDGES`, routed in a channel below the boxes. Same subject/preposition rule.
- **Mark deltas with `(NEW)`** on whatever the current change adds; everything unmarked is reused.
- **One sentence under the diagram defines it by negation** ("No new datastore. No second front door. …"). See the `write-design-spec` skill.

## Workflow

1. **Choose the layout** (table above). If it's not columnar, stop here and use the right tool.
2. Pick the C4 level — **Context** (systems + people), **Container** (deployable units; the usual choice for a spec), or **Component** (inside one container). Don't mix levels in one diagram.
3. Map: boundaries → columns, containers → box lines, interactions → `EDGES` (adjacent) and `SKIP_EDGES` (non-adjacent), each with direction + `[protocol]`.
4. Run the generator, eyeball, then patch into the doc.
5. Add the define-by-negation sentence; add a legend only if a label isn't self-evident.

See [REFERENCE.md](REFERENCE.md) for the C4 element cheat-sheet, the full generator config (including `SKIP_EDGES`), and the alignment failure modes this prevents.
