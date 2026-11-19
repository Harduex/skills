# Learning a style from an interview

The interview shows pairs of sample replies and writes a style from the user's picks. Every rule in the result comes from a pick or a note. Nothing comes from the shipped style.

## 1. Subject

Ask one open question: what does the user mostly work on, and what do they read replies about? Write every sample on that subject, with invented content. Never read the user's files for samples. If the user skips the question, use a small to-do app. Take the topics' examples from the subject too: for a spreadsheet user, a "name" is a cell or column name, and "evidence" is the figures.

## 2. One pair at a time

Show each pair in this shape:

1. One line that says what the sample reply answers. Example: "You asked whether last night's import failed." In the re-explanation scenario, the line also gives the first answer in short.
2. Version X, then version Y. Keep each one short: two or three sentences. Use more only when the topic's side needs it, such as a full paragraph, a table, headings, a complete draft or the full evidence.
3. The choices: X, Y, or "About the same". The user can also write a note.

With a question tool that shows a preview for each option, put each version in its option's preview. Without one, show both versions in the chat and ask for X, Y or "same".

## 3. Topics

Each topic has two sides. One version of the pair shows one side, the other version shows the other side.

| Topic | One side | Other side |
|---|---|---|
| Length | the answer and its key facts | the same, plus a paragraph of background |
| Opening | the answer in the first sentence | the context first, the answer last |
| Layout | several points as bullets | the same points as prose |
| Comparison | a small table | a list |
| Emphasis | key lines in bold | no bold |
| Names | the exact names of things (`retryLimit`, cell `B4`) | plain words ("the retry limit") |
| Teaching order | an example first, then the rule | the rule first, then an example |
| Analogy | one analogy | no analogy |
| Headings | a heading for each part | no headings |
| Decision | the recommendation first, then the options | the options first, the recommendation last |
| Findings list | the recommendation stated once | a verdict on every item |
| Draft for someone else | short and plain | complete and formal |
| Re-explanation | start over from a new angle | add detail to the first answer |
| Proof | one line on how it was checked | the full evidence, such as commands and output, or the figures |

## 4. Scenarios

Set each pair in one reply type: a yes/no answer, an explanation, a decision, a findings list, a status report, a draft for someone else, or a re-explanation after "I don't get it". The topics Decision, Findings list, Draft for someone else and Re-explanation have their own scenario. Spread the other topics over the scenarios, so that each scenario appears at least once.

## 5. Order and stopping

- Ask the broad topics first: length, opening and layout. Then ask the rest.
- Skip a topic that an earlier pick or note already settles. For example, "always as short as possible" settles length in every scenario.
- Plan one pair per topic, plus the two check pairs in section 7: up to 16 pairs. Never show more than 20.
- After every 5 pairs, offer to stop and write the style from the answers so far, unless no pairs are left.
- A note is an answer. It can settle one topic or several, or state a preference that no topic covers. Keep it in the user's words. When it points at the sample, such as "this short", write down what it points at.
- A note counts like a pick on the topic it is about: "I prefer paragraphs" is a layout answer, whatever pair it came with. A note that names no topic, such as "shorter please", is about its pair's topic only. With a word such as "always" or "everywhere", it applies to every reply.
- When a note or pick contradicts an earlier one, the later one wins. A check pair is the exception: a flip there means no clear preference (section 7).

## 6. Writing a pair

1. Write the reply for one side, in the topic's scenario.
2. Write the reply for the other side from the first. Change only what the topic changes. Keep the facts, the scenario and the tone, unless the topic itself is about length, tone or detail. For length, both versions open with the same sentence, and the long one adds its background after it.
3. Before you show the pair, compare the two replies sentence by sentence. Everything outside the topic must match. If anything else differs, rewrite the second reply and compare again.
4. Label the two replies X and Y at random. X is always shown first. Over the interview, show the table's "One side" column as X in about half the pairs.

Never show the comparison, and never say which side a version shows.

## 7. Position check

Make pairs 9 and 10 the check pairs, before the second offer to stop. Each one asks again about a topic that the user picked without a note. Prefer topics where the picked version was X, shown first. If fewer than two topics qualify, check as many as there are, and use the free pair for the next topic. Use new content, and put the picked side in the other position. If the pick flips, the topic has no clear preference. If the user stops before pair 9, use the picks as they are.

## 8. Writing the style

A topic's preference is the user's last word on it: a pick or a note. A topic has no clear preference when that last word is "About the same", or when its check pair flipped. Then:

1. Write one plain rule for each topic with a clear preference. Word it as the side the user chose against the side they turned down, such as "leave out the background". Never turn it into a count or a limit that the samples did not test. If the preference differs by scenario, name the scenario in the rule.
2. Add a rule for each preference that a note states outside the topics.
3. Write no rule for a topic without a clear preference, or for a topic you did not ask about.
4. Add one example, marked GOOD. Start from the picked version that shows the most of the style's rules, never one that a later pick or note overrode. Change only what breaks a rule, and keep its facts. Remove formatting that no rule asks for.
5. Keep every rule about how a reply looks. Write no rule about what to investigate, test or ask.

If fewer than three topics have a clear preference, say so. Then offer the shipped style or a blank style instead, and save the learned one only if the user still wants it.

Ask the user to name the style, and suggest a name. If `output-styles/` already has a file for that name, ask whether to overwrite it or pick another name. Then show the draft. Say that the lines between the dashes at the top are settings for the tool, and that they must stay. Let the user change the draft, and save it only after the user agrees. A learned style looks like this:

```markdown
---
name: Short And Direct
description: Learned from an interview of sample replies.
keep-coding-instructions: true
---

# Output Style: Short And Direct

- Put the answer in the first sentence.
- Give the answer and its key facts. Leave out the background.
- Put several points in bullets, not in a paragraph.
- Use real code names, not plain-word stand-ins.
- In a decision, give the options first and the recommendation last.

GOOD:
> The import failed at 02:10.
> - The `orders` table was locked by the backup job.
> - I'd move the backup to 03:00.
```
