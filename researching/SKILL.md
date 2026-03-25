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

```
## Overview
Authentication uses JWT tokens with Redis-backed sessions. Login flow
goes through OAuth provider, then issues a signed token stored in Redis.

## Components
- `src/api/auth.py:15` — handles login requests
- `src/services/token.py:42` — generates and validates JWT tokens
- `src/middleware/session.py:8` — session management

## Data flow
Request → AuthController.login() → TokenService.generate() → Redis.store() → Response

## Dependencies
- External: Redis (session store), OAuth provider
- Config: AUTH_SECRET, TOKEN_TTL environment variables

## Observations
- Token refresh logic has no rate limiting (potential abuse vector)
- Session cleanup runs on a 1-hour cron but TTL is 30 minutes (redundant)
```

## Principles

- Report what the code does, not what it should do.
- Include specific file paths and line numbers for every claim.
- Separate facts from interpretation. Flag ambiguity explicitly.
- If scope is too broad, propose a narrower focus and ask for direction.
