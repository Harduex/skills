---
name: researching
description: Investigates codebases to understand how features, systems, or flows work. Traces code paths from entry point to execution, analyzes dependencies, and produces structured findings with file references. Use when exploring unfamiliar code, understanding a feature's implementation, or gathering evidence before making changes.
---

# Codebase Research

## Process

```
Research checklist:
- [ ] Confirm scope — specific feature, system, or topic
- [ ] Discover entry points (UI events, API routes, CLI commands, jobs)
- [ ] Trace execution through call chain
- [ ] Map dependencies (libraries, modules, config, env vars)
- [ ] Document data flow (inputs → transformations → storage → outputs)
- [ ] Report findings with file:line references
```

## Example output

The plain answer comes first; the references back it up below.

```
Login hands the browser a signed token and remembers the session in Redis, so
any server can check who you are without asking the database.

When you sign in, the OAuth provider confirms who you are. The app then signs a
token for you and stores your session in Redis, where it expires after 30 minutes.

Worth knowing: refreshing a token has no rate limit, which is a possible abuse
path. The hourly session cleanup is redundant, because sessions already expire
on their own.

**Details**
- `src/api/auth.py:15` — login handler
- `src/services/token.py:42` — signs and validates tokens
- `src/middleware/session.py:8` — checks the session on each request
- External: Redis (session store), OAuth provider
- Config: `AUTH_SECRET`, `TOKEN_TTL`
```

## Principles

- Report what the code does, not what it should do.
- Back every claim with a specific file path and line number, in the details below the plain answer.
- Separate facts from interpretation. Flag ambiguity explicitly.
- If scope is too broad, propose a narrower focus and ask for direction.
