---
name: distribute-fixups
description: Distributes uncommitted working-tree changes back to their originating commits on a multi-commit branch using git commit --fixup and a non-interactive autosquash rebase. Use when the user wants to "distribute" fixes into existing commits, clean up a branch after review feedback, fold review fixups into the right commits, or mentions fixup/autosquash workflows.
---

# Distribute Fixups

Folds uncommitted changes back into the commits that introduced the code they modify. The end state: each logical commit on the branch carries its own fixes, no trailing "review fixes" or "address feedback" commits, and the final tree matches what you had before the rebase.

## Preconditions

- [ ] Branch has more than one commit ahead of base (single-commit branches do not need this — just amend)
- [ ] Working tree has changes to distribute (staged or unstaged)
- [ ] Branch is not already pushed *to a shared remote that others rebuild from* — if it is, confirm with the user before rewriting history
- [ ] Repo allows non-interactive rebase via `GIT_SEQUENCE_EDITOR=true` (non-interactive convention — never run `git rebase -i` with a real editor)

## Source of changes

Before step 1, confirm with the user which mode applies. **Do not guess.**

- **Mode A — uncommitted changes**: Working tree already has the diff to distribute. Proceed to step 1 as-is.
- **Mode B — trailing FIX/WIP commits**: User points at one or more trailing commits (e.g. `FIX review feedback`) whose contents should be redistributed into earlier commits. Unwind them into the working tree first:

  ```bash
  git reset --mixed HEAD~<N>   # N = number of trailing commits to redistribute
  ```

  The unwound commit messages are discarded — the changes are being absorbed into other commits anyway. Then proceed to step 1.

If the commits to redistribute are **buried in the middle** of the branch (not at the tip), the safe path is interactive and beyond the scope of this skill — flag it to the user instead of improvising.

## Workflow

### 1. Map the branch

```bash
git log --oneline <base>..HEAD              # see commits to distribute into
git status                                  # see uncommitted changes
git rev-parse HEAD                          # SAVE THIS — used for verification in step 5
```

Record the pre-rebase HEAD sha. You will diff against it at the end.

### 2. Attribute each change to an originating commit

For each modified file (or each hunk if the file spans multiple commits), find the commit that introduced the code being changed:

```bash
git blame -L <start>,<end> <file>           # narrow to the touched lines
git log --oneline <base>..HEAD -- <file>    # all commits on this branch touching the file
```

Pick the commit whose intent the fix belongs to — usually the commit that introduced the code being patched, not just the last commit that touched the line.

### 3. Stage and fixup-commit, one originating commit at a time

For each originating commit `<sha>`:

```bash
git add <files-or-paths-for-this-commit>
git commit --fixup=<sha>
```

If a single file has hunks belonging to **different** originating commits, split them with `git add -p` (only acceptable interactive use here — there is no non-interactive equivalent that selects hunks). If `-p` is not allowed in your environment, stash, restore one hunk at a time via patch, and commit between each.

Repeat until the working tree is clean.

### 4. Autosquash non-interactively

```bash
GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash <base>
```

`GIT_SEQUENCE_EDITOR=true` exits the sequence editor immediately, accepting the autosquash-ordered todo list as-is. No interactive prompt.

The `-i` is required: on git < 2.44, `--autosquash` without `-i` is silently ignored — the rebase "succeeds" but the `fixup!` commit is replayed as a normal commit at the tip. With `GIT_SEQUENCE_EDITOR=true`, `-i` never actually prompts.

On conflict: resolve in favor of the **consistent end state** the branch is supposed to reach, not whichever side feels safer. `git add` resolved files, `git rebase --continue`. Do not abort unless you are recovering, not navigating.

### 5. Verify tree integrity

The whole point of distribute-fixups is that **only history changed, not the working tree**. Confirm:

```bash
git diff <pre-rebase-sha> HEAD              # MUST be empty
git log --oneline <base>..HEAD              # should show no fixup! commits remain
```

If `git diff` is non-empty, something was lost or doubled during the rebase. Investigate before pushing — do NOT force-push a tree that differs from the pre-rebase state without understanding why.

## Force-push

Only force-push after step 5 passes. Use `--force-with-lease`, never `--force`:

```bash
git push --force-with-lease
```

Never force-push to `main`. Warn the user if they ask for it on a shared branch.

## Red flags

- `git diff <pre-rebase-sha> HEAD` is non-empty → STOP. History is wrong.
- `fixup!` commits remain after rebase → autosquash didn't run; check the rebase actually used `--autosquash` and the fixup target shas are in range.
- Repeated conflicts on the same hunk across multiple fixups → the fixups are out of order or one of them belongs to a different originating commit. Reorder via the targets, not by editing the rebase todo.

## When NOT to use this

- Single-commit branches → just `git commit --amend`.
- Changes that are genuinely new work, not fixes to existing commits → make a new commit, don't force-fit it into an unrelated one.
- Branches already merged or in code review where rewriting history confuses reviewers → coordinate first.
