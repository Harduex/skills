---
name: formal-verification
description: >-
  Rigorously verifies the correctness, safety, or security of code, database
  migrations, authorization/permission rules, configuration, and business logic. Use this
  skill WHENEVER the user wants to check, audit, verify, or prove something about a system —
  for example "is this safe?", "can a user ever read another tenant's data?", "find the gaps
  in these permissions", "make sure this SQL migration won't break production", "prove this
  invariant always holds", or whenever they say they review something by hand and suspect they
  are missing cases. It diagnoses what KIND of verification problem you are facing and routes
  to the right tool — off-the-shelf linters (Squawk, Atlas, Semgrep, CodeQL), SMT solving
  (Z3 / MCP Solver), logic programming (Datalog / Prolog), contract-based verification (Dafny),
  or property-based testing — then guides faithful encoding and honest reporting of what was
  and was not proven. Reach for this skill even when the user has not named a specific tool.
---

# Formal Verification

This skill helps you verify a system rigorously instead of eyeballing it. Its core job is to
turn a vague request ("check my permissions / migration / logic") into the right combination of
a precise property and a deterministic checker — and to be honest about the limits.

## First principle: no specification, no verification

Verification always needs two things: **(1)** the target rendered into a formal model, and
**(2)** a precisely stated property — what must always be true, or must never happen.

Your first move on any verification request is to make the property explicit. If the user only
says "check X", extract or propose the property before touching any tool:

- Ask one sharp question, or propose 2–3 candidate properties and confirm.
- Example: "check my Hasura permissions" is underspecified. The real property is usually
  something like *"no role can ever read a row whose `org_id` differs from the caller's
  session `org_id`"*. State it before encoding it.

The hard part of verification is naming what "correct" means — not running the check. Do this
step even when it feels obvious; an unstated property is the most common reason a verification
effort silently checks the wrong thing.

## Division of labor (why this works)

LLMs are strong translators and weak judges. Deterministic engines are the reverse. So:

- **You (the LLM) translate**: turn the messy real artifact into a formal model + candidate
  properties. This is your strength.
- **The engine judges**: a solver, logic engine, or linter decides — exactly, repeatably, with
  a counterexample when it fails.

Never let "this looks correct to me" stand in for a check an engine could perform. If a property
can be handed to an engine, hand it over.

## The honest ceiling — read before promising anything

- **Some properties cannot be proven** (undecidable or intractable). When that happens, degrade
  gracefully: do a bounded check plus property-based testing, and state plainly what was not
  covered. Do not pretend.
- **A passing check is narrow**: it means the *specified* failure does not occur *within the
  modeled scope*. It does NOT mean "the code is correct".
- **The result is only as good as the translation.** Before trusting any encoding, validate it
  against one case you KNOW is safe (expect: proved) and one you KNOW is broken (expect:
  counterexample). If it does not catch the broken case, your encoding is wrong, not the system.
  This single habit prevents "confidently precise but wrong" answers.

## Step 1 — Frame the work, then route (the context-driven core)

This is the judgment the engines cannot make for you, and it is what makes the skill *smart*
rather than mechanical. Make two calls before encoding anything — sized to the actual target and
to what the user asked for — then route each property to a tier.

**(1) Derive the candidate properties from the artifact.** "Verify X" rarely names the real
property. Read the target, identify its *kind*, and enumerate the failure modes that kind is
prone to. A generic prompt-catalog (extend it per domain — these are starting points, not limits):

| Artifact kind | Properties worth checking (failure modes to hunt) |
|---|---|
| Access / permission / auth rules | tenant or row isolation; privilege escalation; NULL / absent-context holes; cross-operation consistency (writable but not readable?); role subset & inheritance |
| Schema migration | down⇄up reversibility; locks / table rewrites on populated tables; destructive or breaking changes; data loss on rollback |
| State machine / lifecycle | unreachable or dead states; illegal transitions; fail-closed on bad input; an invariant preserved across *every* transition |
| Pricing / config / business rules | rule contradictions; dead branches; bounds & overflow; consistency across the whole rule set |
| Algorithm / data structure | functional correctness vs a contract; termination; boundary conditions |
| Reachability / data flow | who-can-reach-what; ungated paths; effective / inherited sets; taint from source to sink |

Name each surviving candidate as a precise *must-always / must-never* statement, and keep the few
whose violation has the highest blast radius.

**(2) Size breadth and depth to the stakes.** Don't run six engines on a low-stakes helper; don't
single-check a tenant-isolation proof. A rough dial:

