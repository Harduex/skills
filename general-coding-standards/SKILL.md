---
name: general-coding-standards
description: Language-agnostic general coding standards derived from the ASD-STE100 controlled-language principles: a controlled naming vocabulary with a per-project glossary, one-name-one-concept rules, small imperative units with guard conditions first, severity-accurate errors that state consequences, and simplified-technical-English rules for comments, docs, and commit messages. The universal base layer — a project's own coding-standards skill and glossary complement and override it. Use when writing or naming new code, authoring comments, docstrings, READMEs, error messages, logs, or commit messages, reviewing code against a standard, setting up or extending a project glossary, or when the user mentions coding standards, naming conventions, code style, or controlled vocabulary.
---

# Coding Standards: Controlled Language for Code

Code is technical writing. These standards port the controlled-language system
behind aerospace maintenance documentation (ASD-STE100) to any programming
language: a closed vocabulary, hard size limits, imperative structure, and
safety-grade error messages. 40 rules, six bands, stable IDs.

## Core principles

1. **One name, one meaning; one concept, one name.** The vocabulary is closed:
   project glossary → codebase → platform → domain. Never invent a synonym.
2. **Small imperative units.** Short statements, short functions, guard
   conditions first, happy path top-to-bottom.
3. **One topic per container.** A statement does one action; a function does one
   job; a module covers one topic; a paragraph covers one topic.
4. **Errors are safety instructions.** Accurate severity, then what happened or
   what to do, then the consequence if ignored.
5. **Consistency beats preference.** Mirror the closest sibling; divergence
   needs a stated reason.

## Load table

| Task touches | Load |
|---|---|
| naming anything; creating or extending a glossary | [NAMING.md](NAMING.md) — N1–N9 + vocabulary |
| functions, control flow, modules, files | [STRUCTURE.md](STRUCTURE.md) — S1–S9, M1–M5 |
| comments, docs, READMEs, commits, errors, logs | [PROSE.md](PROSE.md) — W1–W4, P1–P8 |
| reviewing or auditing code against this standard | [REVIEW.md](REVIEW.md) |
| tracing a rule to its ASD-STE100 source | [STE-MAPPING.md](STE-MAPPING.md) |

## Author mode — before you write

1. Naming something new? Search the glossary, then the codebase, then the
   platform's vocabulary for the existing term (N1, N3).
2. Writing a function? Guards and validation first (S4); one action per
   statement (S2); happy path as direct commands (S3).
3. Writing an error or log? Pick severity by W1; open with the condition or
   command (W2); close with the consequence (W3).
4. Writing prose? One idea per sentence — 20 words max in instructions, 25 in
   descriptions (P1); no pronoun without one unambiguous referent (P4).

## Review mode

Load [REVIEW.md](REVIEW.md). Sweep band by band: N → S → M → W → P → C.
A finding must name the rule ID it violates or it is dropped. Format:

`**[F1] [ISSUE] [N3] src/billing.ts:42 — Synonym drift: "client" aliases "customer"**`

## Precedence and composition

These are the general standards — the base layer. A project-level
coding-standards skill, the project's glossary, and its agent-instructions
file complement this skill and win on any conflict: load both, apply the
project's rules first, and fall back to these defaults where the project is
silent. Architecture-level skills (functional core / mutable shell, domain
patterns) compose above both: they decide where logic lives; this layer
governs how names, units, and prose read.

## Self-check before done

- Every new name from an approved source? (N1)
- Any unit past its trigger — 25 lines, 4 params, nesting 2, 400-line file —
  without a written justification? (S1, M2)
- Every error: severity accurate, condition first, consequence stated? (W1–W3)
- Prose inside sentence and paragraph caps, pronouns unambiguous? (P1, P3, P4)
