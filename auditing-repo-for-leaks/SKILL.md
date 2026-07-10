---
name: auditing-repo-for-leaks
description: Audits a git repo's full commit history for anything that makes it unsafe to publish — leaked secrets/credentials, PII, work identity, machine-local paths, and accidentally-committed binaries, DB dumps, or key material. Produces a safe-to-publish / not verdict with per-finding severity. Use when asked whether a repo is safe to open-source or make public, to check history for leaked secrets or sensitive data before publishing, or to audit a repo for leaks. This is a leakage audit, NOT a vulnerability scan of the code — for exploitable code flaws use the code-review or verification skill instead.
---

# Repo Leak Audit

Answers one question: **is this repo's history safe to be public?** It sweeps every
commit (not just the current tree) for disclosed sensitive data, then gives a verdict.
It does not judge whether the code is exploitable — that is a different skill.

## Process

```
Audit checklist:
- [ ] Run the sweep script over the full history
- [ ] Confirm the scanner self-test PASSED (else the clean result is meaningless)
- [ ] Triage findings: hard blockers vs cosmetic advisories
- [ ] Write the verdict + remediation note
```

### 1. Run the sweep

```
scripts/scan-history.sh [repo-dir]
```

It locates or fetches `gitleaks`, **self-tests it against a planted key** (a clean
result is only trustworthy if the scanner demonstrably fires on a known secret —
never skip this), then reports six passes over `git rev-list --all`: secrets,
machine-local paths, private keys, committed binaries/dumps/env files, commit-author
identities, and other emails in file contents. Exit `0` clean, `1` hard findings,
`2` self-test failed (untrusted).

### 2. Triage what it finds

Judgment the script can't make — decide per finding:

- **Hard blockers** (must fix before publishing): live secrets/tokens/passwords, any
  `BEGIN … PRIVATE KEY`, committed `.env`/DB dumps/keystores, real customer or
  personal PII.
- **Cosmetic advisories** (usually fine, mention them): machine-local paths like
  `/home/<user>/…` (leaks a username already implied by the repo owner), the commit
  **author email** — it is in every commit by design; flag only if it's a *work*
  address the author didn't mean to expose.
- **Verify, don't assume:** confirm a flagged string is a real secret (a live key, not
  a placeholder/test fixture) before calling it a blocker.

### 3. Report

```
# Repo Exposure Audit — <repo> @ <commit>

Scanner self-test: PASS/FAIL   Commits scanned: <n>

## Verdict: SAFE TO PUBLISH | NOT YET
## Hard findings   (Fn — blocker: what, which commit/file)
## Advisories      (An — cosmetic: what, why it's acceptable)
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
