---
name: general-standards
description: The universal base layer of standards for everything a project authors, code and prose alike, derived from the ASD-STE100 controlled-language specification: a controlled naming vocabulary with a per-project glossary, small imperative units with guard conditions first, severity-accurate errors that state consequences, and a document band covering procedural and descriptive writing, sentence-length counting, punctuation, and cohesion. A project's own coding-standards skill and glossary complement and override it. Use when writing or naming code, authoring comments, docstrings, error messages, logs, or commit messages, writing or rewriting a README, specification, runbook, release note, or any technical document, auditing code or a document against a standard, rewriting someone else's prose into the standard, setting up or extending a project glossary, or when the user mentions coding standards, naming conventions, writing style, documentation style, or controlled vocabulary.
---

# General Standards: One Controlled Language for Code and Prose

Everything a project authors is technical writing — the code, the error
messages, the README. These standards port the controlled-language system
behind aerospace maintenance documentation (ASD-STE100) to all of it: a closed
vocabulary, hard size limits, imperative structure, and safety-grade messages.
50 rules, seven bands, stable IDs.

**"General" names the layer, not the scope of the advice.** This is the base
that every project sits on: a project's own coding-standards skill, its
glossary, and its agent-instructions file complement these rules and win on
any conflict.

## Core principles

1. **One name, one meaning. One concept, one name.** The vocabulary is
   closed: project glossary → codebase → platform → domain. Never invent a
   synonym.
2. **Small imperative units.** Short statements, short functions, short
   sentences, guard conditions first, happy path top-to-bottom.
3. **One topic per container.** Each container holds exactly one topic:
   - A statement does one action.
   - A function does one job.
   - A module covers one topic.
   - A paragraph covers one topic.
4. **Messages are safety instructions.** Accurate severity, then what happened
   or what to do, then the consequence if ignored.
5. **Consistency beats preference.** Mirror the closest sibling. Otherwise,
   any divergence needs a stated reason.

## What are you writing?

| You are writing | Load |
|---|---|
| code, names, functions, modules, or matching a sibling's structure | [VOCABULARY.md](VOCABULARY.md) + [CODE.md](CODE.md) |
| errors, logs, comments, commit subjects | [MESSAGES.md](MESSAGES.md) |
| a README, spec, runbook, release note, any document | [WRITING.md](WRITING.md) + [VOCABULARY.md](VOCABULARY.md) |
| auditing or rewriting code or a document | [REVIEW.md](REVIEW.md) |
| tracing a rule to its ASD-STE100 source | [STE-MAPPING.md](STE-MAPPING.md) |

## Author mode — code

1. Naming something new? Search the glossary, then the codebase, then the
   platform's vocabulary for the existing term (N1, N3).
2. About to inline a computation, conversion, or check? Read the shared
   utility modules' export lists first and reuse the operation that is
   already named there (M6). An expression does not announce itself as a
   dependency, so nothing else will prompt this — and a sibling file older
   than the helper will hand you the pre-helper idiom (M4).
3. Writing a function?
   - Guards and validation first (S4).
   - One action per statement (S2).
   - Happy path as direct commands (S3).
4. Writing an error or log?
   - Pick severity by W1.
   - Open with the condition or command (W2).
   - Close with the consequence (W3).

## Author mode — documents

1. Choose the genre before the first sentence: procedural or descriptive (D1).
   It fixes the shape and the word cap for everything that follows.
2. Write to the cap — 20 words in instructions, 25 in descriptions (P1) — and
   when a sentence looks long, count it by the method (D2) rather than by eye.
3. Use code and glossary terms verbatim. In other words, never paraphrase an
   identifier (P5).
4. No pronoun without one unambiguous referent (P4).

## Review, audit, and rewrite modes

Load [REVIEW.md](REVIEW.md). Sweep band by band: N → S → M → W → P → D → C
(a code diff skips D, and a document skips S and M). A finding must name the rule
ID it violates or it is dropped. Format:

`**[F1] [ISSUE] [N3] src/billing.ts:42 — Synonym drift: "client" aliases "customer"**`

A rewrite is an audit carried through to corrected text: fix the form the
findings name, and leave quotations, proper nouns, and factual claims alone.

## Precedence and composition

A project-level coding-standards skill, the project's glossary, and its
agent-instructions file complement this skill and win on any conflict: load
both, apply the project's rules first, and fall back to these defaults where
the project is silent. Architecture-level skills (functional core / mutable
shell, domain patterns) compose above both: they decide where logic lives. In
contrast, this layer governs how names, units, and prose read.

## Self-check before done

- Every new name from an approved source? (N1)
- Every inlined computation checked against the shared utilities' exports? (M6)
- Any unit past its trigger — 25 lines, 4 params, nesting 2, 400-line file —
  without a written justification? (S1, M2)
- Every message: severity accurate, condition first, consequence stated? (W1–W3)
- Genre chosen, sentences inside the cap when counted by D2, pronouns
  unambiguous? (D1, D2, P1, P4)
