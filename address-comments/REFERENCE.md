# Address Review Comments — Forge Mechanics

Command cookbook for the fetch/reply phases, per forge. All commands are read-only except the reply/comment POSTs, which are approval-gated by the skill. Detect the forge from `git remote -v`.

## GitLab (`glab`)

### Fetching

```bash
glab mr view                      # current branch's MR: iid, title, comment count, reviewers
glab mr view <iid> --comments     # full discussion INCLUDING bot notes (Duo etc.)
glab mr view <iid> --unresolved   # only unresolved discussions
glab mr note list <iid> -F json   # all discussions as JSON (despite the name, each element is a discussion with .notes[])
```

- **Trap: the REST `/discussions` endpoint omits bot reviewer notes** (GitLab Duo). Use the commands above for coverage; use the API only for anchors/IDs, and reconcile counts between the two.
- **Trap: `glab api --paginate` concatenates JSON arrays** (`[…][…]`). Merge before parsing:

```bash
glab api --paginate "projects/<group>%2F<repo>/merge_requests/<iid>/discussions?per_page=100" \
  | jq -s 'add' > discussions.json
```

- Useful per-note fields: `.notes[].author.username`, `.resolvable`, `.resolved`, `.system` (skip true), `.position.new_path`, `.position.new_line`, and the discussion `.id` (needed for replies). Unresolved filter: `any(.notes[]; .resolvable and (.resolved | not))`.
- Completeness check: also list the author's non-resolvable general notes and already-resolved threads before reporting "N comments total".
- Burst `glab api` calls can intermittently return `ERROR Unauthenticated` (rate limit). Prefer the native subcommands; never wrap the API in retry/backoff loops.

### Baseline

```bash
glab api "projects/<group>%2F<repo>/merge_requests/<iid>" | jq .diff_refs   # .head_sha must equal local HEAD
git rev-parse HEAD
```

### Replying

Write the body to a file first (dodges shell quoting of backticks/markdown), then reply by discussion ID (8+ char prefix accepted):

```bash
glab mr note create <iid> --reply <discussion-id> -m "$(cat /path/to/reply.md)"
```

- Use this documented subcommand — do **not** hand-roll a reply through `glab api .../discussions/<id>/notes`, which has two glab traps: `-f body=@file` posts the *literal* text `@file` (glab doesn't read files the way `gh`'s `-F` does), and `--input -` needs an explicit `-H 'Content-Type: application/json'` or it returns `HTTP 415` (glab sends no content-type by default). If forced onto the raw API, send JSON with that header — `-X POST -H 'Content-Type: application/json' --input -` with a `{"body": …}` payload (the form the `code-review` skill uses) — or form-encode via `-f "body=$BODY"` after `BODY="$(cat reply.md)"` (backticks in a variable value aren't re-evaluated). Same rule to fix a botched note in place with `-X PUT` on `.../merge_requests/<iid>/notes/<note-id>`.
- `--file` is mutually exclusive with `--reply`, so a threaded reply must pass the body via `-m "$(cat reply.md)"`, not `--file`.

Posting needs a token with `api` (write) scope; `read_api`-class tokens fail with `403 insufficient_scope` — ask the user to re-auth (`glab auth login --hostname <host>`), never script around it.

## GitHub (`gh`)

Command surface verified against `gh` 2.45; unlike the GitLab section, these flows are not yet session-proven — apply the same post-verification rigor.

### Fetching

Feedback is split across **three comment kinds** — sweep all of them:

```bash
gh pr view                                        # current branch's PR: number, title, reviewers
gh pr view <n> --comments                         # conversation comments + review summaries
gh api --paginate repos/<owner>/<repo>/pulls/<n>/comments | jq -s 'add'   # inline review comments (anchors, in_reply_to)
gh api --paginate repos/<owner>/<repo>/pulls/<n>/reviews  | jq -s 'add'   # review summaries (APPROVED/CHANGES_REQUESTED)
gh api --paginate repos/<owner>/<repo>/issues/<n>/comments | jq -s 'add'  # conversation comments
```

- Useful inline-comment fields: `.user.login`, `.path`, `.line` / `.original_line`, `.id`, `.in_reply_to_id` (group into threads by it), `.pull_request_review_id`.
- Thread resolved-state is GraphQL-only (`reviewThreads.isResolved`); REST shows all comments regardless — if the user wants "unresolved only", query GraphQL or ask them to confirm the live thread state.

### Baseline

```bash
gh pr view <n> --json headRefOid   # must equal local HEAD
git rev-parse HEAD
```

### Replying

```bash
# threaded reply to an inline review comment:
gh api repos/<owner>/<repo>/pulls/<n>/comments -X POST -F in_reply_to=<comment-id> -F body="$(cat /path/to/reply.md)"
# top-level conversation comment:
gh pr comment <n> --body-file /path/to/reply.md
```

## Both forges

- **Verify after posting:** re-fetch the thread and confirm the note landed *threaded in the right discussion* (not a stray top-level comment) **and that the stored body is correct** — a mis-passed body field returns `200` with garbage (e.g. a literal `@path`) as the note text. Never trust the POST exit code alone.
- A ` ```suggestion ` block's header offsets a line *range* relative to the anchor (e.g. GitLab's `suggestion:-1+0`) — read the full range.
- One commit per addressed comment/concern, ordered to match the report IDs, so each reply can cite its SHA. The repo's message convention applies (ticket prefix etc.).
- Splitting one file across two comments: stage per hunk (`git add -p`); for entangled hunks, temporarily revert one fix, commit the other, re-apply.
- Branch close: fold review-fix commits into originating commits (fixup + `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash <base>`); plain `rebase --autosquash` without `-i` does nothing. Verify the tree is byte-identical afterwards.
- A force-push after rebase marks anchored threads "outdated" on both forges — warn the user before they approve it.
- Leave thread resolution to humans; end with a per-ID disposition table (fixed @ SHA / replied / awaiting decision) and what remains gated (push, posts).
