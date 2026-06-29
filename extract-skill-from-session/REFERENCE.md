# Extract Skill From Session — Reference

## Correction catalogue (X1–X13)

Recurring misses observed across many real skill-building sessions. The process in
SKILL.md must avoid all of them; each skill you *build* should actively prevent the
ones in its own domain.

- **X1 · Over-engineering.** Porting a tool, spinning up a new repo, or writing a 130-line parser when a one-liner works; shipping speculative flags / CI / hooks. → Smallest artifact that solves the real need; gate any script on "small + deterministic + proven live"; record "revisit when…" instead of building ahead of a requirement. *("isn't it too ambitious?")*
- **X2 · Editing the installed copy.** Vendored/installed skill copies are overwritten on every reinstall. → Edit the source repo only.
- **X3 · Fatal frontmatter.** An unquoted colon-space (or other invalid YAML) in the description makes some installers drop the skill with no warning. → Validate; keep the description plain or use a quoted / `>-` block. *("I ran install and it pruned my skill, why?")*
- **X4 · Project leak into a generic skill.** Host names, internal tool names, schema terms bleeding into a mirrored generic skill. → Genericize; grep for project nouns; match mirror pairs by content, not directory name.
- **X5 · Over-compression.** Cramming to hit a line target and dropping the very convention you converged on. → Clarity beats the cap; preserve hard-won detail; split depth into REFERENCE.md.
- **X6 · Unverified promotion.** Writing a remembered "fact" that live code contradicts. → Re-confirm against code/data/the skill before writing it.
- **X7 · Assuming soft-links auto-fire.** A capability phrase is instruction text, not an import. → When orchestrating, resolve capability→installed name and inject an explicit "invoke `<name>`".
- **X8 · Hand-doing what a skill covers.** A broad task that prescribes an artifact does **not** exempt the dedicated skill for it. → Soft-link at the trigger moment and use it.
- **X9 · Wrong baseline / out of scope.** Diffing against the branch's own new file or a merge-base instead of the project baseline; touching unrelated code; silently covering only a subset. → Diff against the real sibling/baseline; change only what's asked; surface what you left out.
- **X10 · Wrong name.** Naming for a capability not actually demonstrated, or off the set's pattern. → Name for what it does; match siblings; confirm when ambiguous.
- **X11 · Over-capture / wrong home.** Proposing memory notes the user didn't want; saving to memory what belongs in a skill. → Decline is first-class; route by lifespan; propose, then hold for approval.
- **X12 · Claiming done without running.** Asserting a script or skill works from reasoning alone. → Run it (cold-subagent test for skills); evidence over assertion.
- **X13 · Publishing without approval.** Pushing / committing / posting before an explicit OK, or bundling unrelated changes into the commit. → Stop before any outward action; scope the commit to the one change.

## Home + identity matrix

Decide by genericity. The concrete per-project identities and install commands live in
your memory / AGENTS.md — don't hardcode them into a skill (that would be X4).

| | Generic skill | Project-specific skill |
|---|---|---|
| Source repo | your cross-project skills repo (+ global skills dir) | the project's skill repo |
| Commit identity | your personal identity/convention | the project's identity/convention |
| Availability | everywhere (global install) | that project only (via its skill manager) |
| Mirror? | yes — keep a copy in both if the team also needs it | no |

- **Verify genericity by grep** before mirroring: search the draft for project nouns (repo names, product names, host/domain, schema/tooling terms). Zero hits → safe to mirror; otherwise strip them or relocate the specifics into a project-only skill / AGENTS.md.
- **One owner per name.** A globally-installed skill silently shadows a same-named project skill (personal > project precedence) — the project copy becomes unreachable. Never reuse a name across scopes.
- **Activation.** A skill takes effect only after the source is published *and* reinstalled — the manager re-pulls the remote (`install`, not `sync`, which only reconciles which skills are present). Confirm by grepping the installed copy for a line you just added.

## Validate before shipping (no bundled tooling needed)

Run the draft through an existing YAML linter (or `yaml.safe_load`) and eyeball the rest:

- **frontmatter parses as YAML** — the one silent killer: an unquoted colon-space in the `description` makes some installers drop the skill with **no warning**. Quote it or use a `>-` block.
- `name` is lowercase-hyphen, ≤64 chars, and equals the directory; `description` ≤1024 chars and carries a "Use when…" clause.
- links resolve; the body stays tight (push depth into this file).

For a deeper compliance/concision pass, hand the skill to the **skill-auditing capability**
rather than hand-rolling checks. What no linter can judge — whether the *triggers* are the
right ones, whether the body is genuinely thin, genericity — do by hand: grep for project
nouns, and run the cold-subagent test.

## Trigger phrasings (what should activate this skill)

- "this workflow we did was good… worth a new skill, or update an existing one?"
- "analyze the workflows and the corrections we applied… worth creating an X skill?"
- "write a simple skill that produces this report / does this… don't push it"
- "let's build one more skill called X, similar to `<sibling>`"
- "extract a reusable process from `<a prior session>`"
- "should this be a skill, a script, an AGENTS.md note, or memory?"

## Script-vs-prose gate (Phase 5 detail)

Put logic in a bundled script only when **all** hold: the steps are deterministic; you'd
otherwise regenerate the same code each time; it has run successfully at least once, live.
Until then it stays prose. Prefer an existing tool; measure the alternative (binary size /
source LOC) before porting — "feels foreign" is not a reason. Place the script by the repo's
existing convention, take inputs as args/env (never hardcode connection strings or paths),
and let the prose reference the command while the script owns the mechanics.

## Why this is an orchestrator, not a monolith

The mechanics of *writing* a skill (structure, the description rules, progressive disclosure),
of *mining* a transcript, of *routing* a single lesson, and of *auditing* a catalog already
live in dedicated skills. This skill encodes only what they leave out: the **classify / new-vs-extend
decision**, the **watched-RED distillation**, the **verify-before-promote gate**, the **home+identity
routing**, and the **correction pre-emption** above. If it starts restating the others, it will
bloat and drift — keep it to the judgment, and link the mechanics by capability.
