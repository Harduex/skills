# Messages: Errors, Logs, Comments, Commits

Every message a program emits is a safety instruction, and every comment is
technical writing. Both follow the same controlled-language discipline as the
code around them.

Scope: this band governs errors, warnings, logs, comments, docstrings, and
commit subjects — prose that ships inside the codebase. Standalone documents
are [WRITING.md](WRITING.md). These messages inherit P1's sentence cap and
one-idea rule and P4's pronoun rule. In a comment, a semicolon that joins two
clauses is two sentences: split it. A compressed list (`a → x; b → y`) is a
table cell in disguise and may stay. However, they do not inherit the document band (D1–D8),
because a one-line comment has no genre and no paragraph.

## Errors, warnings, logs

| ID | Rule |
|---|---|
| W1 | Severity words mean one thing, consistently: error = operation failed or data at risk; warn = degraded but running; info = normal operation. Never inflate or bury severity. |
| W2 | Start the message with the command or condition — what to do or what happened, concretely. |
| W3 | State the consequence: what breaks or is at risk if the message is ignored. |
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

## Comments

| ID | Rule |
|---|---|
| W4 | Comments and info-logs never carry load-bearing instructions; if the reader must act, use an error, warning, or assertion. Warnings go before the dangerous operation. |
| W5 | A comment carries only rationale the reader cannot infer from the code: intent, a gotcha, a deliberate exception that looks wrong. Before writing one, make the code say it — rename, extract, or hoist the literal into a named constant. A comment that restates the code is deleted. |
| W6 | A comment describes the code as it stands, never the change that produced it — no "new behavior", "legacy way", "ported from", "transitional until". It names no planning id, test-case code, or session context. External anchors stay: an upstream issue, a tracker ticket (`TODO: <TICKET-ID> — context`), a pinned dependency version. |
| W7 | An edit updates or deletes every comment it invalidates. Moved code keeps its comments verbatim. Commented-out code is deleted; history keeps it. |

W5 and W6 together draw the line: the "why" of the current code stays, the
"what" and the "how it got here" go. A reviewer's likely question is the test
— if the next reader would ask it, answer it in a comment; if the code already
answers it, the comment is noise.

```
W5 BAD:  // increment the retry counter
         retries += 1;
W5 GOOD: // The vendor API returns 200 with an empty body on throttling, so the
         // status code alone cannot signal a retry.
W6 BAD:  // New behavior (D14): also handles PDFs since the spec change
W6 GOOD: // PDFs render through the same pipeline; page count comes from the header.
W6 GOOD: // Workaround for upstream issue vendor/sdk#632, remove once fixed.
```

The comment boundary (W4): a comment states non-inferable rationale about the
code's current behavior. An instruction the reader must obey is not a comment —
enforce it:

```
BAD:  // NOTE: you must call initTemplates() before dispatchReminders() or sends fail.
GOOD: assert(templatesLoaded(), "Call initTemplates() before dispatchReminders(). Sends fail without loaded templates.");
```
