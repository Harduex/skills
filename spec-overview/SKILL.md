---
name: spec-overview
description: Condense a spec, design doc, RFC, ADR, or plan into a one-screen bullet overview that carries the actual decisions — what the system does, how, what it deliberately does not do, and what is still undecided. Use when asked to summarize or give an overview of a spec or design, when a document is too long to re-read before a decision, when briefing someone joining mid-stream, when handing a design to another team, or when someone wants to sanity-check a design they already half-know.
---

# Spec Overview

A one-screen briefing that carries the **decisions**, not the prose around them. Someone should be able to read it and hold the design in their head without opening the document.

That makes it equally usable for catching up, briefing a teammate, handing work to another team, or spotting the claim that is wrong — but the artifact is the same either way. Write the overview; the use follows.

## The rule: every bullet says something specific

**Could someone disagree with this line?** If not, cut it — it is conveying nothing.

- "Handles retries robustly" — unfalsifiable, so it carries no information.
- "Failed deliveries retry 5 times with exponential backoff, then dead-letter" — a real fact, and instantly correctable if it is stale.

Vague bullets feel like coverage while saying nothing. That is the failure mode this format exists to prevent.

## Structure

Root bullets are the spec's **logical parts, not its section order**. Derive them from what the system actually has — typical shapes: the core mechanism · data model · auth and access · the interface surface · safety and failure handling · the domain-specific heart · build cost · handoff · what is still open.

- **Title it with a heading, and carry provenance** — the document's name plus its path and revision, so the reader knows exactly what they are looking at. A bold line is not a title here; every root bullet is already bold, so a bold title reads as a bullet that lost its marker.
- **Open with the deliberate negatives** where the design has them — "no new tables", "no change to existing behaviour", "no new service". A design is defined as much by what it refuses, those claims are the densest information in the document, and they are the fastest thing for a reader to challenge.
- **Root bullets assert, they do not label.** `Sync is a full fetch — every pull returns the complete set (D42)` beats `**Sync** — how syncing works`. The reader should be able to agree or disagree without descending.
- **8 root bullets or so**, each with 2–5 children. One screen.
- **Nest 2 levels, 3 only when a child needs its own qualifier.** Deeper reads as the document.
- **End with what is undecided, enumerated by id** — `TBD-4`, `Q2`, an issue key. Ids are how a reader replies "that one's settled now". Include recently closed ones with their resolution.

## Writing style: plain meaning first, exact name second

Each line does two jobs: a non-expert grasps the intent, and someone who knows the system can check it.

```
BAD  (abstract — true but says nothing)
  - Rate limits are applied per customer rather than globally

BAD  (raw jargon — precise but opaque)
  - 429 + Retry-After, bucket keyed on tenant_id, refill 100/min

GOOD (both)
  - Each tenant gets its own budget — 100 requests a minute, refilled steadily —
    and an exhausted one gets `429` with `Retry-After` so clients back off
    instead of hammering
```

Rules that follow:

- **Anchor to the real identifier** — route paths, field names, roles, decision ids, function names. Without them the reader cannot connect the line to anything.
- **Add a "so that" clause only where the claim would otherwise read as trust-me.** One clause, never a paragraph.
- **Keep the domain's own nouns, and do not narrow them.** Calling uploaded *files* "images" quietly excludes the PDFs the feature also accepts, and the reader ends up correcting your word instead of reading the design.
- **Numbers carry provenance.** "measured 40 ms p50, 900 ms p99 on staging" informs; "generally fast" does not.
- **Gloss jargon inline or drop it.** "no cursor, no tombstones" means nothing outside change-feed design; "no separate change log to keep in step" means the same thing to everyone.

## Workflow

1. **Read the whole spec.** Overviews built from headings inherit the document's structure and miss what it decided.
2. **List the logical parts** — what the system *has*, not what the sections are called.
3. **Per part, pick the 2–5 load-bearing claims** — what someone would have to un-decide to change the design. Skip anything derivable from a claim already listed.
4. **Write each as plain meaning + exact anchor.**
5. **Self-check:** every bullet specific · no bullet needing context the reader lacks · negatives near the top · open items last with ids · one screen.

## When someone pushes back on a line

Treat it as a finding about the **spec**, not the overview. "That's not what edit does" usually means the document is wrong or ambiguous — fix it there, then regenerate. If the challenge turns out to be mistaken, the wording still invited it, so tighten it anyway.

## Worked shape

An imaginary webhook-delivery service, to make the shape concrete without the domain mattering:

```md
## Webhook Delivery (platform/docs/webhooks.md, RFC 2025-03-11)

- **What it does not do** — the load-bearing refusals
  - No new queue technology, no new service, no per-event ordering guarantees
  - No manual replay endpoint — operators re-drive from the table (D7)

- **Delivery is per subscription, not per event** — each subscription has its own queue
  - Ordering holds within a subscription only; nothing orders across them
  - Any `2xx` marks it delivered; everything else retries

- **Retries stop at 5 attempts**, exponential backoff from 10s to 1h
  - Exhausted deliveries land in `dead_letter_events`, kept 30 days

- **Every request is signed; nothing is encrypted at the payload level**
  - `X-Signature` is HMAC-SHA256 over the raw body with the subscription secret
  - Secrets rotate without downtime — two are valid during a 24-hour overlap

- **Build cost: one table, one worker** — reuses the existing job runner

- **Open**
  - TBD-2 — 30-day retention assumed, never confirmed with legal
  - TBD-5 — should a `410` from a subscriber auto-disable it, or just alert?
  - TBD-1 closed — signing is mandatory, not opt-in
```

Ship it in chat by default. Write it to a file only when asked, or when it is going somewhere the conversation cannot reach.
