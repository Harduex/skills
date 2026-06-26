---
name: linear-git-history
description: Use when rewriting a multi-commit branch into clean, single-purpose commits that each build on their own — linearize, curate, or clean up branch history, make every commit a self-contained working milestone, split an overloaded commit, reorder commits so dependencies flow forward, or strip add-then-remove churn — keeping the final tree byte-for-byte identical to the current tip. Also when commits build only cumulatively (an early commit uses a type/util/symbol a later commit introduces) or before an exemplary MR/PR.
---

# Linear Git History

Rewrite a branch's commits — never its final tree. End state: each commit is single-purpose, ordered so dependencies flow forward, carries a why-focused message, and **builds in isolation**; `git diff <tip-before> <tip-after>` is empty.

## When to use

- Curating a feature branch into reviewable, self-contained commits before an MR/PR.
- A commit is overloaded (mixes concerns), or sits before the code it depends on.
- Trailing `FIX`/`WIP`/`MR fixes` commits, or add-then-remove churn, pollute history.

When NOT to use:

- Single-commit branch → `git commit --amend`.
- You only need to fold loose fixes into existing commits, no reorder/split → use the **distribute-fixups** skill alone.
- Branch under active review where SHA churn would disorient reviewers → coordinate first.

## The one invariant that matters most

**Every resulting commit MUST build in isolation.** Check out each commit and run the repo's own typecheck + lint (discover from `package.json`/CI — e.g. `tsc --noEmit`, `eslint`, `go build`, `cargo check`). A final-tree-only check passes even when an early commit references a shared type/util/enum that a *later* commit introduces — so commits `1..n-1` don't compile. This is the failure this skill exists to catch. Do not skip it; do not substitute a final-tree diff for it.

## Workflow

### 0. Anchor

```bash
git rev-parse HEAD                  # ANCHOR — save it; the final tree must equal this
git log --oneline <base>..HEAD      # map the branch (base = main/develop)
```

### 1. Fold trailing fix/WIP commits first

If the branch ends in `FIX`/`WIP`/review-fixup commits, redistribute them into the commits they patch *before* restructuring — use the **distribute-fixups** skill. Genuinely new work becomes its own commit; don't force-fit it into an unrelated one.

### 2. Plan the target commits

One concern per commit, ordered so dependencies flow forward — foundation/shared types and generated artifacts first, then the features that consume them. Derive concerns from the existing commits plus `git diff --name-only <base>..HEAD`, and note which files are shared across concerns.

Ask the user (don't guess) when:

- **Commit dates** matter — present: (1) authentic author dates + authentic order, (2) narrative/dependency order with real but non-monotonic dates, (3) today's dates. A reorder makes authentic dates non-monotonic, so (1) and a reorder are mutually exclusive.
- A split is a genuine judgment call (is X its own milestone or part of Y?).

### 3. Rebuild from the final tree

Building from the final tree means transient files/symbols (added then removed across the old history) never re-enter it — no churn to clean up by hand.

```bash
git reset --mixed <base>           # HEAD + index → base; WORKING TREE stays = anchor
```

Then stage and commit one concern at a time (`git add <paths>` → `git commit -F <msgfile>`):

- **Each changed file belongs to exactly one concern?** Whole-file `git add` per concern suffices (confirm with `git diff --name-only <base>..HEAD`).
- **A file spans concerns?** Split it. Interactive: `git add -p`. Non-interactive (agents/CI): replay each concern's hunks — `git show <origin-sha> -- <file>` → `git apply --cached --3way` — applying earlier-concern hunks before later ones.
- **Shared foundation files** (generated schema dumps, shared type modules, common utils) go *wholly* into the **earliest commit that needs them**, so every later consumer compiles.

### 4. One body per commit

Concise WHY, drafted from the actual diff — not a restatement of changed lines. Note non-obvious decisions or bundled refactors. `git commit -F <file>`.

### 5. Verify each commit builds in isolation

```bash
for sha in $(git rev-list --reverse <base>..HEAD); do
  git checkout -q "$sha"
  <typecheck> >/dev/null 2>&1 && <lint> >/dev/null 2>&1 \
    && echo "PASS $sha" || echo "FAIL $sha"
done
git checkout -q <branch>
```

A `FAIL` names a symbol referenced before it's defined → move that file/hunk to an earlier commit (its earliest consumer) and rebuild from step 3. Re-verify. Typecheckers recompile cold on each checkout, so the sweep is slow — run it in the background.

### 6. Verify zero net change

```bash
git diff <ANCHOR> HEAD                        # MUST be empty
git rev-parse <ANCHOR>^{tree} HEAD^{tree}     # identical hashes = byte-for-byte proof
```

Also: final tip passes typecheck + lint, and no `fixup!`/`WIP` subjects remain.

### 7. Force-push — only after 5 and 6 pass

Hold for the user's explicit approval. Record the pre-push remote tip first, then:

```bash
git push --force-with-lease           # never --force; never to main
```

Re-verify the remote: `git fetch`, then `git diff <pre-push-remote> origin/<branch>` empty and tree hashes equal. The pre-push tip is recoverable via `origin/<branch>@{1}` in the reflog.

## Red flags — STOP

- You verified only the final tree and called it done → you skipped the invariant (step 5).
- Whole-file staging dragged a later concern early (e.g. a feature-flag gate's code landed in the upload commit) → it breaks isolation or defeats the separate commit. Split instead.
- A consumer commit sits before the commit that defines the symbol → reorder.
- `git diff <ANCHOR> HEAD` is non-empty → a hunk was lost or doubled. Do not push.
- About to re-stamp author dates without asking → surface the date decision first.

## Common mistakes

- **Reordering commits that share a file** without preserving hunk-apply order — apply earlier-concern hunks first, or contexts drift and patches conflict.
- **Splitting a generated/aggregate file** (schema dump) across commits — partial copies won't typecheck; put it whole in the foundation commit.
- **Hand-deleting transient churn** instead of rebuilding from the final tree, where it simply never appears.
