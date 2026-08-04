# Architecture Diagrams — Showcase

Every layout this skill can produce, with the config that made it and when to reach for it. All diagrams here are generated (or, for hub-and-spoke, hand-drawn) with the bundled scripts and pass `verify_boxes.py`, including the 120-char review-pane budget. See [SKILL.md](SKILL.md) for the decision table and [REFERENCE.md](REFERENCE.md) for the full config.

## Pick by the reader's first question

| What the reader is asking here | Layout | Why |
|---|---|---|
| **what are we actually building** — the change inventory | `FOOTPRINT` | one box per owning system, one line per unit of work, one arrow per pair naming the hop |
| **who calls whom, in what order** | `SEQ` | labels stack in *time*, so width barely grows with edge count |
| how the pieces sit — 2–3 systems | `LR` | the classic side-by-side read; long labels wrap above their arrow instead of widening |
| the same, 4+ systems | `TB` | one system per row; width ≈ widest box + longest label |
| a system and its few neighbours (C4 Context) | hand-drawn hub-and-spoke | radial, no generator |
| too big/dense, or needs to be interactive | Mermaid-C4 / PlantUML-C4 | the only reason to leave ASCII |

**Read the doc first.** Its headings decide the shape: the first diagram in a design doc is a `FOOTPRINT`, and a doc whose prose already narrates the call sequence (a `Flow` section, numbered "X calls Y" steps) doesn't get that sequence redrawn as a ladder.

---

## FOOTPRINT — what are we actually building

The picture a lead wants before any wire protocol: every route, table, column, trigger, function, and setting the change touches, grouped by **who owns it**. Arrows are the LR sentence style turned vertical — at most one per adjacent pair, naming the hop rather than the messages, so the diagram reads as an architecture instead of three stacked shopping lists. A long label costs height, never width. The last box is the one reviewers stop on: work the change depends on but doesn't own, which is why nothing points at it.

<!-- regen: self -->
```
┌───────────────────────────────────────────────────────────────┐
│ « mobile app  [Swift] — external »                            │
│ offline outbox + local store              (NEW, client work)  │
└───────────────────────────────┬───────────────────────────────┘
                                │ sends refund reads and writes
                                │ to [HTTPS + bearer]
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ « orders-api  [Go] — one new module: internal/refunds/ »      │
│ GET  orders/:id/refunds                      (NEW, v1)        │
│ GET  refunds/:id/receipt/:size               (NEW, v1) + HEAD │
│ GET  orders/:id/capabilities                 (NEW, v1)        │
│ write family ×6  refunds · approve · receipts   (NEW, v1.1)   │
│ reused  bearer-auth + ensure-customer chain, upload routes,   │
│         the shape of internal/invoices/                       │
└───────────────────────────────┬───────────────────────────────┘
                                │ reads and writes refund rows
                                │ in [SQL, customer role]
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ « Postgres  [shop schema] »                                   │
│ refund  +4 columns                                    (NEW)   │
│   xact_id, updated_at, deleted_at, idempotency_key            │
│ deleted_refund  1 table                               (NEW)   │
│ triggers ×3  stamp ins/upd · tombstone on del · attach (NEW)  │
│ SQL functions  ×2 delta, exposed to the API           (NEW)   │
│   ×2 trigger · ×2 write-path (set_state, delete)      (NEW)   │
│ indexes ×3 + 1 CHECK constraint                       (NEW)   │
│ reused  refund model, create_/edit_refund                     │
└───────────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────────┐
│ « not ours — we must ask for these »                          │
│ row filter on refund → order.is_visible  (PLAT-412, security) │
│ edge proxy ×3  buffering off · raised read timeout            │
│         · Range + If-None-Match passthrough      (infra)      │
│ mobile client  write scopes         (AUTH-88, gates v1.1)     │
│ anonymous session tokens            (PLAT-390, ships first)   │
└───────────────────────────────────────────────────────────────┘
```

```python
ORIENTATION = "FOOTPRINT"
COLUMNS = [
    {"boundary": "« mobile app  [Swift] — external »",
     "lines": ["offline outbox + local store              (NEW, client work)"]},
    {"boundary": "« orders-api  [Go] — one new module: internal/refunds/ »",
     "lines": ["GET  orders/:id/refunds                      (NEW, v1)",
               "GET  refunds/:id/receipt/:size               (NEW, v1) + HEAD",
               "GET  orders/:id/capabilities                 (NEW, v1)",
               "write family ×6  refunds · approve · receipts   (NEW, v1.1)",
               "reused  bearer-auth + ensure-customer chain, upload routes,",
               "        the shape of internal/invoices/"]},
    {"boundary": "« Postgres  [shop schema] »",
     "lines": ["refund  +4 columns                                    (NEW)",
               "  xact_id, updated_at, deleted_at, idempotency_key",
               "deleted_refund  1 table                               (NEW)",
               "triggers ×3  stamp ins/upd · tombstone on del · attach (NEW)",
               "SQL functions  ×2 delta, exposed to the API           (NEW)",
               "  ×2 trigger · ×2 write-path (set_state, delete)      (NEW)",
               "indexes ×3 + 1 CHECK constraint                       (NEW)",
               "reused  refund model, create_/edit_refund"]},
    {"boundary": "« not ours — we must ask for these »",
     "lines": ["row filter on refund → order.is_visible  (PLAT-412, security)",
               "edge proxy ×3  buffering off · raised read timeout",
               "        · Range + If-None-Match passthrough      (infra)",
               "mobile client  write scopes         (AUTH-88, gates v1.1)",
               "anonymous session tokens            (PLAT-390, ships first)"]},
]
EDGES = [                                   # at most one per adjacent pair
    {"between": 0, "row": 0, "dir": "R", "label": "sends refund reads and writes to [HTTPS + bearer]"},
    {"between": 1, "row": 0, "dir": "R", "label": "reads and writes refund rows in [SQL, customer role]"},
]
SKIP_EDGES = []     # unused in FOOTPRINT
```

