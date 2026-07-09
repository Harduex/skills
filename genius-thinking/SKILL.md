---
name: genius-thinking
description: A structured deep-reasoning protocol distilled from the documented working methods of history's most exceptional thinkers (Einstein, Feynman, Darwin, Shannon, Poincaré, von Neumann) and from cognitive-science research on creative breakthrough. It replaces the default "first plausible answer" with forced problem interrogation, divergent generation, adversarial selection, and severe testing. Use this skill whenever the user asks for breakthrough or novel ideas, clever/elegant/non-obvious solutions, new algorithms or approaches, research-level problem solving, invention, "think harder", "think like a genius", "don't give me the generic answer" — or whenever a problem is genuinely hard, open-ended, or has resisted standard approaches, even if the user doesn't explicitly ask for deep thinking. Do NOT use for routine factual lookups, trivial fixes, or speed-sensitive tasks.
---

# Genius Thinking

## Why this skill exists

A model's default answer gravitates toward the statistical center of its training data — the most *typical* response. The thinkers this skill is modeled on were defined by systematic departures from typical thinking. Crucially, the historical record shows their breakthroughs came from reproducible *methods*, not mystique: Darwin imported a mechanism from economics, Shannon re-encoded logic as circuitry, Einstein ran physical scenarios to their extremes in his head, Poincaré generated combinations en masse and let an aesthetic filter select.

Therefore: **do not adopt a persona** ("I am now a genius"). Persona claims change tone, not reasoning. Instead, execute the process below. The process IS the genius.

Two load-bearing facts from the research (details in `references/research.md`):

1. **Simonton's equal-odds rule**: across the careers of eminent creators, hit *rate* is roughly constant — geniuses produced more hits by producing more attempts. Quality is a sampling problem. So: generate many genuinely different candidates before judging any.
2. **Problem-finding beats problem-solving**: Getzels & Csikszentmihalyi found that how long creators spent *formulating* the problem predicted the quality of the result. Einstein wrote that formulating a problem is often more essential than solving it. So: spend disproportionate effort on Phase 1.

## The Protocol

Run the phases in order. Do not skip Phase 1 or Phase 2 — those are where default (generic) answers are avoided. Full technique procedures live in `references/techniques.md`; read it when executing Phases 1–2 on a hard problem.

### Phase 1 — Interrogate the problem (before ANY solving)

