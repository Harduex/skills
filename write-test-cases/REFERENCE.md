# Write Test Cases — Reference

## How a senior QA actually generates cases

The dimension labels in SKILL.md are categories. What turns a category into cases is a *prompting question* applied to the target. Walk each dimension with the questions below.

### 1. Happy paths

- What is the primary supported invocation? Write a case for it.
- What are the alternative valid invocations the contract supports? Each one is a case.
- What are the supported input shapes? Empty list, single item, many items, max-allowed items.
- What are the supported result shapes? Synchronous return, async completion, partial result, no-op result.
- Who are the supported actors? Each role that can invoke the happy path is a case.

### 2. Negative & boundary cases

For every input field:

- What is the minimum? Maximum? Empty? Null/undefined? NaN/Infinity? Negative? Zero?
- What is the maximum length / size / count? One under, exact, one over.
- What is structurally invalid? Wrong type, malformed JSON, extra fields, missing required fields.
- What is semantically invalid? Valid shape but referencing nonexistent IDs, expired tokens, deleted resources.

For every result path:

- What does the system return on each documented error condition?
- Are error responses well-formed (status code, body shape, error code field)?
- Are partial failures handled (2-of-3 succeed)?

### 3. State & lifecycle

- Does the result survive a hard reload? A new session? A restarted server?
- Is the operation idempotent? What happens on a duplicate submit, a network retry, a webhook redelivery?
- What happens when two actors perform the same operation concurrently? Race, last-writer-wins, lock, conflict error?
- What happens to associated resources on delete? Cascade, soft-delete, orphan, async cleanup worker?
- What happens mid-operation if the actor cancels, the network drops, the page closes?
- Is there async work spawned by the operation? Verify the work completes and observable side effects land.

### 4. Permissions & authorization

Build the matrix. Rows are roles, columns are actions, cells are expected results.

- Anonymous / unauthenticated
- Authenticated but no resource access
- Viewer / read-only role
- Editor / write role
- Owner / admin role
- Each "shared with" tier the system supports
- Expired session / revoked token

For each role, enumerate: create, read, update, delete, share, lock, archive, restore, transfer ownership, every other supported action. Skip cells the contract makes impossible.

Special cases:

- Resource locked → does the role's write action become read-only?
- Resource soft-deleted → does it become invisible, or visible-but-read-only?
- Resource shared via link → does the anonymous tier inherit the link's permissions?

### 5. Cross-context parity

- If the target is a new instance of an existing category (new entity type, new endpoint, new processor), every existing test of a sibling becomes a parity case.
- If the target shares a UI surface with siblings (a generic file card, a generic editor, a generic action menu), every UI affordance the sibling has should either exist on the new one or be deliberately omitted.
- If the target shares a backend pipeline with siblings (a generic webhook handler, a generic notification path), every observable side effect the siblings produce should either exist for the new one or be deliberately omitted.

The case form here is: "Operation X on the new instance produces the same observable result as on sibling Y." Run both and compare.

### 6. Security

- Can the resource be accessed by ID without auth? (IDOR)
- Can auth be bypassed by token manipulation, cookie tampering, header injection?
- Are user-controlled strings rendered as HTML? As SQL? As shell commands? As LLM prompts?
- Are secrets ever returned in responses, logs, error messages, URLs, redirect targets?
- Is the endpoint rate-limited? Can it be enumerated to leak existence?
- Can stale tokens, signed URLs, or shared links be replayed after revocation?
- Can CSRF reach state-changing endpoints? Is SameSite enforced?
- For file upload: does the server trust client-declared MIME type? File extension? Magic bytes?

Scale depth to blast radius. A read-only internal admin tool needs less than a public payment endpoint.

### 7. Observability & analytics

For every event, log, metric, or trace the feature is supposed to emit:

- Fires on the happy path? Verify presence and payload shape.
- Fires on the error path? Verify the error variant is emitted, not the success variant.
- *Does not* fire when the operation is rolled back or rejected? Verify absence.
- Carries the right correlation IDs (user, request, trace, session)?
- Is sampled correctly? (If sampled, the case must account for that.)

