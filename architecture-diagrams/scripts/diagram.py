#!/usr/bin/env python3
"""Aligned ASCII C4-style box-and-arrow diagram generator (columnar layout).

Two orientations, one config format:

  ORIENTATION = "LR" — boundaries side by side, edge labels inline in the gaps
                       between them. Reads best at 2–3 boundaries with short
                       labels; width grows with every column AND every label,
                       so it blows past a review pane fast.
  ORIENTATION = "TB" — boundaries step down a diagonal (each box STAGGER chars
                       right of the previous), edge labels get full lines to
                       the right of the boxes, and the boundary name is the
                       box's first line. For static structure at 4+ boundaries.
  ORIENTATION = "SEQ" — an RFC-style ladder (OAuth RFC 6749, SIP call flows):
                       boundary boxes across the top, lifelines down the page,
                       one horizontal labeled arrow per message in TIME order.
                       Labels stack in time instead of widening gaps, and
                       returns / skip-level calls are ordinary arrows. The
                       default whenever the diagram tells a request/response
                       story. EDGES is the time-ordered message list; entries
                       use {"from": i, "to": j, "label": …} (any two
                       boundaries); SKIP_EDGES is unused. Keep COLUMNS
                       "lines" short or empty — they widen the header boxes.

Both render the same columnar "swimlane" model — this is NOT a general
graph-layout engine. If your diagram is hub-and-spoke (a C4 Context), deeply
layered, or has many crossing edges, reach for Mermaid-C4 / PlantUML-C4
instead (see ../SKILL.md → "Choosing a layout").

Why it exists: hand-aligning breaks constantly — off-by-one borders, labels
overflowing their gap, headers drifting. Compute the layout instead of
counting spaces. Edit ORIENTATION / COLUMNS / EDGES / SKIP_EDGES below, then:

    python3 diagram.py                 # print the diagram
    python3 diagram.py path/to/doc.md  # splice it into that file's fenced block
                                       # (the ``` block containing the first
                                       #  boundary label)

A diagram must fit a merge-request review pane without sideways scrolling:
the script warns on stderr when the render exceeds TARGET_WIDTH (120 chars).
Fix by switching to "TB" or shortening labels — never by shipping the scroll.

Conventions encoded (C4 — see c4model.com):
  • Each COLUMNS entry is one SYSTEM BOUNDARY (owning team / system), drawn as
    a bordered box. Its header (in guillemets) names it; mark externals, e.g.
    « PROVIDERS — external ». The border IS the boundary.
  • Each inner LINE is a CONTAINER; tag the technology in brackets:
    api gateway  [Go]. Indent sub-details by one space.
  • EDGES are RELATIONSHIPS between adjacent boundaries. The LEFT box (in
    "TB": the UPPER box) is the subject and the preposition points at the
    partner, so each reads as a sentence:
        outbound (dir "R" — rightward / downward):  "forwards token to [HTTPS]"
        return   (dir "L" — leftward / upward):     "receives push req from [HTTPS]"
    Always put the protocol/tech in [brackets].
  • SKIP_EDGES jump OVER one or more boundaries (box 0 → box 2); they route in
    a channel below ("LR") or to the right of ("TB") the boxes. Same subject
    rule (the `from` box is the subject).
  • Append (NEW) to whatever the current change adds; everything else is reused.
"""
import sys

PAD = 1            # inner horizontal padding inside boxes
MIN_GAP = 6        # LR: gap width between boxes when there is no edge label
ORIENTATION = "LR" # "LR" side-by-side | "TB" stacked | "SEQ" RFC-style ladder (best for flows)
STAGGER = 8        # TB: each box shifts this many chars right of the previous (0 = plain stack)
LABEL_WRAP = 20    # SEQ: word-wrap an adjacent-pair arrow label to this width
TARGET_WIDTH = 120 # warn when the render is wider (an MR pane clips ~120 chars)

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

# Adjacent-boundary edges. `between` = index of the LEFT ("TB": upper) column
# of the pair. `row` = 0-based content-row index to attach the arrow (LR only;
# ignored in TB, where edges occupy the gap between the stacked boxes).
# `dir` = "R" (outbound: rightward / downward) or "L" (return: leftward / upward).
EDGES = [
    {"between": 0, "row": 0, "dir": "R", "label": "sends requests to [HTTPS]"},
    {"between": 0, "row": 2, "dir": "L", "label": "receives push from [WebSocket]"},
    {"between": 1, "row": 0, "dir": "R", "label": "requests delivery to [HTTPS]"},
    {"between": 1, "row": 2, "dir": "L", "label": "receives webhooks from [HTTPS]"},
]

# Skip-level edges that jump over a column (an adjacent EDGE can't express a
# col-0 → col-2 hop). `from`/`to` are column indices; the arrowhead lands on
# `to`, direction inferred. LR routes them in channels below the boxes; TB in
# channels to the right. Keep labels short. Many skip edges that cross each
# other means columns are the wrong layout.
SKIP_EDGES = [
    {"from": 0, "to": 2, "label": "authenticates with [OAuth]"},
]


