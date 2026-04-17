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
- [ ] Instrument with tagged debug logging
- [ ] Apply binary chop if cause is obscure
- [ ] Fix root cause with one atomic change
- [ ] Confirm failing test now passes
- [ ] Run full test suite for regressions
- [ ] Clean up all debug instrumentation
- [ ] Document 5 Whys analysis
```

### 1. Isolate

Write a failing test first. This proves you understand the trigger conditions and creates a regression baseline.

### 2. Diagnose

- Read surrounding code before touching anything.
- Scientific method: gather data → hypothesis → test. The hypothesis must explain all observed behaviors.
- Binary chop: bisect commit history, comment out code blocks, reduce input data.
- Usual suspects: recent changes, historically problematic modules, environment differences, race conditions.

### 3. Instrument

Add targeted debug logging before guessing at fixes. Good instrumentation proves or disproves hypotheses with evidence.

#### Logging rules

- **Tag every log line** with a hypothesis ID: `[DEBUG H1]`, `[DEBUG H2]`. This maps output back to specific theories.
- **Wrap debug code in region markers** so it can be found and removed reliably:
  ```python
  # region DEBUG — H1: classify_bird input shape mismatch
  print(f"[DEBUG H1] pixel_values shape: {inputs['pixel_values'].shape}")
  # endregion DEBUG
  ```
  Use language-appropriate markers: `// #region DEBUG` (JS/TS), `# region DEBUG` (Python), `/* region DEBUG */` (C/Java).
- **Log at decision points**, not everywhere. Focus on: function entry/exit with key args, conditional branches taken, values just before the failure site.
- **Log to a dedicated file** when possible (`{project_root}/.claude/debug.log`), not just stdout. This keeps terminal clean and output searchable. Fall back to stdout for environments where file logging is impractical.
- **Clear logs before each reproduction cycle** to avoid stale output confusion.
- **Include types and shapes**, not just values. A `None` where you expected a dict, or a `(3, 224, 224)` where you expected `(1, 3, 224, 224)`, reveals the bug instantly.

#### Anti-patterns

- Scattershot `print("here")` with no context.
- Logging inside tight loops (thousands of lines obscure the signal).
- Leaving debug logging in production code. Always clean up after diagnosis.

### 4. Fix

- Root cause, not symptom. No band-aids, no exception masking.
- One small, atomic change. If it doesn't work, revert immediately.
- Do not refactor during debugging.

### 5. Verify and learn

Confirm the test passes, run the full suite, then provide a 5 Whys analysis.

**Red flags to watch for:** If you catch yourself thinking "quick fix for now" or "I don't fully understand but this seems to work" — stop and return to step 2. After 3+ failed fix attempts, reassess whether you've correctly identified the root cause.

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
- **Error boundary hardening** — wrap risky calls in try/except to prevent cascading failures that mask the real error (but revert to strict after diagnosis)
