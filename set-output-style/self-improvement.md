# Self-improvement

## Rule

Append this block to the CLAUDE.md, with `<STYLE_FILE>` and `<MISS_LOG>` replaced by the real paths.

```markdown
## Output style self-improvement

Keep my output style improving from my corrections. The style is `<STYLE_FILE>`. The miss log is `<MISS_LOG>`.

- When I say I didn't understand and you re-explain in other words or another way, append one entry under the log's newest "Since" section: the date, what I said, what the first explanation did wrong, and what the re-explanation did that worked. Count retries on the same point as one entry. Tag it `gap` if the style has no rule for it, or `slip` if a rule exists and the reply broke it.
- When I praise how a reply is written, add it under "Good examples": what I said, what made the reply work, and the session it came from.
- Don't change the style for a single miss. After each new entry, count the `gap` entries in the newest "Since" section. When they reach 6, or when I ask, propose one revision of the style drawn from those entries.
- Before a revision ships, replay the logged missed answers and the good examples under the old style, the new style and no style, judged blind against the logged corrections. Ship the new style only if it follows the corrections better than both, keeps every good example as good, and invents no facts. If no style does as well, propose dropping the style.
- When a revision ships, start a new "Since <date>" section in the log.
- Keep the style short: prefer one example over one more rule, and a revision should not grow the file. The style stays purely presentational: output formatting only, no behavior rules.
```

## Miss log starting text

Write this as the new miss log, with `<date>` replaced by today's date.

```markdown
# Output-style miss log

Entry format: - **YYYY-MM-DD** `gap`|`slip` — what I said · what the first explanation did wrong · what the re-explanation did that worked

## Good examples

## Since <date>
```
