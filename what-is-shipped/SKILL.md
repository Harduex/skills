---
name: what-is-shipped
description: Produces a report of shipped work for a given period or quarter (Q{N}) by mining merged git history across one or more repos, grouping commits by issue ticket into features, and attributing them to developers. Use when asked to summarize or audit what shipped in a quarter or date range, produce a per-developer feature list, or generate a quarterly delivery report from git history.
---

# What Is Shipped

Turn merged git history into a per-developer feature report for a quarter or date range, across one or more repos.

## Quick start

1. Resolve the period to a date range.
2. List the repos in scope and detect each one's default branch.
3. Dispatch a mining subagent per repo (tiny repos can share one) — keeps the main context clean.
4. Synthesize into one per-developer feature list and save under `docs/reports/`.

## 1. Resolve the period

Calendar quarters: **Q1** Jan–Mar · **Q2** Apr–Jun · **Q3** Jul–Sep · **Q4** Oct–Dec.

Compute the range with `date` (default year = current; clamp the end to today and flag it if the quarter is ongoing/future). For a custom range, set `SINCE`/`UNTIL` directly.

```bash
Y=$(date +%Y) N=2                              # year + quarter
SINCE=$(date -d "$Y-$(((N-1)*3+1))-01" +%F)
QEND=$(date -d "$SINCE +3 months -1 day" +%F)
TODAY=$(date +%F)
UNTIL=$([ "$QEND" \> "$TODAY" ] && echo "$TODAY" || echo "$QEND")
echo "Period: $SINCE .. $UNTIL"
```

## 2. Repos & branches

Repos in scope = whatever the user names; default to the current repo. Don't hardcode the branch — repos differ (`main` vs `master` vs trunk). Detect each repo's default branch and sanity-check volume before fanning out; skip repos with no commits in the window:

```bash
REPOS=(/path/to/repo-a /path/to/repo-b)        # fill in, or just the current repo
for d in "${REPOS[@]}"; do
  b=$(git -C "$d" rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo origin/main)
  echo "== $(basename "$d") ($b) =="
  git -C "$d" log "$b" --since="$SINCE" --until="$UNTIL 23:59:59" --no-merges --format='%an' | sort | uniq -c | sort -rn
done
```

## 3. Mine each repo (subagent per repo)

Dispatch a general-purpose subagent per repo (batch tiny repos into one) with this prompt (substitute `{REPO}`, `{PATH}`, `{BRANCH}`, `{SINCE}`, `{UNTIL}`):

```
Mine git history for a FEATURE report covering {SINCE} → {UNTIL} for the {REPO} repo at {PATH}.

1. Run: git -C {PATH} log {BRANCH} --since="{SINCE}" --until="{UNTIL} 23:59:59" --no-merges --date=short --format='%h|%ad|%an|%s'
2. Group commits by issue-tracker ticket code ([A-Z]+-\d+ in the subject, e.g. ABC-123); same code = one unit of work. If this repo doesn't use ticket-prefixed commits, fall back to grouping by conventional-commit scope/type or by theme.
3. Per unit synthesize: ticket code (or "(no ticket)"); a concise Title of WHAT was built (read all the unit's subjects — describe the deliverable, not individual commits); Author(s) (primary first); Month(s); Category = Feature | Fix | Chore/Refactor/Infra | Tests/Docs. For ambiguous units inspect changed paths via `git -C {PATH} show --stat <hash>` — never full diffs. Spend effort on Features; classify the rest fast.
4. Return ONLY markdown grouped BY DEVELOPER (most commits first):

### <Name> (<N> commits)
**Features**
- `TICKET` — <what was built> _(Month)_
**Other (fixes / refactors / infra / tests)**
- `TICKET` — <short title> — <category> _(Month)_

Every commit appears under exactly one developer; omit no one. If a dev has no features, write "_(none — see Other)_".
```

## 4. Synthesize & save

Merge all repos into one report grouped by developer (order by combined commit count):

- Collapse the same ticket/theme appearing in multiple repos into a **single feature**, tagged with every repo it touched. Secondary-repo commits are often backend plumbing for a feature whose headline lives elsewhere — fold them in, don't list twice.
- Give every feature a stable ID (`F1`, `F2`, …).
- Lead each developer with **Features**; fold fixes/chores into one brief *Also:* line. Put developers with no features last as "Test / fix-only contributors".
- End with a **Summary**: feature count, developer count, and the period's headline themes.

Save to `docs/reports/<TODAY>-<label>.md` (or the repo's existing report convention). Open the file with a metadata table — reporting period, repos + their source branches, method, generated date — and a caveats note (quarter not finished → clamped to today; in-flight branch work excluded).

## Limitations

- Quality depends on disciplined commit messages — ticket-grouping degrades to theme-grouping without them.
- Commit author ≠ always who did the work (pairing, co-authors, "landed by" merges).
- Only merged history is seen; squashed/rebased work can blur attribution and dates.
