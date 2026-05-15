---
name: debugger
description: Systematically diagnoses and resolves software defects through reliable reproduction, the scientific method, evidence-based instrumentation, and root-cause analysis. Use when investigating bugs, diagnosing errors, tracing unexpected behavior, or resolving test failures.
---

# Scientific Debugging

## Checklist

### Reproduction phase

- [ ] Get a reliable reproduction: prefer a failing test; otherwise write a manual recipe
- [ ] If the bug is intermittent, capture logs/traces/timestamps and narrow the triggering conditions before changing code

### Diagnosis phase

- [ ] Read surrounding code before changing anything
- [ ] Verify assumptions; compare working vs broken scenarios
- [ ] Form hypothesis — must explain ALL observed behavior
- [ ] Instrument with tagged logging (one tag per hypothesis)
- [ ] Apply binary chop or stack-trace techniques if cause is obscure

### Fix phase

- [ ] Fix root cause with one atomic change

### Verification phase

- [ ] Confirm repro no longer triggers; run full suite for regressions
- [ ] Remove all debug instrumentation (grep "region DEBUG")
- [ ] Document 5 Whys

## Protocol

Do not skip steps.

### 1. Reproduce

Get a reliable reproduction before changing anything — you can trigger the failure on demand, repeatedly, with the same inputs. Without this, you cannot prove the bug is fixed; you can only believe you fixed it.

Form depends on the bug:

- **Automated test (default)** when the code has test infrastructure and the test cost is proportionate to the fix. Prefer this path whenever it gives practical regression coverage, even for timing-sensitive bugs.
- **Manual recipe** (clicks / curl / command sequence) when the bug is primarily visual or environment-dependent, when the existing harness cannot exercise it reliably, or when building a stable test would cost more than the fix. Document the recipe in the PR.

If both options seem plausible, choose the automated test unless the test would be flaky, misleading, or disproportionately expensive. If neither is reliable yet, first make the bug observable: capture logs, traces, and environment differences until you can repeat the failure or at least narrow it to a smaller intermittent scenario.

### 2. Diagnose

- **Read the surrounding code first.** No tweak-and-pray.
- **Scientific method**: gather data → hypothesis → test. The hypothesis must explain ALL observed behavior, not just a subset.
- **Binary chop**: bisect commits, comment out blocks, reduce input data.
- **Usual suspects**: recently modified code, environment differences, race conditions.
- **Verify assumptions before dismissing a cause.** When ruling out a suspect ("it can't be X because Y"), confirm Y actually holds in the live repro environment. Bugs often live in the gap between assumed and actual conditions — adjacent "latent" issues or dead code paths that the real test scenario exercises.
- **Compare working vs broken.** If the bug has a natural A/B (works in case A, breaks in case B; user X not Y; dev not prod), diff the code paths and state between them. The differences are your suspects. Faster than reasoning forward from first principles.

### 3. Instrument

Add targeted logging **before** guessing at fixes. Evidence beats theory when the cause is non-obvious — empirical attribution is faster than reasoning.

Logging rules:

- **Tag every line with a hypothesis ID** — `[DEBUG H1]`, `[DEBUG H2]`, … — so output maps back to specific theories and you can A/B multiple hypotheses per repro.
- **Wrap debug code in region markers** so cleanup is a single grep:
    ```python
    # region DEBUG — H1: input shape mismatch
    print(f"[DEBUG H1] pixel_values shape: {inputs['pixel_values'].shape}")
    # endregion DEBUG
    ```
    Use language-appropriate fold syntax (`//`, `#`, `/* */`).
- **Log values, types, and shapes** — not breadcrumbs. A `None` where a dict was expected, or `(3,224,224)` where `(1,3,224,224)` was expected, reveals the bug instantly.
- **Log at boundaries** — input AND output of each suspect transformation — so you pinpoint *which step* produces the bad value.
- **Identify the caller.** When a shared function is called from many places and you don't know which, log a stack trace (`new Error().stack`, `console.trace()`, `traceback.format_stack()`) inside it. One repro lists every call site and ordering.
- **Add timestamps for async / order-dependent bugs.** Print order ≠ execution order.
- **Log to a file** (e.g. `.claude/debug.log`) when practical — keeps the terminal clean and the output diffable across runs.
- **Clear logs before each repro cycle** to avoid stale-output confusion.
- **Don't log inside tight loops.** Thousands of lines drown the signal.

### 4. Fix

- Fix the root cause, not the symptom. No band-aids, no exception masking, no workarounds.
- Make exactly one atomic change. If it doesn't work, revert immediately.
- Do not refactor during debugging.

### 5. Verify and learn

- Confirm the repro no longer triggers the bug.
- Run the relevant test suite for regressions.
- Remove all debug instrumentation (`grep "region DEBUG"`).
- Provide a **5 Whys** analysis — drill from symptom to root cause to prevention. Why did this bug exist? What allowed it to reach production? How are similar bugs prevented?

## Red flags

If you catch yourself thinking any of these, **return to Step 2**:

- "Quick fix for now, investigate later."
- "I don't fully understand but this seems to work."
- "Let me try changing X and see what happens."
- "It's probably X, let me fix that." (without evidence)

**After 3+ failed fix attempts, reassess the root cause.** Each fix revealing a new problem in a different place usually signals an architectural mismatch, not a hypothesis problem. Stop and reconsider fundamentals.

## Diagnostic tools

- **git bisect** — find the commit that introduced a regression.
- **Stack-trace the setter** (shared-state clobber bugs): when global/context state mysteriously flips and reading the code doesn't reveal the writer, wrap the setter to capture a stack trace per call. One repro lists every writer and their order. Reach for this **before** extended theoretical analysis when the writer is non-obvious.
- **Error boundary hardening** — temporarily wrap risky calls in try/except (or equivalent) to prevent cascading failures that mask the real upstream error. Revert to strict handling after diagnosis.

## Constraints

- Never refactor during debugging — minimal, surgical fix only.
- No change-marker comments. No `// fix applied` breadcrumbs.
- If the root cause is architectural, propose the fix separately. Don't combine debugging with redesign.
