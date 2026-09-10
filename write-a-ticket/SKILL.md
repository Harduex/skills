---
name: write-a-ticket
description: Write a ticket someone else can act on — a story, a bug report, a sub-task, or a placeholder for work whose scope will drift. Use when asked to write, draft, file or log a ticket, issue, story or bug in Jira, Linear or GitHub, when turning a decision, a review finding or a spec follow-up into tracker work, or when a ticket draft is being reviewed before it is filed. Covers choosing the shape, keeping the ticket minimal, and deciding what belongs in the tracker versus the spec or the merge request.
---

# Writing a tracker ticket

**Minimalist but full.** A ticket earns its length by being complete, never by being thorough. Every section either tells the reader something no other artifact tells them, or it goes.

## The test that settles most arguments

Before writing a section, ask what already owns that detail.

- **A spec, design doc or ADR owns the contract** → state the outcome, link the document, stop. Do not restate the design.
- **A merge request will own the implementation** → say what to build and how you will know it works, not which functions to touch.
- **Nothing owns it.** A defect found in production, a security hole, a reproduction that took real effort → **the ticket is the record.** Evidence belongs in it: exact endpoints, versions, requests, observed responses, root cause. Density is correct here.

Same principle, opposite outputs. Do not carry "keep tickets plain" into a defect that has no other home; the evidence *is* the ticket's value.

## Pick a shape, do not fill a template

| The ticket is | Shape |
|---|---|
| A feature or change someone will build | user story → what is true today → acceptance criteria |
| A sub-task under a parent that already holds the context | acceptance criteria alone, plus how to see it working and a link to the spec |
| A defect in behaviour | problem → steps to reproduce → expected → actual |
| A defect that is its own only record | summary → reproduction with evidence → root cause → severity and scope → acceptance criteria → affected surface |
| Work whose scope will drift while it is built | one broad paragraph of intent, and a line naming where the real record lives |

A user story is `As a <person>, I want <outcome>, so that <reason>`. It describes someone's goal. A list of tasks with "As a developer" bolted on top is not a user story.

## Style rules

- **Self-contained.** Never point at a sibling draft — "same as the other one", "same fix shape". Filed tickets are read alone, so inline the whole root cause and fix even when that repeats a neighbouring ticket.
- **Use the vocabulary the project already uses.** Never substitute a synonym for a named concept. If the domain calls them comments, never write feedback; if it calls them image attachments, never write photos. A synonym reads as a different thing and sends people looking for it.
- **An open question is agreed, never merely left.** Surface every unresolved point while drafting and get a decision on it. A `TBD` survives into the filed ticket only because someone chose to leave it open, and then it is named as one line inside the criteria it affects. A leftover "decisions to make" section means the drafting stopped early: resolve the question, or make the decision the ticket's whole purpose and say so in the title.
- **Sections earn their place.** "Out of scope" is worth writing when it stops someone building the wrong thing, and worth deleting when it lists what nobody would have done anyway. Same for notes, context and background.
- **Acceptance criteria are observable.** A reader must be able to say whether each one happened. "Works correctly" is not a criterion; "opening it as someone with only a link shows no list" is.
- **Match density to the reader, not to what you know.** A story or bug report that a designer, tester or product owner opens carries no file paths, function names, schema keys, migration names or timestamps — however well you know them. Strip them and leave a single pointer line in their place ("Spec: …", "Reference implementation: …"). A sub-task under an epic, or a defect that is its own only record, is opened by the implementer and keeps the detail. When unsure, ask who opens this ticket first.
- **Prose and bullets by default; a table only for evidence.** A table earns its place in a defect that is its own record — a matrix of affected surfaces, a request-and-result repro log. In a story it turns a decision into a spreadsheet; write the same content as bullets.

## Link by capability, not by name

This skill writes the ticket. It does not know your tracker, your forge, or your domain. Invoke whatever skill in your current set provides:

- **the tracker's mechanics** — issue types, required custom fields, boards, sprints, estimates, and who may file
- **the forge workflow**, when the ticket comes out of a merge or pull request review, so the ticket and the review thread stay consistent
- **the domain workflow** for the area the ticket touches, when the acceptance criteria have to name real behaviour

Discover them from the available skill descriptions and invoke them by their real names. Where no such skill exists, the project's own agent instructions usually carry the field ids and board rules.

## Before filing

Show the draft as **rendered markdown, never wrapped in a code fence** — the reader is judging the ticket, not copying it, and raw headings and tables are unreadable. **Show the full draft text and get an explicit go-ahead, every time** — including when an earlier draft of the same ticket was already approved, and including when only a field is changing. Filing is outward-facing and awkward to undo.

Mirror the nearest existing ticket in the same epic or project instead of rebuilding the shape. Tracker mechanics — issue types, required custom fields, boards, sprints, team fields — belong in the project's own agent instructions, not here; read them there and follow them.

**After creating a ticket through an API, read it back.** Create calls routinely accept sprint, estimate and team fields and silently drop them, and the response often does not echo what landed.

## Do not

- Do not expand a small ticket to fill the shape. A one-line bug gets a sentence.
- Do not paste a spec section into a ticket. Link it.
- Do not invent acceptance criteria to reach a tidy number.
- Do not run past what the shape needs. A bug report lands near 15 lines, a story between 25 and 50. When a draft runs much longer, the excess is almost always implementation detail the spec or the merge request already owns.
- Do not file anything without the go-ahead, however obvious the ticket seems.
