#!/usr/bin/env bash
# Read-only status + resume helper for autonomous-build-loop runs.
# Run from your repository root.
#
# Usage:
#   scripts/status.sh                             # list all loops under docs/loop/
#   scripts/status.sh <slug>                      # this loop's note, current slice, journal tail
#   scripts/status.sh --adopt [note] [slice-dir]  # read a continuation note the repo owns
#
# Reads state from disk only — it never runs your project's checks and never
# edits anything. A fresh session runs this first to orient (reinforces L4:
# trust the files, not session memory).
set -euo pipefail

base="docs/loop"

# Candidate names for a repo-owned continuation note, in probe order. Anything
# under docs/loop/ is this skill's own state, not a substrate — see L10.
# The same list lives in init.sh; change both together.
note_candidates() {
  find . -maxdepth 3 \
    \( -name CHECKPOINT.md -o -name STATE.md -o -name HANDOFF.md \
       -o -name CONTINUE.md -o -name PROGRESS.md \) \
    -not -path './.git/*' -not -path "./$base/*" -not -path './node_modules/*' \
    2>/dev/null | sed 's|^\./||' | sort
}

# Key/value status fields, in whichever notation the note uses. A foreign note is
# not obliged to use this skill's; try the common ones before giving up.
note_fields() {
  local n="$1" out
  # YAML frontmatter
  out="$(awk 'NR==1 && /^---[[:space:]]*$/ {f=1; next}
              f && /^---[[:space:]]*$/ {exit}
              f && /^[A-Za-z][A-Za-z0-9_ -]*:/ {print}' "$n")"
  [ -n "$out" ] && { printf '%s\n' "$out" | head -8; return; }
  # **Key:** value
  out="$(grep -E '^\*\*[^*]+:\*\*' "$n" || true)"
  [ -n "$out" ] && { printf '%s\n' "$out" | head -8; return; }
  # ## Key  followed by its first non-empty line.
  # `##+` rather than `#{2,3}`: mawk has no interval expressions.
  out="$(awk '/^##+ /{k=$0; sub(/^#+[[:space:]]*/,"",k);
                         while ((getline l) > 0 && l ~ /^[[:space:]]*$/) {}
                         if (l !~ /^#/ && l !~ /^[[:space:]]*$/) printf "%s: %s\n", k, l}' "$n")"
  [ -n "$out" ] && { printf '%s\n' "$out" | head -8; return; }
  # Key: value
  grep -E '^[A-Za-z][A-Za-z0-9_ -]*:[[:space:]]*[^[:space:]]' "$n" | head -8 || true
}

# The path of the current unit of work. Looked for on the line that names it and
# the two lines after, since a note may put the pointer under its heading.
note_pointer() {
  awk 'tolower($0) ~ /current/ && !found { win = NR; found = 1 }
       found && NR >= win && NR <= win + 2 { buf = buf " " $0 }
       END { if (match(buf, /`[^`]+`/)) { print substr(buf, RSTART+1, RLENGTH-2); exit }
             if (match(buf, /[A-Za-z0-9_.\/-]+\.md/)) print substr(buf, RSTART, RLENGTH) }' "$1"
}

# Render a continuation note plus its work slices. The loop's own state and an
# adopted substrate are the same shape, so both go through here.
#   $1 note path · $2 slice directory · $3 journal path (optional)
show_note() {
  local note="$1" slice_dir="$2" journal="${3:-}" fields slice remaining other dirty hist

  echo "-- status fields --"
  fields="$(note_fields "$note" || true)"
  if [ -n "$fields" ]; then printf '%s\n' "$fields" | sed 's/^/  /'; else echo "  (none found)"; fi

  slice="$(note_pointer "$note" || true)"
  if [ -n "$slice" ]; then
    if [ -e "$slice" ]; then
      echo "slice: $slice (present)"
    else
      echo "slice: $slice (MISSING — already retired, or the pointer is stale: check its history)"
    fi
    [ -n "$slice_dir" ] || slice_dir="$(dirname "$slice")"
  else
    echo "slice: (none named)"
  fi

  remaining="$(find "$slice_dir" -maxdepth 1 -name '[0-9][0-9][0-9]-*.md' 2>/dev/null | wc -l | tr -d ' ')"
  if [ "$remaining" -gt 0 ]; then
    echo "queue: $remaining numbered slice file(s) left in $slice_dir"
  else
    # A foreign convention need not number its slices; count what is there and say so.
    other="$(find "$slice_dir" -maxdepth 1 -name '*.md' \
               ! -name "$(basename "$note")" ! -name 'contract.md' ! -name 'README.md' \
               2>/dev/null | wc -l | tr -d ' ')"
    echo "queue: 0 numbered slices · $other other .md file(s) in $slice_dir"
  fi

  # Never let an unrecognised shape read as "nothing in progress" (L2/L6 in spirit:
  # report what was measured, and say plainly when nothing could be).
  if [ -z "$fields" ] && [ -z "$slice" ]; then
    echo "shape: UNRECOGNISED — no status fields and no current-item pointer were found."
    echo "       Read $note directly; this is NOT evidence that no work is in progress."
  fi

  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    dirty="$(git status --porcelain | wc -l | tr -d ' ')"
    if [ "$dirty" -gt 0 ]; then
      echo "tree:  $dirty uncommitted path(s) — a stopped mid-slice session; reconcile before advancing"
    else
      echo "tree:  clean"
    fi
    echo
    echo "-- recent history under $slice_dir (retired slices live here) --"
    hist="$(git log --oneline -5 -- "$slice_dir" 2>/dev/null || true)"
    if [ -n "$hist" ]; then printf '%s\n' "$hist" | sed 's/^/  /'; else echo "  (none)"; fi
  fi

  if [ -n "$journal" ] && [ -f "$journal" ]; then
    echo
    echo "-- latest journal entry ($journal) --"
    awk '/^## /{last=NR} {L[NR]=$0} END{if(last==""){print "(no entries)"} else {for(i=last;i<=NR;i++) print L[i]}}' "$journal"
  fi
}

if [ "${1:-}" = "--adopt" ]; then
  shift
  note="${1:-}"
  slice_dir="${2:-}"

  if [ -z "$note" ]; then
    note="$(note_candidates | head -1 || true)"
    if [ -z "$note" ]; then
      echo "error: no continuation note found — pass its path: $0 --adopt <note> [slice-dir]" >&2
      exit 1
    fi
    echo "note:  $note   (probed — pass a path to override)"
  else
    [ -f "$note" ] || { echo "error: $note not found" >&2; exit 1; }
    echo "note:  $note"
  fi
  [ -n "$slice_dir" ] || slice_dir="$(dirname "$note")"

  show_note "$note" "$slice_dir"
  exit 0
fi

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

echo "== loop: $slug =="

if [ -f "$dir/CHECKPOINT.md" ]; then
  show_note "$dir/CHECKPOINT.md" "$dir" ".loop/$slug/journal.md"
  exit 0
fi

# Runs scaffolded before the note-and-slices shape: a plan.md task table with a
# committed journal. Read as-is so an in-flight loop keeps resuming.
plan="$dir/plan.md"
journal="$dir/journal.md"
echo "(plan.md shape)"

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
