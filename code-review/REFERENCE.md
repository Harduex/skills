# Code Review Reference

## Safety Constraint

This skill operates in **read-only mode** with respect to remotes. The following are explicitly forbidden:
- `git push`, `git push --force`, or any variant
- `glab mr merge`, `glab mr close`, `glab mr approve`, or any write operation against GitLab
- Creating or deleting remote branches
- Posting comments on MRs (unless the user explicitly asks)

The only remote-read operations allowed are:
- `git fetch origin <branch>` — to get MR source branches locally
- `glab mr view` / `glab mr diff` — to read MR descriptions and diffs

## Security Checklist

Check every change against these categories. Most security bugs are not exotic — they are ordinary mistakes in these areas.

### Input & Injection
- User input used in SQL, shell commands, HTML, or URL construction without sanitization
- Template literals or string concatenation building queries instead of parameterized queries
- `dangerouslySetInnerHTML`, `eval()`, `exec()`, `innerHTML`, or equivalent
- File paths constructed from user input (path traversal)
- Permission and role-based access for any data layer the project uses (Hasura/Postgres RLS, Firebase rules, custom RBAC) — verify queries use the correct role and that any "permission-aware" helpers actually enforce what their names imply (check the implementation, not the name)

### Authentication & Authorization
- Endpoints missing the project's auth middleware
- Authorization checks that verify identity but not permission level
- Secrets, API keys, or tokens hardcoded or logged
- JWT validation that doesn't check expiration, issuer, or audience

### Data Exposure
- Sensitive fields (passwords, tokens, PII) included in API responses, logs, or error messages
- Verbose error messages in production that leak internals (stack traces, SQL errors)
- Debug endpoints or admin routes left enabled

### Concurrency & State
- Time-of-check to time-of-use (TOCTOU) bugs
- Shared mutable state without synchronization
- React state updates on unmounted components, stale closures in effects

### Dependencies
- New dependencies added — check for known vulnerabilities, maintenance status, and license
- Lockfile updated to match `package.json` / `Cargo.toml` / `go.mod` / equivalent
- **Pinned deps**: many projects pin specific framework versions because newer ones break integrations. Read the project's conventions doc (`CLAUDE.md`, `AGENTS.md`, etc.) for the list, and flag any attempt to upgrade a pinned dep without explicit approval

## Review Dimensions — Extended

### Correctness Deep Dive
- **Error handling**: Are errors propagated, swallowed, or logged-and-forgotten? Does the caller know when something fails?
- **Boundary conditions**: Empty collections, zero/negative values, max int, Unicode edge cases
- **Async correctness**: Unhandled promise rejections, missing `await`, callback ordering assumptions
- **State transitions**: Can the system reach an invalid state? Are transitions atomic where they need to be?
- **Null safety**: if the project relaxes its compiler's null/undefined safety (e.g. TypeScript `strictNullChecks: false`, Kotlin platform types, etc.), the compiler won't catch entire classes of bugs. Review these paths manually.

### Design Heuristics
- **Single responsibility**: Does this change make one module responsible for more unrelated things?
- **Coupling direction**: Do lower-level modules now depend on higher-level ones?
- **Abstraction leakage**: Does the interface expose implementation details that callers shouldn't know about?
- **Duplication vs. wrong abstraction**: Three copies of similar code is better than a premature abstraction. But five copies with subtle differences is a bug farm.
- **Architecture boundaries**: Most multi-service projects have rules about what belongs in which service (e.g. analytics events in the API server, not the web client; background work in a worker, not the request handler). Read the project's conventions doc for the boundary rules and flag any change that crosses them without justification.

## The Psychology of Reviewing

### For the reviewer (you)
- You are reviewing the code, not the person. Never say "you should have" — say "this could."
- Assume the author had a reason for their approach. If it looks wrong, ask why before suggesting a replacement.
- If multiple valid approaches exist, defer to the author's choice unless there's a concrete reason not to.
- Distinguish between "I would do it differently" (not actionable) and "this has a specific problem" (actionable).

### For effective feedback
- **The 10-minute rule**: If a design debate has gone back and forth without resolution, suggest trying one approach and evaluating the concrete result.
- **Batch related comments**: Group findings by theme rather than scattering them across the diff.
- **Proportional effort**: A 5-line bug fix does not need a 50-line review. Match depth to risk.

## Automation Already in Place

Most projects have linters, formatters, and type-checkers configured. **Discover what's available** from the project's `package.json` scripts, `Makefile`, `pre-commit` config, CI workflow files, or equivalent — then run the ones that fit the change scope. Do not manually flag issues the project's tooling already catches; just run the tools and report results.

Focus human review on what the tooling cannot catch:
- Logic errors and incorrect assumptions
- Security holes (see [Security Checklist](#security-checklist))
- Design problems and abstraction quality
- Null/undefined safety in projects that relax compiler strictness
- Architectural boundary violations
- Missing tests for non-trivial behavior

## Publishing Mechanics (GitLab)

**Anchoring — verify before posting.** GitLab accepts any plausible line number without error; wrong anchors post "successfully" as misplaced noise.
1. Get the MR's current `diff_refs` (`glab api projects/:proj/merge_requests/:iid`) and `git fetch` first. Do not assume the local checkout matches origin — the MR head may have moved since you reviewed (pushes and rebases shift line numbers), so verify anchors against the fetched `head_sha` blobs (`git grep ... <head_sha>`), never against the local working tree.
2. Locate each anchor in the live head: `git grep -nF '<code snippet>' <head_sha> -- <path>`. Anchor on lines the MR **adds**; a context (unchanged) line requires both `old_line` and `new_line` — and usually means you should anchor on the new code that causes the issue instead.

**Posting:** `glab api -f 'position[...]=...'` **silently drops the position** (glab sends a JSON body, so bracket keys never parse into a nested hash) and leaves an unanchored top-level note. Send a nested JSON payload instead:

```bash
echo '{"body": "🤖 **Claude review · ISSUE**\n\n...", "position": {"position_type": "text", "base_sha": "...", "head_sha": "...", "start_sha": "...", "new_path": "src/file.ts", "new_line": 42}}' \
  | glab api projects/:proj/merge_requests/:iid/discussions -X POST -H 'Content-Type: application/json' --input -
```

**Verify after posting:** the response note must have `"type": "DiffNote"` and a non-null `position` (a `DiscussionNote` with null position means the anchor was dropped). Then re-fetch the notes and confirm each anchor line's content matches its finding.

**Replying to GitLab Duo threads:** reply in-thread with `glab mr note create <iid> --reply <discussion-id> -m "..."` (`--reply` accepts a full discussion ID or an 8+ char prefix; get IDs from `glab mr note list <iid> -F json`). Always start the reply with `@GitLabDuo` or the bot won't see it. Verify Duo's premises against ground truth before acting on a finding — it reviews blind to SQL function bodies and the lockfile, so its "if X, then bug" findings (and its suggested fixes) are frequently wrong against the real code. Posting notes needs a token with `api` (write) scope; a read-only token (`read_api`/`ai_workflows`) returns `403 insufficient_scope` on POST — re-auth with `glab auth login --hostname <your-gitlab-host>`.
