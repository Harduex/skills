---
name: investigate-before-asking
description: "Use when a design, spec, or integration carries unknowns about an external or unfamiliar system — another team's codebase, service, API, wire format, schema, or closed package — and before asking the owning team anything. Also when TBDs block finalizing a design, when a claim about an external system's behavior needs verification, or when asked whether enough information exists to finalize. Covers anything discoverable from researchable artifacts: local checkouts, org code hosting, issue trackers, git history, live databases, docs and wikis."
---

# Investigate Before You Ask

Understanding an external system is **your** job, not the owning team's. Reconstruct its real behavior from artifacts; cross a team boundary only with questions that cannot be answered any other way. The result is evidence-grounded knowledge and near-zero coordination drag — every question you answer yourself stays off another team's calendar.

## The Iron Rule

**Source locally before remotely, and verify the unknown's own premise before hunting its answer.**

- A repo you're about to search on the org code host may already be cloned on this machine — check the local projects directories **first**, sync the checkout, then read it there. Remote API search while a local checkout exists is the failure this skill exists to prevent.
- The claim embedded in the question ("X stores that in Y") is itself unverified. Test the premise first — it is wrong or half-wrong often enough that answering the literal question wastes the investigation.

## Workflow

1. **Enumerate and classify every unknown.** Three bins: *inferable from artifacts* (research it), *owner-must-confirm* (code can narrow it, only the owner can commit to it), *decision-not-fact* (product/PM calls — route to humans immediately; do not research what is not a fact).
2. **Verify premises** for each inferable unknown before chasing answers.
3. **Walk the source ladder, cheapest first.** Read [`ATLAS.md`](ATLAS.md) beside this skill first — it maps where truth lives for this org. A fresh install ships it as a self-describing skeleton: fill it in for your org, and grow it as investigations teach you the map. Ladder: local checkouts, plus the in-repo docs/wikis and self-describing API schemas (e.g. an OpenAPI endpoint) that ride along (sync before use) → git archaeology — `log`, `blame`, `reflog`, commit messages, MR/issue discussions — for *when and why* something changed → live database/schema → org code host and issue tracker → a time-boxed spike or learning test against the real dependency (unexercised rung — expand it the first time an investigation needs one) → the owning team, approached last with a concrete, reproducible question.
4. **Bound every fetch.** Size-check a repo via the host API before cloning; default to shallow (`--depth 1`) or sparse (`--filter=blob:none --sparse`) clones scoped to the directories you need.
5. **Fan out parallel read-only investigators**, one per evidence domain (a codebase, a tracker, a database), using the dispatch brief below. For a deep single-repo dig, invoke your set's codebase-research capability inside the investigator.
6. **Grade the evidence, issue verdicts, write the ask-list** per the output contract.

## Dispatch brief (include verbatim in every investigator prompt)

> Research task, read-only. Report raw findings with repo, file path, and line numbers; quote verbatim code/comment snippets for load-bearing claims. Flag anything uncertain as UNVERIFIED with the reason. Distinguish what the code *defines* from what live data *contains*. Check whether a code path has runtime consumers before treating it as live behavior. Do not propose designs.

## Evidence ladder and traps

| Rank | Evidence | Trap it guards against |
|---|---|---|
| 1 | Wire contract / type definition | proves a field *cannot* exist, where data sampling only shows it *doesn't currently* |
| 2 | Source code with live callers | **dead-code trap**: a convincing code path with zero runtime consumers describes nothing |
| 3 | Live data sample | carries a mandatory caveat — this environment's data may not represent production |
| 4 | Code comment / doc / commit message / MR discussion | often stale; grade below the code it describes |
| 5 | Inference / derivation | label it as yours ("derivation, not a code comment") |

An **empirical constant** in code ("works, unclear why", magic offsets) is a signpost: ground truth lives in a system someone else owns — hunt *that* repo before adopting the constant. Likewise a **closed package or binary** is not a dead end: its source repo usually exists somewhere findable on the org host — hunt it before declaring a fact unknowable.

## Red flags — stop and course-correct

| Rationalization | Reality |
|---|---|
| "Faster to just ask the owning team" | Your question joins their queue for days; the artifact answers in minutes and more precisely |
| "The host API search is right here" | Check the local projects directories first — the clone may already exist |
| "The lead already explained how it works" | That is a premise, not a fact — verify it; secondhand models are half-wrong often enough |
| "The comment/doc says so" | Grade it: below code, below contracts |
| "The data shows no such field" | Data-level absence ≠ contract-level impossibility — find the type/schema that proves it |

## Output contract

Per unknown: **verdict** (`answered` / `owner-must-confirm` / `decision-not-fact`) · the evidence with file:line references · explicit caveats (UNVERIFIED items, environment limits). Then the **ask-list**: only the non-inferable residue, each entry naming the owning team, the existing ticket it rides on, and the concrete question — phrased so it is quick to answer and impossible to misunderstand. Investigator caveats are binding: re-read them before acting on any conclusion they qualify. A source location discovered during the hunt becomes an `ATLAS.md` row — the atlas grows by rule, not by memory.

## Soft links

- Deep comprehension of one codebase → your set's codebase-research capability.
- Org code-host operations (search, clones, MR/issue reads) → your set's code-hosting skill, if present.
- Database/schema digging → your set's schema-operations skill, if present.
