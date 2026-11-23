---
name: prototyping-ui
description: Builds clickable UI prototypes as single offline HTML files that a ticket can carry as design context. Use when the user asks for a prototype, a mockup, design options or clickable versions of a screen, panel or component ("let's make a design prototype", "show me a few options for this", "mock this up"), wants to pick between design versions, or wants to keep refining a prototype toward one settled design. Not for system or software architecture, and not for a page that only explains an answer.
---

# Prototyping UI

A prototype answers "what should this look like, and how should it behave?" by letting the user click it. Its value is the loop: a few versions, the user picks one, rounds of refinement, one settled design. The finished file has two readers: the people who review the design, and the coding agent that later implements the ticket and reads the page as its visual and behavioral context.

Build one only when the user asks. Other skills may offer it; never start one unasked.

## The loop

1. **Ground it.** Read the ticket or request and the screen the feature lives in. Load your set's UX-design skill, if one exists, to inventory the existing components and every state the feature needs. Gather real sample data.
2. **Versions.** Default to 3 and never more than 5, unless the user names a number. Make them structurally different: layout, hierarchy, primary control. Colour tweaks are not versions. Put all of them in the one file behind a switcher, each with two or three lines of trade-offs, and mark your recommendation.
3. **Pick.** The user picks one or combines parts. Then delete the other versions and the switcher from the source; hidden versions still read as live designs to the implementing agent. Record each dropped version in the decisions list, one line each, with why it lost and anything taken from it.
4. **Refine, round by round.** Apply each round's feedback to the same file. Say in one line what changed, add any new decision to the list, and ask what is next. When a sub-question has real alternatives (two places for a control), give it a small local switcher and reduce it the same way once picked.
5. **Settle.** When the user calls it done: open the page from disk, click through every state, check the console is clean, and confirm the decisions list matches the page. Then hand it off.

After every round, give the file's absolute path, and open it when a desktop session exists (`xdg-open`, `open` or `start`).

## The file

- **One file that opens offline.** A single `.html` with inline CSS, JS and data. No CDN, web fonts, `fetch`, module `src`, workers or `localStorage`: it must work when opened from a downloaded ticket attachment.
- **Real sample data.** The project's real items, names and copy, never placeholder text. Inline it as one data block at the end of the file, so an agent reading the source meets the markup and logic first. When the data is extracted from project or library files rather than typed in, keep a small build script and a template named after the page, beside it, and rebuild instead of hand-editing the output.
- **The project's own parts and words.** Mock the surrounding screen with its existing components. Name panels, fields and controls as the code names them, so the implementing agent can map each part to a component.
- **Every state one click away.** Empty, loading, error and long values each get a toggle, so nobody has to imagine them.
- **Decisions on the page.** A short list near the top: what is settled and why, what is deliberately left out, and the versions that lost. State on the page that it is a design reference, not code to copy.
- **One stable name** from the first round to the last, such as `<feature>-prototype.html`, with no date, version or "options" in it, so links from the ticket and the spec stay valid. Keep it, with its template and build script, beside the design spec or the ticket's research notes, never in a scratch folder. If neither exists, ask the user where it should live.

## Handing it off

The ticket attaches the page and says in one line what it settles; the acceptance criteria stay in the ticket text (your set's ticket-writing skill owns that). A design spec, if there is one, owns the contract and links the page; the page never restates the contract. When the design changes later, update the same file, re-attach it, and note the change on the ticket. The user's request to attach covers the upload; any ticket text you wrote yourself, such as that line, is shown to the user and posted only after their go-ahead.
