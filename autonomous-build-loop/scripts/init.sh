#!/usr/bin/env bash
# Scaffold the on-disk state for an autonomous-build-loop run.
# Run from your repository root. Creates docs/loop/<slug>/ with the durable
# continuation note, the done contract, and the first task slice — plus a
# git-ignored journal under .loop/<slug>/ for failures and retries.
#
# Completed slices are deleted in their own completion commit, so the tree stays
# small and git history keeps every task's instructions.
#
# Usage: scripts/init.sh [--force] <slug> ["Feature title"]
set -euo pipefail

force=0
if [ "${1:-}" = "--force" ]; then force=1; shift; fi

slug="${1:-}"
title="${2:-$slug}"

if [ -z "$slug" ]; then
  echo "usage: $0 [--force] <slug> [\"Feature title\"]" >&2
  exit 2
fi
if ! printf '%s' "$slug" | grep -qE '^[a-z0-9][a-z0-9-]*$'; then
  echo "error: slug must be kebab-case (a-z, 0-9, -), got: '$slug'" >&2
  exit 2
fi

dir="docs/loop/$slug"
jdir=".loop/$slug"
if [ -e "$dir" ]; then
  echo "error: $dir already exists — refusing to overwrite live loop state." >&2
  echo "       inspect it with scripts/status.sh $slug, or remove it deliberately first." >&2
  exit 1
fi

# Candidate names for a repo-owned continuation note, in probe order. Anything
# under docs/loop/ is this skill's own state, not a substrate — see L10.
# The same list lives in status.sh; change both together.
note_candidates() {
  find . -maxdepth 3 \
    \( -name CHECKPOINT.md -o -name STATE.md -o -name HANDOFF.md \
       -o -name CONTINUE.md -o -name PROGRESS.md \) \
    -not -path './.git/*' -not -path './docs/loop/*' -not -path './node_modules/*' \
    2>/dev/null | sed 's|^\./||' | sort
}

if [ "$force" -eq 0 ]; then
  existing="$(note_candidates || true)"
  if [ -n "$existing" ]; then
    echo "error: this repo already owns a continuation note — scaffolding a second" >&2
    echo "       source of truth for state is the L10 failure mode. Found:" >&2
    printf '%s\n' "$existing" | sed 's/^/         /' >&2
    echo "       bind to it instead (scripts/status.sh --adopt), or pass --force if" >&2
    echo "       this repo genuinely wants both." >&2
    exit 1
  fi
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

cat > "$dir/CHECKPOINT.md" <<'EOF'
# Checkpoint — __TITLE__   (slug: __SLUG__)

<!-- The one durable note every new session reads FIRST. Keep it current, and keep
     it a state description rather than a log: only what the next session cannot
     re-derive from the code, the contract, or git history. -->

**Status:** ready
**Current task:** `docs/loop/__SLUG__/001-first-task.md`

## Orientation
- Goal: <one paragraph — what and why>
- Branch: <branch-name>
- Key paths: `<path>` — <role>
- Build / run / test: `<cmd>` · `<cmd>`
- Contract: `docs/loop/__SLUG__/contract.md`

## Last completed
- <none yet>

## Last verification
- <the measured result of the last completed task's checks — command and outcome>

## Locked decisions
- <a durable choice and why; only what a later session must not re-litigate>

## Known blockers
- <none>

## Next action
Read the current task, invoke the capabilities it names, and implement only that task.
EOF

cat > "$dir/001-first-task.md" <<'EOF'
# Task 001 — <the capability this task adds>

**Status:** ready
**Contract rows:** <which contract IDs this task must turn green>
**Required capabilities:** <what to invoke before editing — domain workflow, test-first authoring, verification>

## Goal

<one sentence: the observable capability that exists when this task is done>

## Allowed scope

- `<path>` — <create or change, and why>

Do not change unrelated behavior while completing this task. Record any unavoidable
scope expansion in `CHECKPOINT.md`.

## Implementation contract

- <an invariant the change must preserve>

## Test-first execution

- [ ] **RED:** write the smallest failing test for the missing behavior; confirm it fails for that reason and not a setup mistake.
- [ ] **GREEN:** implement the minimum production code that satisfies it.
- [ ] **REFACTOR:** improve names and structure while tests stay green; add no unrequested behavior.

## Acceptance criteria

- [ ] <observable outcome, checkable>

## Required verification

- [ ] Run the narrow tests this task adds and show they pass.
- [ ] Run the contract gates and record the measured result.
- [ ] Apply your verification capability before claiming this task complete.

## Completion

One commit carries implementation and tests, the advanced `CHECKPOINT.md`, and
`git rm docs/loop/__SLUG__/001-first-task.md`. No second state commit. Do not start
the next task in the same step. If a human decision or evidence is needed instead,
set the checkpoint to `waiting-human`, commit the evidence, and keep this file.
EOF

mkdir -p "$jdir"
printf '*\n' > ".loop/.gitignore"   # makes .loop/ invisible to git without touching the repo's .gitignore

cat > "$jdir/journal.md" <<'EOF'
# Journal — __TITLE__   (ephemeral, git-ignored; newest at bottom)

Failures, retries, drift, and measured check output — the loop's Reflexion memory
(L5/L8). Durable outcomes graduate to `CHECKPOINT.md`; this file dies with the branch.

## __STAMP__ · loop initialized
- Did: scaffolded docs/loop/__SLUG__/ (CHECKPOINT.md, contract.md, 001-first-task.md) and this journal.
- Next: fill the contract and the first task slice, commit the loop state, then start cycle 1.
EOF

# Fill placeholders (kept out of the heredocs so nothing else expands).
for f in "$dir/contract.md" "$dir/CHECKPOINT.md" "$dir/001-first-task.md" "$jdir/journal.md"; do
  sed -i "s|__TITLE__|$title|g; s|__SLUG__|$slug|g; s|__STAMP__|$stamp|g" "$f"
done

echo "scaffolded $dir/"
echo "  CHECKPOINT.md   contract.md   001-first-task.md"
echo "and $jdir/journal.md (git-ignored)"
echo
echo "next:"
echo "  1. fill contract.md    — every done-item a command with an exit code"
echo "  2. fill CHECKPOINT.md  — orientation a zero-context session can resume from"
echo "  3. write the task slices — one file per session-sized task, 001 first"
echo "  4. commit the loop state, then start cycle 1"
