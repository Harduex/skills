---
name: extract-skill-from-session
description: Turn a workflow you just ran — with the corrections that shaped it — into a reusable skill. Use when you ask whether a good session is worth a new skill or an update, when extracting a repeatable process from past sessions, or when deciding if a learning belongs in a skill versus a script, an AGENTS.md note, or memory.
---

# Extract Skill From Session

Crystallize a *proven* workflow — and the corrections that shaped it — into a skill. The session was the experiment; this turns the result into something reusable.

This is an **orchestrator**: it encodes only the judgment the mining/authoring skills don't, and links the rest by capability. **Decline-to-build is a valid outcome** — most of what feels skill-worthy mid-session isn't.

**Link by capability, not by name** (names drift between sets and projects; capabilities don't). Resolve each to a skill in your current set by its description; if none exists, do that step inline:
- **mine a past session's transcript** → a session-analysis capability
- **route a single fact/lesson to its home** → a lesson-capture capability
- **author the skill's structure/frontmatter** → a skill-writing capability
- **audit a skill for compliance/concision** → a skill-auditing capability

## When to use / not

Use when a workflow has **converged** — you re-derived or corrected it enough that codifying beats re-deriving. **Not** for a one-off, not before it has stabilized, and not for a single fact or preference (that is the lesson-capture capability, not this). The honest test: *would a future session redo this from scratch without it?*

## 0 · Classify before you build

1. **Skill-worthy at all?** Drop from consideration anything code/git-discoverable, already encoded elsewhere, or machine-specific; drop **temporary/in-flight** detail entirely (it dies with the branch).
2. **Is it a workflow?** This skill handles a repeatable, multi-step **workflow** (→ a skill) or a proven deterministic **command** (→ a script the prose references). Anything atomic — an always-on rule, a project convention, a situational fact, a piece of history — is a *lesson*: hand it to the lesson-capture capability, which owns routing it (global instructions / AGENTS.md / memory / docs), and **stop**. The dividing line is the **unit of work** — a process vs a fact; frequency then decides skill-vs-a-few-AGENTS-lines.
3. **New skill vs extend one.** Extend the skill whose triggers already cover the domain — don't fragment one workflow across two. Mint new only for a distinct goal + mechanics; if you can't confirm an existing owner, default to a new skill and ask before folding into another. Keep each single-purpose; cross-reference, never cram.

## 1 · Source the workflow

From **this** session (reflect on the turns), a **prior named** session, or a **recurring** ad-hoc pattern across chats. For the latter two, mine the transcript(s) via the session-analysis capability. If the workflow **spans repos/services**, pin which repo owns each step — that boundary is often the watched RED. **The corrections you applied are the highest-value content** — they are the artifact, more than the happy-path mechanics.

## 2 · Distill — encode the watched RED

- The skill's one non-negotiable rule = the **failure you actually hit this session**, not a hypothetical. The session is your proof it matters.
- Purge the discoverable, the decaying (hardcoded paths/structure), and the generic; keep the non-obvious *why*, the quirks, the behavioral overrides.
- **Cut generality hard.** Bias to the smallest artifact; record an explicit "revisit when…" instead of shipping a speculative knob.

## 3 · Verify before promote (hard gate)

Re-confirm **every** claim against live code/data/the existing skill before writing it — promoting a remembered version of the session is the classic miss. When the skill captures a just-shipped implementation, drive it off the **canonical commits + the as-built doc** (ADR/postmortem), not recall; a late-found bug becomes "the skill should prescribe X," never "the code is broken." Produce a gap report (covered / underspecified / missing / do-not-generalize), then **stop for sign-off** before editing.

## 4 · Route: home + identity

Generic (domain-neutral) → your cross-project skills home; project-specific (repo names, ticket keys, internal paths/tools) → the project skill repo. **Verify genericity by grepping for project nouns** before mirroring, and strip them from any generic copy. **One owner per skill name** — a globally-installed skill silently shadows a same-named project skill. Match each repo's commit-identity convention (check its log / your memory). See [REFERENCE.md](REFERENCE.md) for the full matrix.

## 5 · Author (hand to the skill-writing capability)

- **Description = triggering conditions only** (third person, ≤1024 chars). A workflow summary here becomes a shortcut agents take *instead of* reading the skill. It must be **valid YAML** — an unquoted colon-space silently prunes the skill from some installers.
- **Thin: encode only the ~20% that isn't covered elsewhere.** Soft-link other capabilities by capability **+ the trigger moment** ("before drawing a diagram, if a diagramming skill is present, use it") — never by name, except inside one co-maintained repo. **Capability phrases don't self-fire**: when you orchestrate, resolve capability→installed name and inject an explicit "invoke `<name>`" into each subagent.
- **No fragile anchors** — never embed commit SHAs (they don't resolve cross-repo and rebases rot them); reference immutable docs by path and code by searchable pattern; inline a ≤5-line snippet only when a before/after is the best teacher.
- **Bundle a script only** once the logic has collapsed to something small, deterministic, and proven live; prefer an off-the-shelf tool, port only if none exists for the language. The script owns the logic; prose references the command. **Self-run it** before claiming it works.
- **Name for the capability actually demonstrated**; match the set's naming; confirm if ambiguous.
- Before shipping, confirm the **frontmatter parses as YAML** (any YAML linter, or `yaml.safe_load`) — an unquoted colon-space in the `description` is the classic silent-prune culprit. For a deeper compliance/concision pass, hand it to the skill-auditing capability.

## 6 · Test cold

Give a **fresh subagent** only the new skill + a realistic task; confirm it picks the right path, drives any script, and obeys the discipline. (Discipline skills: pressure-test that they hold under temptation. Technique skills: check the output is correct.)

## 7 · Ship (gated)

Edit the skill's **source** repo, never an installed/vendored copy (overwritten on reinstall). **Show the draft, then commit with the repo's identity convention.** **Never push or post without explicit approval.** A skill is inert until published **and** reinstalled (your manager re-pulls the remote — `install`, not `sync`); verify by grepping the installed copy. Mirror a generic skill to your cross-project home.

## Pre-empt these corrections

The recurring misses this skill exists to prevent — full catalogue (X1–X13) in [REFERENCE.md](REFERENCE.md). The four that bite most: **don't over-engineer** (X1), **stay in scope / diff against the real sibling** (X9), **verify before you assert** (X6/X12), and **stop before any push or post** (X13).
