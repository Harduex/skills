# Deep Research Reference

Algorithmic foundations and advanced techniques underlying the deep research methodology. This reference distills concepts from inference-time scaling research, process-supervised reasoning, and agentic information synthesis architectures.

## Algorithmic foundations

### The Plan-Search-Read-Iterate-Output pipeline

Research is not a single-pass operation. The pipeline operates as a **stateful loop**, where each cycle refines the agent's understanding:

- **Plan**: Formulate causal-chain search strategies. Identify what you know, what you don't, and what you need to find next. Each plan update should be informed by prior findings.
- **Search**: Execute targeted queries. Use multiple formulations — synonyms, related terms, domain-specific jargon. Aim for 5-15 distinct queries per sub-question for complex topics.
- **Read**: Extract structured findings. Don't just skim — identify claims, evidence, methodology, and limitations. Track the source for every fact.
- **Iterate**: Evaluate progress. Update the plan based on what was found. Add new sub-questions that emerged. Mark resolved items. This is the critical feedback loop.
- **Output**: Synthesize only when the stopping criteria are met. The output phase is terminal — don't enter it prematurely.

### Inference-time scaling

Intelligence in research tasks scales with **deliberation time**, not just model size. Key implications:

- Spending more computation on reasoning (exploring alternatives, verifying steps, backtracking from dead ends) systematically improves output quality.
- A single fast answer is almost always worse than an iterative, self-correcting investigation.
- The agent should **invest time proportional to question complexity** — trivial sub-questions get quick answers; complex ones get deep investigation.

## Core techniques

### 1. Systematic collation (graph-based exploration)

**Problem**: Keyword search is brittle. A single query hits only one slice of the information space. Critical information is fragmented across many sources.

**Solution**: Treat the information space as a directed graph:

- Each source is a **node**. Links, citations, and references are **edges**.
- After finding a relevant source, follow its outbound edges: cited references, linked pages, related documents, author's other work.
- Maintain an **exploration map** — track which nodes have been visited and which remain unexplored.
- Systematically visit unvisited nodes until the graph is sufficiently covered.

**Practical application for an agent**:
- After reading a key source, extract 2-3 follow-up queries from its content (terms, entities, cited works).
- Check "neighboring" information: same author, same publication, same topic category.
- Don't stop at page 1 of search results — reformulate queries to reach different parts of the graph.

### 2. Entity resolution and deduplication

**Problem**: The same concept appears under multiple names across sources. Without resolution, the findings list inflates with duplicates that look different but mean the same thing.

**Solution**:
- Before adding a finding to the master list, check if a semantically equivalent entry already exists.
- Merge entries that refer to the same entity, concept, or data point — even if the surface form differs (e.g., "Q3 2024 revenue" vs. "third quarter top-line earnings 2024").
- When merging, keep the most precise/authoritative version and note the alternative forms.
- Flag genuinely distinct items that _look_ similar but differ in important ways.

### 3. Epistemic stopping criteria

**Problem**: In open-ended research, the search space is effectively infinite. The agent must decide when to stop without external termination signals.

**Three-signal stopping heuristic**:

1. **Saturation**: New searches return information already in the master list. The marginal value of additional queries approaches zero.
2. **Coverage**: All sub-questions in the plan have at least one well-supported answer. No critical gaps remain.
3. **Convergence**: Multiple independent sources agree on key findings. The confidence distribution has stabilized.

**Critical distinction**: "I haven't found it yet" (absence of evidence — keep searching with different queries) vs. "I've exhaustively searched likely sources and it doesn't exist" (evidence of absence — document this conclusion and stop).

### 4. Process supervision (step-level self-evaluation)

**Problem**: Evaluating only the final output misses intermediate errors that compound. A wrong turn early in research can cascade into a fundamentally flawed report.

**Solution**: After every discrete step (each search, each document read, each synthesis attempt), evaluate:

- **Relevance**: Did this step produce information relevant to a sub-question?
- **Progress**: Did the master list meaningfully change? If not, why?
- **Direction**: Is the current search trajectory productive, or should I pivot?
- **Consistency**: Do new findings contradict existing ones? If so, investigate.

If 2-3 consecutive steps produce no meaningful progress, **change strategy**: reformulate queries, try different source types, or reconsider the sub-question framing.

### 5. Generator-Verifier-Reviser pattern

For high-stakes findings or synthesis sections, apply a three-pass quality loop:

| Role | Action | Routing |
|---|---|---|
| **Generator** | Produce the initial draft of a finding or section | Always runs first |
| **Verifier** | Critically examine the draft: Is it accurate? Complete? Properly cited? Does it contain unsupported claims? | If correct → output. If minor issues → Reviser. If fundamentally flawed → restart Generator. |
| **Reviser** | Apply targeted fixes without discarding valid work | Send back to Verifier for re-check |

**When to apply this pattern**:
- Synthesizing contradictory sources
- Making quantitative claims
- Drawing causal conclusions
- Writing the executive summary

**When to skip it** (simple cases):
- Reporting a single undisputed fact from a reliable source
- Listing items without interpretation

### 6. Hypothesis branching

When the evidence is ambiguous or the research question has multiple valid interpretations:

- **Branch**: Formulate 2-3 competing hypotheses
- **Investigate each**: Seek evidence for and against each hypothesis independently
- **Evaluate**: Which hypothesis has the strongest evidentiary support?
- **Report**: Present the winner with confidence level, but acknowledge alternatives

This prevents premature commitment to a single narrative and reduces confirmation bias.

## Quality checklist

Before delivering the final output, verify:

```
[ ] All sub-questions from the plan are addressed (or explicitly marked as unanswerable)
[ ] Every factual claim has at least one cited source
[ ] Contradictions between sources are acknowledged and discussed
[ ] No unsupported speculative claims (or clearly labeled as speculation)
[ ] Entity resolution applied — no inflated/duplicate findings
[ ] Stopping criteria met — additional searching would yield diminishing returns
[ ] Structure matches the agreed output format
[ ] Confidence levels stated for uncertain areas
```

## Failure modes to recognize

| Failure mode | Symptom | Recovery |
|---|---|---|
| **Tunnel vision** | All searches use similar terms; only one perspective found | Reformulate with antonyms, adjacent domains, or opposing viewpoints |
| **Infinite recursion** | Each search spawns more sub-questions without convergence | Apply stopping criteria; prioritize sub-questions by relevance |
| **Authority bias** | Over-reliance on a single "authoritative" source | Seek independent corroboration from at least 2 other sources |
| **Hedging** | Padding the report with low-confidence, irrelevant findings to appear thorough | Remove findings below a usefulness threshold; admit gaps instead |
| **Premature synthesis** | Jumping to conclusions before sufficient evidence is gathered | Check coverage against the plan; if sub-questions remain open, continue investigating |
| **Scope creep** | Research expands into tangentially related areas | Refer back to original question; only expand scope if user approves |
