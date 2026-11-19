# Replay test

How to test a style revision before it ships. The test rewrites real past replies under each style, has blind judges compare the rewrites against the user's own corrections, and asks the user to judge the close calls.

## 1. Pick the cases

1. **Sort the misses.** For each entry in the miss log's newest "Since" section, find the exchange in the session transcripts by searching for a phrase of the user's message. Compare the reply the user pushed back on with the re-explanation that landed, and label the entry:
   - **real:** the re-explanation added something the first reply lacked, such as a concrete case, a definition, the answer moved to the front, or a map of the parts.
   - **tired:** the first reply already had it. Quote the passage that proves it.
   - **fact:** the miss came from a wrong or unchecked claim, not from the writing.
   - **page:** the miss was in a page or a file, not in a chat reply.

   Only real misses become cases. Show the user the list before going on.
2. **Build one case per real miss.** A case file has three sections:
   - `## Context`: the task in a few lines, then the facts the assistant had established before the reply, from earlier turns and tool results. Never add facts found later, and never the re-explanation's wording or examples.
   - `## Question`: the user's message, verbatim.
   - `## Original answer`: everything the user saw in that turn, verbatim: progress lines, the reply, and any question box or form.

   Put the user's pushback, verbatim, in a separate reaction file. Keep the re-explanation that landed for yourself. Never show it to rewriters or judges.
3. **Build a regression set,** so that the test also catches a revision that makes good replies worse. Use every praised reply in "Good examples", about six ordinary replies that landed (the user's next message moves on), and the cases of earlier rounds. Cover a short status, a decision with options, a list of findings, an explanation, a draft for someone else, and a report after testing.

## 2. Rewrite

- Test three styles: the old one, the new one, and no style, which is a one-line file: "You write replies in your own default way. No output style applies." Give every style the same always-on instructions the user has, such as a CLAUDE.md line about formatting.
- Rewrite every set twice per style, with a fresh agent for each set and try. One agent makes some choices once for all its cases, such as keeping or dropping progress lines. Two tries keep one agent's choice from deciding the result.
- Brief each rewriter with the template below. Give it only the style, the always-on lines and the case files.

## 3. Judge

- Copy the rewrites into one folder per case under shuffled labels (A, B, C). Keep the key outside the folders that the judges open.
- Use one fresh judge per set and try, with the template below. The requirements are the user's own corrections from every entry in the log, each quoted in the user's words, plus "facts intact".
- Tally the wins per style. Trust a win that both tries agree on, and treat a split as a close call.

## 4. Ask the user about the close calls

Show the user up to six blind pairs. Each pair is the same part of the old and the new rewrite of one case, two or three sentences each, in random order as X and Y. Offer an "About the same" choice and room for a note. Put one line before each pair that says what the user had asked. Unblind the pairs after the user answers. Their notes often name what neither style fixes: log those for the next revision.

## 5. Decide

Ship the new style only if it wins the misses, does no worse on the regression set, and keeps every praised reply as good. It must also have no fact problem that the old style doesn't share. Record the result in the miss log: move the counted entries under "Addressed by <version>", and say which ones the test showed fixed, which it could not test, and which were not counted and why.

## Limits

- A rewrite can only rearrange and reword what the original reply knew. A rule that needs new content, such as the user's own numbers or a worked example that was never written, can't win in this test. Such a rule ships untested, or is dropped.
- Progress lines appear in the chat before the reply, while the work runs. Judge the reply from its first sentence after them. Otherwise a rewriter's choice to keep them decides the result.
- Judges word their verdicts differently. Ask for the fixed winner line in the template, so that the tally needs no guessing.

## Rewrite brief (template)

```markdown
You rewrite a coding assistant's chat replies under one output style.

- Follow STYLE exactly as if it were your own system prompt, and follow ALWAYS_ON too.
- Presentation only: change the order, words, structure, length and emphasis. Do not redo the work, and do not answer a different question.
- Keep every fact the user needs, including warnings, commitments and the decisions asked of them.
- Invent nothing. You may use facts from a case's Context section, because the assistant knew them.
- Write each reply exactly as the user would see it, and nothing else. Do not mention the style or these rules.
- Open only STYLE, ALWAYS_ON and the case files. For each CASES/X.md, write OUT/X.md.
```

## Judge brief (template)

```markdown
You judge blind rewrites of a coding assistant's replies. Each case has the original answer, the reader's reaction, and rewrites A, B and C under unnamed styles. One of them may use no style.

Requirements (apply only those that fit the case):
- R1 <the correction, in a few words>. ("<the user's own words>")
- ...
- Rn Facts intact. Nothing is invented, bent, or dropped that the reader needs.

A reaction that pushes back marks a missed reply: judge whether the pushback would recur. A reaction that moves on or praises marks a reply that landed: judge whether the rewrite would still land.

Progress lines, written while the work ran (such as "Reading the file…"), appear in the chat before the reply. Judge the reply from its first sentence after them, but still count any fact that a rewrite dropped.

Decide the winner in this order: no fact problem, then the reaction does not recur, then the fewest requirements broken, then the least reading. Call a negligible difference a tie.

For each case, write a table (rewrite, requirements broken, reaction recurs?, fact problems, note), then exactly one line:
Winner: <A|B|C|tie|tie A+B>, <negligible|small|large>

Open only the cases, the reactions and the blind folders.
```
