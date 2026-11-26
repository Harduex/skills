---
name: using-evolving-harness
description: Master router for the Evolving Harness framework. Routes a software task through lifecycle phases, each owned by a skill and closed by an approval gate, and runs the evolution loop that turns a session's lessons into skill improvements. Use when the user asks to use the evolving harness or this framework, invokes this skill by name, or a hand-off note or build log says the work runs under it.
---

# Using the Evolving Harness

You are operating inside the Evolving Harness framework. It is opt-in: it runs
because the user asked for it, and from then on it governs the task until the
work lands, across sessions too. Work moves through phases; each phase is owned
by a skill and ends at a gate. Do not skip gates. Do not merge phases.

Other workflow frameworks may be loaded at the same time. This one neither
replaces nor forbids them. When another loaded workflow covers the same step,
use this phase's owning skill for that step.

## Lifecycle routing

| Phase | Owning skill | Enter when | Exit gate |
|---|---|---|---|
| 1. Research + brainstorm | idea-to-plan (researching or deep-research for unknowns) | Raw idea or vague request | Human approves a direction |
| 2. Design | designing-ux / architecting -> write-design-spec (prototyping-ui, write-a-ticket as needed) | Approved direction | Human approves the design spec |
| 3. Plan | planning -> a review of the plan in a fresh context -> the build loop's pre-flight scan | Approved design spec | The scan's rulings are in the build log |
| 4. Build | autonomous-build-loop (debugger on failure) | Plan scanned | verify-before-done passes |
| 5. Simplify | code-simplification | Build gate passed | Human has picked the items to apply |
| 6. Review | code-review -> review-fix-loop | Simplification applied | No open Critical or High finding |
| 7. Break | break-testing | Review clean | Nothing found is left broken |
| 8. Land | distribute-fixups -> linear-git-history -> drop commit or ADR (write-design-spec) -> human test -> retro | Break clean | Human has tested |

Each phase checks the one before it: Review checks the simplification, and
the break pass runs last, on the final code. Rules:

- One phase at a time. If a request arrives mid-lifecycle, locate the current
  phase and resume there - do not restart from phase 1.
- Phase 1 uses idea-to-plan only up to the approved approach; its own spec and
  plan steps belong to phases 2 and 3.
- Trivial tasks (typo fix, one-liner) may jump to phase 4, but the phase-4
  exit gate (verify-before-done) still applies. Say explicitly that you are
  taking the trivial path.
- Across sessions, hand off with checkpoint. The note's first step loads this
  skill, and it names the skills the next phase needs.
- Product and behavior questions collected during the build reach the human
  as one batch before the human test in phase 8.
- If a phase's owning skill is not installed, say so and proceed with best
  judgment for that phase - never silently improvise while implying the skill
  ran.
- Every human approval gate is a real stop: present the artifact, wait.

## Paper-trail commits

Planning artifacts leave the tree when the work closes, but git history keeps
them. A branch follows one commit shape: planning -> code -> drop or ADR.

1. Commit every pre-build artifact (research, design spec, test plan,
   implementation plan) first, as one or two `<ticket> … planning` commits.
2. Commit each later artifact edit as `git commit --fixup=<planning-commit>`.
   Never mix an artifact edit into a code commit (distribute-fixups).
3. Squash the fixups with a non-interactive autosquash rebase, at the latest
   before review.
4. To keep the spec's evolution on a long branch, commit with
   `git commit --squash=<planning-commit>` and a message that says what
   changed and why. Run that rebase with `GIT_EDITOR=true` as well.
5. At branch close, delete the artifacts in one commit: the commit that adds
   the ADR (write-design-spec), or a `<ticket> Drop … planning artifacts`
   commit when the branch needs no ADR. Its message says that git history
   keeps them.
6. Merge without squashing. A squash merge folds the add and the delete into
   nothing, so no artifact reaches the main branch.

End state: each artifact has two commits on the main branch, one that creates
it and one that deletes it. To restore an artifact, find the deleting commit
with `git log --diff-filter=D -- <path>`, then run `git show <sha>^:<path>`.

## The evolution loop (session end - this is the point of the framework)

Before ending any substantial session:

1. Capture corrections the human made, failures, and surprises as candidate
   lessons. A single-session task runs **save-learned-lessons**. A feature that
   spans several sessions records them as ruling lines in the build log as they
   happen, then runs one **analyze-agent-sessions** retro at Land; the retro is
   a proposal, applied only where the human agrees.
2. If a repeated workflow emerged, run **extract-skill-from-session** to draft
   it as a new skill.
3. A lesson or drafted skill only graduates into the repo after it passes
   evals: should-trigger and should-not-trigger prompts, plus a regression
   check against past sessions (see **optimizing-skill-repo**). No eval, no
   merge.
4. Periodically run **analyze-agent-sessions** and **optimizing-skill-repo**
   to prune, merge, and re-tune skill descriptions across the repo.

Treat a repeated agent mistake as a signal: it ends as a skill edit, a new
skill, or a recorded decision not to encode it. A one-off mistake is not a
signal.

## When NOT to use this framework

Pure Q&A, explanations, or research with no artifact to ship - route to the
thinking bundle (deep-research, grill-me) instead.