| Stakes | Breadth — how many properties | Depth — per property |
|---|---|---|
| Low / mechanical | the one obvious property | a linter, or a single solver check |
| Medium | the 2–4 that matter | solver + the mandatory known-good / known-bad validation |
| High / security / irreversible | enumerate exhaustively, incl. the easy-to-miss | solver + adversarial known-bad + a second lens (PBT or an independent encoding) |

Sizing controls *what* you check and *how hard* — never *whether* you validate the encoding. The
known-good / known-bad check (in "the honest ceiling" above) is mandatory at every level; scaling
breadth down never means skipping it.

**Then classify each property by its shape** and route to the cheapest engine that covers it.
Most real cases combine several shapes — decompose and route each part:

- **(A) Known anti-pattern in a common artifact** — unsafe migration (locks, destructive ops,
  breaking changes), injection, hardcoded secret, a known broken-authz pattern.
  → **Tier 1 off-the-shelf linter.** Zero encoding, instant value. Always check if this applies
  first. Limit: only finds patterns someone already wrote a rule for.

- **(B) "Can data/state ever satisfy a forbidden condition?"** over booleans / arithmetic /
  enums / strings — permission filters, access rules, config consistency, pricing or discount
  rules, "is this branch dead", "do these two rules contradict".
  → **SMT solving (Z3).** Encode the *violation* and check satisfiability. UNSAT = proved safe
  within the model; SAT = a concrete counterexample (the exact values that break it).

- **(C) Relational / transitive / reachability** — who-can-reach-what, role inheritance,
  dependency or call graphs, data-flow, "is table T reachable from role R via any relationship".
  → **Datalog / Prolog.** Facts + rules + a fixpoint query. Naturally computes effective sets
  (e.g. inherited-role permissions).

- **(D) Functional correctness of an algorithm or state machine against a contract**, where a
  real proof is worth real effort.
  → **Contract verification (Dafny).** Write code + pre/post-conditions + invariants, discharged
  to an SMT solver. High effort — reserve for crown-jewel logic, not everyday code.

- **(E) Need breadth and cheap counterexamples, proof not required.**
  → **Property-based testing** (Hypothesis / fast-check / QuickCheck). Generate many inputs
  against an invariant. Not a proof, but finds real bugs fast and complements every option above.

Pick the cheapest tier that actually covers the stated property. Do not reach for a solver when
a linter or a property test already answers the question, and do not over-apply heavy
verification to low-stakes code — match effort to stakes.

See **`references/engines.md`** for exact install and invocation of each tool. Read it when you
have chosen a tier.

## Step 2 — Encode and run

For the encoding recipes (especially the SMT "satisfiability-of-the-violation" pattern), a fully
worked example, and the faithfulness checklist, read **`references/encoding-patterns.md`** when
you reach tier B or C. Apply the known-good / known-bad validation from the honest-ceiling
section before trusting any result.

## Step 3 — Report with scope discipline

Always report in this shape:

```
Property checked:  <the precise property, in plain language>
Tool / engine:     <what did the checking>
Result:            PROVED (within scope) | COUNTEREXAMPLE | NOT DETERMINED
Counterexample:    <the minimal concrete input that breaks it, if any>
Scope & caveats:   <what was modeled, what was simplified, what was NOT checked>
```

Then ALWAYS close with a **plain-language summary** — a few sentences a non-specialist could act
on, even when the structured report above is precise. Cover, in lay terms:

- the bottom line (is it safe / what broke), with no solver jargon (`unsat`/`sat` → "proven / a
  hole was found");
- the single most important actionable takeaway (e.g. "don't drop this constraint — it's what
  holds the guarantee up");
- the honest caveat restated plainly (what you did NOT check, so a clean result isn't mistaken
  for "everything is correct").

The structured block is the evidence; the plain-language summary is what the user reads first and
remembers. Lead the chat reply with the structured report, end with this summary.

Never upgrade "tests passed" or "linter is clean" into the word "verified". Scope honesty is the
difference between a useful tool and a false sense of security.

## Step 4 — Grow the project's verification library

Each property the user cares about becomes a small, named, reusable check (a saved spec, rule
base, or solver script) so future runs only supply the situation-specific facts. Over time this
growing menu of checks — not any single tool — is what makes verification "general" for the
project. When you build a new check, suggest saving it for reuse.

## Reference files

- `references/engines.md` — install + invocation + when-to-use for every tool above, plus the
  **Environment setup** ladder for getting an engine running on a locked-down box.
- `references/encoding-patterns.md` — SMT and Datalog encoding recipes, a worked Hasura
  permissions example, and the translation-faithfulness checklist.
- `scripts/setup-engine.sh` — idempotent `uv`-first installer for the Python engines (Z3, clingo,
  Hypothesis, …); prints the interpreter to run specs with. Run it before a tier-B/C/E check.
  `engines.md` has the verified no-root command for every other engine too.
