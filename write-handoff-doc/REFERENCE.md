# Handoff Document — Annotated Skeleton

The section order below is the proven shape for a contract-style handoff (an API, a data format, a protocol). For a feature or behavior handoff, keep 1–4, 6, 7 and derive the middle from the reader's tasks the same way. Skip a section only when it would genuinely be empty — never leave an empty heading.

```markdown
# The <thing> for <audience>                      ← or "How <thing> works in <system>"

*Last updated <D Month YYYY>. <status line — pick one:
  "The agreed proposal, ready for final review"  |  "Describes what <system> does today">
 — supersedes "[<old published doc title>](<link>)" (<its date>), which described an earlier
 revision. Field names are final unless this review changes them.*

<One intro paragraph: what the thing is, who this document is for, what it covers
("the complete client-facing contract: what crosses the wire, the rules a client must
follow, and what it deliberately does not do"), and what becomes the living reference
once implementation lands. No Background. No Motivation. No team history.>

## The short version

<ONE paragraph, ~8–12 sentences, carrying ~90%: the one read that lets a reviewer decide.
Name the core mechanism, the identity model, the safety/retry story, and the biggest
"there is no X" reliefs ("no sync protocol, no cursor, no merge step"). The only
paragraph licensed to exceed prose caps.>

## <Reader task 1 — e.g. Authentication>

<Callers table: who | what's on the wire | limits. Then the obtain/refresh mechanics
in 2–3 sentences, then the failure shapes (expired, missing) with exact codes.>

## <Reader task 2 — e.g. Reading>

<The request, verbatim. Then ONE annotated example response — every field present,
every field carrying an inline comment with its meaning and its null semantics.
Then bold-led paragraphs, one per rule the reader must obey:>

**<Claim first.>** <Elaboration. Pair every data rule with the UI action and the
field that drives it: keep the cache + hide the node + `reason` picks the message.>

## <Identity / core-concept section>

<A two-row "who mints it | what it's for" table beats prose for dual identifiers.
A 3-column before/during/after lifecycle snippet in a code block beats both.>

## <Reader task 3 — e.g. Writing>

<Route list in one code block. One annotated create example. Then per-operation
subsections, each ≤1 short paragraph + its edge cases as bullets.>

## <Conventions section — rules the system does not enforce>

| Rule | Cost of ignoring it |
|---|---|
| <imperative rule, bold if load-bearing> | <the concrete consequence, not "undefined behavior"> |

## What it deliberately does not do

- **No <thing>.** <What to do instead, where an instead exists.>

## Error codes                                    ← contract handoffs only

| Code | When | <Their> reaction |
|---|---|---|

## Open items on <their> side

<Only their work. Lead with the shared effect: "None block the API, but until they
land, affected <things> simply have <observable degraded state>:">
```

## Per-section judgment notes

- **Dateline status**: "proposal, ready for review" and "describes what exists" are different documents — the first invites pushback, the second forbids it. Pick consciously; the exemplar pair used one of each. The date is the handoff's own last edit. Omit "field names are final…" when the source doesn't assert it.
- **Error-table placement**: the late `## Error codes` section fits a multi-route contract; a single small surface folds its failure shapes into the task section instead. The *their-reaction* column is the invariant either way.
- **Short version**: write it last, from the finished doc, not first from the spec — it must summarize what the document actually says.
- **Annotated example blocks**: one complete example beats three partial ones. Every field appears once with its null semantics; a field whose meaning needs more than a comment gets a bold-led paragraph below, not a longer comment.
- **The their-reaction column** is what makes an error table a handoff artifact instead of a server changelog: every row tells the reader what to build.
- **Their open items**: naming your internal tracker ticket is noise to them; naming the observable effect until fixed ("until then, the placement field stays null") is the useful form.

## Sync-back: folding published-copy edits into the repo source

When the human edits the published copy (Google Doc review polish) and hands it back:

1. Diff their text against the repo file **change by change**; apply each substantive delta.
2. **Skip the medium's artifacts** — they are formatting, not edits: empty headings inserted as page spacing, `\.`/`\+` escapes, `:----` table alignment, lost code-fence languages, curly quotes/apostrophes, soft line breaks.
3. Where their edit contains a grammar slip, apply the corrected form to the repo **and report the exact words back** so they can align the published copy — the two must stay word-identical, and silent divergence in either direction is the failure.
4. Commit the sync as its own commit, named as a fold-in of the published copy's review.
