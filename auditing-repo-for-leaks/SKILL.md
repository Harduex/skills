---
name: auditing-repo-for-leaks
description: Audits a git repo's commit history — all of it, or only the commits not yet pushed — for anything that makes it unsafe to publish — leaked secrets/credentials, PII, work identity, machine-local paths, private notes, and accidentally-committed DB dumps, key material, logs, archives, or files the repo's own .gitignore excludes. Produces a safe-to-publish / not verdict that says where each finding is, never what it contains. Use before pushing to a public remote, when asked whether a repo is safe to open-source or make public, to check history for leaked secrets or sensitive data before publishing, or to audit a repo for leaks. This is a leakage audit, NOT a vulnerability scan of the code — for exploitable code flaws use the code-review or verification skill instead.
---

# Repo Leak Audit

Answers one question: **is this repo's history safe to be public?** It sweeps the
commits about to be published (or every commit) for disclosed sensitive data, then
gives a verdict. It does not judge whether the code is exploitable — that is a
different skill.

## Show where, never what

Report every finding by its location — commit, file, line, gitleaks fingerprint —
and by its kind (`github-pat`, "email address", "looks like personal notes"). Never
open a flagged file, print a matched value, or quote one in the report. The user
opens the file and judges. The scan output already follows this rule; keep it in
every command you run and every line you write.

| If you think | Do this instead |
|---|---|
| "I should confirm the key is real before calling it a blocker" | It stays a blocker. Give its location; the user says whether it is fake. |
| "I'll read the committed files to catch what the scanner missed" | Read file names and commit messages only (step 2). |
| "The value looks fake / harmless, I'll say so" | Say nothing about the value. Give its location and kind. |

## Process

```
Audit checklist:
- [ ] Pick the commits: --unpushed before a push, every commit before going public
- [ ] Run the sweep script; confirm the self-test PASSED (else the clean result is meaningless)
- [ ] Read the file names and commit messages of the same commits
- [ ] Triage findings: hard blockers vs advisories
- [ ] Write the verdict + remediation note
```

### 1. Run the sweep

```
bash scripts/scan-history.sh [--unpushed] [repo-dir]
```

Use `--unpushed` before a push: it scans only commits that are on no remote, so
findings that are already published and already judged do not come back. A repo
with no remote has every commit unpushed, so its first scan is always full. Run
without the flag to decide whether a repo can go public.

It locates or fetches `gitleaks`, **self-tests it against a planted key** (a clean
result is only trustworthy if the scanner demonstrably fires on a known secret —
never skip this), prints how many commits it scanned, then runs eight passes, each
printing locations only: secrets, machine-local paths, private keys, DB/dump/env/key
files, logs and archives, commit-author identities, other emails in file contents,
and committed files the repo's own `.gitignore` excludes. Exit `0` clean, `1` hard
findings, `2` self-test failed (untrusted).

### 2. Read the names and messages

For the same commits (`<range>` is `--all --not --remotes` with `--unpushed`, else
`--all`):

```
git log <range> --name-only --format= | sort -u     # every file the commits touched
git log <range> --format='%h %s%n%b'                # every commit message
```

List anything whose name or message suggests it is private or meant for this
machine only — personal notes, notes about another project, scratch or export
files, local state or settings — as an advisory: its location and a few words on
why. Do not open it.

### 3. Triage what it finds

- **Hard blockers** (must fix before publishing): secrets/tokens/passwords, any
  `BEGIN … PRIVATE KEY`, committed `.env`/DB dumps/keystores. They stay blockers
  until the user says otherwise — never downgrade one because it looks fake.
- **Advisories** (list them; the user decides): logs and archives, committed files
  the repo's `.gitignore` excludes, the suspects from step 2, emails in file
  contents, machine-local paths like `/home/<user>/…` (leaks a username already
  implied by the repo owner), and the commit **author email** — it is in every
  commit by design; flag it only if it's a *work* address the author didn't mean
  to expose.
- **A secret the user says is fake:** append its `Fingerprint:` line from the scan
  output to `.gitleaksignore` at the repo root and commit that file once the user
  agrees. gitleaks skips the finding from then on, on every machine. The file holds
  the location, never the secret.

### 4. Report

```
# Repo Exposure Audit — <repo> @ <commit>

Scanner self-test: PASS/FAIL   Commits scanned: <n> (all | unpushed)

## Verdict: SAFE TO PUBLISH | NOT YET
## Hard findings   (Fn — blocker: kind, commit/file/line)
## Advisories      (An — kind, commit/file, why it may matter)
## Clean           (what was checked and came back empty)
```

Tag each finding with a stable id (`F1`, `A1`) so it can be referenced in follow-up.

## Remediation — and when NOT to rewrite

If a hard finding exists, the fix is to purge it from history (`git filter-repo
--replace-text`, then force-push) **and rotate the exposed credential** — rotation is
the part that actually protects you.

Rewriting public history has sharp caveats — weigh them before proposing it:

- **A rewrite does not un-publish.** Once a repo is public, old commits are already
  cloned, cached by SHA, and possibly forked/archived. Rewriting cleans the canonical
  history, not every copy. For an already-leaked *secret*, **rotation is mandatory**;
  the rewrite is cosmetic cleanup on top.
- **Tags and releases hold their own copy.** Force-pushing `main` does not move release
  tags — they still point at the original commits, so the leaked data survives there.
  Fully purging means rewriting the tags too, which **re-points every release tag to a
  commit its binaries were never built from** (broken provenance) and, because pushing
  an existing tag is a ref *update*, **re-triggers the release CI for every tag** (a
  wall of failed runs if the workflow does `gh release create` on an existing release).
- **So for a low-value, already-public disclosure** (e.g. a local path, a username the
  owner already reveals), the honest recommendation is often **leave it** — the rewrite's
  disruption outweighs scrubbing a cosmetic string. Reserve rewrites for genuine secrets,
  and pair them with rotation.

Always take a full backup first (`git clone --mirror`) and confirm the tree is
byte-identical afterward except for the intended change.
