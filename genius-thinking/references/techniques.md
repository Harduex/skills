# Techniques Playbook

Step-by-step procedures for the methods named in SKILL.md. Each entry: procedure → micro-example → when to reach for it.

Contents: 1. Assumption audit · 2. Crux isolation · 3. Elegance criteria · 4. Extreme probing · 5. Inversion · 6. Cross-domain transplant · 7. Representation change · 8. Contradiction dissolution (TRIZ) · 9. Janusian forcing · 10. Rising-sea generalization · 11. Thought-experiment construction · 12. Cold re-approach · 13. Feynman explanation test · 14. Disconfirmation log · 15. Shannon's checklist · 16. Fragment salvage

## 1. Assumption audit

1. Write the problem as usually stated.
2. Underline every noun and constraint; for each, ask "who decided this, and does physics/math require it?"
3. Sort into: **hard** (law of nature, mathematical necessity, explicit user requirement) vs **soft** (convention, habit, "how it's always done", unstated default).
4. For each soft assumption, note in one line what becomes possible if it's dropped.

*Micro-example:* "Make this API faster." Soft assumptions found: responses must be computed at request time (→ precompute/cache), the client needs the full object (→ send a diff), one request = one response (→ stream partials), the caller must wait (→ async + webhook). Four solution families appear before any profiling.

**Reach for it:** always — it is the cheapest generator of non-obvious options.

## 2. Crux isolation

Ask, in order: (a) If I had an oracle for one sub-problem, which one makes everything else routine? (b) What has actually killed previous attempts — is it the same wall each time? (c) Am I avoiding a sub-problem because it's hard? (Hamming: the important door, not the convenient one.)
Output: one sentence — "This is hard because ___." All Phase-2 candidates must attack that sentence.

*Micro-example:* "Build a recommender for a brand-new marketplace" → the crux is not the model, it's cold-start: zero interaction data. Candidates must attack cold-start (content features, transfer from a related corpus, incentivized exploration), not fight over ranking architectures.

## 3. Elegance criteria (define before searching)

Write 3–5 properties the ideal solution would have. Useful vocabulary: *simple* (fewest moving parts), *symmetric* (handles all cases by the same mechanism, no special-casing), *general* (solves the neighbors of the problem too), *inevitable* ("obvious in retrospect"), *generative* (opens further moves). These become scoring axes in Phase 3 — Poincaré's filter, made explicit.

## 4. Extreme probing

For each key parameter: set it to 0, 1, and ∞ and ask what the problem becomes. Delete each constraint one at a time; note which deletion makes the problem trivial — that constraint is where the difficulty lives, so attack *it*.

*Micro-example:* Scheduling meetings across time zones. Zero participants: trivial. Two: an interval intersection. Infinite: no common hour exists → the real problem is fairness of rotation, not slot-finding. The ∞ case reveals the honest problem statement.

## 5. Inversion

1. State the goal. 2. Invert: "How would I *guarantee* failure / achieve the opposite?" 3. Enumerate failure-guaranteeing moves concretely. 4. Negate each into a design constraint or a candidate mechanism. Variant (Shannon): solve the reverse problem (decompress instead of compress, verify instead of generate) — the reverse is often easier and its solution maps back.

*Micro-example:* "Design an onboarding users complete." Inverted: guarantee abandonment → demand data before showing value, add steps with invisible progress, require email verification mid-flow. Negations: value-first ordering, visible progress, defer verification to after the first success moment.

## 6. Cross-domain transplant (structural analogy)

Gick & Holyoak's finding: transfer fails on surface features and succeeds on structure. So:
1. Abstract the problem into a relational skeleton: entities → relations → constraint → objective, with domain nouns removed.
2. Pick 2–3 distant donor fields. Default roster: evolution/immune systems, markets/auctions, thermodynamics/annealing, epidemiology, ecology, distributed systems/protocols, control theory, city planning, jazz improvisation.
3. Find the donor's structure that matches the skeleton; import its *mechanism*.
4. Kepler's step: mark exactly where the analogy breaks, and treat the break as information about your problem.

*Micro-example:* "Allocate compute among competing internal teams" → skeleton: scarce divisible resource, self-interested claimants, private valuations, recurring rounds. Donor (auctions): second-price mechanisms elicit honest valuations. Import: internal token-budget auction. Break point: teams aren't firms — collusion and politics differ → add budget decay to prevent hoarding. The break produced the second feature.

## 7. Representation change

Ask: what is this problem when written as — a graph? a geometry? a probability distribution? a physical system (flows, forces, energy minima)? a market? a state machine? an information channel? Pick the encoding in which the *crux* becomes a named, solved object.

*Micro-example:* "Detect circular ownership among shell companies" is tangled as table joins; as a directed graph it is literally cycle detection — a solved problem with linear-time algorithms. The difficulty was the notation.