Carry a count wherever there is one (`+4 columns`, `×2`, `1 table`) — counts are what make the scope legible at a glance. Indent a line one space to detail the line above it. Ticket ids on the `not ours` lines are what turn the box into an ask list.

---

## SEQ — the request/response ladder

An RFC-style ladder (the shape OAuth RFC 6749 and the SIP call-flow RFCs use to fit multi-party flows in 72 columns). Boundary boxes head the lifelines; time runs down; each message is one labeled arrow. Returns are leftward arrows, and a call that skips over a party is just a longer arrow — no routing channels. Adding messages costs **height, not width**.

<!-- regen: self -->
```
┌─────────────┐      ┌─────────────┐    ┌──────────────┐   ┌────────────────┐
│ « BROWSER » │      │ « GATEWAY » │    │ « AUTH SVC » │   │ « ORDERS API » │
└──────┬──────┘      └──────┬──────┘    └───────┬──────┘   └────────┬───────┘
       │                    │                   │                   │
       │ sends GET /orders  │                   │                   │
       │   with cookie to   │                   │                   │
       │      [HTTPS]       │                   │                   │
       ├───────────────────▶│                   │                   │
       │                    │   validates the   │                   │
       │                    │  session against  │                   │
       │                    │      [gRPC]       │                   │
       │                    ├──────────────────▶│                   │
       │                    │  returns user +   │                   │
       │                    │ scopes to [gRPC]  │                   │
       │                    │◀──────────────────┤                   │
       │                    │      forwards request to [HTTP]       │
       │                    ├───────────────────┼──────────────────▶│
       │                    │  responds with order list to [HTTP]   │
       │                    │◀──────────────────┼───────────────────┤
       │  renders JSON to   │                   │                   │
       │      [HTTPS]       │                   │                   │
       │◀───────────────────┤                   │                   │
       │                opens SSE stream to [HTTPS]                 │
       ├────────────────────┼───────────────────┼──────────────────▶│
       │                    │                   │                   │
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
    {"from": 0, "to": 1, "label": "sends GET /orders with cookie to [HTTPS]"},
    {"from": 1, "to": 2, "label": "validates the session against [gRPC]"},
    {"from": 2, "to": 1, "label": "returns user + scopes to [gRPC]"},
    {"from": 1, "to": 3, "label": "forwards request to [HTTP]"},      # skips a lifeline — just a longer arrow
    {"from": 3, "to": 1, "label": "responds with order list to [HTTP]"},
    {"from": 1, "to": 0, "label": "renders JSON to [HTTPS]"},
    {"from": 0, "to": 3, "label": "opens SSE stream to [HTTPS]"},     # skip-level, no routing channel needed
]
```

Keep header `lines` short or empty — box width, not label width, is what limits how many lifelines fit.

---

## LR — side-by-side structure (2–3 systems)

The original columnar layout, and still the most readable one: each arrow is a sentence in the gap between two boxes, returns are `◀` arrows, skip-level calls route in a channel below. Gaps are sized to their labels while the whole diagram fits the 120-char budget — so a diagram that already fits renders exactly as it always did (this one is 115 chars).

<!-- regen: self -->
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

### The same layout once the labels outgrow the pane

Width is a budget, not a consequence. Past 120 chars the gaps share what's left and each label wraps onto lines above its arrow — the last line stays inline, so the sentence still reads into the arrowhead. The config below is the one from `diagram.py`'s header, which used to render 150 chars wide and clip:

<!-- regen: default -->
```
« CLIENT — external »                       « PLATFORM »                                 « PROVIDERS — external »
┌──────────────────────┐                    ┌───────────────────────┐                    ┌─────────────────────────────┐
│ mobile app  [Swift]  │─ sends requests ──▶│ api gateway  [Go]     │─ requests ────────▶│ email / push  [SaaS]        │
│                      │  to [HTTPS]        │                       │  delivery to       │                             │
│                      │                    │                       │  [HTTPS]           │                             │
│  offline cache (NEW) │                    │  app service  [Node]  │                    │  identity provider  [OAuth] │
│                      │◀─── receives push ─│  feature API (NEW)    │◀──────── receives ─│                             │
│                      │              from  │                       │     webhooks from  │                             │
│                      │       [WebSocket]  │                       │           [HTTPS]  │                             │
│                      │                    │  database  [Postgres] │                    │                             │
└───────────┬──────────┘                    └───────────────────────┘                    └──────────────┬──────────────┘
            │                                                                                           ▲
            └ authenticates with [OAuth] ───────────────────────────────────────────────────────────────┘
```

Costing height instead of width is the whole trick: nothing about the layout changes, and no diagram that already fits is touched.

---

## TB — stacked structure (4+ systems, no time order)

One boundary per row, each edge label on its own full line to the right. Width is bounded by the widest box plus the longest label, regardless of how many systems stack up — so it stays in the pane where LR wouldn't.

<!-- regen: self -->
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

<!-- regen: TB, STAGGER=8 -->
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
