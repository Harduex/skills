# Architecture Diagrams — Showcase

Every layout this skill can produce, with the config that made it and when to reach for it. All diagrams here are generated (or, for hub-and-spoke, hand-drawn) with the bundled scripts and pass `verify_boxes.py`, including the 120-char review-pane budget. See [SKILL.md](SKILL.md) for the decision table and [REFERENCE.md](REFERENCE.md) for the full config.

## Pick by the story, not by habit

| The diagram's story | Layout | Why |
|---|---|---|
| **who calls whom, in what order** (most design-spec flows) | `SEQ` | labels stack in *time*, so width barely grows with edge count |
| static structure, 2–3 systems, short labels | `LR` | compact side-by-side; width grows with every label |
| static structure, 4+ systems, no time order | `TB` | one system per row; width ≈ widest box + longest label |
| a system and its few neighbours (C4 Context) | hand-drawn hub-and-spoke | radial, no generator |
| too big/dense, or needs to be interactive | Mermaid-C4 / PlantUML-C4 | the only reason to leave ASCII |

**Tiebreaker:** if there's *any* ordering story, use `SEQ`. `LR`/`TB` are for pure box-and-line structure.

---

## SEQ — the request/response ladder (default for flows)

An RFC-style ladder (the shape OAuth RFC 6749 and the SIP call-flow RFCs use to fit multi-party flows in 72 columns). Boundary boxes head the lifelines; time runs down; each message is one labeled arrow. Returns are leftward arrows, and a call that skips over a party is just a longer arrow — no routing channels. Adding messages costs **height, not width**.

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐   ┌────────────────┐
│ « BROWSER » │     │ « GATEWAY » │     │ « AUTH SVC » │   │ « ORDERS API » │
└──────┬──────┘     └──────┬──────┘     └───────┬──────┘   └────────┬───────┘
       │                   │                    │                   │
       │ GET /orders with  │                    │                   │
       │  cookie [HTTPS]   │                    │                   │
       ├──────────────────▶│                    │                   │
       │                   │ validates session  │                   │
       │                   │     via [gRPC]     │                   │
       │                   ├───────────────────▶│                   │
       │                   │   returns user +   │                   │
       │                   │  scopes to [gRPC]  │                   │
       │                   │◀───────────────────┤                   │
       │                   │       forwards request to [HTTP]       │
       │                   ├────────────────────┼──────────────────▶│
       │                   │   responds with order list to [HTTP]   │
       │                   │◀───────────────────┼───────────────────┤
       │  renders JSON to  │                    │                   │
       │      [HTTPS]      │                    │                   │
       │◀──────────────────┤                    │                   │
       │                opens SSE stream to [HTTPS]                 │
       ├───────────────────┼────────────────────┼──────────────────▶│
       │                   │                    │                   │
```

```python
ORIENTATION = "SEQ"
COLUMNS = [
    {"boundary": "« BROWSER »", "lines": []},
    {"boundary": "« GATEWAY »", "lines": []},
    {"boundary": "« AUTH SVC »", "lines": []},
    {"boundary": "« ORDERS API »", "lines": []},
]
# EDGES is the time-ordered message list; from/to are any two boundaries.
EDGES = [
    {"from": 0, "to": 1, "label": "GET /orders with cookie [HTTPS]"},
    {"from": 1, "to": 2, "label": "validates session via [gRPC]"},
    {"from": 2, "to": 1, "label": "returns user + scopes to [gRPC]"},
    {"from": 1, "to": 3, "label": "forwards request to [HTTP]"},      # skips a lifeline — just a longer arrow
    {"from": 3, "to": 1, "label": "responds with order list to [HTTP]"},
    {"from": 1, "to": 0, "label": "renders JSON to [HTTPS]"},
    {"from": 0, "to": 3, "label": "opens SSE stream to [HTTPS]"},     # skip-level, no routing channel needed
]
```

Keep header `lines` short or empty — box width, not label width, is what limits how many lifelines fit.

---

## LR — side-by-side structure (2–3 systems, short labels)

The original columnar layout: one boundary per column, labels inline in the gaps, returns as `◀` arrows, skip-level calls routed in a channel below. Best when there's no time order and few systems — but every label widens its gap, so it outgrows a review pane fast (this one is 115 chars; add one sentence-length label and it clips).

```
« CLIENT »                                      « PLATFORM »                                 « PROVIDERS »
┌──────────────────────┐                        ┌──────────────────┐                         ┌────────────────────┐
│ mobile app  [Swift]  │─ requests to [HTTPS] ─▶│ gateway  [Go]    │─ delivers via [HTTPS] ─▶│ email/push  [SaaS] │
│  offline cache (NEW) │◀────── push from [WS] ─│  service  [Node] │                         │  identity  [OAuth] │
│                      │                        │  db  [Postgres]  │                         │                    │
└───────────┬──────────┘                        └──────────────────┘                         └──────────┬─────────┘
            │                                                                                           ▲
            └ authenticates with [OAuth] ───────────────────────────────────────────────────────────────┘
