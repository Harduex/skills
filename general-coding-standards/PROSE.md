# Prose: Errors, Logs, Comments, Docs, Commits

Everything English in a codebase is technical writing and follows the same
controlled-language discipline as the code.

## Errors, warnings, logs

| ID | Rule |
|---|---|
| W1 | Severity words mean one thing, consistently: error = operation failed or data at risk; warn = degraded but running; info = normal operation. Never inflate or bury severity. |
| W2 | Start the message with the command or condition — what to do or what happened, concretely. |
| W3 | State the consequence: what breaks or is at risk if the message is ignored. |
| W4 | Comments and info-logs never carry load-bearing instructions; if the reader must act, use an error, warning, or assertion. Warnings go before the dangerous operation. |

The error formula is severity + condition + consequence. **The consequence is
the part writers omit** — a message that names the failure but not its impact
makes the operator guess whether it matters. Never assume the impact is
obvious; write it.

```
BAD:  console.log("something went wrong loading cert")
      (buried severity, no condition, no consequence)

GOOD (expired):        logger.error("TLS certificate at " + path + " expired on " + notAfter +
                       ". HTTPS clients will reject every connection until it is replaced.")
GOOD (expiring soon):  logger.warn("TLS certificate at " + path + " expires in " + days +
                       " days. Renew it before then or HTTPS connections will start failing.")
```

The comment boundary (W4): a comment states non-inferable rationale about the
code's current behavior. An instruction the reader must obey is not a comment —
enforce it:

```
BAD:  // NOTE: you must call initTemplates() before dispatchReminders() or sends fail.
GOOD: assert(templatesLoaded(), "Call initTemplates() before dispatchReminders(). Sends fail without loaded templates.");
```

## Written prose (comments, docs, READMEs, commits)

| ID | Rule |
|---|---|
| P1 | Sentences: 20 words max in instructions, 25 in descriptions; one idea per sentence. |
| P2 | Instructions (READMEs, runbooks) are numbered imperative steps, one action each, condition first, the real action verb named (not "use X to do Y"). |
| P3 | Descriptive docs: one topic per paragraph, 6 sentences max per paragraph, information given gradually. |
| P4 | Every pronoun has exactly one possible referent; repeat the noun instead of a dangling "it"/"this"; keep the connecting "that". |
| P5 | Prose uses code and glossary terms verbatim — never paraphrase an identifier. |
| P6 | No Latin abbreviations (e.g., i.e., etc.) — write the English words. |
| P7 | Inclusive language, in prose and identifiers. |
| P8 | Commit subjects are one imperative sentence describing one change. |

Worked contrasts:

```
P2 BAD:  Use the migration script to update the schema.
P2 GOOD: 1. If the database is running, stop it.
         2. Run `migrate up`.

P4 BAD:  The scheduler restarts the worker when it crashes.   (which one crashes?)
P4 GOOD: The scheduler restarts the worker when the worker crashes.

P8 BAD:  fixed some stuff in auth and also cleaned up tests
P8 GOOD: fix token refresh race in auth middleware
```