False positives (events fire when they shouldn't) are as much a defect as false negatives.

### 8. Non-functional

Include only the dimensions that materially apply.

- **Accessibility** — keyboard-only flow, screen reader output, focus management on dynamic content, color contrast for status indicators, motion-reduce respect.
- **Internationalization** — locale formatting (dates, numbers, currency), RTL layout, long-string overflow, multi-byte input.
- **Performance** — latency at p50/p95 under realistic load, behavior at large input (10x, 100x expected), memory growth across long sessions.
- **Cross-platform** — every officially supported browser, OS, screen size, input mode (mouse, touch, keyboard).

Document the supported matrix; don't fabricate coverage outside it.

## Stopping rules per dimension

Each dimension has a natural saturation point. Stop when you hit it.

- **Happy paths**: every documented invocation × every supported result shape. If you find yourself rewording the same flow, stop.
- **Negative & boundary**: every input field has one minimum, one maximum, one empty, one structurally invalid case. Beyond that is diminishing returns.
- **State & lifecycle**: cover reload, concurrency, cleanup. If the target has no async work, no concurrency, and no persistence, this dimension is trivially complete.
- **Permissions**: enumerate cells of the matrix that can plausibly differ. Identical cells collapse into one parametric case.
- **Cross-context parity**: one parity case per sibling per shared affordance. Do not re-run every sibling test.
- **Security**: the list above is the budget. Going deeper is a security audit, not a test plan.
- **Observability**: one case per declared signal.
- **Non-functional**: one case per declared support matrix entry.

## Worked example

Target: `POST /api/comments` — create a comment on a document.

Coverage Summary:

> Test plan for `POST /api/comments` (commit `abc123`). Covers happy creation across owner/editor/viewer roles, negative cases for invalid documents and bad payloads, state behavior under retry and concurrency, the full role × action × document-state matrix for authorization, parity against the existing `POST /api/replies` endpoint, security checks for IDOR and XSS via comment body, and observability of the `comment.created` analytics event. Performance and accessibility are out of scope (server-only endpoint). Critical: 4 | High: 9 | Medium: 7 | Low: 2.

Sample cases:

```
**TC-HAPPY-1: Owner creates comment on owned document** — Critical
- Preconditions: SETUP-OWNER, document `doc_uuid` owned by current user
- Steps:
  1. POST /api/comments with { document_uuid: doc_uuid, body: "Hello" }
- Expected: 201 with { comment_uuid: <uuid>, created_at: <iso8601> }
- Verify in: DB row in `comments` table with body="Hello" and author_uuid=owner

**TC-NEG-3: Empty body is rejected** — High
- Preconditions: SETUP-OWNER, document `doc_uuid`
- Steps:
  1. POST /api/comments with { document_uuid: doc_uuid, body: "" }
- Expected: 400 with { error: "body_required" }
- Verify in: API response body; no DB row created

**TC-AUTH-7: Viewer on locked document cannot comment** — High
- Preconditions: SETUP-VIEWER on `doc_uuid` where doc_uuid.locked=true
- Steps:
  1. POST /api/comments with { document_uuid: doc_uuid, body: "Hi" }
- Expected: 403 with { error: "document_locked" }
- Verify in: API response body; no DB row created

**TC-STATE-2: Duplicate submit with same idempotency key returns the original** — Medium
- Preconditions: SETUP-OWNER, document `doc_uuid`, prior POST with idempotency_key="k1" returned comment_uuid="c1"
- Steps:
  1. POST /api/comments with same body and idempotency_key="k1"
- Expected: 200 with comment_uuid="c1" (not a new comment)
- Verify in: DB shows exactly one row for that idempotency key

**TC-PARITY-1: Comment creation emits the same analytics shape as reply creation** — Medium
- Preconditions: SETUP-OWNER, document `doc_uuid`
- Steps:
  1. POST /api/comments with valid payload
  2. POST /api/replies on the created comment with valid payload
- Expected: both produce analytics events with the same field set (event, user_uuid, document_uuid, parent_uuid, body_length, timestamp)
- Verify in: Analytics event stream

**TC-SEC-2: XSS payload in body is stored verbatim and rendered escaped** — Critical
- Preconditions: SETUP-OWNER, document `doc_uuid`
- Steps:
  1. POST /api/comments with body=`<script>alert(1)</script>`
- Expected: 201; DB stores the raw string; GET /api/comments returns it escaped
- Verify in: DB row body matches input; response body contains `&lt;script&gt;` not `<script>`
```

Out of scope:

- Performance: server-only endpoint, contract is unbounded body size by design
- Accessibility / i18n: no UI surface in this target
- Cross-platform: API endpoint, single supported transport
