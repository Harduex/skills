---
name: review-fix-loop
description: Orchestrates a multi-pass, multi-agent review→fix→verify loop over a branch, diff, or feature — parallel lens reviews produce severity-tagged findings, the most serious are fixed (one commit each), the work is re-verified, and the loop repeats until clean. Use when asked to thoroughly review and fix a branch/PR/feature with subagents, run a review loop, do an exhaustive or adversarial audit-with-fixes, or harden a change before merge. Composes your set's review, verification, debugging, and domain workflows by capability per phase instead of duplicating them.
---

# Review–Fix Loop

A loop that **finds, fixes, and re-verifies** — not a single-pass review. It *orchestrates* other workflows; it never re-implements them.

**Link by capability, not by name.** Each phase below names a *capability* ("a code-review workflow", "a verification workflow"). Invoke whatever skill in your current set provides that capability — discover it from the available skill descriptions at runtime. Skill names drift between projects and over time; capabilities don't. If your set lacks one, do that step directly.

**Bind capabilities → skills at the orchestrator, then pass names down.** A capability phrase does not self-fire: the agent must match it to an installed skill's *description* and invoke that skill **by its real name**. Do this resolution once, up front, where you (the orchestrator) can see the full skill list — then bake the concrete name into each dispatched agent's prompt as an explicit "invoke `<name>` first" step. A subagent can silently skip a vague "use a review workflow"; it won't skip a named instruction. If no installed skill matches a capability, do that step inline.

## When to use

Substantial branches, features, audits, or pre-merge hardening — where one reviewer or one pass isn't enough. **Not** trivial diffs. Scale lens count and verify-votes to diff size. Needs a way to run subagents in parallel (a workflow / parallel-dispatch tool; sequential agents are the fallback).

## One pass

1. **Scope** — get the diff (`git diff <base>...HEAD`); enumerate the changed surfaces (backend, data, UI, tests, infra).
2. **Review — parallel, lens-split.** Dispatch one agent per lens. Each agent **invokes the review/domain workflows relevant to its lens** and returns **structured, severity-tagged findings** (a schema — so only findings, not transcripts, return to you). Lenses: *correctness/security · logic/data · UI · tests · **symmetry with existing patterns*** (G2).
3. **Aggregate** — dedupe across lenses; write `review-pass-N.md` (stable IDs, severity, `file:line`). **Verify every finding against the code yourself before accepting it** (G3).
4. **Fix** — resolve Critical + High + clear high-value items. **One commit per fix, never amend** (G5). Parallel fixers edit *disjoint* files (no git); you serialize the commits. Do small surgical fixes inline.
5. **Verify** — typecheck + lint + tests green via your verification workflow; report evidence, not claims.
6. **Adversarially verify the fixes** — a skeptic pass over the fix diffs (each verifier tries to *refute*), plus one fresh full-diff sweep for anything the fixes introduced or earlier passes missed.
7. **Gate** — continue iff any **Critical OR genuine new/unresolved High** remains; else write `review-final-report.md` and **stop**. Cap at ~3 passes.

## Non-obvious policy (why this loop, not a naive one)

- **G1 — Gate on Critical *and* High.** Critical-only ships real bugs; a careful feature may never hit "Critical" yet still have shipping-blockers (CI breakers, concurrency bugs).
- **G2 — Symmetry is a first-class lens.** "Does each new unit match its closest existing sibling — naming, location, structure?" A general correctness review reliably *misses* this; give it a dedicated agent.
- **G3 — Verify findings before acting.** Agents emit confident false positives. Reproduce/trace each before fixing; a disproven finding produces **no** change.
- **G4 — Know what the loop misses → hand to the human.** Product/UX judgment ("should this even appear?") and live visual behavior are not reliably caught by code review. Surface them as decisions; don't loop on them.
- **G5 — Serialize commits.** Parallel agents can't race the index. One commit per fix; disjoint files; the orchestrator commits.

## Capabilities by phase

Match each to a skill in your set by its description; if absent, do it directly.

| Phase | Capability to invoke |
|---|---|
| Review lenses | code review; security review; correctness/formal verification; **plus your domain reviewers** for each surface (data layer, UI, schema, tests) |
| Fan-out | parallel subagent dispatch / workflow orchestration |
| Fix | systematic debugging (for bugs); test-first authoring (for coverage); the domain workflow for the area being changed |
| Verify | verify-before-claiming-done (run the gates; evidence over assertions) |
| Prevent recurrence | feed recurring findings back into your design-spec, architecture, and test-planning workflows so the next change starts symmetric |

## Efficiency

Structured-output schemas keep your context clean. Run reviews in the background and act on completion — don't poll. Scope later passes to the changed diff, not a full re-review. Ensure dispatched agents can load skills (use a general-purpose agent type if your fan-out tool defaults otherwise).

See [REFERENCE.md](REFERENCE.md) for a findings schema, a fan-out script skeleton, the lens taxonomy, and the failure-mode catalog.
