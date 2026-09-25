# Guardrails

The skeptic runs every check here before a candidate reaches the user.

## Contents

- [Verification checks](#verification-checks)
- [Confidence levels](#confidence-levels)
- [Never simplify these](#never-simplify-these)
- [The report bar](#the-report-bar)
- [Sources](#sources)

## Verification checks

Run each check with a command, not by reading alone.

1. **Why does it exist? (Chesterton's fence)** Run `git log -L` or `git blame` on the lines, read the linked ticket or commit message, and find the tests that cover it. If no reason turns up, say "reason unknown". Never read the absence of a reason as permission.
2. **Deletion test.** Would removing it concentrate complexity, or only move it somewhere less visible? Moved complexity is not a candidate.
3. **Reachability.** For "unused" claims, prove that no non-test producer reaches it. Grep for string references, framework entry points, dynamic imports, DI registrations, and config keys.
4. **Boundary.** Is it an exported API, route, wire format, persisted shape, error message, or event name that something outside the scope may depend on? (Hyrum's law.)
5. **Essential or accidental.** Does a real domain rule or an external interface force this complexity? Essential complexity can only be moved, not removed.
6. **Behavior invariants.** Name what the code guarantees today: outputs, errors raised, side effects, and ordering. For every deleted line, name the invariant it enforced and show where the new code keeps it. Removing a duplicate side effect (a second identical refetch) is a behavior change. Report it as an observation for the user to decide.
7. **Performance.** See G6. State the impact on every candidate that touches the listed areas.

## Confidence levels

| Level | Meaning | At apply time |
|---|---|---|
| **HIGH** | Every check passed with evidence. | Edit. |
| **MEDIUM** | The mechanism is real, but one piece of evidence is missing (a caller, a history reason, a deployment fact). | Ask the question that supplies the evidence first. Permission to edit is not permission to resolve doubt in favor of deletion. |
| **LOW** | Touches security, concurrency, persistence, or a protocol. Or the reason it exists stays unknown after checking. | Do not edit. Present it for the user's judgment only. |

There are no intermediate levels. When unsure between two levels, choose the lower one.

## Never simplify these

- **G1 Load-bearing code you cannot explain.** A guard, retry, or check whose purpose you cannot state is not yours to delete.
- **G2 Essential complexity.** Domain rules and conformance to external interfaces stay. Abstracting them away abstracts away the essence.
- **G3 Public surface without an explicit yes.** Exported APIs, routes, wire formats, persisted data, error text, ordering, and timing all have users you cannot see.
- **G4 Things that vary independently.** Two look-alike blocks can be coincidence. DRY is about knowledge, not text. Never share business logic across bounded contexts or services.
- **G5 Security, validation, and boundary error handling.** Never thin, collapse, or define away input validation, auth checks, or error handling at a system boundary.
- **G6 Anything that makes the code slower.** A simplification must not add work. Flag and prove the impact when a candidate touches any of these:
  - a cache, memoization (`useMemo`, `React.memo`), or batching
  - parallel work (`Promise.all`, goroutines, worker pools) that would become sequential
  - a lookup structure (map or set) that would become a scan
  - a query shape (N+1 risk, a lost index or filter)
  - a hot path, a render loop, or startup code
  
  A possible slowdown needs a measurement, or the candidate becomes MEDIUM and turns into a question.
- **G7 Readability.** Revealing intention outranks fewer elements. No nested ternaries, dense one-liners, or clever tricks presented as simplifications.
- **G8 Legitimate indirection.** Proxies and decorators, deliberate dependency cuts, framework extension points, and test seams are kept on purpose.
- **G9 Big-bang changes.** Every step leaves the system working. A simplification that needs a rewrite is a proposal for the user, not an edit.

## The report bar

The list is a short set of wins the user will act on, not a log of everything noticed. A candidate is shown only when all three hold:

1. **Verified.** The premise was checked against the real code. "May", "likely", and "could" are hypotheses: verify them or drop them.
2. **Consequential, with a number.** It names what disappears (lines, files, concepts, config keys, dependencies), the existing thing to reuse, or the future change that gets cheaper. A future-cost claim must point to past occurrences in `git log`.
3. **Actionable in scope.** The fix fits the chosen scope. Anything wider becomes a one-line follow-up after the list.

| Report | Drop |
|---|---|
| "Reuse helper X, deletes ~60 lines", with the helper named | "Could be simpler", "over-engineered", or "won't scale" with no replacement and no number |
| Verified dead code, dead config, or a rolled-out flag | Style, naming, formatting, or comment wording |
| A layer or wrapper that collapses, with the file count | A new abstraction without two or more real consumers today |
| A same-class sweep: "12 pass-through wrappers in `uploads/`" | The same class drip-fed as 12 separate items |
| A special case that moves into the shared mechanism | Performance concerns, which are out of scope except under G6 |
| A closed justification loop, deleted as one unit | Pre-existing noise outside the scope |
| | UI copy and wording, which are product calls |
| | Any change to behavior. Note it after the list as an observation, never as a candidate. |

- **Small sweeps fail.** A sweep of tiny items (unreachable guards, needless `?.`) that removes fewer than about 10 lines in total is not consequential. Drop it.
- **Size.** At most about 10 candidates, and fewer is normal. If the list runs long because borderline items crept in, re-filter it. People act on the first handful, and the rest erodes trust in the sharp ones.
- **No nitpick tier.** Anything that would earn one fails the bar.
- **Stop rule.** Stop when the remaining candidates would not make the code easier to change. Where several shapes are equally valid, the current one wins.

This table is a starting calibration. Refine it from which candidates users actually pick.

## Sources

- Chesterton's fence — https://www.lesswrong.com/w/chesterton-s-fence
- Hyrum's law — https://www.hyrumslaw.com/
- Brooks, No Silver Bullet (essence and accidents) — http://worrydream.com/refs/Brooks-NoSilverBullet.pdf
- Beck's four rules of simple design — https://martinfowler.com/bliki/BeckDesignRules.html
- Abramov, Goodbye Clean Code — https://overreacted.io/goodbye-clean-code/
- Don't share libraries among microservices — https://phauer.com/2016/dont-share-libraries-among-microservices/
- grug brain developer — https://grugbrain.dev/
- Every, ce-simplify-code (preserve outputs, errors, side effects, ordering) — https://github.com/EveryInc/compound-engineering-plugin
- LLM refactoring safety study — https://arxiv.org/abs/2411.04444
