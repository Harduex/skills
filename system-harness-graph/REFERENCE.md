# System Harness Graph — Reference

Full data-model schema, customization, and how to verify an edited engine. The workflow lives in [SKILL.md](SKILL.md); this is the field-by-field detail.

## The data JSON

One object. Only `kinds`, `nodes`, and `edges` are required.

### `kinds` — the layers (required)

```json
"kinds": { "service": { "label": "Services", "hue": "#22d3bb" }, "core": { "label": "Product", "hue": "#cdd6ea" } }
```

- Keyed by kind id. `label` shows in the legend/panel; `hue` is the node colour in **layer** mode.
- Include an entry for every `k` used by a node. A missing kind auto-fills to neutral grey (a warning is printed) — define it instead.
- One kind is conventionally `core` (the centre node's kind).

### `nodes` — components (required)

Each node: `{ id, k, t, d, ... }`.

| field | req | meaning |
|-------|-----|---------|
| `id` | ✓ | unique slug; edges and `cat` reference it |
| `k` | ✓ | kind id (→ colour/layer) |
| `t` | ✓ | short label shown on the graph |
| `d` | ✓ | one-line "what it is" (panel + tooltip) |
| `m` |  | mono meta line (e.g. a path, a tech, a count) |
| `core` |  | `true` on exactly one node — the pinned centre |
| `anchor` |  | `true` on one node **per kind** — the layer hub members cluster around |
| `cat` |  | on members: the `id` of their anchor (which layer they sit in) |
| `dom` |  | optional sub-domain id → a second colour axis (see `domains`) |

Rules the renderer enforces: ids unique; exactly one `core` (warns otherwise); every non-core/non-anchor node should carry a `cat` that names a real `anchor` node (hard error if it names a non-anchor).

**Shape to copy:** one `core`, one `anchor` per kind, then members with `cat`. See `examples/sample.json`.

### `edges` — the wiring (required)

`[from, to, rel, note?]` — node id, node id, relation id, optional short note.

- List only **meaningful cross-links**. The structural edges (core→each anchor, each member→its anchor) are generated automatically — never list them.
- `from`/`to` must be existing node ids (hard error otherwise).
- `rel` picks the edge style/colour; unknown rels auto-fill (warning). `note` is the small label shown on the connection row.
- Edges may point at an **anchor** id (e.g. "this component spans *the whole services layer*") not just a leaf.

### `domains` — optional second colour axis

```json
"domains": { "async": { "label": "Async", "hue": "#a3e635" } }
```

Tag nodes with `dom: "async"`. When any node has a `dom`, a **Colour · domain** toggle appears; otherwise it's hidden. Use it to cross-cut the layer view (e.g. sync vs async, owned-team, risk tier).

### `rels` — override relation types

Defaults: `provision`, `direct`, `compose`, `drive`, `record`, `span` (see SKILL.md). To customise:

```json
"rels": { "calls": { "label": "calls", "hue": "#22d3bb", "dash": "", "w": 2, "desc": "invokes at runtime" } }
```

`dash` is an SVG `stroke-dasharray` (`""` = solid); `w` is stroke width; `desc` shows in the legend key.

### Header + chrome (all optional)

| field | default |
|-------|---------|
| `title` | sets `<title>` + the H1 |
| `subtitle` | dimmed continuation of the H1 |
| `eyebrow` | small mono kicker above the H1 |
| `lede` | intro paragraph (inline HTML allowed) |
| `overviewTitle` | heading of the idle detail panel |
| `stats` | array of `[value, label]`; if omitted, auto-counts members per kind + connections + layers |
| `footer` | array of HTML strings (one per line) |
| `accent` | primary chrome hue; defaults to the first non-core kind's hue |
| `anchorAngles` | `{ anchorId: degrees }` to pin layer positions; if omitted, anchors are spread evenly from the top |

Shape of the array/object-valued fields:

```json
"stats": [[9, "services"], [3, "data stores"], [14, "connections"]],
"anchorAngles": { "A-services": 90, "A-data": 210, "A-external": 330 }
```

`title` is injected into the file's static `<title>` tag by the renderer (so the browser tab is correct immediately) **and** set as the H1.

## The renderer

```
python3 scripts/render-graph.py DATA.json [-o OUT.html] [-t TEMPLATE.html]
```

- Default output: `docs/<DATA-stem>.html`, **resolved against the current working directory** (the `docs/` dir is created there) — run it from your project root, or pass `-o` for an explicit path. Default template: `assets/graph.template.html` next to the script.
- Validates the model (see rules above): **hard-fails** (non-zero, nothing written) on a missing edge endpoint or a `cat` that isn't an anchor; **warns** on no/duplicate core, unknown kind, or a member with no `cat`. `stdout` = the output path; `stderr` = the summary + warnings.
- The summary reports semantic and **structural** edge counts separately (`14 semantic edges (+18 structural drawn)`). The rendered SVG line count is their sum — core→anchor (one per layer) plus member→anchor (one per member) are generated, so a jsdom/DOM count higher than your edge list is expected, not a bug.
- The injected data is HTML-safe (`<` is escaped) so it can't break out of the `<script type="application/json">` block.

## How the render behaves

- **Layout:** anchors are pinned on a ring around the core; members settle via a small force sim (charge repulsion, gravity toward their anchor, weak springs along semantic edges, collision), pre-solved for ~520 ticks on load. The seed is random, so exact positions vary per load; topology is stable. Node radius scales with semantic degree; hubs auto-label.
- **Interactions:** click a node → isolate its neighbourhood + animate packets along live edges; click an anchor/legend chip → focus that layer; toggle relation chips → reveal that wiring globally; colour toggle → layer vs domain; search; drag to rearrange (reheats the sim); Esc / background → reset.
- **Self-contained:** no network, no CDN, no fonts fetched — opens from `file://`. Honours `prefers-reduced-motion` (drops packets and entrance motion).

## Verifying an edited engine

The data is validated by the renderer, but if you change `assets/graph.template.html` itself, confirm it still boots. Syntax-check, then headless-boot with jsdom (positions/DOM build without a real browser):

```bash
# 1. JS syntax
python3 -c "h=open('assets/graph.template.html').read();a=h.index('\"use strict\";');b=h.rindex('</script>');open('/tmp/_c.js','w').write(h[a:b])" && node --check /tmp/_c.js

# 2. render an example, then boot it in jsdom (npm i jsdom --no-save in a scratch dir)
python3 scripts/render-graph.py examples/sample.json -o /tmp/_g.html
node -e '
const {JSDOM}=require("jsdom");const errs=[];
const d=new JSDOM(require("fs").readFileSync("/tmp/_g.html","utf8"),{runScripts:"dangerously",pretendToBeVisual:true,
  beforeParse(w){w.matchMedia=()=>({matches:false,addEventListener(){},removeEventListener(){}});
    Object.defineProperty(w.HTMLElement.prototype,"clientWidth",{get:()=>900});
    Object.defineProperty(w.HTMLElement.prototype,"clientHeight",{get:()=>680});
    w.addEventListener("error",e=>errs.push(String(e.error&&e.error.stack||e.message)));}});
setTimeout(()=>{const doc=d.window.document;
  console.log("errors:",errs.length, "nodes:",doc.querySelectorAll(".node").length, "edges:",doc.querySelectorAll("#edges line").length);
  process.exit(0);},400);'
```

Expect `errors: 0` and non-zero node/edge counts. Two things jsdom *cannot* do — `setPointerCapture` (guarded in the engine) and exiting on its own while the packet `requestAnimationFrame` loop runs (the check `process.exit(0)`s to sidestep it). Neither is a real-browser problem.
