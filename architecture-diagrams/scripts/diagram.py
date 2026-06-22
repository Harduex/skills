#!/usr/bin/env python3
"""Aligned ASCII C4-style box-and-arrow diagram generator (columnar layout).

What this renders: a left-to-right row of system boundaries, each drawn as one
bordered box whose inner lines are its containers `[tech]`, connected by labelled
arrows. It does ONE shape well — the columnar "swimlane" diagram. It is NOT a
general graph-layout engine. If your diagram is hub-and-spoke (a C4 Context),
deeply layered, or has many crossing edges, columns are the wrong shape — reach
for Mermaid-C4 / PlantUML-C4 instead (see ../SKILL.md → "Choosing a layout").

Why it exists: hand-aligning the columnar case breaks constantly — off-by-one
borders, labels overflowing their gap, headers drifting. Compute the layout
instead of counting spaces. Edit COLUMNS / EDGES / SKIP_EDGES below, then:

    python3 diagram.py                 # print the diagram
    python3 diagram.py path/to/doc.md  # splice it into that file's fenced block
                                       # (the ``` block whose first line is the
                                       #  first boundary label)

Conventions encoded (C4 — see c4model.com):
  • Each COLUMN is one SYSTEM BOUNDARY (owning team / system), drawn as a
    bordered box. Its header (in guillemets) names it; mark externals, e.g.
    « PROVIDERS — external ». The border IS the boundary.
  • Each inner LINE is a CONTAINER; tag the technology in brackets:
    api gateway  [Go]. Indent sub-details by one space.
  • EDGES are RELATIONSHIPS between adjacent columns. The LEFT box is the
    subject and the preposition points at the partner, so each reads as a
    sentence:
        outbound (→):  "forwards token to [HTTPS]"
        return  (←):   "receives push req from [HTTPS]"
    Always put the protocol/tech in [brackets].
  • SKIP_EDGES jump OVER one or more columns (col 0 → col 2); they route in a
    channel below the boxes. Same subject/preposition rule (left box = subject).
  • Append (NEW) to whatever the current change adds; everything else is reused.
"""
import sys

PAD = 1        # inner horizontal padding inside boxes
MIN_GAP = 6    # gap width between boxes when there is no edge label

# One dict per column = one boundary box. `lines` are the container rows.
# (Generic example — replace with your own systems.)
COLUMNS = [
    {"boundary": "« CLIENT — external »",
     "lines": ["mobile app  [Swift]", " offline cache (NEW)"]},
    {"boundary": "« PLATFORM »",
     "lines": ["api gateway  [Go]", " app service  [Node]", " feature API (NEW)", " database  [Postgres]"]},
    {"boundary": "« PROVIDERS — external »",
     "lines": ["email / push  [SaaS]", " identity provider  [OAuth]"]},
]

# Adjacent-column edges. `between` = index of the LEFT column of the pair.
# `row` = 0-based content-row index to attach the arrow.
# `dir` = "R" (left→right) or "L" (right→left, a return arrow).
EDGES = [
    {"between": 0, "row": 0, "dir": "R", "label": "sends requests to [HTTPS]"},
    {"between": 0, "row": 2, "dir": "L", "label": "receives push from [WebSocket]"},
    {"between": 1, "row": 0, "dir": "R", "label": "requests delivery to [HTTPS]"},
    {"between": 1, "row": 2, "dir": "L", "label": "receives webhooks from [HTTPS]"},
]

# Skip-level edges that jump over a column (an adjacent EDGE can't express a
# col-0 → col-2 hop). `from`/`to` are column indices; the arrowhead lands on
# `to`, direction inferred. Routed in a channel below the boxes. Keep labels
# short — the run spans only from the source center to the target center.
# Many skip edges that cross each other means columns are the wrong layout.
SKIP_EDGES = [
    {"from": 0, "to": 2, "label": "authenticates with [OAuth]"},
]


