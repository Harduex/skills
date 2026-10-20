---
name: explaining-visually
description: Decides when an answer needs a visual explanation — one self-contained HTML page with a labelled diagram, a step-through, or a slider explorable that the user opens in a browser — and writes that page. Use when the user asks to see, visualize, diagram, chart, animate, or play with something; when the user still does not understand after a text re-explanation of the same point; or when an answer's core is change over time, a what-if between interacting quantities, or a spatial layout that a Markdown table or a short ASCII sketch cannot carry. Not for requests to build an HTML page, site, or component as a deliverable, and not for facts, definitions, yes/no answers, commands, code to copy, or comparisons a short Markdown table covers.
---

# Explaining Visually

Text is the default. A page is a second channel for the few answers whose core is a shape that prose carries badly, and the chat reply stays complete without it. A short reply plus a page is a concise answer, not piling on more. **Run the gate before every explanation for the rest of the conversation**, not only on the turn that loaded this skill.

## The gate — in order, stop at the first match

1. **Text only** when the user prefers text; when they asked for an HTML page, site, or component as a deliverable (that is a normal build task); or when the answer is a fact, definition, yes/no, opinion, command, or code to copy.
2. **Page** when the user asks to see, visualize, diagram, chart, animate, simulate, or play with it.
3. **Page on the second miss** of the same point. A miss is a sign that a point has not landed: "I don't get it", "still confused", "what?", the same question rephrased, or a follow-up that repeats the misconception. "I keep mixing up X" counts as one miss. Aim the page at the step that is not landing.
4. **Page, proactively,** when the core is change over time or a sequence of states (a step-through the user advances), a what-if between interacting quantities (sliders with live results), or a spatial layout (a labelled diagram), and a static table or short ASCII sketch can't show it because the user would need to vary an input, step through states, or see positions. You must be able to say what the page shows that text can't.
5. **Otherwise text.** If a visual would still help, end with one line offering the page.
   - First miss: re-explain from scratch — plainer, on one concrete example from the user's own case.
   - Third miss: stop adding media. Ask which step loses them, and look for a missing prerequisite.

## The page

- One self-contained `.html` file with inline CSS and JS. No CDN, no web fonts, no `fetch`, no `<script type="module" src>`, no workers loaded from files: all of these break when a page is opened from disk. Don't rely on `localStorage`.
- One idea per page, built on the user's own values, code, or example.
- The key point is readable before any interaction, and controls start in a realistic state. Every number comes from a formula or data shown on the page.
- System fonts, light and dark themes (`prefers-color-scheme`), keyboard-usable controls, and labels beside the parts they name. No decoration.
- For an explorable, put one "predict first" prompt before the controls and one check question after them. Never ask "makes sense?".
- A map of a system's components belongs to your set's system-graph skill, if one exists.

## Delivering it

- Save the page to `~/.agent/visuals/<YYYY-MM-DD>-<slug>.html`, creating the folder if needed. Open it when a desktop session exists (`xdg-open`, `open`, or `start`).
- Reply with the answer in one to three sentences, what to try first on the page, and its absolute path.
- If the conversation is summarized, carry this line into the summary: `Re-load explaining-visually before building or updating a visual page.`
