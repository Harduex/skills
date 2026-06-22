#!/usr/bin/env python3
"""Verify ASCII box integrity in a diagram (or every fenced diagram in a .md).

Catches what a HAND-DRAWN diagram silently ships: a box missing a border, a
broken side wall, a misaligned corner, or column-mate boxes of unequal width.
The columnar generator (diagram.py) produces correct boxes by construction —
this is the safety net for the hand-drawn shapes (vertical chains, hub-and-spoke)
that have no generator.

    python3 verify_boxes.py doc.md        # lint every fenced diagram block
    python3 verify_boxes.py diagram.txt   # lint a raw diagram
    ... | python3 verify_boxes.py         # lint stdin

Exit 0 = clean, 1 = problems found. Skip-edge routing channels (a └/┘ whose
│ chain descends from a ┬ on a box bottom) are recognised and ignored, so
generator output with SKIP_EDGES does not false-positive.
"""
import sys
from collections import defaultdict

TL, TR, BL, BR = "┌", "┐", "└", "┘"
CORNERS = set(TL + TR + BL + BR)
VWALL = set("│├┤┼")   # legal characters down a box side
DOWN_TEE = "┬"        # a routing vertical descends from this on a box bottom
UP_TEE = "┴"          # a connector rises into this on a box top


def grid_of(text):
    rows = text.split("\n")
    w = max((len(r) for r in rows), default=0)
    return [list(r.ljust(w)) for r in rows]


def at(g, r, c):
    return g[r][c] if 0 <= r < len(g) and 0 <= c < len(g[r]) else " "


def find_boxes(g):
    """Every closed box as (top, left, bottom, right); plus its consumed corners."""
    boxes, consumed = [], set()
    for r in range(len(g)):
        for c in range(len(g[r])):
            if g[r][c] != TL:
                continue
            c2 = next((cc for cc in range(c + 1, len(g[r])) if g[r][cc] in CORNERS), None)
            if c2 is None or g[r][c2] != TR:
                continue
            r2 = next((rr for rr in range(r + 1, len(g)) if at(g, rr, c) == BL), None)
            if r2 is None or at(g, r2, c2) != BR:
                continue
            if all(at(g, ri, c) in VWALL and at(g, ri, c2) in VWALL for ri in range(r + 1, r2)):
                boxes.append((r, c, r2, c2))
                consumed |= {(r, c), (r, c2), (r2, c), (r2, c2)}
    return boxes, consumed


def terminator(g, r, c, step):
    """Walk the │ chain from (r,c) in row-direction `step`; return the first
    non-wall char that ends it."""
    while at(g, r + step, c) in VWALL:
        r += step
    return at(g, r + step, c)


def lint(text, label):
    g = grid_of(text)
    boxes, consumed = find_boxes(g)
    problems = []

    for r in range(len(g)):
        for c in range(len(g[r])):
            ch = g[r][c]
            if ch not in CORNERS or (r, c) in consumed:
                continue
            if ch == BL and terminator(g, r, c, -1) != DOWN_TEE:
                problems.append(f"  line {r+1} col {c+1}: box bottom-left └ with no matching top border (broken/missing box)")
            elif ch == TL and terminator(g, r, c, +1) != UP_TEE:
                problems.append(f"  line {r+1} col {c+1}: box top-left ┌ not closed (broken/missing bottom or side wall)")

    by_col = defaultdict(set)
    for (r, c, r2, c2) in boxes:
        by_col[c].add(c2 - c)
    for c, widths in sorted(by_col.items()):
        if len(widths) > 1:
            problems.append(f"  boxes starting at col {c+1} have unequal widths {sorted(widths)} (column-mates should match)")

    print(f"[{label}] {len(boxes)} box(es) — {'OK' if not problems else 'PROBLEMS'}")
    for p in problems:
        print(p)
    return not problems


def blocks(text):
    """Yield (label, diagram) for each fenced block with box chars, else all of it."""
    lines = text.split("\n")
    fences = [i for i, l in enumerate(lines) if l.strip().startswith("```")]
    emitted = False
    for a, b in zip(fences[::2], fences[1::2]):
        body = "\n".join(lines[a + 1:b])
        if any(ch in body for ch in CORNERS):
            emitted = True
            yield f"block@line{a+1}", body
    if not emitted:
        yield "diagram", text


if __name__ == "__main__":
    src = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    results = [lint(d, lbl) for lbl, d in blocks(src)]
    sys.exit(0 if all(results) else 1)
