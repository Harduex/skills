#!/usr/bin/env bash
# Deterministic contract checker for an autonomous-build-loop run.
# Runs the checks declared in docs/loop/<slug>/contract.md — i.e. YOUR OWN
# declared commands — from the repo root, and reports pass/fail per item.
# Because it runs the real commands, nothing can self-grade (L2), and the
# contract file is the single source of truth for "done" (L1/L6).
#
# Usage: scripts/check.sh <slug>
# Exit:  0 = every runnable check passed · 1 = a check failed · 2 = usage/parse error
set -uo pipefail   # deliberately no -e: run every check, then aggregate

slug="${1:-}"
[ -n "$slug" ] || { echo "usage: $0 <slug>" >&2; exit 2; }
contract="docs/loop/$slug/contract.md"
[ -f "$contract" ] || { echo "error: $contract not found" >&2; exit 2; }

# Contract rows look like:  | C1 | <description> | `command` |
mapfile -t rows < <(grep -E '^\|[[:space:]]*C[0-9]+[[:space:]]*\|' "$contract")
if [ "${#rows[@]}" -eq 0 ]; then
  echo "error: no contract rows (| Cn | … | \`cmd\` |) found in $contract" >&2
  exit 2
fi

out="$(mktemp)"; trap 'rm -f "$out"' EXIT
fail=0
for row in "${rows[@]}"; do
  id="$(printf '%s' "$row" | sed -E 's/^\|[[:space:]]*(C[0-9]+)[[:space:]]*\|.*/\1/')"
  # command = text inside the last backtick pair on the row
  cmd="$(printf '%s' "$row" | grep -oE '`[^`]+`' | tail -1 | sed 's/^`//; s/`$//')"
  if [ -z "$cmd" ] || printf '%s' "$cmd" | grep -q '<command>'; then
    echo "SKIP $id — no command set yet"
    continue
  fi
  echo "RUN  $id — $cmd"
  eval "$cmd" >"$out" 2>&1; rc=$?          # runs your declared check, by design
  if [ "$rc" -eq 0 ]; then
    echo "PASS $id"
  else
    echo "FAIL $id (exit $rc)"
    tail -5 "$out" | sed 's/^/       | /'
    fail=1
  fi
done

[ "$fail" -eq 0 ] && echo "== all green ==" || echo "== some checks failed =="
exit "$fail"