## 8. Contradiction dissolution (TRIZ-style)

1. State the trade-off: "Improving X worsens Y."
2. Refuse the compromise; ask for both.
3. Try the separations: in **time** (X now, Y later — e.g., write fast to a log, restructure asynchronously), in **space** (X here, Y there — hot path vs cold path), in **scale** (X at the component level, Y at the system level — cheap unreliable parts, reliable whole: RAID, TCP), by **condition** (X in mode A, Y in mode B — adaptive systems).
4. Sample principles from Altshuller's list worth trying directly: segmentation, inversion, merging, nesting, dynamization, self-service (the harmful thing does useful work), intermediary, cheap disposables.

*Micro-example:* "Thorough code review vs shipping speed." Separate in scale: machines review exhaustively at the line level, humans review only architecture; in time: ship behind a flag now, deep-review before flag flip. The trade-off dissolves instead of being split.

## 9. Janusian forcing

1. Take the two opposites the problem seems to force a choice between. 2. Assert both simultaneously as a design requirement. 3. Ask what system makes both literally true (usually via different levels, frames, or observers — Bohr's complementarity; Einstein's falling man both moving and at rest).

*Micro-example:* "The database must be strongly consistent AND always available." Both true — at different grain: per-key linearizability with cross-key eventual consistency; or consistent core, available cache with bounded staleness contracts. The forced conjunction generated the architecture.

## 10. Rising-sea generalization (Grothendieck)

When direct attack stalls: 1. Ask "what is this a special case of?" 2. Climb one or two abstraction levels. 3. Check whether the general problem has known structure or is — surprisingly often — *easier* because irrelevant detail fell away. 4. Descend with the general solution.

*Micro-example:* "Merge these two customer-record formats" resists as a one-off; generalized to "define a schema-mapping algebra with conflict-resolution policies", each concrete merge becomes a configuration. Also the difference between inventing an answer and inventing a *method*.

## 11. Thought-experiment construction (Einstein pattern)

1. Idealize: strip friction — infinite resources, perfect components, zero latency. 2. Push one variable to its limit. 3. Hunt for a contradiction between two principles you believe. 4. The contradiction localizes the breakthrough: one principle must bend — decide which, and that decision *is* the insight. Then re-add the friction and check survival. Tesla's variant: run the design under load, over time, in imagination; watch for wear.

## 12. Cold re-approach (incubation for agents)

An agent cannot sleep on a problem, but the incubation literature says the benefit is largely *fixation release* — dropping a wrong frame. Emulate: after a full attempt, deliberately restart from a blank slate in a *different representation* (technique 7) or from the inverted problem (technique 5), forbidding reuse of the first attempt's framing. Compare results only afterwards.

## 13. Feynman explanation test

Explain the chosen solution in plain language, to an imagined bright newcomer, with no jargon. Rules: every "obviously" is a red flag; every place the explanation reaches for a technical term as a *shield* rather than a shorthand marks a gap. Route each gap back to Phase 2 as its own micro-problem. A solution that cannot be explained simply is not yet understood — treat that as a finding, not an embarrassment.

## 14. Disconfirmation log (Darwin's golden rule)

While developing the favored candidate, keep a running list titled "evidence against". Every counter-case, awkward fact, or edge that doesn't fit gets written *at the moment it appears* (Darwin: hostile facts are precisely the ones memory drops). Before finalizing, the log must be answered item by item — refuted, absorbed, or conceded as an open limitation in the final answer.

## 15. Shannon's checklist (1952, near-verbatim)

Run down when stuck: **Simplify** — strip the problem to its essential core, even losing realism, solve that, then add reality back. **Similar problems** — what known solved problem is this shaped like? **Restate** — say it in several different vocabularies. **Analyze structurally** — break into parts; solve the parts. **Invert** — solve it backwards. **Generalize** — once any specific answer exists, widen it.

## 16. Fragment salvage

When killing a candidate in Phase 3, extract before burial: (a) any mechanism that worked locally, (b) any constraint it revealed, (c) any question it raised. Keep a fragment list; before finalizing, scan it once — da Vinci's notebooks in miniature. Hybrids of a survivor plus a dead candidate's organ are a common source of the actual winner.

---

## Phase quick-reference card

- **Phase 1:** techniques 1, 2, 3, 4 (audit, crux, elegance, extremes)
- **Phase 2:** techniques 5–10, 15 (the generators; ≥5 mechanism-distinct candidates, one bold)
- **Phase 3:** techniques 14, 16 + hostile review + elegance scoring
- **Phase 4:** techniques 11, 12, 13 (stress, cold re-approach, explanation test)
- **Phase 5:** falsification design + established/inferred/speculative labeling
