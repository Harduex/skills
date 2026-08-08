# Skill Authoring Reference

## Contents

- Frontmatter: the Agent Skills spec fields
- Frontmatter: Claude Code extensions
- Portability rules
- String substitutions and dynamic context
- Degrees of freedom
- Progressive disclosure patterns
- Testing skills
- Anti-patterns

## Frontmatter: the Agent Skills spec fields

The [Agent Skills spec](https://agentskills.io/specification) defines exactly
six fields. These work in every runtime that implements the standard.

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | 1-64 chars; lowercase letters, numbers, hyphens; no leading/trailing/consecutive hyphens; must match the directory name |
| `description` | Yes | 1-1024 chars; what the skill does and when to use it |
| `license` | No | License name or pointer to a bundled license file |
| `compatibility` | No | ≤500 chars; environment requirements (product, packages, network). Most skills don't need it |
| `metadata` | No | String-to-string map for your own tooling; use distinctive key names |
| `allowed-tools` | No | Space-separated pre-approved tools (experimental in the spec). The field name is portable; rule syntax like `Bash(...)` and the grant semantics are runtime-specific — see the extensions table |

Validate with the reference tool: `skills-ref validate ./my-skill`.

## Frontmatter: Claude Code extensions

Claude Code accepts all spec fields plus these. All optional; boolean fields
accept true/false (and yes/no, on/off, 1/0).

| Field | What it does |
|---|---|
| `when_to_use` | Extra trigger context appended to the description in listings (combined cap ~1536 chars) |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` |
| `arguments` | Named positional args for `$name` substitution |
| `disable-model-invocation` | `true` = only the user can invoke (via `/name`); the model never auto-loads it. For side-effectful workflows. The description then documents the skill for the human in the `/` menu — model-trigger keywords are moot |
| `user-invocable` | `false` = hidden from the `/` menu. For background knowledge |
| `allowed-tools` | Tools usable without permission prompts during the invoking turn |
| `disallowed-tools` | Tools removed while the skill is active |
| `model` / `effort` | Model or effort override while the skill is active |
| `context: fork` | Runs the skill in a subagent instead of the main thread |
| `agent` | Subagent type for `context: fork` |
| `background` | With `context: fork`: `false` waits for the result in-turn |
| `hooks` | Hooks scoped to the skill's lifecycle |
| `paths` | Glob patterns; auto-load only when working on matching files |
| `shell` | `bash` (default) or `powershell` for inline `!` commands |

## Portability rules

Where the skill will run decides which fields you may use:

- **Claude Code** (personal, project, plugin skills): every field above.
- **claude.ai uploads, Skills API, `package_skill.py`**: ONLY the spec's six
  fields. Any other key fails packaging/upload with a hard error
  ("Unexpected key(s) in SKILL.md frontmatter").
- **Other runtimes** (Codex, Gemini CLI, ...): assume spec fields only.

For a skill that must travel, restrict frontmatter to the spec six — Claude
Code loads spec-only frontmatter unchanged. Claude Code-only body features
(dynamic context injection below) silently do nothing elsewhere; don't make
correctness depend on them in a portable skill.

## String substitutions and dynamic context

Claude Code substitutes these in the skill body:

| Variable | Meaning |
|---|---|
| `$ARGUMENTS` | All invocation arguments (appended as `ARGUMENTS: <value>` if absent) |
| `$0`, `$1`, ... | Single argument by position (`$ARGUMENTS[N]` long form) |
| `$name` | Named argument declared in `arguments` |
| `${CLAUDE_SKILL_DIR}` | Directory containing this SKILL.md |
| `${CLAUDE_PROJECT_DIR}` | Project root |
| `${CLAUDE_SESSION_ID}` | Current session id |

Dynamic context injection: a `` !`command` `` line runs the command and
replaces the line with its output *before* the model reads the skill —
e.g. `` !`git diff HEAD` `` grounds the instructions in the live diff.

Bundled script without permission prompts — use the same variable in
`allowed-tools` and the body:

```yaml
---
name: render-chart
description: Render a chart from a CSV file. Use when ...
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)
---
Run `${CLAUDE_SKILL_DIR}/scripts/render.sh <csv-file>`.
```

Drop the trailing `*` (`Bash(${CLAUDE_SKILL_DIR}/scripts/deploy.sh)`) when a
fragile script must run with no arguments — the tighter rule matches the
low-freedom instruction in the body.

## Degrees of freedom

Match instruction specificity to the task's fragility:

- **High freedom** (prose heuristics): many valid approaches, context
  decides. "Analyze structure, check edge cases, suggest improvements."
- **Medium freedom** (template with parameters): a preferred pattern exists,
  variation is fine. Pseudocode or a script with knobs.
- **Low freedom** (exact commands, no parameters): fragile or destructive
  sequences. "Run exactly `python scripts/migrate.py --verify --backup`.
  Do not add flags."

Narrow bridge with cliffs → exact guardrails. Open field → direction and
trust.

## Progressive disclosure patterns

Loading is staged: metadata (name + description) is always in context; the
SKILL.md body loads on activation; other files load only when followed.
Budget accordingly — the body should be lean, bundled files can be big.

- **High-level guide with references**: quick start inline; "Form filling:
  see [FORMS.md](FORMS.md)" for the rest.
- **Domain organization**: `reference/finance.md`, `reference/sales.md` —
  a sales question never loads finance schemas.
- **Conditional details**: basic path inline, "For tracked changes: see
  [REDLINING.md](REDLINING.md)".

Keep references one level deep — a chain (SKILL.md → advanced.md →
details.md) gets partially read (`head -100`) and information is lost. Give
files over 100 lines a table of contents so partial reads still reveal scope.
Name files by content (`form_validation_rules.md`, not `doc2.md`); forward
slashes always.

## Testing skills

A skill is tested code: no skill (or edit) ships without evidence it changes
behavior.

1. **Baseline (RED)**: fresh subagent, representative task, no skill.
   Capture what fails, what gets improvised, which wrong defaults appear.
   No failure → no skill needed. Baseline side-effectful workflows
   (deploys, notifications) against a dry run or sandbox, never live
   targets.
2. **With the skill (GREEN)**: same task, fresh subagent, skill loaded. Ask
   it to report gaps, ambiguities, and contradictions it hit — testers find
   holes authors can't see.
3. **Fold back and re-test (REFACTOR)**: every reported gap becomes an edit;
   re-run until the scenarios pass clean.

Match the test to the skill type: discipline skills (rules under pressure)
need pressure scenarios and a rationalization table; technique and reference
skills need application/retrieval scenarios like the above. If several
models will run the skill, test with the smallest one you support — what
Opus infers, Haiku needs stated.

## Anti-patterns

- **Workflow summary in the description** — the agent follows the summary
  and skips the body. Triggers only.
- **Time-sensitive content** — "before August 2025 use the old API" rots;
  keep a collapsed "old patterns" section if history matters.
- **Too many options** — give one default and an escape hatch, not a menu
  of five libraries.
- **Multi-language example dilution** — one excellent example; agents port
  well.
- **Windows paths** — `scripts\helper.py` breaks on Unix; always
  `scripts/helper.py`.
- **Magic constants in scripts** — `TIMEOUT = 47  # why?` If you can't
  justify the value, the agent can't either.
- **Narrative storytelling** — "In session X we found..." is not reusable;
  distill the technique.
