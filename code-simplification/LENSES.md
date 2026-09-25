# Lenses

Each lens lists smells as **smell → how to spot it → named fix**. A smell is a prompt to look closer, not a verdict. Every candidate still passes [GUARDRAILS.md](GUARDRAILS.md).

## Contents

- [L1 Delete](#l1-delete)
- [L2 Reuse](#l2-reuse)
- [L3 Deepen and collapse](#l3-deepen-and-collapse)
- [L4 State and control](#l4-state-and-control)
- [L5 Altitude](#l5-altitude)
- [L6 AI over-build](#l6-ai-over-build)
- [Detector leads](#detector-leads)
- [Sources](#sources)

## L1 Delete

The easiest code to change is code that is gone.

- **Dead code** → no live producer or caller → Remove Dead Code, Remove Parameter.
- **Speculative generality** → a hook, parameter, or option that serves only an unrequested future → Inline Function, Inline Class, Collapse Hierarchy. YAGNI exempts seams that keep code easy to change.
- **Fully rolled-out feature flag** → one branch is always taken in every environment → delete the flag and the dead branch.
- **Config nobody sets** → every deployment uses the default → hardcode or compute the default.
- **Unused dependency** → nothing imports it → remove it from the manifest.
- **Orphans** → helpers, types, or styles left behind by an earlier removal → delete them with the thing they served.

## L2 Reuse

One job, one mechanism.

- **Hand-rolled copy of an existing helper** → grep the shared utilities and the feature's local helpers, then read the helper's body before trusting its name → call the existing helper. Name it and the lines that disappear.
- **Two mechanisms doing one job** → two caches, two fetch layers, or two event buses for the same concern → consolidate onto the incumbent.
- **Duplicate libraries** → two packages solve the same problem → keep the incumbent. Every added technology costs across the stack.
- **The wrong abstraction** (the reverse case) → a shared helper swollen with flags and conditionals for each caller → inline it back into every caller, keep only what each caller uses, then re-extract from current needs. Duplication is cheaper than the wrong abstraction.
- **Copy-paste of three or more** → the same non-trivial logic in three places that change together → one small local helper next to its consumers.

## L3 Deepen and collapse

A module earns its interface by hiding more than it exposes. See [DEEPENING.md](DEEPENING.md) for the full treatment.

- **Shallow module** → the interface costs about as much to learn as the body it hides → merge it into its caller or its neighbour.
- **Pass-through method or layer (Middle Man)** → most members only forward calls → Remove Middle Man, Inline Function.
- **Pass-through variable** → a value threaded through layers that never read it → read it where it is already in scope, or use a context object.
- **Interface with one implementation, factory or strategy with one case** → Collapse Hierarchy, Inline Class. One adapter is a hypothetical seam. Two adapters make a real one.
- **Conjoined methods** → you cannot understand one without reading the other → Inline Function. Keep pure helpers factored out. Inline single-caller functions that mutate state.
- **Flag argument** → a boolean or mode selects which operation runs → Remove Flag Argument: split it into named functions.
- **Information leakage** → one design decision is spread over several modules → move it into the one module that owns the decision.
- **Wrapper around a library that adds nothing** → Remove Middle Man and call the library directly.
- **Deep or refusing inheritance** → a subclass uses only part of its parent → Replace Subclass with Delegate, Remove Subclass.

## L4 State and control

State is the main source of accidental complexity. Control flow comes next.

- **Derived or redundant state** → a stored value kept in sync by hand → Replace Derived Variable with Query. A cache of an immutable source is fine.
- **Premature cache** → no evidence of a hot path or an expensive source → remove it only with proof it is not needed (GUARDRAILS.md, G6).
- **Needless async or concurrency** → an async function that awaits nothing, or a queue with one producer and one consumer in-process → make it synchronous or direct.
- **Catch-and-ignore around a call** → define the error out of existence. Change the semantics (for example "ensure absent") so the error cannot occur. Never apply this to validation or security failures.
- **Deep nesting** → Guard Clauses: return early and leave the happy path unindented.
- **Excess generics** → a type parameter used by one concrete type → de-generalize it to the concrete type.

## L5 Altitude

Fix the root cause at the right depth.

- **Special case layered on shared infrastructure** → an `if (kind === 'x')` in a shared helper, or a per-caller workaround → change the underlying mechanism once, generally.
- **Symptom patch** → a retry, a delay, or a null check that hides a cause nobody traced → trace the cause and fix it there. The removed patch goes with the fix.
- **Shotgun surgery** → adding one instance of a concept touches many files → move the scattered pieces into one module. Count the files per instance before and after.

## L6 AI over-build

Code written by agents over-builds in recognizable ways. Judge against the surrounding code, never against a guess about authorship.

- **Defensive checks on trusted paths** → validation, null checks, or try/catch for states the types or callers rule out → delete them. Validate only at system boundaries.
- **Fallback chains** → "try new, else old" with no version signal, or silent defaults on bad internal state → keep one path and let failures stay visible.
- **Compatibility shims** → re-exports, renamed unused variables, `// removed` markers, adapters for callers that no longer exist → delete them once nothing deployed, persisted, public, or external consumes them.
- **Comment noise** → comments that restate the code or narrate the change → delete them. Keep non-obvious rationale.
- **Over-configurability** → options, props, or parameters nobody passes → hardcode the value.
- **Single-use abstractions** → a helper, hook, or class with one caller that adds a name but hides nothing → inline it.
- **Closed justification loops** → a fallback exists only because a test exercises it, and the test exists only for that fallback → treat the pair as one candidate and delete both together.
- **Test bloat** → duplicated cases, implementation-detail assertions, mocks where a real in-process collaborator works → consolidate at the public interface.
- **Type workarounds** → `any` casts or ignore comments that silence the checker → fix the type or narrow it properly.

## Detector leads

A tool hit is a lead. Confirm it by hand before it becomes a candidate.

| Need | Tool | False-positive traps |
|---|---|---|
| Unused files, exports, dependencies (JS/TS) | `knip` | Dynamic imports with computed paths, missing framework plugins or entry patterns, path aliases, generated files. Fix the config before ignoring. |
| Unused code (Python) | `vulture --min-confidence 100` for certain hits | `getattr` and other implicit access. Hits below 100% confidence are leads only. |
| Unused code (Go) | `deadcode -test ./...` | `//go:linkname`, build tags, library packages with no `main`. Use `-whylive` to explain a live hit. |
| Unused dependencies (Python) | `deptry` | Optional extras, plugins loaded by name. |
| Duplicate blocks | `jscpd --min-tokens 30`, `pmd cpd` | Look-alike code that changes for different reasons. Check git history before merging duplicates. |
| Hard-to-read functions | Cognitive complexity (`eslint-plugin-sonarjs`) | Rank the functions inside a hotspot. Deep nesting is the target. |

Before deleting anything a tool calls unused, grep for string references: routes, DI registrations, reflection, config keys, and framework entry points.

## Sources

- Ousterhout, *A Philosophy of Software Design*: deep modules, conjoined methods — https://github.com/johnousterhout/aposd-vs-clean-code
- Ousterhout, define errors out of existence — https://wiki.tcl-lang.org/page/Define+Errors+Out+of+Existence
- Metz, The Wrong Abstraction — https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
- Fowler, Yagni — https://martinfowler.com/bliki/Yagni.html
- Fowler, Flag Argument — https://martinfowler.com/bliki/FlagArgument.html
- Fowler, Feature Toggles (toggles as inventory) — https://martinfowler.com/articles/feature-toggles.html
- Refactoring catalog — https://refactoring.com/catalog/ · smells — https://refactoring.guru/smells
- Moseley and Marks, Out of the Tar Pit (state as the main source of complexity) — https://curtclifton.net/papers/MoseleyMarks06a.pdf
- Carmack on inlined code — http://number-none.com/blow/john_carmack_on_inlined_code.html
- McKinley, Choose Boring Technology — https://mcfunley.com/choose-boring-technology
- Anthropic, prompting best practices (over-engineering) — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- GitClear, AI code quality (duplication up, refactoring down) — https://www.gitclear.com/the_ai_code_quality_maintainability_gap
- deslop-GPT (closed justification loops, confidence gate) — https://github.com/MrZoyo/deslop-GPT
- knip, handling issues — https://knip.dev/guides/handling-issues
- SonarSource, Cognitive Complexity — https://www.sonarsource.com/docs/CognitiveComplexity.pdf
