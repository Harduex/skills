---
name: functional-programming
description: Functional programming principles for structuring code as Data, Calculations, and Actions. Enforces immutability, pure functions, side-effect isolation, and functional core / mutable shell architecture. Use when writing new features, refactoring code, reviewing architecture, or when user mentions functional programming, pure functions, side effects, immutability, or data-first design.
---

# Functional Programming: Data > Calculations > Actions

Categorize every piece of code into one of three categories and **prioritize them in this order**: Data first, Calculations second, Actions last.

## Decision Checklist

When writing or reviewing code, ask in order:

1. **Can this be data?** Express it as an immutable value, config object, lookup table, or declarative structure. Data cannot break your system.
2. **Can this be a calculation?** Write a pure function: same inputs, same output, no side effects. Calculations are safe to call anywhere, anytime.
3. **Must this be an action?** Only then use side effects. Keep actions thin — no business logic inside them.

## Quick Rules

| Category | What it is | Rules |
|---|---|---|
| **Data** | Immutable values, configs, schemas | Never mutate after creation. Spread to derive new values. Prefer complex data over complex code. |
| **Calculations** | Pure functions (queries) | No side effects. No hidden inputs (globals) or outputs (exceptions, mutations). Referentially transparent. |
| **Actions** | Side effects (commands) | Push to edges. No business logic inside. Separate from queries — asking a question must never change the answer. |

## Architecture Pattern: Functional Core / Mutable Shell

```
┌─────────────────────────────────┐
│         Mutable Shell           │  ← Thin. Reads external state,
│   (API handlers, effects, IO)   │    calls core, applies results.
│                                 │
│  ┌───────────────────────────┐  │
│  │     Functional Core       │  │  ← Fat. Pure calculations,
│  │  (business logic, rules,  │  │    all decisions made here.
│  │   transforms, validation) │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

- **Shell** supplies data to the core, then applies the core's decisions as side effects.
- **Core** receives plain data, returns plain data. Never calls the shell.

## Applying This

See [REFERENCE.md](REFERENCE.md) for detailed principles, concrete examples, and anti-patterns.
