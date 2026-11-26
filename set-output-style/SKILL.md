---
name: set-output-style
description: "Sets up an answer-formatting output style at user or project level: the style shipped in output-style.md, a blank one, or one learned by interviewing the user with pairs of sample replies, with optional self-improvement from the user's corrections. Use when the user wants to install, start, learn, or change their output style. Purely cosmetic — never alters reasoning, tool usage, file edits, or the factual content of the work."
disable-model-invocation: true
---

# Set Output Style

Files in this skill's directory:

- `output-style.md` is the shipped style. Its frontmatter `name` is the style's display name. Do not restate or summarize it: it is the single source of truth.
- `self-improvement.md` holds the self-improvement rule and the miss log's starting text.
- `interview.md` is the interview that learns a style from the user's picks.
- `replay-test.md` is the method for testing a style revision before it ships.

## 1. Ask

Ask the first two questions together, with a structured question tool if available. Skip a question that the user's request already answers.

- **Style:** the shipped style (say its display name), a blank style that starts empty, or a style learned from an interview: the user picks between pairs of sample replies, up to 16 pairs.
- **Level:** user level (all projects, `~/.claude/`) or project level (this repo, `.claude/`).

Then ask the third: **Turn on self-improvement?** With it on, each time the user says they didn't understand an answer, the miss is logged, and once enough misses collect, a tested revision of the style is proposed. It works the same for every style.

## 2. Install the style

Below, `<dir>` is `~/.claude/` at user level, or the project's `.claude/` at project level.

1. Create `<dir>output-styles/` if missing, then add the style file:
   - **Shipped style:** copy `output-style.md` there. Always copy, never symlink: installed copies stay independent of this skill.
   - **Blank style:** create `my-style.md` there with only this frontmatter. Keep `keep-coding-instructions: true`, because without it Claude Code drops its own coding instructions while the style is active.

     ```markdown
     ---
     name: My Style
     description: Your own answer style. It starts empty and grows from your corrections.
     keep-coding-instructions: true
     ---
     ```
   - **Learned style:** run the interview in `interview.md`. Save the style it produces as `<name>.md`, where `<name>` is the style's display name in lowercase with hyphens. The interview already asks about an existing file with that name, so skip step 2.
2. If that file already exists there and differs from what you would write, ask before overwriting it, and keep it if they decline. It may hold the user's own revisions.
3. Set `"outputStyle"` to the style's display name in `<dir>settings.json`. At project level, use `settings.local.json` instead if the user doesn't want the setting shared. If `"outputStyle"` is already set to a different style, ask before changing it.

## 3. Turn on self-improvement (only if the user said yes)

1. Create the miss log at `<dir>output-style-misses.md` from the starting text in `self-improvement.md`, unless the file already exists. Never put it in `output-styles/`: Claude Code loads every Markdown file there as a style.
2. Append the rule from `self-improvement.md` to the CLAUDE.md at the same level: `~/.claude/CLAUDE.md`, or the project's root `CLAUDE.md`. Create the file if missing. Replace its two placeholders with the real paths: `~/.claude/...` at user level, repo-relative paths at project level. Skip this step if that CLAUDE.md, or a file it imports with `@`, already has a rule for an output-style miss log.

The rule goes in CLAUDE.md, not in the style, because the style stays purely presentational and CLAUDE.md is loaded in every session.

## 4. Finish

Apply the style to your own answers for the rest of this session. Claude Code reads style files at startup, so tell the user the setting takes effect after a restart or in a new session. Confirm what was written and where.
