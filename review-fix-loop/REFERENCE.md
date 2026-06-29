# Review–Fix Loop — Reference

Depth for the loop in [SKILL.md](SKILL.md). Everything here is capability-based — adapt the mechanics to whatever fan-out and skill primitives your harness provides.

## Findings schema

Force every review agent to return this (or equivalent). A schema is the point: only findings — not transcripts — flow back to the orchestrator, so its context stays clean and dedup is mechanical.

```jsonc
{
  "lens": "string",                 // which lens produced this
  "summary": "string",              // 2-4 sentences; state plainly if the slice is clean
  "findings": [{
    "severity": "Critical|High|Medium|Low",
    "file": "string", "line": "string",   // file:line or range
    "title": "string",
    "rationale": "string",          // WHY it's a problem, with evidence read from the code
    "suggestedFix": "string",
    "evidenceRefs": ["string"],     // sibling/spec/identifier references that ground it
    "category": "correctness|security|symmetry|coverage|design-fidelity|nit"
  }]
}
```

Severity calibration: **Critical** = data-loss / security / will-break-in-prod. **High** = real bug, CI breaker, missing important coverage, genuine security gap. **Medium** = maintainability / edge case. **Low** = nit. Tag unsigned-off product/design choices `design-fidelity` and route them to the human (G4), never as High.

## Fan-out skeleton (illustrative — adapt to your harness)

```
phase('Review')
const results = await parallel(LENSES.map(lens => () =>
  agent(promptFor(lens), { schema: FINDINGS_SCHEMA, agentType: 'general-purpose' })
))
// agentType matters: dispatched agents must be able to load the lens's skills.
return results.filter(Boolean)
```

Before fan-out, **resolve each lens's capabilities to the actual skill names in your set** (you have the full skill list; a subagent may not) and bake them into `promptFor(lens)` as explicit "invoke `<name>`" steps — don't make the subagent re-match. Each `promptFor(lens)` then tells the agent to (1) invoke those named workflows, (2) read the real code and verify before reporting, (3) cite `file:line` + the established pattern it deviates from, (4) emit the schema. Then the orchestrator aggregates and writes `review-pass-N.md`.

Adversarial-verify pass (step 6): per surviving finding, dispatch ≥1 skeptic prompted to *refute* it (default to "not real" when unsure); keep only findings that survive. Add one fresh full-diff agent for what the fixes introduced.

## Lens taxonomy

- **Correctness / security** — logic, auth/permission boundaries, injection, data-loss, migration reversibility. Compare any self-secured/permission code to its established analog.
- **Logic / data** — pure-function correctness, state & concurrency (cancellation, re-entry, races), cache/consistency, error/degrade paths.
- **UI** — design-system tokens vs hardcoded values, responsive behavior, accessibility, loading/empty states, copy.
- **Tests** — coverage of the risky/new branches vs the test plan, flakiness, fixture/selector reuse, false-greens (a test that passes even when the code is wrong).
- **Symmetry (G2)** — every new unit vs its closest existing sibling: naming/suffix conventions, file location, structure, error handling, test-title style. Unexplained divergence is a finding. This lens is what a correctness review misses.

## Commit & verify mechanics

- One commit per fix; never amend; never push without explicit approval.
- Parallel fixers run **edit-only on disjoint files**; the orchestrator stages exact paths and commits each fix. Do small, fully-understood fixes inline rather than dispatching.
- Per-fix gate: typecheck the changed code. After all fixes: full typecheck + lint + the relevant test suites, green, with the output shown.
- A fix that's a bug → drive it through a systematic-debugging workflow (root cause before patch). A fix that's missing coverage → test-first.

## Failure-mode catalog

| Failure | Symptom | Guard |
|---|---|---|
| Critical-only gate | real Highs ship; "0 Critical → done" while CI breaks | **G1**: gate on Critical *and* High |
| Symmetry blindness | new unit diverges from siblings (naming, location); caught only post-merge | **G2**: dedicated symmetry lens + push the rule into design-time workflows |
| False-positive findings | a confident but wrong finding drives a needless/harmful change | **G3**: reproduce/trace before acting; disproven → no change |
| Wrong target / product miss | loop "passes" but the behavior is still wrong, or it's a UX call | **G4**: hand product-UX + live-visual judgment to the human |
| Commit races | parallel fixers corrupt the index / interleave commits | **G5**: disjoint files, edit-only, orchestrator serializes |
| Agents can't load skills | reviews are shallow, miss project conventions | dispatch with a general-purpose agent type; pass exact capability names in the prompt |
| Polling waste | burning turns checking on background work | act on completion notifications; don't poll |
| Over-firing | a multi-agent loop on a trivial diff | the scope guard — single-pass review for small changes |
| Unbounded looping | re-litigating subjective Mediums forever | cap passes (~3); stop when no Critical/High; subjective items → human |
