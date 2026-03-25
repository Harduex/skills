---
name: architecting
description: Designs system architectures, evaluates technical trade-offs, and defines module boundaries. Proposes 2-3 approaches with clear rationale. Use when designing a new system, evaluating architectural options, or making significant technical decisions.
---

# System Architecture

## Process

1. **Understand constraints** — clarify requirements, load characteristics, team capabilities, and timeline before proposing anything.
2. **Evaluate trade-offs** — make every trade-off explicit:
   - Speed-to-market vs. maintainability
   - Simplicity vs. flexibility
   - Consistency vs. availability
   - Build vs. buy
3. **Propose options** — present 2-3 viable approaches with clear rationale. Recommend one and explain why.
4. **Define boundaries** — establish module boundaries, API contracts, and data ownership. Specify what each component is and is not responsible for.

## API and interface design

Treat all interfaces as products for other developers:

- Clear affordances and signifiers
- Intuitive naming that describes effect and purpose
- Encapsulate complexity behind friendly facades
- Prevent misuse through design, not documentation

## Example output

```
## Options

### A: Event-driven with message queue
- Decoupled services communicate via events
- Pro: independent scaling, failure isolation
- Con: eventual consistency, debugging complexity
- Fits: high-throughput, loosely-coupled domains

### B: Synchronous API gateway
- Central gateway routes to backend services
- Pro: simple mental model, strong consistency
- Con: gateway bottleneck, tight coupling
- Fits: low-latency, consistency-critical domains

## Recommendation: Option A
[Rationale tied to specific project constraints]

## Module boundaries
[Component ownership, API contracts, data flow]
```

## Principles

- Code is written for humans first, machines second.
- Favor simplicity. The right complexity is the minimum needed for current requirements.
- Evaluate data models based on actual access patterns, not convention.
- Propose refactoring opportunities but never execute without explicit permission.
