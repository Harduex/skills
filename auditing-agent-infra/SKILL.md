---
name: auditing-agent-infra
description: Audits the AI coding agent ecosystem and compares against a project's current agent infrastructure. Researches Claude Code, Cursor, Codex, Gemini CLI, and other tools for new features, skill standards, and best practices, then produces a gap analysis with proposals. Use when asked to audit agent infrastructure, compare agent tools, or review agent setup.
---

# Agent Infrastructure Audit

## Process

```
Audit checklist:
- [ ] Snapshot project's current agent setup
- [ ] Research each platform's latest state
- [ ] Compare findings against project infrastructure
- [ ] Identify gaps and rate by impact/effort
- [ ] Draft report and present for review
```

### 1. Snapshot current state

Discover the setup this project actually has rather than assuming one:

- **Agent config** — search the repo root and `.github/` for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `copilot-instructions.md`, `.claude/`, `.agents/`, `.cursor/rules/`, and any skill or rule directories they point to. Note the auto-memory or knowledge store if the tool keeps one.
- **Distribution** — infer how skills and MCP servers arrive from the files that configure them (a skills manifest such as `agents.toml` means a skill package manager is in use; `.mcp.json` lists project MCP servers). Each tool found this way joins the research list in step 2.
- **Report location** — find where the project keeps point-in-time audits or reports (e.g. `docs/audits/`, `docs/reports/`) and follow its naming; if there is none, ask before creating one.

### 2. Research platforms

Start with the tools and platforms step 1 found, then cover the general list. For each, investigate the latest state of:

- **Claude Code** — skills discovery, MCP integrations, hooks, memory systems
- **Cursor** — rule format changes, memory features, agent mode, MCP support
- **OpenAI Codex** — AGENTS.md conventions, memory, skill format, sandbox capabilities
- **GitHub Copilot** — instruction formats, agent mode, MCP support
- **Gemini CLI** — conventions, agent capabilities
- **Agent Skills standard** — spec changes, new tooling, distribution methods

Cross-cutting concerns:
- Memory and knowledge persistence (new standards?)
- Skill/tool distribution (package managers, registries)
- MCP server ecosystem (relevant to project's stack)
- Context window management best practices

### 3. Compare and report

Use web search and web fetch. Prioritize official docs and release notes.

## Report template

```
# Agent Infrastructure Audit — <date>

## Current Setup
[Project's agent config, installed skills, memory setup]

## Ecosystem Updates
[Per-platform findings — only notable changes]

## Gap Analysis
| Area | Current | Available | Priority |
|------|---------|-----------|----------|
| ...  | ...     | ...       | High/Med/Low |

## Proposals
[Numbered, actionable recommendations with effort estimates]

## Sources
[Links to docs, release notes consulted]
```
