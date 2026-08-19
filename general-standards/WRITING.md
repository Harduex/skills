# Writing: Documents, Sentences, and the Word Count

A README, a specification, a runbook, and a release note are procedures and
descriptions in the controlled-language sense. The P band governs the sentence.
Similarly, the D band governs the document around it.

Scope: standalone documents. Prose that ships inside the codebase — comments,
errors, logs, commit subjects — is [MESSAGES.md](MESSAGES.md).

## Sentences and prose (P band)

| ID | Rule |
|---|---|
| P1 | Sentences: 20 words max in instructions, 25 in descriptions; one idea per sentence. |
| P2 | Instructions (READMEs, runbooks) are numbered imperative steps, one action each, condition first, the real action verb named (not "use X to do Y"). |
| P3 | Descriptive docs: one topic per paragraph, 6 sentences max per paragraph, information given gradually. |
| P4 | Every pronoun has exactly one possible referent; repeat the noun instead of a dangling "it"/"this"; keep the connecting "that". |
| P5 | Prose uses code and glossary terms verbatim — never paraphrase an identifier. |
| P6 | No Latin abbreviations (e.g., i.e., etc.) — write the English words. |
| P7 | Inclusive language, in prose and identifiers. |
| P9 | Prose word choice comes from the approved set. The prose swap table in [VOCABULARY.md](VOCABULARY.md) names the words to avoid and what to write instead. |

Worked contrasts:

```
P2 BAD:  Use the migration script to update the schema.
P2 GOOD: 1. If the database is running, stop it.
         2. Run `migrate up`.

P4 BAD:  The scheduler restarts the worker when it crashes.   (which one crashes?)
P4 GOOD: The scheduler restarts the worker when the worker crashes.
```

## The document band

| ID | Rule |
|---|---|
| D1 | Choose the genre before the first sentence. Procedural text is numbered imperative steps under a 20-word cap. Descriptive text is paragraphs under a 25-word cap, six sentences maximum. A document that mixes them marks the boundary with a heading. |
| D2 | Count a sentence by the method, not by eye. An identifier, a number, a number with its unit, an abbreviation, a quoted string, a title or heading or label, a proper noun, and a hyphenated cluster each count as one word. A parenthetical insert counts as one word. Inside a vertical list, a colon ends the sentence. |
| D3 | No semicolons in running prose. Split the sentence. A table cell is a compressed list, not a sentence, so the rule does not reach inside one. |
| D4 | Parentheses serve seven purposes: cross-references, item labels, step labels, abbreviations, singular and plural pairs, short explanations, and alternatives. A use outside that list is a trigger, not a ban: keep it with a stated reason, or give it its own sentence. |
| D5 | Skip the possessive form when you are not sure the sentence is correct with it. Stacked possessives are always wrong. |
| D6 | Join sentences on related topics with explicit connecting words. Two adjacent paragraphs with no connective read as two documents. |
| D7 | Put an article or a demonstrative before a noun wherever the grammar allows one. |
| D8 | Release information gradually, and let key words and phrases carry the structure. Orientation before detail; never a configuration dump before the reader knows what it configures. |

D2 is what makes P1 checkable. Without a counting method, a 20-word cap is a
guess: `BILLING_WORKER_CONCURRENCY`, `30 seconds`, and `"not found"` each look
like several words and each counts as one.

Worked contrasts:

```
D2:  Set BILLING_WORKER_CONCURRENCY to 4 before you restart the worker.
     Counts as 9 words: Set / BILLING_WORKER_CONCURRENCY / to / 4 / before /
     you / restart / the / worker.

D3 BAD:  Stop the worker; the queue drains on its own.
D3 GOOD: Stop the worker. The queue drains on its own.

D5 BAD:  Check the service's configuration's default timeout.
D5 GOOD: Check the default timeout in the service configuration.

D6 BAD:  The worker retries three times. The queue holds failed jobs for a day.
D6 GOOD: The worker retries three times. After the third failure, the queue
         holds the job for a day.
```
