---
name: set-output-style
description: Sets up the answer-formatting style defined in output-style.md at the level the user picks — user-wide, current project, or this session only. Purely cosmetic — never alters reasoning, tool usage, file edits, or the factual content of the work.
disable-model-invocation: true
---

# Set Output Style

`output-style.md` in this skill's directory defines the style; its frontmatter `name` is the style's display name. Do not restate or summarize the style — it is the single source of truth.

First ask the user at which level to set it up (use a structured question tool if available), then perform the chosen setup yourself:

- **User level (all projects):** copy `output-style.md` into `~/.claude/output-styles/` (create the directory if missing), then set `"outputStyle"` to the style's display name in `~/.claude/settings.json`. Takes effect on new sessions or `/clear`.

- **Project level (this repo):** same, but copy into the project's `.claude/output-styles/` and set `"outputStyle"` in the project's `.claude/settings.json` (or `settings.local.json` if the user doesn't want it shared).

Always copy — never symlink; installed copies stay independent of this skill's directory.

Before writing at user or project level, check the target settings file's existing `"outputStyle"`:

- **Not set, or already this style:** proceed without asking; overwrite an existing copy of the style file (that's an update).
- **Set to a different style:** ask the user whether to override it before changing the setting.

- **This session only:** no files touched — read `output-style.md` (ignoring its frontmatter) and apply its directives to every final answer for the rest of the session.

For user or project level, also apply the style in the current session immediately, since the setting only loads on a fresh session. Confirm what was written and where.
