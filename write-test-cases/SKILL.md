---
name: write-test-cases
description: Generates a comprehensive, prioritized test plan for a feature, change, or system area — enumerating cases across happy paths, negative and boundary cases, state and lifecycle, permissions, cross-context parity, security, observability, and non-functional dimensions a senior QA would consider. Outputs a structured, reviewable checklist that downstream skills or humans can execute. Use when planning manual or automated test coverage for a new feature, a branch or diff, a ticket, a system area, or a bug fix, before any test execution begins.
---

# Writing Test Cases

A test plan is the *coverage decision* — which cases are worth running and in what order. It is not test code, not a test framework choice, and not an execution log. **A reader who only reads the Coverage Summary must understand what is being tested and why.** Everything else is elaboration.

This skill is execution-agnostic. It does not assume a test framework, a project, or a stack. Hand off the produced plan to a runner (manual, Playwright, Cypress, pytest, browser MCP, etc.) for execution.

## Step 0: Establish the target

When invoked, **always ask the user** what the plan should cover before proceeding:

> What should I write test cases for?
>
> 1. **A feature or system area** — describe it, or point me at the design doc / spec / README
> 2. **A branch or diff** — I'll read the changes and derive cases from them
> 3. **A ticket or bug report** — point me at the issue and any reproduction notes
> 4. **A specific module or function** — name it and I'll scope cases to its contract
>
> (Or describe what you want covered and I'll figure it out.)

Wait for the answer. Then orient with whichever of these applies:

- Read the design spec, ticket description, or commit messages to understand intent
- Read the changed files (or the module under test) end-to-end, not just the diff
- Read sibling implementations if the target is a new instance of an existing category (new entity, new endpoint, new processor) — parity gaps are a common defect class and the cases must enforce parity
- Read project conventions (`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, or equivalent) for project-specific test constraints, fixture conventions, and known sharp edges

## Step 0.5: Scope large targets into modules

**Do not enumerate cases across a sprawling feature in one pass.** Coverage thins, real cases get missed, and the plan degenerates into restating the happy path eight ways. Before enumerating, assess size and split if needed.

### When to split

Split if **any** apply:

- The target touches more than ~10 distinct user-visible behaviors
- The target spans multiple layers (UI, API, data, background workers) that can be tested independently
- The target has more than one primary actor (e.g. owner vs collaborator vs anonymous)

### How to split

Derive modules **from the actual target**, not from a fixed template. Group by behavior, not by file structure. Propose the split to the user before enumerating:

> This feature decomposes into N modules:
> 1. <module derived from the target>
> 2. <module derived from the target>
> 3. <module derived from the target>
>
> Want me to plan each in turn, or do you have a different split in mind?

Wait for confirmation. Plan each module in its own pass. Cases stay grouped by module so the user can execute incrementally.

## Step 1: Enumerate cases by coverage dimension

For each module (or for the whole target if not split), walk these eight dimensions in order. **Skip a dimension only if it would genuinely be empty** — write one line explaining why ("no auth boundary; pure client-side calculation").

1. **Happy paths** — the primary intended flows. Every supported invocation, every supported input shape, every supported result shape. Not just "the demo flow" — every shape the contract allows.
2. **Negative & boundary cases** — invalid input, empty input, max-length input, off-by-one, null/undefined/NaN, expected failure modes, error responses, malformed payloads. For each input field, ask: what is the minimum, maximum, empty case, and structurally invalid case?
3. **State & lifecycle** — persistence across reload/restart/session expiry, idempotency under retry, concurrency between parallel actors, cleanup of resources after delete/cancel/error, partial-failure recovery, in-flight state during cancellation.
4. **Permissions & authorization** — every role × every action × every resource state. If there are N roles and M actions, the matrix is N×M; enumerate the cells that can plausibly differ. Include unauthenticated, expired session, and revoked access where applicable.
5. **Cross-context parity** — adjacent features, entity types, or code paths that should behave identically. If a new instance is added to an existing category, every existing case in that category becomes a parity case for the new one. Asymmetry is one of the most common defect classes.
6. **Security** — auth bypass, IDOR (object access by ID without auth check), injection (SQL, command, prompt, XSS), CSRF, secret exposure in responses/logs/URLs, rate-limit bypass, replay attacks. Scale depth to the target's blast radius.
7. **Observability & analytics** — every event, log line, metric, and trace the feature is supposed to emit fires when expected, and *does not fire* when not expected. False negatives in observability are a real defect class.
8. **Non-functional** — accessibility (keyboard, screen reader, contrast), internationalization (locale, RTL, long strings), performance (latency under realistic load, large input degradation), cross-platform (browsers, OS, mobile/desktop). Include only the dimensions that materially apply to the target.

For each dimension, ask the prompting questions in [REFERENCE.md](REFERENCE.md) — they are how a senior QA actually generates cases, not just category labels.

## Step 2: Prioritize and sequence

Tag every case with a priority. The priority drives execution order, not the structure of the plan.

- **Critical** — data loss, security boundary, revenue path, release-blocker
- **High** — primary user flow, core contract, broken-on-release would be embarrassing
- **Medium** — secondary flow, degraded UX, rare but plausible edge case
- **Low** — cosmetic, defensive, low-probability scenario

Sequence within each priority bucket by **setup cost**. Cases that share a setup (same user, same fixture, same seeded state) run consecutively to amortize the cost. State this explicitly: "Cases TC-A-1 through TC-A-7 share owner+folder+upload setup; run as one session."

## Step 3: Deliver the plan

Output a single markdown document with this structure:

1. **Title + frontmatter** — `**Target:** <one sentence>`, `**Date:** YYYY-MM-DD`, `**Source:** <spec / branch / ticket pointer>`.
2. **Coverage Summary** — one paragraph stating what is covered, what is deliberately *not* covered, the dimensions exercised, and the case-count by priority (`Critical: N | High: N | Medium: N | Low: N`).
3. **Preconditions** — environment, credentials/roles, fixtures, seed data, feature flags. State once; cases reference by name.
4. **Cases**, grouped by module then by dimension. Each case follows the standard shape (below).
5. **Execution sequencing** — short numbered list of suggested execution batches, each batch sharing a setup.
6. **Out of scope** — bulleted list of dimensions deliberately skipped and why. *Every* skipped dimension from Step 1 must appear here.

### Case shape

```
**TC-<module>-<n>: <Short title>** — <Critical|High|Medium|Low>
- Preconditions: <named precondition or inline setup>
- Steps:
  1. <action>
  2. <action>
- Expected: <verifiable outcome>
- Verify in: <UI | API response | DB row | Log line | Metric | Event payload>
```

Use real identifiers from the target (table names, endpoint paths, role names, field names) — not placeholders. The case must be executable by someone who has not read the source code.

## Style rules

- **One case = one assertion.** If a case has three "Expected" bullets, it is three cases. Splitting them is what makes failures attributable.
- **State the verification surface.** "Verify in: DB row" is concrete and points to where truth lives. "Verify it works" is not a test case.
- **Use real identifiers.** Real role names, table names, endpoints, field names from the target. Not "the user" — `owner` or `next-anonymous` or whatever the project calls it.
- **No execution detail.** Do not pin a framework, a selector strategy, or a test runner. The plan must survive being executed manually, by Playwright, by a browser MCP, or by a human QA.
- **Skipped dimensions and skipped cases are explicit.** Every Step-1 dimension you skipped appears in *Out of scope* with a one-line reason. Every case you declined to author for a reason — covered by parity, deferred to a sibling test, blocked on missing fixture — also appears in *Out of scope*, named, with the reason. Silent omission is the failure mode this section prevents.
- **Coverage Summary is load-bearing.** Someone who reads only that paragraph must know which dimensions are covered and which are not.

## Forbidden

- Test code or test-framework syntax. A case is a *spec*, not an implementation.
- Cases that test the framework or a third-party library you do not own ("verify React rendered the component" — no).
- Cases for states the contract makes impossible. If the type system or schema rules out a state, it does not need a test.
- "Smoke test" as a category. Smoke tests are a *subset* of cases tagged by priority, not a dimension.
- Restating the happy path under multiple dimensions. A single case covers happy-path; negative/boundary/state/etc. are *different* cases, not rephrasings.
- Speculative future cases ("when feature X ships, we will need…"). Either it is in scope, or it is in *Out of scope*.
- Silent parity-by-inheritance. "The sibling system covers this" is a valid *Out of scope* entry, not a reason to omit the case without record. If a reader cannot tell which cases you decided not to write, the plan is incomplete.

## Stopping conditions

The plan is done when:

- Every dimension in Step 1 has either at least one case or an explicit *Out of scope* entry
- Every case has a verifiable Expected outcome and a named verification surface
- Critical and High cases together cover every supported contract path
- The Coverage Summary reads as a complete one-paragraph summary on its own

Inflating beyond this point produces theatre, not coverage. Stop.

## Review checklist

- [ ] Target, Date, and Source lines at the top
- [ ] Coverage Summary is one paragraph with explicit in/out scope and a case-count by priority
- [ ] Preconditions stated once, referenced by name in cases
- [ ] Every case has Preconditions, Steps, Expected, and Verify-in
- [ ] Every case carries a Priority tag
- [ ] Every Step-1 dimension is either represented in Cases or explicitly listed in Out of scope
- [ ] Cases use real identifiers from the target, not placeholders
- [ ] Execution sequencing groups cases that share setup
- [ ] No test-framework code, no implementation detail, no smoke-test category

See [REFERENCE.md](REFERENCE.md) for the prompting questions per coverage dimension and a worked example.
