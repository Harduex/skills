# Architecture Diagrams — Reference

## Why generate instead of hand-draw

Hand-aligned ASCII fails in predictable ways. The generator removes all of them:

| Failure mode (hand-drawn) | Cause | Generator's fix |
|---|---|---|
| Right border of a box drifts row-to-row | a content line is longer than the box's dash count | box width = `max(len(line))`; every row `ljust` to it |
| Arrow doesn't touch the boxes | label padded with stray leading/trailing space | arrows are built to exactly the gap width, flush `─…▶` / `◀…─` |
| Label overflows into the next box | gap narrower than the label | gap = `max(label)+5`, so the longest arrow still has ≥1 filler dash |
| Header / boundary labels misaligned with boxes | counted separately from the boxes | header positions computed from the same widths + gaps |
| Edit one box, everything below shifts | manual respacing | re-run; layout recomputed |
| Diagram wider than the review pane | side-by-side boundaries × sentence labels | `ORIENTATION = "SEQ"` (or `"TB"`); both scripts warn past 120 chars |

Rule of thumb: if you typed more than one space in a row to line something up, stop and use the script.

For the shape the generator doesn't cover (hub-and-spoke), you must hand-draw — so check the result with `scripts/verify_boxes.py` (box-integrity + width linter; see SKILL.md → "Hand-drawn shapes"). It recognises skip-edge routing, so it is also safe to run over generator output.

## C4 element cheat-sheet

C4 has four nested levels; pick one per diagram, never mix:

- **Context** — the system in its world: people (actors) + the software system + neighbouring systems. Audience: everyone.
- **Container** — the deployable/runnable units inside the system (apps, services, DBs, SPAs) and how they talk. **Default for a design doc / RFC.**
- **Component** — the major parts inside a single container. Use sparingly.
- **Code** — classes/functions. Rarely worth a diagram; let the IDE do it.

