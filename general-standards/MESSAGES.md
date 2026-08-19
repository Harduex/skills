# Messages: Errors, Logs, Comments, Commits

Every message a program emits is a safety instruction, and every comment is
technical writing. Both follow the same controlled-language discipline as the
code around them.

Scope: this band governs errors, warnings, logs, comments, docstrings, and
commit subjects — prose that ships inside the codebase. Standalone documents
are [WRITING.md](WRITING.md). These messages inherit P1's sentence cap and
P4's pronoun rule. However, they do not inherit the document band (D1–D8),
because a one-line comment has no genre and no paragraph.

## Errors, warnings, logs

| ID | Rule |
|---|---|
| W1 | Severity words mean one thing, consistently: error = operation failed or data at risk; warn = degraded but running; info = normal operation. Never inflate or bury severity. |
| W2 | Start the message with the command or condition — what to do or what happened, concretely. |
| W3 | State the consequence: what breaks or is at risk if the message is ignored. |
| W4 | Comments and info-logs never carry load-bearing instructions; if the reader must act, use an error, warning, or assertion. Warnings go before the dangerous operation. |
| P8 | Commit subjects are one imperative sentence describing one change. |

P8 keeps its P-band ID because it is prose, but it lives here because commits ship with the code.

```
P8 BAD:  fixed some stuff in auth and also cleaned up tests
P8 GOOD: fix token refresh race in auth middleware
```

The error formula is severity + condition + consequence. **The consequence is
the part writers omit** — a message that names the failure but not its impact
makes the operator guess whether it matters. Never assume the impact is
obvious. Instead, write it.

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
