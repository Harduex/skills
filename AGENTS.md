# Agentic AI Coding Starter Template

A clean, minimalist starter kit for agentic AI-assisted software development. Provides 7 specialized agent personas and 1 methodology skill, built on the [Agent Skills](https://agentskills.io) open standard for cross-tool compatibility.

## What's inside

```
.claude/
  skills/           # Agent Skills standard (cross-tool compatible)
    researcher/     # Codebase exploration and investigation
    planner/        # Product strategy and task breakdown
    architect/      # System design and technical decisions
    engineer/       # Implementation and coding standards
    reviewer/       # Code review, testing, quality assurance
    debugger/       # Bug diagnosis and root cause analysis
    designer/       # UI/UX design and user experience
    zero-assumptions/  # Requirements interrogation methodology
  agents/           # Claude Code subagents (isolated context)
  rules/            # Modular coding rules
CLAUDE.md           # Project-level instructions
```

## Quick start

### Claude Code

1. Copy the `.claude/` directory and `CLAUDE.md` into your project root
2. Start Claude Code in your project
3. Skills auto-discover. Use `/researcher`, `/architect`, etc. or let Claude invoke them automatically
4. Subagents are available via `/agents` for isolated task delegation

### Other tools (Cursor, VS Code, Gemini CLI, etc.)

The skills in `.claude/skills/` follow the [Agent Skills open standard](https://agentskills.io). Any compatible tool will discover and activate them automatically.

For tools that don't support auto-discovery, copy the relevant `SKILL.md` content into your tool's instruction/rules configuration.

## The 7 agents

| Agent | Consolidates | When to use |
|-------|-------------|-------------|
| **Researcher** | Feature Researcher, Data Analyst | Investigating how a feature works, tracing code paths, gathering evidence |
| **Planner** | Product Manager, Scrum Master, PMM | Defining requirements, breaking down work, prioritizing tasks, GTM strategy |
| **Architect** | System Architect, Tech Lead | Designing systems, evaluating trade-offs, setting technical direction |
| **Engineer** | Software Engineer | Writing code, implementing features, fixing bugs |
| **Reviewer** | QA Tester | Reviewing code quality, designing test strategies, identifying edge cases |
| **Debugger** | Bug Hunter | Diagnosing defects, root cause analysis, systematic debugging |
| **Designer** | Product Designer | Mapping user journeys, wireframing, accessibility, interaction design |

### Methodology skill

**zero-assumptions** - A rigorous requirements interrogation methodology. Refuses to proceed with vague specifications. Demands precise constraints before implementation. Use it when scoping complex systems.

## How skills and agents relate

**Skills** (`.claude/skills/`) are portable instruction sets following the Agent Skills standard. They load into the current conversation context when activated. They work across all compatible AI tools.

**Agents** (`.claude/agents/`) are Claude Code-specific subagents that run in isolated contexts with their own tool restrictions. Each agent preloads its corresponding skill. Use agents when you want context isolation (e.g., research that reads many files without cluttering your main conversation).

**Rules** (`.claude/rules/`) are always-on coding standards loaded into every Claude Code session. They enforce baseline quality without needing explicit invocation.

## Customization

### Add a new agent

1. Create a skill: `.claude/skills/my-agent/SKILL.md` with required `name` and `description` frontmatter
2. Optionally create a subagent: `.claude/agents/my-agent.md` that preloads the skill
3. The agent is immediately available

### Modify an existing agent

Edit the `SKILL.md` file directly. Changes take effect in the next session (or immediately if using live reload).

### Remove an agent

Delete its directory from `.claude/skills/` and its file from `.claude/agents/`.

### Add project-specific rules

Create new `.md` files in `.claude/rules/`. They are loaded automatically.

## Design principles

- **Minimalism over completeness** - Each file earns its place. No redundant explanations.
- **Progressive disclosure** - Only skill metadata loads at startup (~100 tokens each). Full content loads on activation.
- **Cross-tool portability** - Skills follow the open standard. Agents and rules enhance Claude Code specifically.
- **Assume capability** - Instructions tell the model what to do, not what it already knows.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
