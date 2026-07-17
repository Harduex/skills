---
name: using-evolving-harness
description: Master router for the Evolving Harness framework. Consult this skill at the start of ANY non-trivial software task - a new feature, refactor, bug fix, migration, or raw idea - to route the work through the correct lifecycle skills with explicit approval gates, and again before ending a session to run the evolution loop that turns the session's lessons into skill improvements. Use it whenever you are unsure which skill applies, in what order phases run, or whether a phase can be skipped.
---

# Using the Evolving Harness

You are operating inside the Evolving Harness framework. Work moves through
phases; each phase is owned by a skill and ends at a gate. Do not skip gates.
Do not merge phases.

## Lifecycle routing

| Phase | Owning skill | Enter when | Exit gate |
|---|---|---|---|
| 1. Frame | idea-to-plan | Raw idea or vague request | Human approves the plan outline |
| 2. Design | designing / architecting -> write-design-spec | Approved outline | Human approves the design spec |
| 3. Plan | planning | Approved design spec | Task list with verification steps exists |
| 4. Test-first | write-test-cases | Plan approved | Failing tests exist for the first task |
| 5. Build | autonomous-build-loop (debugger on failure) | Failing tests exist | verify-before-done passes |
| 6. Review | code-review -> review-fix-loop | Build gate passed | No open review findings |
| 7. Land | checkpoint (+ git-ops skills if installed) | Review clean | Work committed with clean history |

Rules:

- One phase at a time. If a request arrives mid-lifecycle, locate the current
  phase and resume there - do not restart from phase 1.
- Trivial tasks (typo fix, one-liner) may jump to phase 5, but the phase-5
  exit gate (verify-before-done) still applies. Say explicitly that you are
  taking the trivial path.
- If a phase's owning skill is not installed, say so and proceed with best
  judgment for that phase - never silently improvise while implying the skill
  ran.
- Every human approval gate is a real stop: present the artifact, wait.

## The evolution loop (session end - this is the point of the framework)

Before ending any substantial session:

1. Run **save-learned-lessons**: capture corrections the human made, failures,
   and surprises from this session as candidate lessons.
2. If a repeated workflow emerged, run **extract-skill-from-session** to draft
   it as a new skill.
3. A lesson or drafted skill only graduates into the repo after it passes
   evals: should-trigger and should-not-trigger prompts, plus a regression
   check against past sessions (see **optimizing-skill-repo**). No eval, no
   merge.
4. Periodically run **analyze-agent-sessions** and **optimizing-skill-repo**
   to prune, merge, and re-tune skill descriptions across the repo.

Treat every agent mistake as a permanent signal: it must end as a skill edit,
a new skill, or an explicit recorded decision not to encode it.

## When NOT to use this framework

Pure Q&A, explanations, or research with no artifact to ship - route to the
thinking bundle (deep-research, grill-me, zero-assumptions) instead.
