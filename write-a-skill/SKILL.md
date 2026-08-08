---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill, or to update, audit, or modernize an existing skill's structure, frontmatter, or description.
---

# Writing Skills

_Authoring mechanics. If you're crystallizing a workflow you just ran (with the corrections that shaped it) rather than building from a fresh spec, enter via the extract-a-workflow-into-a-skill capability in your set — it adds the whether / what / where judgment, then leans on the steps below for structure._

## Process

1. **Gather requirements** - ask user about:
   - What task/domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?

2. **Baseline first** - run 1-3 representative scenarios WITHOUT the skill
   (fresh subagent). Document what fails; no failure → nothing to teach.

3. **Draft the skill** - create:
   - SKILL.md with concise instructions addressing the observed failures
   - Additional reference files if content exceeds the budget below
   - Utility scripts if deterministic operations needed

4. **Test with the skill** - rerun the scenarios in a fresh subagent with
   the skill loaded. Fold every reported gap back in, then re-test.

5. **Review with user** - present the draft: does it cover the use cases,
   is anything missing or unclear, should any section be more/less detailed?

## Skill Structure

```
skill-name/            # directory name = skill name (must match frontmatter)
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
```

## Frontmatter

The Agent Skills spec allows exactly six fields; Claude Code adds optional
extensions (invocation control, subagent execution, tool grants). Full field
tables, portability rules, and string substitutions:
[REFERENCE.md](REFERENCE.md).

- `name`: 1-64 chars, lowercase letters/numbers/hyphens only; no leading,
  trailing, or consecutive hyphens. Must match the directory name.
- `description`: max 1024 chars, third person. First sentence: what it does.
  Then "Use when [specific triggers, symptoms, keywords]" — and **never a
  workflow summary**: agents follow the summary instead of reading the body.
- Skills that must upload to claude.ai or the Skills API may use ONLY the
  spec's six fields — anything else fails the upload with a hard error.

## Body Guidelines

- Be concise: agents are already smart; add only what they don't know.
  Challenge every paragraph's token cost.
- Match freedom to fragility: heuristics for open-ended tasks, exact
  commands for fragile sequences (REFERENCE.md, "Degrees of freedom").
- One excellent example beats many mediocre ones. Consistent terminology;
  no time-sensitive info.
- References one level deep from SKILL.md; give reference files over 100
  lines a table of contents.
- For multi-step workflows, provide a checklist the agent can copy and tick
  off; for quality-critical output, add a validate → fix → repeat loop.

## When to Add Scripts

Add utility scripts when the operation is deterministic (validation,
formatting), the same code would be generated repeatedly, or errors need
explicit handling. Scripts save tokens and beat generated code on
reliability; they must handle errors themselves, not punt to the agent,
and justify every constant.

## When to Split Files

Split into separate files when SKILL.md exceeds 100 lines (hard cap from
the spec: 500), when content has distinct domains (finance vs sales
schemas), or when advanced features are rarely needed.

## Cross-Skill References

In a generic/portable skill, reference other skills **by capability, never
by name** ("your set's browser-driving skill, if one exists") — names drift
between sets and projects; capabilities don't. Hard names are allowed only
inside a project-specific skill referring to siblings in the same
co-maintained set.

## Review Checklist

- [ ] Baseline run showed a real failure the skill addresses
- [ ] `name` matches directory; lowercase/hyphens; ≤64 chars
- [ ] Description includes triggers ("Use when..."), no workflow summary
- [ ] Only spec fields if the skill must be portable beyond Claude Code
- [ ] SKILL.md under 100 lines; references one level deep
- [ ] No time-sensitive info; consistent terminology
- [ ] Concrete examples included; scripts handle their own errors
- [ ] Cross-skill references follow the capability-vs-name rule
- [ ] Re-tested with the skill loaded; reported gaps folded back in
