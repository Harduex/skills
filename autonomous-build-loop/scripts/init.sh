#!/usr/bin/env bash
# Scaffold the on-disk state for an autonomous-build-loop run.
# Run from your repository root. Creates docs/loop/<slug>/ with the three
# state files the loop reads at the start of every cycle and writes at the end.
#
# Usage: scripts/init.sh <slug> ["Feature title"]
set -euo pipefail

slug="${1:-}"
title="${2:-$slug}"

if [ -z "$slug" ]; then
  echo "usage: $0 <slug> [\"Feature title\"]" >&2
  exit 2
fi
if ! printf '%s' "$slug" | grep -qE '^[a-z0-9][a-z0-9-]*$'; then
  echo "error: slug must be kebab-case (a-z, 0-9, -), got: '$slug'" >&2
  exit 2
fi

dir="docs/loop/$slug"
if [ -e "$dir" ]; then
  echo "error: $dir already exists — refusing to overwrite live loop state." >&2
  echo "       inspect it with scripts/status.sh $slug, or remove it deliberately first." >&2
  exit 1
fi

stamp="$(date -u +%Y-%m-%dT%H:%MZ)"
mkdir -p "$dir"

cat > "$dir/contract.md" <<'EOF'
# Done contract — __TITLE__

<!-- Each row is DONE only when its command exits 0. The loop halts when every row is green.
     Rule (L1): if a done-item can't be reduced to a command + exit code, it does NOT belong
     here — move it to the human-verified list below. A contract of vague goals can never halt. -->

| ID | Done when… | Check (exit 0 = pass) |
|----|------------|------------------------|
| C1 | <what is observably true when this is done> | `<command>` |

Human-verified acceptance (NOT loopable — hand to the human):
- <e.g. empty-state copy reads well>
EOF

cat > "$dir/plan.md" <<'EOF'
# Plan — __TITLE__   (slug: __SLUG__)

## Orientation  <!-- a fresh agent reads this FIRST; keep it current -->
- Goal: <one paragraph — what and why>
- Branch: <branch-name>
- Key paths: `<path>` — <role>
- Build / run / test: `<cmd>` · `<cmd>`
- Contract: `docs/loop/__SLUG__/contract.md`
- Resume: start at the first non-`done` task below; read the `journal.md` tail for recent context.

## Tasks
| # | Task — self-contained, written for an agent with zero prior context | Status | Commit | Notes |
|---|----------------------------------------------------------------------|--------|--------|-------|
| 1 | <first task> | todo |  |  |
EOF

cat > "$dir/journal.md" <<'EOF'
# Journal — __TITLE__   (append-only; newest at bottom)

## __STAMP__ · loop initialized
- Did: scaffolded docs/loop/__SLUG__/ (contract.md, plan.md, journal.md).
- Next: fill contract.md and plan.md, commit the loop state, then start cycle 1.
EOF

# Fill placeholders (kept out of the heredocs so nothing else expands).
for f in contract.md plan.md journal.md; do
  sed -i "s|__TITLE__|$title|g; s|__SLUG__|$slug|g; s|__STAMP__|$stamp|g" "$dir/$f"
done

echo "scaffolded $dir/"
echo "  contract.md   plan.md   journal.md"
echo
echo "next:"
echo "  1. fill contract.md — every done-item a command with an exit code"
echo "  2. fill plan.md     — orientation header + ordered, self-contained tasks"
echo "  3. commit the loop state, then start cycle 1"
