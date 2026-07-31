# Review Mode: Auditing Against the Standard

Scope: this checklist audits **standards compliance** — naming, structure,
prose, error quality. It complements a correctness review (bugs, security,
data integrity); it never replaces one. Run your set's code-review capability
for correctness; run this for the standard.

## Workflow

1. Load the band checklists below; have [NAMING.md](NAMING.md) vocabulary
   tables at hand.
2. Sweep the diff band by band: N → S → M → W → P → C. Coverage comes from the
   bands, not from reviewer taste.
3. A candidate finding must name the rule ID it violates, or it is dropped.
   Taste is not a finding.
4. One confirmed instance → sweep the whole diff for the same class and report
   it as one finding listing every site.
5. Rank findings by severity; output in the format below.

## Finding format

`**[F#] [BLOCKER|ISSUE|SUGGESTION] [<ruleID>] path:line — Short title**`
then one sentence naming the defect, and the suggested fix.

Severity semantics (shared with the code-review capability):

- **BLOCKER** — bugs, security, data-loss risk. A W1 severity inflation or
  burial that hides one of these is itself a BLOCKER.
- **ISSUE** — verified standard violations and divergence from siblings.
- **SUGGESTION** — improvement that still passes the bar.

There is no NITPICK tier: anything that would earn it either maps to a rule
(then it is an ISSUE/SUGGESTION with that rule ID) or gets dropped.

## Band checklists

**N — Names**
- Does any new name alias an existing concept? (N3)
- Any banned vague word from the NAMING.md table? (N1)
- Any noun-named function, verb-named type, non-predicate boolean? (N4)
- Any compound name over 3 words? (N6)
- Any name the ticket introduced that contradicts the codebase term? (N3)
- Any unexplained abbreviation, joke, or regionalism? (N7)
- Spelling locale consistent? (N9)

**S — Statements & functions**
- Function over 25 lines / 4 params / nesting 2 without justification? (S1)
- Any statement doing two things — mutation inside a condition, chained side effects? (S2)
- Guards after the action instead of first? (S4)
- Hidden control flow — implicit hooks, action-at-a-distance? (S5)
- Meta-programming where a plain function works? (S6)
- A class whose only job is running one action? (S7)
- Compressed one-liners that trade clarity for brevity? (S8)
- Three or more parallel branches inlined instead of vertical/data-driven? (S9)

**M — Modules**
- More than one topic in the file/class? (M1)
- File > 400 lines or class > 7 public members, unjustified? (M2)
- Helpers above the public surface? (M3)
- Structure diverges from the closest sibling without a reason? (M4)
- Hidden or cyclic dependencies? (M5)

**W — Errors & logs**
- Any level mismatching W1 semantics (error that isn't a failure, failure logged as info)? (W1)
- Any message that doesn't open with the concrete condition or command? (W2)
- Any failure message that omits the consequence? (W3)
- Any comment or info-log carrying an instruction the reader must obey? (W4)

**P — Prose**
- Instructions not numbered/imperative/condition-first? (P2)
- Sentences over the 20/25-word caps; paragraphs over 6 sentences? (P1, P3)
- Dangling "it"/"this" with two possible referents? (P4)
- Identifiers paraphrased instead of quoted? (P5)
- Latin abbreviations? (P6) Non-inclusive terms? (P7)
- Commit subject not one imperative sentence? (P8)

**C — Consistency**
- Same problem solved differently than the closest sibling, no reason stated? (C1)
- A rename that word-swapped instead of renaming by meaning? (C2)
- Idiom-dependent names — `spinUp`, `kickOff`, `windDown`? (C3)
- New domain term used without a glossary entry? (C4)
- A term that already means something else on this platform? (C5)

## Numeric triggers

| Trigger | Rule |
|---|---|
| function > 25 lines | S1 |
| function > 4 parameters | S1 |
| nesting > 2 levels | S1 |
| file > 400 lines | M2 |
| class > 7 public members | M2 |
| compound name > 3 words | N6 |
| instruction sentence > 20 words | P1 |
| descriptive sentence > 25 words | P1 |
| paragraph > 6 sentences | P3 |

Exceeded + no written justification = ISSUE. Exceeded + stated reason = passes.
