---
name: scaffold-project-harness
description: Scaffolds or retrofits a project's agent harness — the AGENTS.md instruction file plus a standard set of per-domain project skills (coding standards, design system, data layer, db ops, e2e tests, browser-testing wrapper, domain playbooks). Use when setting up agent instructions or skills for a new project, when a project has no harness yet, or when mapping the standard skill taxonomy onto an existing codebase.
---

# Scaffold Project Harness

Set up (or fill gaps in) a project's agent harness: one instruction file the agent always sees, plus per-domain skills it loads on demand. Interview the user at the decision points marked below; derive everything else from the codebase.

## Process

```
Scaffold checklist:
- [ ] Phase 1: Detect what exists
- [ ] Phase 2: Map the stack to skill domains
- [ ] Phase 3: Pick the skills home (ask)
- [ ] Phase 4: Instruction file (AGENTS.md + CLAUDE.md pointer)
- [ ] Phase 5: Create the applicable skills
- [ ] Phase 6: Verify wiring
```

### Phase 1 — Detect what exists

Look for `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/skills/`, and a skills-manager config (e.g. `agents.toml`). Anything present → retrofit mode: audit it, fill gaps only, never overwrite hand-written content. Nothing present → greenfield mode.

### Phase 2 — Map the stack to skill domains

Read the package manifests and top-level layout, then fill this mapping — one skill per domain that actually exists in the project:

| Domain in the project | Skill to create | Naming rule |
|---|---|---|
| Any code at all | `coding-standards` | fixed name, always created |
| UI layer | `ui-design-system` | fixed name |
| Data/API client layer | after the stack, e.g. `graphql-urql`, `trpc-react-query`, `rest-openapi` | technology noun, no project prefix |
| Database & migrations | after the stack, e.g. `hasura-ops`, `prisma-migrations`, `alembic-ops` | technology noun, no project prefix |
| E2E / integration tests | `<project>-<framework>-tests`, e.g. `acme-playwright-tests` | project-prefixed (fixture-bound) |
| Live browser testing | `<project>-<tool>`, e.g. `acme-chrome-devtools` | project-prefixed wrapper over your set's generic browser-driving skill |
| Recurring multi-surface task | verb-named playbook, e.g. `adding-<entity>`, `sync-<thing>` | verb/gerund |

Naming rules in one line: convention skills are technology nouns (they trigger on natural vocabulary); a project prefix is reserved for skills inseparable from project fixtures (test accounts, seeded data, dev URLs); workflows and playbooks get verb names.

### Phase 3 — Pick the skills home (ask the user)

- Exactly one of `.agents/skills/` / `.claude/skills/` exists → use it.
- Both or neither → ask the user: `.claude/skills/` (Claude Code native) vs `.agents/skills/` (multi-tool, manager-installed). Also ask whether skills live in-repo or in a shared skills repo pulled in by a manager — in the shared-repo case installed copies are throwaway, edits go to the source repo, and AGENTS.md must say so.

### Phase 4 — Instruction file

`AGENTS.md` at repo root; `CLAUDE.md` contains only `@AGENTS.md`. Sections (skeleton in REFERENCE.md): orientation, non-negotiables checklist, domain→skill routing table, pinned dependencies, critical constraints/gotchas, agent-environment quirks, docs map. Constraints you can't derive from the code get a `TODO(owner)` marker, not an invention.

### Phase 5 — Create the skills

For each mapped domain, create `<skill>/SKILL.md` using the content checklists in REFERENCE.md. Hard rules:

- The frontmatter description is the router: first sentence = what it does; second = "Use when …" with generous, concrete triggers (keywords, file types, symptoms).
- SKILL.md body under ~100 lines; depth (token tables, exhaustive gotchas) goes to `REFERENCE.md`; `scripts/` only for deterministic helpers.
- Every rule must cite something real in the repo — a file, a command that runs, an existing sibling to mirror. Derive conventions by reading the closest existing code; never invent a convention the codebase doesn't show. What can't be derived: `TODO`.

### Phase 6 — Verify

- [ ] Every created skill's description has "Use when" triggers.
- [ ] The routing table in AGENTS.md lists exactly the skills that exist.
- [ ] All commands quoted in skills actually run in this repo.
- [ ] Retrofit mode: nothing hand-written was overwritten; report what was added vs skipped.

## Templates

See [REFERENCE.md](REFERENCE.md) for the AGENTS.md skeleton and per-skill content checklists.
