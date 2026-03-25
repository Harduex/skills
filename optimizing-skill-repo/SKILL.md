---
name: optimizing-skill-repo
description: Audits and optimizes a collection of agent skills for compliance, concision, and cross-tool portability. Applies Agent Skills spec, Anthropic best practices, and progressive disclosure principles. Use when reorganizing skills, auditing skill quality, or optimizing a skill catalog.
---

# Optimize Skill Repo

Systematically audit and improve a skill collection. Interview the user at each decision point — provide recommended answer, wait for confirmation before proceeding.

## Process

```
Optimization checklist:
- [ ] Phase 1: Structure — flatten, remove scaffolding, decide repo purpose
- [ ] Phase 2: Inventory — classify each skill (keep/merge/drop/rewrite)
- [ ] Phase 3: Research — fetch latest spec + best practices
- [ ] Phase 4: Audit — check every skill against principles
- [ ] Phase 5: Rewrite — apply fixes, deduplicate, add examples/checklists
- [ ] Phase 6: Verify — final compliance pass
```

### Phase 1: Structure

Resolve these decisions with the user:

1. **Repo purpose** — browsable catalog, drop-in kit, or package source?
2. **Folder layout** — flat at root (recommended for catalogs) or grouped?
3. **Non-skill files** — which docs, configs, wrappers to keep/drop/rewrite?
4. **Single README** — minimal, no per-skill descriptions (catalog grows)

### Phase 2: Inventory

For each skill, classify:

- **Keep** — distinct purpose, non-obvious process, earns its tokens
- **Merge** — overlaps significantly with another skill
- **Drop** — redundant, project-specific, or teaches what models already know
- **Rewrite** — good concept but needs generalization or trimming

Present classification table. User approves before proceeding.

### Phase 3: Research

Fetch latest standards:

- Agent Skills spec at agentskills.io/specification
- Anthropic best practices at platform.claude.com skill authoring docs
- Any other authoritative agent instruction guidelines

Extract actionable principles (see Audit Principles below).

### Phase 4: Audit

Check every skill against:

**Spec compliance**:
- `name` matches directory, lowercase + hyphens, ≤64 chars
- `description` ≤1024 chars, third person, "Use when [triggers]"
- SKILL.md body under 100 lines (500 per spec, 100 for tight catalogs)
- References one level deep from SKILL.md

**Content quality**:
- No teaching known things (SOLID, DRY, Nielsen's heuristics — models know these)
- Imperative language ("Analyze X" not "You should analyze X")
- Consistent terminology throughout
- No time-sensitive information

**Effectiveness patterns**:
- Workflow checklist for multi-step processes
- Input/output examples for skills where output format matters
- Match freedom to fragility (high freedom for judgment, low for fragile ops)
- Progressive disclosure (details in REFERENCE.md, not SKILL.md)

**Cross-skill health**:
- No content duplicated across skills
- Each skill has distinct, non-overlapping purpose
- Descriptions differentiate clearly for agent discovery

Present audit table with issues per skill.

### Phase 5: Rewrite

Apply fixes in batch:

- Rename folders to gerund form (Anthropic convention)
- Strip known-to-models content
- Deduplicate shared content (pick one owner skill)
- Add checklists and examples where missing
- Split overlong SKILL.md into SKILL.md + REFERENCE.md
- Generalize project-specific skills or drop them

### Phase 6: Verify

Final pass:
- Line counts all within limits
- Name-directory consistency
- Description compliance
- No orphaned references
- Structure is flat and clean
