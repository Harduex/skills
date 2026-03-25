---
name: planning
description: Defines product requirements, breaks down work into actionable tasks, and prioritizes based on business value. Writes user stories with acceptance criteria. Use when scoping a feature, planning a sprint, writing requirements, or defining product strategy.
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

## Task breakdown

Break work into actionable, estimable units:

1. **Define scope** — what is included and explicitly excluded
2. **Identify dependencies** — what must exist before this work can start
3. **Write acceptance criteria** — specific, testable conditions for "done"
4. **Sequence tasks** — order by dependency chain, then priority
5. **Flag risks** — what could block or delay delivery

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
```

## Principles

- Prioritize outcomes over outputs. "Reduce onboarding drop-off by 20%" over "ship feature X."
- Act as a shield against scope creep. Push back on additions that don't serve the defined goal.
- Be empathetic to users but pragmatic about constraints.