```

```python
ORIENTATION = "LR"
COLUMNS = [
    {"boundary": "« CLIENT »", "lines": ["mobile app  [Swift]", " offline cache (NEW)"]},
    {"boundary": "« PLATFORM »", "lines": ["gateway  [Go]", " service  [Node]", " db  [Postgres]"]},
    {"boundary": "« PROVIDERS »", "lines": ["email/push  [SaaS]", " identity  [OAuth]"]},
]
EDGES = [
    {"between": 0, "row": 0, "dir": "R", "label": "requests to [HTTPS]"},
    {"between": 0, "row": 1, "dir": "L", "label": "push from [WS]"},       # return arrow
    {"between": 1, "row": 0, "dir": "R", "label": "delivers via [HTTPS]"},
]
SKIP_EDGES = [{"from": 0, "to": 2, "label": "authenticates with [OAuth]"}]  # non-adjacent, routed below
```

---

## TB — stacked structure (4+ systems, no time order)

One boundary per row, each edge label on its own full line to the right. Width is bounded by the widest box plus the longest label, regardless of how many systems stack up — so it stays in the pane where LR wouldn't.

```
┌────────────────┐
│ « INGEST »     │
│ uploader  [Go] │
└───────┬────────┘
        ├─────────── publishes job to [PubSub]
        ▼
┌─────────────────┐
│ « QUEUE »       │
│ topic  [PubSub] │
└────────┬────────┘
         ├────────── pulls job from [PubSub]
         ▼
┌─────────────────┐
│ « TRANSCODE »   │
│ ffmpeg  [C]     │
│  gpu pool (NEW) │
└───────┬─────────┘
        ├─────────── writes renditions to [GCS API]
        ▼
┌───────────────┐
│ « STORE »     │
│ bucket  [GCS] │
└─────┬─────────┘
      ├─────────── serves origin to [HTTPS]
      ▼
┌────────────┐
│ « CDN »    │
│ edge cache │
└────────────┘
```

```python
ORIENTATION = "TB"
STAGGER = 0   # 0 = plain vertical stack (narrowest); >0 steps each box right (see below)
COLUMNS = [
    {"boundary": "« INGEST »", "lines": ["uploader  [Go]"]},
    {"boundary": "« QUEUE »", "lines": ["topic  [PubSub]"]},
    {"boundary": "« TRANSCODE »", "lines": ["ffmpeg  [C]", " gpu pool (NEW)"]},
    {"boundary": "« STORE »", "lines": ["bucket  [GCS]"]},
    {"boundary": "« CDN »", "lines": ["edge cache"]},
]
EDGES = [
    {"between": 0, "row": 0, "dir": "R", "label": "publishes job to [PubSub]"},
    {"between": 1, "row": 0, "dir": "R", "label": "pulls job from [PubSub]"},
    {"between": 2, "row": 0, "dir": "R", "label": "writes renditions to [GCS API]"},
    {"between": 3, "row": 0, "dir": "R", "label": "serves origin to [HTTPS]"},
]
```

### TB with `STAGGER = 8` — the same config, stepped down a diagonal

A cosmetic variant: each box shifts right of the previous, so the flow reads down the page's diagonal instead of a flat left edge. Costs width; use only when the stagger genuinely aids reading.

```
┌────────────────┐
│ « INGEST »     │
│ uploader  [Go] │
└───────────┬────┘
            ├─────────────── publishes job to [PubSub]
            ▼
        ┌─────────────────┐
        │ « QUEUE »       │
        │ topic  [PubSub] │
        └────────────┬────┘
                     ├────────────── pulls job from [PubSub]
                     ▼
                ┌─────────────────┐
                │ « TRANSCODE »   │
                │ ffmpeg  [C]     │
                │  gpu pool (NEW) │
                └────────────┬────┘
                             ├──────────── writes renditions to [GCS API]
                             ▼
                        ┌───────────────┐
                        │ « STORE »     │
                        │ bucket  [GCS] │
                        └───────────┬───┘
                                    ├────────── serves origin to [HTTPS]
                                    ▼
                                ┌────────────┐
                                │ « CDN »    │
                                │ edge cache │
                                └────────────┘
```

---

## Hand-drawn hub-and-spoke — a C4 Context

No generator covers the radial shape: a system in the centre with a few neighbours or people around it. Draw it by hand using the box/arrow conventions, then lint it with `verify_boxes.py` (it checks box integrity *and* the width budget). Keep the spokes few — radial ASCII stops being readable past a handful of edges.

```
                      ┌──────────────────┐
                      │  Support Agent   │
                      │    [Person]      │
                      └────────┬─────────┘
                               │ manages tickets via [HTTPS]
                               ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  Billing System  │◀─▶│   HELP DESK      │◀─▶│  Email Provider  │
│  [external]      │   │   (this system)  │   │  [SaaS]          │
└──────────────────┘   └────────┬─────────┘   └──────────────────┘
       syncs invoices           │ reads profile from [REST]
       via [REST]               ▼
                      ┌──────────────────┐
                      │   Identity IdP   │
                      │   [OAuth]        │
                      └──────────────────┘
```

```
$ python3 scripts/verify_boxes.py hub.txt
[diagram] 5 box(es) — OK
```

---

## Conventions common to all layouts

- **Boundary** = a bordered box with a `« guillemet »` header; mark externals `« … — external »`. The border is the C4 system boundary.
- **Container** = a line inside the box, tagged `name  [tech]`. Indent sub-details one space.
- **Every arrow reads as a sentence:** the subject is the source box, and the preposition points at the partner — `sends requests to [HTTPS]`, `receives push from [WebSocket]`. Always bracket the `[protocol]`.
- **Mark deltas `(NEW)`** on whatever the current change adds.
- **Define by negation** in one sentence under the diagram: *"One trigger, one function. No queue, no new endpoint."*
