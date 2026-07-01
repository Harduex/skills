---
name: system-harness-graph
description: Builds a self-contained interactive HTML node-link graph of any system — every component becomes a node clustered by layer, with typed, colour-coded edges for how the parts connect and talk to each other. Use when the user wants to visualise, map, or explore how the pieces of a system, codebase, architecture, agent harness, service mesh, or data model relate — an explorable force-directed graph rather than a static ASCII diagram — or wants to turn an inventory of components and relationships into a shareable HTML page. Renders to a standalone file (no server, no CDN) saved under docs/. For a fixed C4 box-and-arrow diagram inside a markdown doc, use an architecture-diagram skill instead.
---

# System Harness Graph

Turn a system into an **explorable** picture: every component is a node, clustered by the layer it belongs to, wired by typed edges that show how the parts connect. The output is one standalone `.html` file that opens in any browser — no server, no CDN, no hosted-artifact service.

## What it produces

A single HTML file with a force-clustered node-link graph. Colour encodes the **layer**, node size encodes **connectivity**, faint webs are **structure** (core → layer → member) and coloured edges are **behaviour**. Interactions: click a node to isolate its neighbourhood (signal packets flow along its live edges), toggle a relation type to see that wiring everywhere, recolour by layer or sub-domain, search, and drag to rearrange.

## When to use / not

- **Use** when someone wants to *see how a system hangs together* and poke at it — a codebase's modules, a service architecture, an agent harness, a data model, a dependency web.
- **Not** for a static, print-ready C4 diagram in a markdown/RFC — that is an architecture-diagram skill's job. Not worth it for a 2–4 box relationship (just describe it in prose).

## The one rule — ground every node and edge in a real source

**Read the files. Do not trust a prior diagram, a summary, or your own recall.** This skill exists because a hand-made map is confidently wrong in ways that survive for months: the session it came from inherited an older graph and had to correct multiple "facts" (a component count that was off by ten, a plugin count that was doubled). A graph that *looks* authoritative while encoding stale or invented links is worse than no graph.

- For every edge, prefer an **explicit** anchor in the source (a config entry, an import, a documented reference).
- Where a link is genuinely **conceptual/inferred** (not stated anywhere), keep it but say so in its `note` — don't launder a guess into a fact.
- Verify counts and names against the source before you write them, not after.

## Workflow

1. **Scope + inventory.** Fix the system and its sources of truth. Read them — fan out read-only subagents when breadth is large (one per subsystem). Produce a flat list of components and, for each, its real connections with the source that grounds each one.
2. **Build the data model** — one JSON file. Follow the schema below and copy the shape of `examples/sample.json`. Minimum: `kinds` (the layers + a hue each), `nodes` (exactly one `core`, one `anchor` per kind, and members each carrying `cat`), and `edges`. List only the *meaningful* cross-links — structural edges are generated for you.
3. **Render** — run it from the directory you want the `docs/` folder in; the default output path is **relative to your current working directory**:
   ```bash
   python3 <skill>/scripts/render-graph.py DATA.json          # → ./docs/DATA.html
   python3 <skill>/scripts/render-graph.py DATA.json -o path/to/my-map.html
   ```
   It **hard-fails** (non-zero exit, nothing written) on a broken model — a missing edge endpoint, or a `cat` that doesn't name a real anchor. It **warns but still renders** on softer issues (no/duplicate core, an unknown kind, a member with no `cat`). Read the summary line — it reports node, semantic-edge and auto-generated structural-edge counts, so a broken model never ships silently.
4. **Verify.** Trust the script's validation, then open the file in a browser and confirm it reads. If you edited the engine template (not just the data), run the jsdom boot check in [REFERENCE.md](REFERENCE.md) — the live render is often the only way to catch a layout regression, and a headless browser may be blocked.
5. **Save + share.** Output lands under `docs/` by default — a plain file you can open, commit, or send. It is deliberately *not* published to any hosted-artifact service; keep it local unless the user asks otherwise.

## Data model (minimal)

Full field reference in [REFERENCE.md](REFERENCE.md). The essentials:

- **`kinds`** — `{ id: { label, hue } }`. The layers of the system; colour maps to layer. One id should be `core`.
- **`nodes`** — array of `{ id, k, t, d }` plus:
  - one node with `core: true` (the centre), and one `anchor: true` node **per kind** (the layer hubs),
  - members with `cat: "<anchor-id>"` (which layer they cluster in), optional `m` (mono meta line), optional `dom` (sub-domain, a second colour axis).
- **`edges`** — array of `[from, to, rel, note?]`. Only the meaningful cross-links; the core→anchor and member→anchor structure is generated automatically.
- Optional: `domains` (sub-domain colours), custom `rels`, and header copy (`title`, `subtitle`, `eyebrow`, `lede`, `overviewTitle`, `stats`, `footer`, `accent`, `anchorAngles`).

## Relation types (defaults)

Override or replace via `rels`; these are the built-ins:

| rel | meaning |
|-----|---------|
| `provision` | installs · registers · enables · sources |
| `direct` | gates · injects · imports · precedes |
| `compose` | wraps or calls another component |
| `drive` | operates a live tool or service |
| `record` | writes / reads data or docs |
| `span` | reaches another module or spawns work |

## Notes

- **The layout is intentionally organic.** A force simulation with a random seed means exact positions differ on every load; the clustering and the topology are stable. This is the look — don't make it deterministic unless asked (swap the two `Math.random()` seeds for a seeded PRNG if you must).
- **The template is generic.** All system-specific content lives in the data JSON; `assets/graph.template.html` never needs editing to map a new system.

## Files

- `assets/graph.template.html` — the self-contained engine (CSS + force sim + interactions). Edit only to change *behaviour or looks*; re-run the boot check after.
- `scripts/render-graph.py` — injects a data model into the template, validates it, writes the HTML.
- `examples/sample.json` — a runnable example: `python3 scripts/render-graph.py examples/sample.json`.