def build():
    """LR: boundaries side by side, edge labels inline in the gaps."""
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
    """LR: draw SKIP_EDGES in stacked channels below the boxes. Each edge gets
    its own horizontal run; deeper edges' verticals cross shallower runs as ┼."""
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


def build_tb():
    """TB: boundaries step down a diagonal (each box STAGGER chars right of
    the previous); edge labels get full lines to the right, so total width
    stays ≈ the boxes' diagonal + longest label at any boundary count. The
    boundary name is the box's first line — it can never detach from it."""
    n = len(COLUMNS)
    iws = [max([len(l) for l in c["lines"]] + [len(c["boundary"])]) + 2 * PAD
           for c in COLUMNS]
    lefts = [i * STAGGER for i in range(n)]
    rights = [lefts[i] + iws[i] + 1 for i in range(n)]

    def lanes(p):                      # lane columns for the pair (p, p+1),
        k = len([e for e in EDGES if e["between"] == p])
        lo = max(lefts[p], lefts[p + 1]) + 1      # spread across the overlap
        hi = min(rights[p], rights[p + 1]) - 1    # of the two boxes' spans
        return [lo + ((hi - lo) * (j + 1)) // (k + 1) for j in range(k)]

    grid, box_mid = [], {}
    for i, col in enumerate(COLUMNS):
        L, iw = lefts[i], iws[i]
        pad, w = " " * L, iw - 2 * PAD
        above = [e for e in EDGES if e["between"] == i - 1]
        below = [e for e in EDGES if e["between"] == i]
        top, bot = ["─"] * iw, ["─"] * iw
        # a lane leaves its subject box through a tee; the partner box keeps a
        # plain border with the arrowhead pointing at it
        for e, x in zip(above, lanes(i - 1) if above else []):
            if e["dir"] == "L":
                top[x - L - 1] = "┴"
        for e, x in zip(below, lanes(i) if below else []):
            if e["dir"] == "R":
                bot[x - L - 1] = "┬"
        grid.append(pad + "┌" + "".join(top) + "┐")
        first = len(grid)
        for l in [col["boundary"]] + col["lines"]:
            grid.append(pad + "│" + " " * PAD + l.ljust(w) + " " * PAD + "│")
        box_mid[i] = first + (1 + len(col["lines"])) // 2
        grid.append(pad + "└" + "".join(bot) + "┘")

        if i == n - 1:
            break
        xs = lanes(i)
        ups = [x for e, x in zip(below, xs) if e["dir"] == "L"]
        downs = [x for e, x in zip(below, xs) if e["dir"] == "R"]
        margin = max(rights[i], rights[i + 1]) + 2   # this gap's label column

        def bar_row(heads, head_ch):
            row = [" "] * (max(xs) + 1)
            for x in xs:
                row[x] = "│"
            for x in heads:
                row[x] = head_ch
            return "".join(row)

        if ups:                        # ▲ heads touch the border they enter
            grid.append(bar_row(ups, "▲"))
        for e, x in zip(below, xs):    # one full-width label line per edge
            row = [" "] * margin
            for xo in xs:
                row[xo] = "│"
            row[x] = "├"
            for cx in range(x + 1, margin):
                row[cx] = "┼" if row[cx] == "│" else "─"
            grid.append("".join(row) + " " + e["label"])
        if downs:
            grid.append(bar_row(downs, "▼"))

    return route_skips_tb(grid, box_mid, rights) if SKIP_EDGES else grid


def route_skips_tb(grid, box_mid, rights):
    """TB: draw SKIP_EDGES in stacked vertical channels right of the boxes.
    The label rides inline in the tee-out run; later channels cross earlier
    runs (and edge-label rows) as ┼."""
    base = max([max(len(r) for r in grid) + 2]
               + [rights[e["from"]] + len(e["label"]) + 5 for e in SKIP_EDGES])
    xs = [base + 4 * j for j in range(len(SKIP_EDGES))]
    rows = [list(r) + [" "] * (xs[-1] + 1 - len(r)) for r in grid]

    used = {}
    def row_for(i):                    # middle content row; stack if a box is reused
        r = box_mid[i] + used.get(i, 0)
        used[i] = used.get(i, 0) + 1
        return r

    for e, cx in zip(SKIP_EDGES, xs):
        rs, rt = row_for(e["from"]), row_for(e["to"])
        rsx, rtx = rights[e["from"]], rights[e["to"]]
        rows[rs][rsx] = "├"             # tee out of the subject box, label inline
        run = "─ " + e["label"] + " "
        for k, ch in enumerate(run):
            rows[rs][rsx + 1 + k] = ch
        for c in range(rsx + 1 + len(run), cx):
            rows[rs][c] = "┼" if rows[rs][c] == "│" else "─"
        rows[rt][rtx + 1] = "◀"         # arrowhead lands on the target box
        for c in range(rtx + 2, cx):
            rows[rt][c] = "┼" if rows[rt][c] == "│" else "─"
        top_r, bot_r = min(rs, rt), max(rs, rt)
        rows[top_r][cx], rows[bot_r][cx] = "┐", "┘"
        for r in range(top_r + 1, bot_r):
            rows[r][cx] = "┼" if rows[r][cx] == "─" else "│"

    return ["".join(r).rstrip() for r in rows]


def build_seq():
    """SEQ: an RFC-style ladder (cf. OAuth RFC 6749, SIP call flows) —
    boundary boxes across the top, lifelines down the page, one horizontal
    labeled arrow per message in time order. All labels share the horizontal
    band between lifelines and stack in TIME (rows), so width barely grows
    with edge count; returns and skip-level calls are just leftward or
    longer arrows. EDGES is the time-ordered message list here."""
    n = len(COLUMNS)

    def wrap(text, w):
        out, cur = [], ""
        for wd in text.split():
            if cur and len(cur) + 1 + len(wd) > w:
                out.append(cur)
                cur = wd
            else:
                cur = cur + " " + wd if cur else wd
        return out + [cur] if cur else [""]

    msgs = []
    for e in EDGES:                    # accept from/to, or LR's between/dir
        a = e["from"] if "from" in e else e["between"] + (e["dir"] == "L")
        b = e["to"] if "from" in e else e["between"] + (e["dir"] != "L")
        msgs.append((a, b, e["label"]))

    boxes = [[c["boundary"]] + c["lines"] for c in COLUMNS]
    ows = [max(len(l) for l in b) + 2 * PAD + 2 for b in boxes]
    gaps = []                          # lifeline spacing: fit the neighbour
    for p in range(n - 1):             # half-boxes and this gap's own labels
        lab = max([max(len(l) for l in wrap(m[2], LABEL_WRAP))
                   for m in msgs if {m[0], m[1]} == {p, p + 1}] + [0])
        gaps.append(max(lab + 4, ows[p] - ows[p] // 2 + ows[p + 1] // 2 + 3, MIN_GAP))
    xs = [ows[0] // 2]
    for g in gaps:
        xs.append(xs[-1] + g)
    width = xs[-1] + (ows[-1] - ows[-1] // 2)

    grid = []
    depth = max(len(b) for b in boxes)
    for r in range(depth + 2):         # header boxes, centred on lifelines
        row = [" "] * width
        for i, b in enumerate(boxes):
            L = xs[i] - ows[i] // 2
            if r == 0:
                seg = "┌" + "─" * (ows[i] - 2) + "┐"
            elif r == depth + 1:
                seg = "└" + "─" * (ows[i] - 2) + "┘"
                seg = seg[:xs[i] - L] + "┬" + seg[xs[i] - L + 1:]
            elif r - 1 < len(b):
                seg = "│" + " " * PAD + b[r - 1].ljust(ows[i] - 2 * PAD - 2) + " " * PAD + "│"
            else:
                seg = "│" + " " * (ows[i] - 2) + "│"
            row[L:L + ows[i]] = seg
        grid.append("".join(row).rstrip())

    def bar_row():
        row = [" "] * width
        for x in xs:
            row[x] = "│"
        return row

    grid.append("".join(bar_row()).rstrip())
    for a, b, label in msgs:
        lo, hi = sorted((xs[a], xs[b]))
        for line in wrap(label, max(hi - lo - 3, LABEL_WRAP)):
            row = bar_row()            # the label may sit over crossed lifelines
            start = lo + 1 + (hi - lo - 1 - len(line)) // 2
            row[start:start + len(line)] = line
            grid.append("".join(row).rstrip())
        row = bar_row()
        for c in range(lo + 1, hi):
            row[c] = "┼" if row[c] == "│" else "─"
        if xs[b] > xs[a]:              # arrowhead touches the target lifeline
            row[lo], row[hi - 1] = "├", "▶"
        else:
            row[hi], row[lo + 1] = "┤", "◀"
        grid.append("".join(row).rstrip())
    grid.append("".join(bar_row()).rstrip())
    return grid


def patch_markdown(path, diagram):
    """Replace the fenced ``` block containing the first boundary label."""
    text = open(path, encoding="utf-8").read().split("\n")
    anchor = COLUMNS[0]["boundary"][:12]
    hit = next(i for i, l in enumerate(text) if anchor in l and not l.startswith("#"))
    start = next(i for i in range(hit, -1, -1) if text[i].strip().startswith("```")) + 1
    end = next(i for i in range(hit, len(text)) if text[i].strip() == "```")
    text[start:end] = diagram
    open(path, "w", encoding="utf-8").write("\n".join(text))


if __name__ == "__main__":
    d = {"TB": build_tb, "SEQ": build_seq}.get(ORIENTATION, build)()
    print("\n".join(d))
    width = max((len(l) for l in d), default=0)
    if width > TARGET_WIDTH:
        sys.stderr.write(
            f"\n[WARN] {width} chars wide — exceeds TARGET_WIDTH={TARGET_WIDTH} "
            f"(an MR review pane). "
            + ('Set ORIENTATION = "SEQ" or shorten labels.\n' if ORIENTATION != "SEQ"
               else 'Shorten labels or trim header boxes.\n'))
    if len(sys.argv) > 1:
        patch_markdown(sys.argv[1], d)
        sys.stderr.write(f"\n[patched {sys.argv[1]}]\n")
