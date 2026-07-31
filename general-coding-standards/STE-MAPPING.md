# STE Provenance: Where Every Rule Comes From

This skill translates **ASD-STE100 Simplified Technical English, Issue 9,
January 2025** (Aerospace, Security and Defence Industries Association of
Europe) — 53 writing rules in 9 sections, 8 general recommendations (GR), and a
controlled dictionary — into the 40 coding rules of this skill.

Every source item below is mapped to a skill rule or explicitly marked N/A with
a reason. Each row **paraphrases** the source rule's full meaning in this
file's own words: the specification is copyrighted and is not reproduced here.
Section and page numbers locate the original for readers who hold a licensed
copy. Several source rules merge into one coding rule; that is why 53 + 8 + 1
source items produce 40 rules.

## Part 1 — Writing rules

| STE | What the source rule requires (paraphrase) | Page | → Skill rule / N/A |
|---|---|---|---|
| 1.1 | Draw every word from an approved source: the controlled dictionary, or a recognized technical noun or technical verb. | 43 | N1 |
| 1.2 | Each dictionary word may be used only as the part of speech the dictionary assigns it. | 43 | N4 |
| 1.3 | Each dictionary word carries exactly the meaning the dictionary assigns it — no other senses. | 43 | N2 |
| 1.4 | Only the sanctioned forms of verbs and adjectives are allowed. | 43 | N5 |
| 1.5 | Words that qualify as technical nouns — they fit one of the named domain categories — are permitted even when the dictionary lacks them. | 43 | C4 |
| 1.6 | A word outside the dictionary is allowed only when it is, or belongs to, a technical noun. | 43 | N1 |
| 1.7 | Never turn a technical noun into a verb. | 43 | N4 |
| 1.8 | Pick the technical nouns your company, industry, or field has standardized. | 43 | N8 |
| 1.9 | When choosing among technical nouns, prefer the short, easily understood one. | 43 | N7 |
| 1.10 | Regional expressions, slang, and jargon are barred from technical nouns. | 43 | N7 |
| 1.11 | An item keeps a single technical noun — never several names for one thing. | 43 | N3 |
| 1.12 | Verbs that qualify as technical verbs — they fit a named domain category — are permitted. | 43 | C4 |
| 1.13 | Never turn a technical verb into a noun. | 45 | N4 |
| 1.14 | Spell per American English, except where an official directive overrides. | 45 | N9 |
| 2.1 | Cap noun clusters at three words. | 61 | N6 |
| 2.2 | A technical noun longer than three words is first written out fully; afterwards a shorter form, or hyphens joining the tightly bound parts, keeps it clear. | 61 | N6 |
| 3.1 | Verbs take only the forms the dictionary lists for them. | 67 | N5 |
| 3.2 | Permitted verb usage: infinitive, command form, the three simple tenses, and past participle serving as an adjective — nothing else. | 67 | S3, N5 |
| 3.3 | A past participle serves as an adjective describing a condition; that is not passive voice. | 66 | N5 |
| 3.4 | Never stack auxiliary verbs into complicated constructions. | 67 | S6 |
| 3.5 | An "-ing" form appears only inside a technical noun or as its modifier. | 67 | N5 |
| 3.6 | Prefer active voice; passive is tolerated only in description, and only where the actor is unknown. | 67 | S5 |
| 3.7 | Express an action through an approved verb, never through a noun or another part of speech standing in for it. | 74 | S7 |
| 4.1 | Keep sentences brief and clear. | 77 | S1 |
| 4.2 | Brevity never comes from dropping words or contracting them. | 77 | S8 |
| 4.3 | Complicated material becomes a vertical list. | 77 | S9 |
| 4.4 | Link sentences on related topics using connecting words and phrases. | 77 | M5 |
| 4.5 | Where it fits, put an article or a demonstrative before nouns. | 77 | P4 |
| 5.1 | Procedural sentences stay within twenty words. | 87 | S1, P1 |
| 5.2 | Each sentence holds a single instruction, except for genuinely simultaneous actions. | 87 | S2, P2 |
| 5.3 | Instructions take the command form. | 87 | S3, P2, P8 |
| 5.4 | A precondition the reader needs comes first, as a descriptive clause set off by a comma; the command follows. | 87 | S4, P2 |
| 5.5 | Notes exist to inform; they never instruct. | 87 | W4 |
| 6.1 | Release information bit by bit. | 93 | M3, P3 |
| 6.2 | Structure text logically around key words and phrases. | 93 | M4 |
| 6.3 | Descriptive sentences stay within twenty-five words. | 93 | P1 |
| 6.4 | Group related material into paragraphs. | 93 | P3 |
| 6.5 | A paragraph covers a single topic. | 93 | M1, P3 |
| 6.6 | A paragraph holds six sentences at most. | 93 | M2, P3 |
| 7.1 | Signal the level of risk with the fitting label word — injury/death versus damage to objects each get their own. | 101 | W1 |
| 7.2 | A safety instruction opens with an exact, truthful command or condition. | 101 | W2 |
| 7.3 | Add the explanation that reveals the risk or the possible outcome. | 105 | W3 |
| 8.1 | Standard punctuation is fine; semicolons are the exception and are barred. | 105 | N/A — English punctuation mechanics; the clarity intent (short, single-idea statements) is carried by S2 and P1 |
| 8.2 | Hyphenate words that belong directly together. | 107 | N6 |
| 8.3 | Parentheses serve enumerated purposes: cross-references, item callouts, step labels, abbreviations, singular/plural pairs, explanations, alternatives. | 107 | N/A — English punctuation mechanics; general prose clarity is carried by the P band |
| 8.4 | In vertical lists, a colon closes a sentence for counting purposes, like a period. | 107 | N/A — word-count mechanics; code size units are lines, parameters, and nesting (S1, M2) |
| 8.5 | A parenthesized insert adds one to the sentence's word tally. | 107 | N/A — word-count mechanics; code size units are lines, parameters, and nesting (S1, M2) |
| 8.6 | Certain elements — numbers, measurements, abbreviations, identifiers, quotations, titles, proper names — each tally as a single word. | 107 | N/A — word-count mechanics; code size units are lines, parameters, and nesting (S1, M2) |
| 8.7 | A hyphenated cluster tallies as a single word. | 114 | N/A — word-count mechanics; code size units are lines, parameters, and nesting (S1, M2) |
| 9.1 | When swapping one word for an approved one breaks down, recast the whole sentence instead. | 114 | C2 |
| 9.2 | Apply each approved word properly — some carry restricted, context-bound meanings. | 118 | N2, C2 |
| 9.3 | Never combine words into phrasal verbs. | 114 | C3 |
| 9.4 | Keep terminology and phrasing uniform throughout. | 114 | C1, P5 |

