# Code: Statements, Functions, Modules

Procedures in controlled language are short, imperative, one instruction per
sentence, condition first. Functions are procedures. Likewise, modules are
chapters.

## Statements & functions

| ID | Rule |
|---|---|
| S1 | Keep units small. Review triggers: function > 25 lines, > 4 parameters, nesting > 2 levels — split or justify. |
| S2 | One action per statement. No chained side effects, no mutation inside conditions. |
| S3 | Write the happy path as direct imperative commands, top to bottom. |
| S4 | Conditions before actions: guard clauses and input validation come first. |
| S5 | Keep the actor visible: explicit calls over hidden control flow, implicit hooks, or action-at-a-distance. |
| S6 | Use the simplest construct that works; no meta-programming where a function does. |
| S7 | Model actions as verbs (functions), not doer-nouns (`Processor.run()` wrapping one action). |
| S8 | Never compress at the cost of clarity: no code golf, no cryptic ternary chains, no omitted optional syntax that aids reading. |
| S9 | Three or more parallel items or branches go vertical: a list, table, map, or config — not an inline chain. |

## Modules

| ID | Rule |
|---|---|
| M1 | One topic per file, module, or class. |
| M2 | Size split-signals: file > 400 lines or class > 7 public members warrants a split or a written justification. |
| M3 | Order top-down: public surface first, helpers below — a file reads like a newspaper. |
| M4 | Sibling modules mirror each other's structure and section order. |
| M5 | Dependencies are explicit, declared at the top, and acyclic. |
| M6 | Reuse the codebase's existing vocabulary of operations. Before inlining a computation, conversion, or check that has a standard name, read the shared utility modules' export lists and use the name that is already there. Enumerate the exports; do not guess at a name you would have to know already. |

M3, M4, and M5 have prose counterparts — D8, D8, and D6 in [WRITING.md](WRITING.md)
— because the source rules behind them govern both a file's layout and a
document's. Applying one does not discharge the other.

## Worked example

```ts
// BEFORE — violates S4 (guards last), S2 (mutation in condition), S7 (doer-noun), S1 (nesting)
class SubscriptionProcessor {
  process(sub: Subscription, now: Date) {
    if (sub) {
      if (sub.status === "active") {
        if ((sub.renewals = sub.renewals + 1) < MAX_RENEWALS) {
          return renew(sub, now);
        } else { return expire(sub); }
      } else { return null; }
    } else { throw new Error("bad input"); }
  }
}

// AFTER — S4 guards first, S2 one action per statement, S7 a verb, S3 imperative happy path
function renewSubscription(sub: Subscription, now: Date): Renewal | null {
  if (!sub) throw new Error("renewSubscription: sub is required");
  if (sub.status !== "active") return null;
  if (sub.renewals >= MAX_RENEWALS) return expire(sub);

  sub.renewals += 1;
  return renew(sub, now);
}
```

Triggers are triggers, not bans: exceeding one requires a written justification
at the site or in review — an idiomatic exception with a stated reason passes.