def build():
    n = len(COLUMNS)
    rows = max((len(c["lines"]) for c in COLUMNS), default=0)
    for c in COLUMNS:
        c["lines"] = c["lines"] + [""] * (rows - len(c["lines"]))
    widths = [max((len(l) for l in c["lines"]), default=1) for c in COLUMNS]

    gaps = []
    for p in range(n - 1):
        labels = [e["label"] for e in EDGES if e["between"] == p]
        gaps.append(max([len(l) + 5 for l in labels] + [MIN_GAP]))

    def arrow(label, d, w):
        k = w - len(label) - 4  # filler dashes; guaranteed >= 1 by the +5 above
        return ("─ " + label + " " + "─" * k + "▶") if d == "R" \
            else ("◀" + "─" * k + " " + label + " " + "─")

    def box_rows(lines, w):
        inner = w + 2 * PAD
        body = ["│" + " " * PAD + l.ljust(w) + " " * PAD + "│" for l in lines]
        return ["┌" + "─" * inner + "┐"] + body + ["└" + "─" * inner + "┘"]

    br = [box_rows(COLUMNS[i]["lines"], widths[i]) for i in range(n)]
    edge_at = {(e["between"], e["row"]): arrow(e["label"], e["dir"], gaps[e["between"]])
               for e in EDGES}

    out = []
    for r in range(len(br[0])):
        cr = r - 1  # content-row index (top border is -1)
        line = br[0][r]
        for p in range(n - 1):
            seg = edge_at.get((p, cr)) if cr >= 0 else None
            line += (seg if seg else " " * gaps[p]) + br[p + 1][r]
        out.append(line)

    ow = lambda w: w + 2 * PAD + 2
    col_start = [0]
    for i in range(n - 1):
        col_start.append(col_start[-1] + ow(widths[i]) + gaps[i])
    centers = [col_start[i] + ow(widths[i]) // 2 for i in range(n)]
    total_w = col_start[-1] + ow(widths[-1])

    buf = [" "] * total_w
    for i, c in enumerate(COLUMNS):
        for j, ch in enumerate(c["boundary"]):
            buf[col_start[i] + j] = ch
    diagram = ["".join(buf).rstrip()] + out

    return route_skips(diagram, centers, total_w) if SKIP_EDGES else diagram


def route_skips(diagram, centers, total_w):
    """Draw SKIP_EDGES in stacked channels below the boxes. Each edge gets its
    own horizontal run; deeper edges' verticals cross shallower runs as ┼."""
    grid = [list(line.ljust(total_w)) for line in diagram]
    border = grid[-1]                       # boxes' bottom-border row
    depth = len(SKIP_EDGES) + 1             # channel rows needed
    chan = [[" "] * total_w for _ in range(depth)]

    for i, e in enumerate(SKIP_EDGES):
        ca, cb = centers[e["from"]], centers[e["to"]]
        lo, hi = sorted((ca, cb))
        hidx = i + 1                        # this edge's horizontal channel row
        border[ca] = border[cb] = "┬"       # tee down out of both boxes
        for x, is_target in ((ca, False), (cb, True)):
            for d in range(hidx):           # verticals from just-below-box to the run
                ch = "▲" if (d == 0 and is_target) else "│"
                chan[d][x] = "┼" if chan[d][x] == "─" else ch
        chan[hidx][lo], chan[hidx][hi] = "└", "┘"
        for x in range(lo + 1, hi):
            if chan[hidx][x] == " ":
                chan[hidx][x] = "─"
        for j, ch in enumerate(" " + e["label"] + " "):
            if lo + 1 + j < hi:
                chan[hidx][lo + 1 + j] = ch

    return ["".join(r).rstrip() for r in grid] + ["".join(r).rstrip() for r in chan]


def patch_markdown(path, diagram):
    text = open(path, encoding="utf-8").read().split("\n")
    anchor = COLUMNS[0]["boundary"][:12]
    start = next(i for i, l in enumerate(text) if l.startswith(anchor))
    end = next(i for i in range(start, len(text)) if text[i].strip() == "```")
    text[start:end] = diagram
    open(path, "w", encoding="utf-8").write("\n".join(text))


if __name__ == "__main__":
    d = build()
    print("\n".join(d))
    if len(sys.argv) > 1:
        patch_markdown(sys.argv[1], d)
        sys.stderr.write(f"\n[patched {sys.argv[1]}]\n")