## General recommendations

| STE | What the source recommends (paraphrase) | Page | → Skill rule / N/A |
|---|---|---|---|
| GR-1 | Keep the conjunction "that" before subordinate clauses; dropping it invites ambiguity. | 123 | P4 |
| GR-2 | "with" carries several senses — reread such sentences for ambiguity, and keep the real action verb in view. | 124 | P4, P2 |
| GR-3 | Where a pronoun could point at more than one noun, substitute the noun itself. | 124 | P4 |
| GR-4 | When "this" could point at several things, restate the context it refers to. | 125 | P4 |
| GR-5 | Watch for look-alike words whose English sense differs from their sense in your native language. | 125 | C5 |
| GR-6 | Skip Latin shorthand and write the English phrase out — readers may not know the abbreviation. | 126 | P6 |
| GR-7 | Write gender-neutrally; biased or gendered wording has no place. | 126 | P7 |
| GR-8 | The apostrophe-s possessive is allowed but hard on non-native readers — skip it when unsure. | 127 | N/A — English-grammar caution; prose simplicity is carried by P1 |

## Part 2 — Dictionary

| STE | What the source provides (paraphrase) | Page | → Skill rule / N/A |
|---|---|---|---|
| Part 2 | A closed list of approved words (875), each with its sanctioned meaning and usage examples, plus 1,274 unapproved words, each pointing at approved replacements. Domain vocabulary lives outside the list, in the technical noun/verb categories. | 131 | N1, N2, N3 + the NAMING.md vocabulary mechanism (glossary template, approved verbs, banned words) |

## Updating for a future STE issue

When a new issue of the specification ships, diff its changelog against this
table: a changed source rule identifies exactly which skill rules to revisit.
The maintainers keep a verbatim, citation-verified extraction worksheet in a
private source notebook; this public table carries only paraphrases.
