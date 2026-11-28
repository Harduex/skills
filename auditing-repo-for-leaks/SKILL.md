---
name: auditing-repo-for-leaks
description: Audits a git repo's commit history — all of it, or only the commits not yet pushed — for anything that makes it unsafe to publish — leaked secrets/credentials, PII, work identity, machine-local paths, private notes, and accidentally-committed DB dumps, key material, logs, archives, or files the repo's own .gitignore excludes. Reports findings and inspected coverage without exposing matched values. Use before committing or pushing, when asked whether a repo is safe to open-source or make public, to check history for leaked secrets or sensitive data before publishing, or to audit a repo for leaks. This is a leakage audit, NOT a vulnerability scan of the code — for exploitable code flaws use the code-review or verification skill instead.
---

# Repo Leak Audit

Answers one question: **is this repo's history safe to be public?** It sweeps the
commits about to be published (or every commit) for disclosed sensitive data, then
reports findings and inspection limits, not a guarantee of safety. Exploitability
review is a different skill.

## Show where, never what

Report every finding by its location — commit, file, line, gitleaks fingerprint —
and by its kind (`github-pat`, "email address", "possible note data"). Keep matched
values out of reports and logs. Respect the user's privacy boundary: inspect only
authorized context, without dumping payloads; otherwise request owner review.
A match establishes neither a real credential nor current validity.

| If you think | Do this instead |
|---|---|
| "A password match proves a live credential" | Report an unresolved candidate; inspect authorized context or ask the owner. |
| "A fixture path proves it is harmless" | A path is only a clue; confirm the content/provenance within the permitted scope. |
| "The owner already confirmed this example" | Reuse that decision; no security remediation or visibility change is needed. |

## Process

```
Audit checklist:
- [ ] Pick the scope: staged index before a commit; --unpushed or all local refs for history
- [ ] Run the sweep script; confirm the self-test PASSED (else the clean result is meaningless)
- [ ] Read the file names and commit messages of the same commits
- [ ] Triage: confirmed leaks, unresolved candidates, false positives, advisories
- [ ] Report inspected refs/range, commit count, skipped content, and findings
```

### 1. Run the sweep

```
bash scripts/scan-history.sh [--unpushed] [repo-dir]
```

For a **local pre-commit audit**, use an available Gitleaks executable (including
its cache path) to scan the staged index. Missing tools/errors mean INCOMPLETE:

```
gitleaks git --staged --redact=100 --report-format json --report-path <private-report.json> <repo-dir>
```

Keep the raw report outside the repository; show only safe finding fields. This
checks what would be committed, not unstaged/untracked files. `--unpushed` below
checks already-created local commits; it does not replace the staged check.

Use `--unpushed` before a push: it scans only commits that are on no remote, so
findings that are already published and already judged do not come back. A repo
with no remote has every commit unpushed, so its first scan is always full. Run
without the flag to inspect all history reachable from local refs.

It locates or fetches `gitleaks`, **checks synthetic positive and negative controls** (a clean
result is only trustworthy if the scanner demonstrably fires on a known secret —
never skip this), prints how many commits it scanned, then runs eight passes, each
printing locations only: secrets, machine-local paths, private keys, DB/dump/env/key
files, logs and archives, commit-author identities, other emails in file contents,
and committed files the repo's own `.gitignore` excludes. Exit `0` means no
candidates in scope, `1` means review required, and
`2` means incomplete/untrusted. Missing tools, failed controls, scanner errors or
failed history passes must never be reported as clean.

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
why. Content inspection still requires authorization.

### 3. Triage what it finds

- **Confirmed leaks:** evidence establishes actual private data or a credential
  that granted access. State exposure and current validity separately.
- **Unresolved candidates:** scanner matches and `.env`/DB/key filenames need
  authorized context or owner review. Do not infer live access or prescribe
  rotation, rewriting, or privatization from the match alone. Never test a
  credential against a service without explicit authorization.
- **Advisories** (list them; the user decides): logs and archives, committed files
  the repo's `.gitignore` excludes, the suspects from step 2, emails in file
  contents, machine-local paths like `/home/<user>/…` (leaks a username already
  implied by the repo owner), and the commit **author email** — it is in every
  commit by design; flag it only if it's a *work* address the author didn't mean
  to expose.
- **Confirmed false positives:** owner-confirmed nonfunctional examples/fixtures
  and keys documented as public by design need no security remediation. Reuse
  that decision. With approval, record the Gitleaks `Fingerprint:` in the existing
  `.gitleaksignore`; do not suppress a whole fixture directory or credential rule.

### 4. Report

```
# Repo Exposure Audit — <repo> @ <commit>

Scanner controls: PASS/FAIL   Scan completion: COMPLETE/INCOMPLETE
Scope: <local refs/range or staged index; commit count when applicable>
Not inspected: <skipped/inaccessible content and hosted surfaces>

## Result: NO FINDINGS IN INSPECTED SCOPE | REVIEW REQUIRED | INCOMPLETE
## Findings / candidates (Fn — kind, safe location, evidence and disposition)
## Advisories      (An — kind, commit/file, why it may matter)
## Clean           (what was checked and came back empty)
```

No findings is a bounded result. History scans do not inspect unstaged/untracked
local content, remote-only history, hosted caches/artifacts, or binary/media and
archive payloads. Report additional authorized checks separately.

Tag each finding with a stable id (`F1`, `A1`) so it can be referenced in follow-up.

## Calling workflows

Return findings to the calling workflow's decision process. Its delegated reviewer
may assess authorized evidence and record provisional decisions. The reviewer cannot
invent owner confirmation or expand inspection permissions. Unresolved findings and
incomplete scans do not pass the audit gate. Independent local work may continue.
Carry the audit result and pending decisions into the human handoff. A clean audit
never authorizes publication.

## Remediation — and when NOT to rewrite

For confirmed exposed credentials that remain usable or were reused, rotate or
revoke first. Choose history cleanup according to actual exposure and owner intent;
it is not automatic. Rewrites, pushes, and visibility changes require authorization.

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