1. **Restate from first principles.** Strip the problem to its fundamental constraints and quantities. Ask of each element: is this a law of nature, or a convention someone chose? (Feynman rebuilt every result he used from scratch; what you cannot rebuild, you do not understand.)
2. **Audit assumptions.** List every assumption embedded in the standard framing — including the ones so obvious they feel like facts. Mark each: *physical necessity* vs *inherited habit*.
3. **Find the crux.** Identify the single sub-problem that makes this hard — the one which, if solved, makes the rest routine (Hamming's discipline of attacking the important door, not the convenient one). Concentrate effort there; refuse to spread effort evenly.
4. **Define elegance before searching.** Write down the properties an ideal solution would have (simplicity, symmetry, generality, "obvious in retrospect"). Poincaré and Dirac used aesthetic criteria as a *selection instrument*, not decoration — you will use this list in Phase 3.
5. **Probe the extremes.** Set each key parameter to 0, 1, and infinity; delete each constraint one at a time and observe what becomes possible. Extreme cases expose the problem's true structure.

### Phase 2 — Diverge (quantity precedes quality)

Generate **at least 5 candidate approaches that differ in core mechanism**, not in implementation detail. Anchor-resistance rule: the first idea that comes to mind is almost certainly the training-data mode — write it down, label it "baseline / likely generic", and require every other candidate to differ from it structurally.

Force diversity by drawing each candidate from a different generator:

- **Inversion** (Jacobi's "invert, always invert"; Shannon's reversal strategy): solve the reverse problem, or ask "how would I guarantee failure?" and negate.
- **Cross-domain transplant** (Darwin ← Malthus's economics; Shannon ← Boolean algebra; Kepler, who called analogies his most faithful masters): pick 2–3 distant fields — evolution, markets, immune systems, thermodynamics, ecology, distributed protocols — and ask how each solves the structurally-analogous problem. Map *relations*, not surface features (Gick & Holyoak: transfer works only at the structural level).
- **Representation change** (Descartes' coordinates, Feynman's diagrams, Shannon's circuits): re-encode the problem as a graph, a geometry, a probability distribution, a physical system, a market. Some problems are hard only in their current notation.
- **Contradiction dissolution** (TRIZ, from Altshuller's study of ~40,000 patents): state the core trade-off as "improving X worsens Y", then look for moves that *dissolve* the trade-off (separate in time, space, scale, or condition) rather than balance it.
- **Janusian synthesis** (Rothenberg's studies of laureates): force two opposites to be simultaneously true and design the system in which both hold.

At least one candidate must feel uncomfortable to propose. Popper's engine of progress is the bold conjecture; a maxim Freeman Dyson championed applies — it is better to be wrong than to be vague. Label the bold one as speculative and propose it anyway.

### Phase 3 — Select adversarially

Generation and evaluation are different cognitive modes; never do them simultaneously.

1. For each candidate, state the **strongest objection a hostile expert rival would raise** — not a token weakness, the killing blow if there is one.
2. Apply **Darwin's golden rule**: actively hunt for evidence and cases *against* the candidate you currently like best, and write them down immediately (Darwin noted that unfavorable observations were exactly the ones memory lets slip).
3. Score survivors against the elegance criteria from Phase 1.4.
4. Kill without mercy, but **salvage fragments**: a dead candidate often contains one live mechanism — extract it and check whether it strengthens a survivor. Keep 1–2 survivors.

### Phase 4 — Develop via thought experiment

1. Run the survivor mentally at the extremes from Phase 1.5, plus adversarial inputs and degenerate cases (Einstein's method: idealize, push to the limit, watch for contradiction — the falling-observer experiment is the template).
2. **Feynman explanation test**: explain the solution in plain language as if to a bright newcomer. Every point where the explanation stumbles or hides behind jargon marks a real gap — return that specific piece to Phase 2.
3. Follow anomalies. Dunbar's in-vivo lab studies found that breakthroughs cluster around *unexpected* findings that researchers chose to chase rather than discard. If something in the development doesn't fit, that misfit is the most valuable object in the room.

### Phase 5 — Verify honestly

1. Design the **severe test**: state concretely what result or observation would falsify the solution (Popper). If nothing could, that is a defect — say so.
2. Separate, explicitly: what is established / what is inference / what is speculation.
3. State residual confusion openly. Comfort with unresolved doubt — Keats's "negative capability", Feynman's insistence on living with not-knowing — is a feature of strong thinkers, not a weakness to hide. Hamming's formulation: believe your idea enough to push it, doubt it enough to notice its flaws.

## Output contract

Unless the user asks otherwise, the final answer presents:

1. The reframed problem and the identified crux (brief).
2. The chosen solution, fully developed.
3. Why it beats the strongest alternatives — including a one-line epitaph for each killed candidate (this shows the search, and lets the user resurrect one).
4. The falsification test and confidence level, with speculation clearly flagged.

Do not dump the whole protocol transcript on the user; show the distilled result of it.

## Traits to embody while executing (from the biographical record)

- **Stay in the confusion.** Do not grab premature closure; the discomfort of an unresolved problem is the working state (Newton kept problems "constantly before me" until light dawned; Poincaré's insights arrived only after long saturation).
- **Courage over vagueness.** Commit to specific, checkable claims.
- **Consensus is data, not verdict.** Expert opinion earns weight, not deference (Feynman: science is belief in the ignorance of experts).
- **Chase the detail that doesn't fit.** Anomalies outrank confirmations.
- **Play.** Feynman's Nobel-line work started with idly analyzing a wobbling cafeteria plate. Permit at least one playful, "silly" candidate in Phase 2 — treat it seriously enough to find out what's inside it.

## Anti-patterns — never do these

- Persona cosplay ("Speaking as Einstein…"). Changes voice, not thought.
- Converging on the first idea, or generating five superficial variants of it.
- Listing textbook approaches when the user signaled they already know them.
- Hedged mush that commits to nothing (violates courage-over-vagueness).
- Equal effort everywhere instead of crux concentration.
- Hiding uncertainty to appear more impressive — falsifies Phase 5 and destroys trust.

## Calibration — matching depth to the problem

- **Hard / open-ended / user asked for brilliance** → full protocol, and read `references/techniques.md` for the detailed procedures.
- **Medium difficulty** → light pass: assumptions + crux (Phase 1), 3 candidates (Phase 2), hostile review (Phase 3).
- **Routine** → this skill should not have triggered; answer directly.

## References

- `references/research.md` — the evidence base: per-thinker case studies and the cognitive-science findings, with the operational lesson each yields. Read when you need to justify or deepen a method, or when the user asks where this comes from.
- `references/techniques.md` — step-by-step procedures for every technique named above, with worked micro-examples. Read when executing the full protocol.
