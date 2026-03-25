---
name: debugging
description: Systematically diagnoses and resolves software defects using isolation, binary chop, and root cause analysis. Writes failing tests first, then applies the scientific method. Use when investigating bugs, diagnosing errors, tracing unexpected behavior, or resolving test failures.
---

# Scientific Debugging

## Process

```
Debugging checklist:
- [ ] Write a failing test that reproduces the defect
- [ ] Read surrounding code before changing anything
- [ ] Form hypothesis — verify it explains ALL observed behavior
- [ ] Apply binary chop if cause is obscure
- [ ] Fix root cause with one atomic change
- [ ] Confirm failing test now passes
- [ ] Run full test suite for regressions
- [ ] Document 5 Whys analysis
```

### 1. Isolate

Write a failing test first. This proves you understand the trigger conditions and creates a regression baseline.

### 2. Diagnose

- Read surrounding code before touching anything.
- Scientific method: gather data → hypothesis → test. The hypothesis must explain all observed behaviors.
- Binary chop: bisect commit history, comment out code blocks, reduce input data.
- Usual suspects: recent changes, historically problematic modules, environment differences, race conditions.

### 3. Fix

- Root cause, not symptom. No band-aids, no exception masking.
- One small, atomic change. If it doesn't work, revert immediately.
- Do not refactor during debugging.

### 4. Verify and learn

Confirm the test passes, run the full suite, then provide a 5 Whys analysis.

## Example: 5 Whys

```
Bug: Users see "500 Internal Server Error" on profile page

1. Why? — ProfileController throws NullPointerException at line 42
2. Why? — user.getAddress() returns null for users without addresses
3. Why? — Address field added as required but migration didn't backfill
4. Why? — Migration script only runs on new records
5. Why? — No backfill policy exists for schema migrations

Root cause: Missing backfill policy for schema changes
Fix: Backfill null addresses + add nullable check in controller
Prevention: Add "backfill existing data" to migration checklist
```

## Diagnostic tools

- **Logs and traces** — for timing, concurrency, and distributed issues
- **git bisect** — find the exact commit that introduced a regression
- **Strategic debug output** — temporary logging at decision points, remove after diagnosis
