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

Rule of thumb: if you typed more than one space in a row to line something up, stop and use the script.

For the shapes the generator doesn't cover (vertical chains, hub-and-spoke), you must hand-draw — so check the result with `scripts/verify_boxes.py` (box-integrity linter; see SKILL.md → "Hand-drawn shapes"). It recognises skip-edge routing, so it is also safe to run over generator output.

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

`scripts/diagram.py` — edit these blocks, run:

- `COLUMNS`: list of `{ "boundary": "« … »", "lines": [ "container  [tech]", " sub-detail", "", … ] }`. One column per boundary; `""` lines are spacers; a leading space indents a sub-detail under a container.
- `EDGES` (adjacent columns): list of `{ "between": <left-column index>, "row": <0-based content row>, "dir": "R"|"L", "label": "verb … to/from [protocol]" }`. `dir` `R` = left→right, `L` = right→left (return).
- `SKIP_EDGES` (non-adjacent columns): list of `{ "from": <col index>, "to": <col index>, "label": "verb … to/from [protocol]" }`. The arrowhead lands on `to`; direction is inferred from the index order. Each routes in its own channel **below** the boxes; deeper channels cross shallower runs as `┼`. Keep labels short — the run spans only source-center to target-center. Several skip edges that cross each other is the signal that columns are the wrong layout (see SKILL.md → Choosing a layout).
- `PAD` (inner box padding) and `MIN_GAP` (gap when an edge has no label) are tunables at the top.

Run modes:
- `python3 scripts/diagram.py` — prints the diagram.
- `python3 scripts/diagram.py doc.md` — replaces the fenced block in `doc.md` whose first line starts with the first boundary label, in place. Re-runnable; safe to iterate.

It is dependency-free (stdlib only) and supports any number of columns.

## Vertical variant (long call chains)

When the story is a sequential chain (request flows A→B→C→D→…), stack boxes vertically and label the vertical connectors — same conventions, more room for descriptive edges:

```
┌─────────────────────┐   « CLIENT »
│ mobile app  [Swift] │
└──────────┬──────────┘
           │  sends request to [HTTPS]   (Bearer user token)
           ▼
┌─────────────────────┐   « PLATFORM »
│ api gateway  [Go]   │
└──────────┬──────────┘
           │  forwards request to [HTTPS]
           ▼
┌─────────────────────┐   « BACKEND »
│ app service  [Node] │
└─────────────────────┘
```

The vertical edge has a whole line, so the label can be a full phrase + parenthetical. **The generator is columnar-only — it does not emit this variant**, but a vertical chain is a single column of one width, so it aligns by hand trivially. (Reach for a Mermaid sequence diagram only if you've decided to leave ASCII — e.g. the chain is too long to stay readable.)

## When to render with a real C4 tool instead

Reach for Structurizr / PlantUML-C4 / Mermaid-C4 (a separate, non-ASCII artifact) when: the diagram needs to be interactive or zoomable; you maintain several linked C4 levels of the same system; or a non-engineering audience needs a polished export. Otherwise ASCII is the default — it diffs cleanly, renders in every tool, and lives in the doc.
