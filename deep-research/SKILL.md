---
name: deep-research
description: Conducts autonomous, multi-step deep research on complex topics using iterative planning, systematic exploration, source synthesis, and verified output generation. Use when the user asks for deep research, comprehensive analysis, literature review, technical investigation, due diligence, or any task requiring exhaustive multi-source information synthesis.
---

# Deep Research

Autonomous research agent that iteratively plans, searches, reads, verifies, and synthesizes findings into a comprehensive, cited report. Modeled on agentic research architectures: plan-driven, process-supervised, systematically exhaustive.

## Core loop

Execute this cycle until the research question is fully answered:

```
1. PLAN   → Break the question into sub-questions; identify knowledge gaps
2. SEARCH → Execute targeted queries for each sub-question (web, codebase, docs)
3. READ   → Ingest and extract key findings; track sources
4. VERIFY → Cross-check facts across sources; flag contradictions
5. ITERATE → Update the plan: mark answered sub-questions, add new ones from discoveries
6. OUTPUT → Synthesize into a structured, cited report only when stopping criteria are met
```

Repeat steps 1-5 until convergence. Do NOT jump to output prematurely.

## Research principles

1. **Systematic collation over keyword search** — Model the information space as a graph. Explore methodically: follow citation chains, navigate directory structures, check related entities. Never rely on a single search.
2. **Entity resolution** — Recognize when different sources describe the same entity/concept with different surface forms. Deduplicate and merge, don't inflate.
3. **Process supervision** — Evaluate each intermediate step. After every search/read cycle, ask: "Did this move me closer to a complete answer? What's still missing?"
4. **Epistemic stopping** — Distinguish *absence of evidence* (keep searching) from *evidence of absence* (conclude it doesn't exist). Stop when marginal returns from new queries drop below usefulness.
5. **Admit uncertainty** — If information cannot be found or verified, say so explicitly. Never fabricate or hedge with low-confidence padding.

## Workflow

### Phase 1: Scope and plan
- Clarify the research question with the user if ambiguous
- Decompose into 3-8 sub-questions covering distinct facets
- Identify the expected output format (report, comparison table, timeline, etc.)
- Present the plan to the user for approval before proceeding

### Phase 2: Investigate
- Execute searches for each sub-question using multiple query formulations
- Read and extract findings; maintain a running **master list** of facts + sources
- After each search-read cycle, self-evaluate:
  - Which sub-questions are answered? Which have gaps?
  - Did new findings reveal sub-questions not in the original plan?
  - Are any findings contradictory? If so, investigate further.
- Continue iterating until all sub-questions are satisfactorily covered

### Phase 3: Verify and synthesize
- Cross-reference key claims across independent sources
- Apply **Generator-Verifier-Reviser** pattern for critical findings:
  - Generate: draft the finding
  - Verify: check it against sources — is it accurate, complete, properly attributed?
  - Revise: fix any issues found; if fundamentally flawed, regenerate from scratch
- Resolve contradictions explicitly (explain the discrepancy, cite both sides)

### Phase 4: Output
- Structure the report with clear sections, headings, and logical flow
- Cite sources inline (links, file paths, or references)
- Include a confidence assessment for uncertain areas
- End with key takeaways and any remaining open questions

## Output format

Default to this structure unless user specifies otherwise:

```
## Executive summary
[2-4 sentence overview of findings]

## Findings
### [Sub-question 1]
[Findings with inline citations]
### [Sub-question 2]
...

## Contradictions / Uncertainties
[Any unresolved conflicts or gaps]

## Sources
[Numbered list of all sources consulted]
```

## Anti-patterns — avoid these

| Anti-pattern | Correct behavior |
|---|---|
| Single search, then synthesize | Multiple iterative searches with plan updates |
| Padding with low-confidence claims | Admit gaps; state what's unknown |
| Treating all sources as equal | Evaluate source reliability; prefer primary sources |
| Stopping at first plausible answer | Continue until marginal returns diminish |
| Monolithic unstructured output | Structured sections with inline citations |

See [REFERENCE.md](REFERENCE.md) for algorithmic foundations, advanced techniques, and the theoretical framework behind this methodology.
