---
name: planning
description: Defines product requirements, breaks down work into actionable tasks, and prioritizes based on business value. Writes user stories with acceptance criteria. Use when writing an implementation plan, breaking a feature into ordered tasks with acceptance criteria, planning a sprint or milestone, maintaining a product roadmap or postponed ideas, or when asked to "plan" work before coding.
---

# Product Planning

## Process

```
Planning checklist:
- [ ] Understand the problem (who, what, why, success metric)
- [ ] Define scope (included and explicitly excluded)
- [ ] Identify dependencies and blockers
- [ ] Break into tasks with acceptance criteria
- [ ] Sequence by dependency chain, then priority
- [ ] Flag risks and unknowns
```

## Product roadmap

When maintaining product direction or capturing postponed ideas, use the project's existing roadmap; if this convention is requested and absent, create `docs/ROADMAP.md` by default and link it from the root harness and documentation index (using paths relative to each linking file). A roadmap is an outcome and sequencing record, separate from an implementation task list:

1. State product outcomes/themes and lasting constraints.
2. Group work into relative horizons (for example Now / Next / Later); use dates only when agreed. Preserve the user's selected ordering; identify recommendations as recommendations.
3. Give each initiative a stable ID, intended outcome, horizon/relative priority, decision status, dependencies or next decision, and a link to detailed research/specs.
4. At a decision boundary, capture explicitly postponed ideas as deferred and discussed-but-undecided ideas as proposed. Deduplicate existing entries and retain their IDs; distinguish approval, selected direction, implementation and release status.
5. Update statuses after actual decisions or verified delivery. Retain a compact delivered section or link to history. Keep detailed evidence in its existing documents.

Roadmap placement is not implementation authorization. Do not turn a brainstorm into a commitment, invent delivery dates, or start deferred work. For a narrowly scoped approved task, preserve unrelated entries and record only relevant status changes.

## Task breakdown

Break work into actionable, estimable units:

1. **Define scope** — what is included and explicitly excluded
2. **Identify dependencies** — what must exist before this work can start
3. **Write acceptance criteria** — specific, testable conditions for "done"
4. **Annotate each task** — `Skills:`, `Reuse:`, `Mirrors:`, `Assumptions:` (see format below)
5. **Sequence tasks** — order by dependency chain, then priority
6. **Flag risks** — what could block or delay delivery

## Requirements format

```
### [Feature name]

**User story**: As a [persona], I want [action] so that [outcome]

**Acceptance criteria**:
- Given [context], when [action], then [result]
- Given [context], when [action], then [result]

**Edge cases**:
- [Failure state or boundary condition]

**Out of scope**:
- [Explicitly excluded items]

**Tasks** (each carries):
- Skills: [domain/standards skills the executor must invoke before this task]
- Reuse: [existing helpers/patterns surveyed — name the search performed and its outcome]
- Mirrors: [closest existing sibling to match]
- Assumptions: [what this task assumes about the codebase; if execution disproves one, stop and revise the plan]
```

## Principles

- Prioritize outcomes over outputs. "Reduce onboarding drop-off by 20%" over "ship feature X."
- Act as a shield against scope creep. Push back on additions that don't serve the defined goal.
- Be empathetic to users but pragmatic about constraints.
