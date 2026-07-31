---
name: verify-before-done
description: Use before claiming any implementation is done, fixed, complete, or passing — and before committing or handing work over for testing. Green typecheck/lint is not verification; the changed behavior must be exercised and the evidence shown.
---

# Verify Before Done

A change is "done" only when you have watched it work. Static gates (typecheck, lint, even a green unrelated test run) prove the code compiles — not that the feature behaves.

## The gate

Before saying done / fixed / implemented / passing, or committing a nontrivial change:

1. **Run the affected tests** — the specs that cover the changed behavior, not just the suite that happened to be open. If none cover it, say so.
2. **Exercise the changed behavior itself** — drive the real flow, not a proxy:
   - UI → your project's browser-driving skill (navigate, click, observe the actual result)
   - API/backend → the real request (curl, spec, or console) against a running stack
   - CLI/script → run the real command on real input
3. **Show the evidence** — paste the test output, the observed behavior, the response body. A claim without its evidence is a hypothesis.

## Where the evidence goes

Default to **chat prose with stable IDs** (`TC-3`, `F2`) so the human can answer "about F2…".
That is the form they actually engage with.

- **A file only when it has a reader who is not in this conversation** — an MR body, a ticket, a handoff — or when they asked for a file. Verification reports written for the person you're talking to get deleted; don't produce them by reflex.
- **User-visible behavior that prose can't settle** → offer to film it, via your set's verification-filming workflow if it has one. A film replaces the written report and its screenshots; never both.
- Keep any such artifact untracked unless asked, and if it vanishes mid-session assume the human removed it — say so in one line, don't recreate it, don't investigate your tooling.

## If you cannot verify

Say so explicitly: "implemented, NOT verified — needs X" beats a false "done". Never let a handoff imply verification that didn't happen; the human testing your unverified work is the failure mode this skill exists to prevent.

## Claims about cause

"X broke because Y" and "this fix resolves it" need the same bar: reproduce the failure, apply the change, observe the failure gone. Correlation with your last edit is not causation — environment flakiness confounds it.
