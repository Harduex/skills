# Encoding patterns, a worked example, and the faithfulness checklist

Read this when you reach tier B (SMT) or C (Datalog) in SKILL.md. The biggest risk at these
tiers is a faithful-looking but wrong translation, which produces a precise wrong answer. The
checklist at the end is how you avoid that.

## The SMT recipe (property shape B)

The pattern is always "prove a bad thing is impossible by failing to find it":

1. **Identify the symbolic variables.** Two groups: the *subject* (attributes of the row /
   object / state being decided on, e.g. `row_org_id`, `row_owner_id`) and the *context* (caller
   inputs the system trusts, e.g. `session_org_id`, `session_user_id`, `session_role`).
2. **Encode each rule as a constraint** over those variables, mirroring the real operators
   (`_and`→`And`, `_or`→`Or`, `_eq`→`==`, `_in`→membership, `_not`→`Not`).
3. **State the property, then assert its violation.** If the property is "access implies same
   org", the violation is `access_granted AND row_org_id != session_org_id`.
4. **Check satisfiability.**
   - `unsat` → no inputs violate the property → PROVED within the model.
   - `sat` → read `model()` for the exact counterexample.

### Worked example — Hasura tenant isolation (Z3 / Python)

Property: *a role can never read a row from a different org than its session org.*

```python
from z3 import *

row_org     = Int('row_org')
session_org = Int('session_org')

# The role's SELECT row filter, translated from the Hasura permission metadata.
# Suppose the filter is:  { "org_id": { "_eq": "X-Hasura-Org-Id" } }
select_filter = (row_org == session_org)

s = Solver()
# Assert the VIOLATION: the filter grants read, yet the row belongs to another org.
s.add(select_filter, row_org != session_org)

print(s.check())     # unsat  -> isolation holds for this filter
                     # sat    -> s.model() shows org values that leak
```

If you instead translate a *broken* filter (say someone wrote `_gte` instead of `_eq`, or
omitted the org check entirely), the same script returns `sat` with a concrete leaking
assignment. That contrast is exactly how you validate your encoding (see checklist below).

> **Z3 Python API note:** a `CheckSatResult` is not hashable — don't key a dict on it
> (`{sat: 'safe'}[r]` raises `TypeError: unhashable type`). Compare directly: `r == sat` /
> `r == unsat`. (Seen on z3-solver 4.16.) Drive a multi-property run through a small harness
> that records `(name, expected, got)` per check so the known-good/known-bad cases self-report.

### Useful questions you can ask the same way
- **Cross-operation consistency:** assert `update_filter AND Not(select_filter)` → is there a row
  a role can modify but cannot see?
- **Role subset:** assert `roleA_filter AND Not(roleB_filter)` → does A exceed B where it should
  not?
- **Dead rule:** assert a single `_or` branch alongside the negation of the others → is it ever
  the sole reason access is granted?

## The Datalog recipe (property shape C)

For reachability and inherited/effective sets:

```prolog
% Facts extracted from schema + permission metadata
has_direct_access(reporter, reports).
relationship(reports, users).        % reports table relates to users
permission_allows_traversal(reports, users).

% Rule: a role reaches a table directly, or through a permitted relationship (transitively)
reaches(Role, T) :- has_direct_access(Role, T).
reaches(Role, T) :- reaches(Role, T0), relationship(T0, T),
                    permission_allows_traversal(T0, T).

% Query: which (role, table) pairs are reachable but not on the allow-list?
% leak(Role, T) :- reaches(Role, T), \+ allowed(Role, T).
```

For inherited roles, add `inherits(child, parent).` and a rule that unions the parent's access
into the child; the fixpoint then computes the *effective* permission set automatically.

## The faithfulness checklist

Before trusting any tier-B/C result, confirm the translation handles these — each is a classic
source of silent, confident error:

- **SQL three-valued logic / NULL.** In SQL/Postgres a comparison with `NULL` is `unknown`, not
  `false`. Permission filters inherit this. Model nullable columns explicitly (e.g. an optional
  flag) rather than assuming two-valued logic, or you will miss leaks that hinge on `NULL`.
- **Absent context variables.** What if a session variable is missing or empty? Model the
  "unset" case; many real leaks live there.
- **Relationship / `_exists` semantics.** A filter that reaches through a relationship is a join,
  not a local predicate — encode the existence quantifier, do not flatten it away.
- **Inherited-role union.** Effective permission is the union across inherited roles; check the
  combined set, not each role alone.
- **Numeric width / overflow.** If real values are bounded integers, use bitvectors or add range
  constraints, or the solver may "prove" safety using impossible values.
- **Defaults and presets.** Insert/update `check` clauses and preset values change what rows can
  exist; include them.

## The non-negotiable validation step

After encoding, run the encoding against:
1. a case you KNOW is safe → expect PROVED, and
2. a case you KNOW is broken (deliberately weaken one rule) → expect a COUNTEREXAMPLE.

If the broken case does not produce a counterexample, the encoding is wrong — fix it before
trusting any "PROVED" result. Only after both behave correctly should you scale to the full
metadata. Start narrow (one table, one operation, one property) and widen.
