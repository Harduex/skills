# AI Coding Agents Starter Kit

A drop-in team of 7 specialized AI agents for software projects. Copy the `.claude/` directory into any project to get structured, role-based AI assistance out of the box.

Built on the [Agent Skills](https://agentskills.io) open standard for cross-tool compatibility.

## Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| **Researcher** | Codebase exploration, code path tracing, dependency analysis | Read-only |
| **Planner** | Requirements, task breakdown, prioritization, acceptance criteria | Read-only |
| **Architect** | System design, trade-off evaluation, technical decisions | Read-only + Bash |
| **Engineer** | Implementation, production-ready code, full-stack development | Full access |
| **Reviewer** | Code review, security audit, test strategy design | Read-only + Bash |
| **Debugger** | Root cause analysis, scientific debugging, defect resolution | Full access |
| **Designer** | User journeys, wireframes, accessibility, interaction patterns | Read-only |

Plus **zero-assumptions**, a requirements interrogation methodology that demands precise constraints before implementation.

## Quick start

### Claude Code

1. Copy `.claude/` and `CLAUDE.md` into your project root
2. Start Claude Code
3. Use `/researcher`, `/architect`, etc. or let Claude invoke them automatically
4. Subagents are available via `/agents` for isolated task delegation

### Other tools

The skills in `.claude/skills/` follow the [Agent Skills specification](https://agentskills.io/specification). Any compatible tool (Cursor, VS Code, Gemini CLI, etc.) will discover and activate them automatically.

For tools without auto-discovery, copy the relevant `SKILL.md` content into your tool's instruction configuration.

## How it works

```
.claude/
  skills/       # Portable instruction sets (Agent Skills standard)
  agents/       # Claude Code subagents (isolated context, tool restrictions)
  rules/        # Always-on coding standards
```

- **Skills** are cross-tool compatible. They load into conversation context when activated. Only metadata (~100 tokens each) loads at startup; full content loads on invocation.
- **Agents** are Claude Code-specific subagents that run in isolated contexts with their own tool restrictions. Each agent preloads its corresponding skill.
- **Rules** enforce baseline code quality and workflow standards in every session.

## Recommended workflow

1. **Explore** -- Use the researcher to understand the problem space
2. **Plan** -- Use the planner to define requirements and break down tasks
3. **Design** -- Use the architect for technical decisions; the designer for UX
4. **Build** -- Use the engineer to implement
5. **Verify** -- Use the reviewer for quality; the debugger for issues

## Customization

**Add an agent:** Create a skill in `.claude/skills/<name>/SKILL.md` with `name` and `description` frontmatter. Optionally create a subagent in `.claude/agents/<name>.md`.

**Modify an agent:** Edit the `SKILL.md` directly. Changes take effect next session.

**Remove an agent:** Delete its directory from `.claude/skills/` and its file from `.claude/agents/`.

**Add project rules:** Create `.md` files in `.claude/rules/`. They load automatically.

See [AGENTS.md](AGENTS.md) for full documentation.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## License

[MIT](LICENSE)
