# Scaffold Project Harness — Templates

## AGENTS.md skeleton

```md
<one-paragraph orientation: what the agent's role is in this repo, e.g. overseer
that delegates to subagents and keeps its context clean>

# Non-negotiables (checklist — applies to every task and sub-step)

- Before writing code in a domain, invoke that domain's skill (see routing below).
- No new helper/util/component without a reuse search first; state what you searched.
- Adding a new instance of an existing category? Open the closest sibling
  end-to-end and mirror it; any divergence needs a stated reason.
- Plan-vs-code conflict → the code wins: stop, state the discrepancy, re-derive.
- Before claiming done/fixed: exercise the changed behavior and show the evidence.
  Green typecheck/lint is not verification.

# Skill routing

UI → ui-design-system; general code → coding-standards; <data layer> → <skill>;
schema/migrations → <skill>; tests → <skill>; live browser → <skill>.

# Pinned dependencies (DO NOT upgrade without approval)

- <package> <version> — <reason>  (TODO(owner) if unknown)

# Critical constraints

- <hard-won gotchas that cost hours when violated>  (TODO(owner))

# Agent environment

- <editor-less git flags, package-runner quirks, commit-message convention,
  how to run the local stack>

# Repository docs

- <map of docs/ subdirs: living guides vs point-in-time audits vs plan
  templates — load on demand, never all at once>
```

If skills come from a shared repo via a manager, add: "To change a skill, edit
it in <source repo> and reinstall — the installed copies under `.agents/skills/`
and `.claude/skills/` are overwritten on every install."

## Per-skill content checklists

### coding-standards (always)

- Pre-code gate: the reuse-search commands (where utils/helpers live), the
  sibling-mirroring rule, plan-vs-code precedence.
- Language/style rules the repo actually enforces (read lint/compiler config).
- Comment policy (rationale-only, never narrate the diff).
- Verification commands: exact typecheck, lint, and test invocations.
- Routing pointers to the other domain skills (this skill doubles as the hub).

### ui-design-system (if UI)

- Styling stack: what to use and what is banned (be explicit about the bans).
- Token sources — which files export colors/spacing/typography and the import
  rules — plus one canonical styled-component example copied from the repo.
- Responsive breakpoints, icon workflow, animation conventions if present.
- Exhaustive token tables → this skill's own REFERENCE.md.

### data-layer skill (named after the stack)

- Client setup/config location and how pages/components obtain it.
- Query/mutation/fragment conventions; where generated types come from.
- Caching behavior and staleness gotchas (the "UI didn't update after
  mutation" class of bug).
- End-to-end recipe: how to add a new query/entity.

### db-ops skill (named after the stack)

- Migration workflow: create, apply, revert — and ordering rules.
- Roles/permissions model and how to grant access for a new table/column.
- The exact post-schema-change command chain (codegen → typecheck → lint), in
  order.
- Derived/computed-field gotchas: read the definition before trusting a name.

### e2e-tests skill (project-prefixed)

- Layered architecture: specs → page objects → role actions → data setup →
  constants, with the directory for each layer.
- Fixtures and roles: how a test obtains an authenticated context.
- Selector registry convention (how elements are tagged and looked up).
- Test-data creation policy (API-first vs through the UI) and suite commands.

### browser-testing wrapper (project-prefixed)

- Dev URLs, test accounts, and the login flow step by step.
- Seeded data and known fixtures worth reusing.
- Only project facts live here — mechanics stay in the generic browser-driving
  skill this one wraps; keep SKILL.md a thin entry point.

### local-stack

- How to start, stop, and seed the local environment (exact commands).
- Env/config file locations and how runtime config is loaded.
- Known failure modes and their recovery runbook ("stack broken? read this
  before restarting anything").

### release-ops

- Environments and what deploys where; the promotion path.
- CI/CD pipeline quirks: what blocks a merge, what runs when, known flakes.
- Release process and feature-flag workflow (how to gate a new feature).

### observability

- Where logs, metrics, and analytics events actually live (which datastore
  per signal — often not the app database) and how to query each.
- How to add a new event/metric so it lands in the right place.
- Dashboards/alerts worth knowing and what feeds them.

### background-jobs skill (named after the stack)

- Job/queue conventions: where handlers live, how to add one.
- Retry, parking, and dead-letter semantics.
- How to run and observe a job locally.

### auth-model (when not absorbed by db-ops)

- Roles/identities and how a request acquires one.
- How to protect a new route/resource; where the checks live.
- Test identities and how to impersonate each role locally.

### i18n (if localized)

- How to add a user-facing string end-to-end.
- Translation workflow and file locations; what must never be hardcoded.
- Locale-specific pitfalls the repo has hit (dates, plurals, RTL).

### domain playbook (verb-named, e.g. adding-<entity>)

- Every surface a new instance must touch (lists, search, detail views,
  notifications, analytics, permissions, mobile/API parity …) as a checklist.
- The closest existing sibling to mirror, named, with its key files.
- Per-surface verification: how to prove each surface behaves like the
  siblings.
