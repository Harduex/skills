---
name: code-reviewing
description: Reviews code for correctness, security, and maintainability. Designs test strategies covering unit, integration, and end-to-end tests. Supports local changes, specific commits, or pull/merge requests. Use when reviewing code changes, designing test plans, or assessing test coverage.
---

# Code Review

## Step 0: Determine what to review

Ask the user which mode they want:

1. **Local changes** — unstaged, staged, or full branch diff against main
2. **Specific commits** — one or more SHAs or a range
3. **Pull/merge request** — by URL or number

## Process

```
Review checklist:
- [ ] Understand intent (read commit messages or ask)
- [ ] Read full files, not just diffs — diffs hide context
- [ ] Check edge cases (null, empty, boundary, concurrent access)
- [ ] Check error paths (explicit handling, no swallowed exceptions)
- [ ] Check security (input validation, query parameterization, secrets, auth)
- [ ] Check performance (N+1 queries, unnecessary allocations, missing indexes)
- [ ] Verify it follows existing codebase patterns
- [ ] Assess test coverage for changed code paths
- [ ] Run available linters/type checkers, focus review on what tools miss
```

## Findings format

```
**[SEVERITY] file_path:line — Title**
Description of the issue and why it matters.
Suggested fix (code sketch if applicable).
```

Severity levels:

- **Blocker** (must fix): Bugs, security vulnerabilities, data loss risks
- **Issue** (should fix): Performance problems, missing error handling, design concerns
- **Suggestion** (consider): Alternative approaches, readability improvements
- **Praise** (highlight): Elegant solutions, solid tests, good refactoring

Rules: frame critiques as questions, every Blocker/Issue needs a concrete suggestion, include at least one Praise if warranted.

## Example

```
**Blocker** — `api/users.py:47` — SQL injection via user_id
`user_id` from query params is interpolated directly into SQL.

- cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
+ cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

## Verdict

End every review with:

1. **Verdict**: Approve, Request Changes, or Needs Discussion
2. **Summary**: What the change does well and what needs attention
3. **Risk**: Low / Medium / High — based on blast radius and test coverage

## Test strategy

Design coverage across three levels:

1. **Unit tests** — functions in isolation, mock external dependencies
2. **Integration tests** — module interactions with realistic test data
3. **End-to-end tests** — critical user flows only, high-value paths

## Principles

- Review the code, not the person. "This could" not "you should have."
- If multiple valid approaches exist, defer to the author unless there's a concrete reason not to.
- Match review depth to risk. A 5-line fix doesn't need a 50-line review.
