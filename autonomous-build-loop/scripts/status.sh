#!/usr/bin/env bash
# Read-only status + resume helper for autonomous-build-loop runs.
# Run from your repository root.
#
# Usage:
#   scripts/status.sh            # list all loops under docs/loop/
#   scripts/status.sh <slug>     # progress + next task + latest journal entry
#
# Reads state from disk only — it never runs your project's checks and never
# edits anything. A fresh session runs this first to orient (reinforces L4:
# trust the files, not session memory).
set -euo pipefail

base="docs/loop"
slug="${1:-}"

if [ -z "$slug" ]; then
  if [ ! -d "$base" ]; then
    echo "no loops found under $base/"
    exit 0
  fi
  echo "loops under $base/:"
  found=0
  for d in "$base"/*/; do
    [ -d "$d" ] || continue
    echo "  - $(basename "$d")"
    found=1
  done
  [ "$found" -eq 1 ] || echo "  (none)"
  exit 0
fi

dir="$base/$slug"
if [ ! -d "$dir" ]; then
  echo "error: $dir not found (run scripts/init.sh $slug first)" >&2
  exit 1
fi

plan="$dir/plan.md"
journal="$dir/journal.md"

echo "== loop: $slug =="

if [ -f "$plan" ]; then
  task_rows="$(grep -E '^\|[[:space:]]*[0-9]+[[:space:]]*\|' "$plan" || true)"
  count() { printf '%s\n' "$task_rows" | grep -icE "\|[[:space:]]*$1[[:space:]]*\|" || true; }
  echo "tasks: $(count done) done · $(count doing) doing · $(count todo) todo · $(count blocked) blocked"
  next="$(printf '%s\n' "$task_rows" | grep -iE '\|[[:space:]]*(doing|todo|blocked)[[:space:]]*\|' | head -1 || true)"
  [ -n "$next" ] && echo "next:  $(printf '%s' "$next" | sed 's/^[[:space:]]*//')"
else
  echo "(no plan.md)"
fi

echo
echo "-- latest journal entry --"
if [ -f "$journal" ]; then
  awk '/^## /{last=NR} {L[NR]=$0} END{if(last==""){print "(no entries)"} else {for(i=last;i<=NR;i++) print L[i]}}' "$journal"
else
  echo "(no journal.md)"
fi
