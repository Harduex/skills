---
name: spec-overview
description: Condense a spec, design doc, RFC, ADR, or plan into a one-screen bullet overview built for fast human review — every claim short, checkable, and anchored to the real identifier so a domain reader can spot what is wrong at a glance. Use when asked to summarize or give an overview of a spec or design, to produce something reviewable quickly, when a doc is too long to re-read before a decision, or when someone needs to sanity-check a design they already half-know.
---

# Spec Overview

A review instrument, not a summary. The reader already knows the domain; they are scanning for the claim that is **wrong**. Optimize for that.

## The test every bullet must pass

**Could a domain reader disagree with this line?** If not, cut it.

- "Handles retries robustly" — nobody can disagree. Dead weight.
- "Failed deliveries retry 5 times with exponential backoff, then land in the dead-letter queue" — instantly correctable ("no, we dropped it to 3").

Vague bullets survive review by saying nothing. They are the main failure mode.

## Structure

Root bullets are the spec's **logical parts, not its section order**. Derive them from what the system actually has — typical shapes: the core mechanism · auth/access · the API or interface surface · safety and failure handling · the domain-specific heart · build cost · handoff to another team · what is still open.

- **8 root bullets or so**, each with 2–5 children. One screen.
- **Nest 2 levels, 3 only when a child needs its own qualifier.** Deeper reads as the doc.
- **Always end with what is undecided.** Corrections concentrate there.
- **Lead the doc's own deliberate negatives** — "no new tables", "never assumed", "no scopes inspected". Negative claims are the highest-signal lines in any design and the easiest to falsify.

## Writing style: plain meaning first, exact name second

Each line does two jobs: a non-expert grasps the intent, and an expert can check it against the code.

```
BAD  (abstract — true but uncheckable)
  - Rate limits are applied per customer rather than globally

BAD  (raw jargon — checkable but opaque)
  - 429 + Retry-After, bucket keyed on tenant_id, refill 100/min

GOOD (both)
  - Each tenant gets its own budget — 100 requests a minute, refilled steadily —
    and an exhausted one gets `429` with `Retry-After` so clients back off
    instead of hammering
```

Rules that follow from this:

- **Anchor to the real identifier** — route paths, field names, roles, decision ids, function names. Those are the correction handles.
- **Add the "so that" clause only where the claim would otherwise read as trust-me.** One clause, never a paragraph.
- **Keep the domain's own nouns, and do not narrow them.** Calling uploaded *files* "images" quietly excludes the PDFs and archives the feature also accepts — the reader then corrects your word instead of reviewing the design.
- **Numbers carry provenance.** "measured 40 ms p50, 900 ms p99 on staging" invites a correction; "generally fast" does not.
- **Gloss jargon inline or drop it.** "no cursor, no tombstones" means nothing outside change-feed design; "no separate change log to keep in step" means the same thing to everyone.

## Workflow

1. **Read the whole spec.** Overviews built from headings inherit the doc's structure and miss what it decided.
2. **List the logical parts.** Ask what the system *has*, not what the doc's sections are called.
3. **Per part, pick the 2–5 load-bearing claims** — what someone would need to un-decide to change the design. Skip anything derivable from a claim already listed.
4. **Write each as plain meaning + exact anchor.**
5. **Self-check:** every bullet falsifiable · no bullet needing context the reader lacks · undecided items last · under one screen.
6. **Offer it for correction, then feed corrections back.** The overview is a round trip: what the reader challenges usually belongs in the spec, not only in the summary.

## When corrections come back

Treat each as a finding about the **spec**, not the summary. A reader who says "that's not what edit does" has found a defect in the doc — fix it there, then regenerate the overview. If the challenge turns out to be wrong, the doc's wording still invited it; say so and tighten the wording.

## Worked shape

Shown on an imaginary webhook-delivery service, to make the shape concrete without the domain mattering:

```md
**Webhook Delivery**

- **Delivery** — each event is queued per subscription, not per event
  - Ordering is guaranteed within a subscription only; nothing orders across them
  - A subscriber returning any `2xx` marks it delivered; everything else retries

- **Retries** — 5 attempts, exponential backoff from 10s to 1h
  - Exhausted deliveries land in `dead_letter_events`, kept 30 days
  - No manual replay endpoint — operators re-drive from the table (D7)

- **Security** — every request signed, nothing encrypted at the payload level
  - `X-Signature` is HMAC-SHA256 over the raw body with the subscription secret
  - Secrets rotate without downtime: two are valid during a 24-hour overlap

- **Build cost** — one table, one worker, no new service
  - Reuses the existing job runner; no queue technology introduced

- **Open**
  - Retention: 30 days assumed, never confirmed with legal (TBD-2)
  - Whether a 410 from a subscriber should auto-disable it, or just alert
```

Ship it in chat by default. Write it to a file only when asked, or when it is going somewhere the conversation cannot reach.