Element notation in our ASCII dialect (the columnar generator):
- Boundary / system: a **column, drawn as one bordered box**, headed `« Name — external »` (drop "external" for the system you own). The border is the boundary, not a container.
- Container: a **line inside that box**, `name  [technology]` — e.g. `api gateway  [Go]`, `database  [Postgres]`. (A true nested per-container box is not drawn — that's a deliberate ASCII simplification; if you need it, use a real C4 tool.)
- Person: a line `Name  [Person]`.
- Relationship: a labelled arrow, `subject-verb … to/from [protocol]` — adjacent columns via `EDGES`, non-adjacent via `SKIP_EDGES`.

## Relationship labels — the rule in full

The left box is always the grammatical **subject**; the **preposition points right at the partner**. This keeps every line readable left-to-right even when the arrow points left.

| Arrow | Reads as | Example |
|---|---|---|
| `→` outbound | `<subject> <verb> <object> to [protocol]` | `sends requests to [HTTPS]` |
| `←` return | `<subject(left, the receiver)> receives <object> from [protocol]` | `receives push from [WebSocket]` |

Keep labels to a verb + object + preposition + `[protocol]`. Put detail (endpoints, payload shapes) in the doc's prose / contract section, not the diagram. Append `(NEW)` to boxes or labels the current change introduces.

## Generator config

`scripts/diagram.py` — one config drives both orientations; edit these blocks, run:

- `ORIENTATION`: `"SEQ"` (RFC-style ladder — the default for request/response flows), `"LR"` (boundaries side by side, labels inline in the gaps — static structure, 2–3 boundaries), or `"TB"` (boundaries stacked, every label on its own full line to the right, the boundary name as the box's first line — static structure, 4+ boundaries).
- `STAGGER` (8): `"TB"` only — how far right each box steps from the previous one, so the flow reads down the page's diagonal instead of a flat stack. `0` = plain stack (narrowest possible render).
- `LABEL_WRAP` (20): `"SEQ"` only — adjacent-pair arrow labels word-wrap to this width, which is what keeps lifeline spacing (and total width) small. Arrows spanning several lifelines get their full span before wrapping.
- `TARGET_WIDTH` (120): the script warns on stderr when the render is wider — a code-review pane clips it behind a horizontal scrollbar. Fix with `"TB"` or shorter labels, never by shipping the scroll.
- `COLUMNS`: list of `{ "boundary": "« … »", "lines": [ "container  [tech]", " sub-detail", "", … ] }`. One entry per boundary; `""` lines are spacers; a leading space indents a sub-detail under a container.
- `EDGES` (adjacent boundaries): list of `{ "between": <left/upper column index>, "row": <0-based content row>, "dir": "R"|"L", "label": "verb … to/from [protocol]" }`. `dir` `R` = outbound (rightward / downward), `L` = return (leftward / upward). `row` places the arrow in `"LR"`; `"TB"` ignores it (edges occupy the gap between the stacked boxes, one label line each). **In `"SEQ"`, `EDGES` is the time-ordered message list**: entries are `{ "from": <col>, "to": <col>, "label": … }` between *any* two boundaries (the `between`/`dir` form also works for adjacent pairs), and the label states the source's action.
- `SKIP_EDGES` (non-adjacent boundaries; unused in `"SEQ"` — put every message in `EDGES` there): list of `{ "from": <col index>, "to": <col index>, "label": "verb … to/from [protocol]" }`. The arrowhead lands on `to`; direction is inferred from the index order. Each routes in its own channel — below the boxes in `"LR"`, to the right of them in `"TB"` — and deeper channels cross shallower runs as `┼`. Keep labels short. Several skip edges that cross each other is the signal that this is the wrong layout (see SKILL.md → Choosing a layout).
- `PAD` (inner box padding) and `MIN_GAP` (`"LR"` gap when an edge has no label) are tunables at the top.

Run modes:
- `python3 scripts/diagram.py` — prints the diagram.
- `python3 scripts/diagram.py doc.md` — replaces the fenced block in `doc.md` containing the first boundary label, in place. Re-runnable; safe to iterate, including when switching orientation.

It is dependency-free (stdlib only) and supports any number of boundaries.

## Reading each layout's notation

A rendered example of every layout, with the config that produced it, lives in **[SHOWCASE.md](SHOWCASE.md)** — the gallery, not repeated here. What each layout's glyphs mean:

- **SEQ** (the RFC ladder — OAuth RFC 6749 and the SIP call-flow RFCs are the canon): each boundary box tops a lifeline, time flows down, every arrow is one message with its label above it, and the arrowhead touches the target lifeline (`├──▶` rightward, `◀──┤` leftward). An arrow crossing an uninvolved lifeline draws it as `┼`. Labels stack in *time*, so adding messages costs height, not width, and a skip-level call is just a longer arrow — no routing channel. Keep header `lines` short or empty: box width, not label width, limits how many lifelines fit.
- **TB**: the boundary name is the box's first line (it can never detach), and each box steps `STAGGER` chars right of the previous so the flow reads down the diagonal (`STAGGER = 0` = plain stack). A lane leaves its subject box through a tee (`┬` down, `┴` up), its arrowhead touches the partner's plain border, and each edge's label sits on its own line tee'd off its lane (`├`), crossing sibling lanes as `┼`. Skip edges tee out of the box's right wall with the label inline and drop down a channel into the target box.
- **LR**: one boundary per column, header above the box, labels inline in the gaps; return arrows are `◀`, and skip-level calls route in a channel below the boxes. Width grows with every label — it leaves the review pane first.

## When to render with a real C4 tool instead

Reach for Structurizr / PlantUML-C4 / Mermaid-C4 (a separate, non-ASCII artifact) when: the diagram needs to be interactive or zoomable; you maintain several linked C4 levels of the same system; or a non-engineering audience needs a polished export. Otherwise ASCII is the default — it diffs cleanly, renders in every tool, and lives in the doc.
