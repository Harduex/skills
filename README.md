# Evolving Harness

A self-improving harness for AI-assisted software development, built on a flat
catalog of reusable [Agent Skills](https://agentskills.io). Each skill is a
self-contained folder; on top of the catalog, the **Evolving Harness** adds a
lifecycle router, four themed plugin bundles, and a session-end loop that turns
each session's lessons back into skills.

There are two ways to use this repo, and they don't interfere:

1. **Flat catalog** — pull individual skills into any project (unchanged).
2. **Plugin bundles** — install a whole themed bundle through the Claude Code
   plugin marketplace.

## The flat catalog (unchanged)

Install skills using any compatible Agent Skills package manager, or copy
individual skill folders directly into your project:

```
npx skills add Harduex/skills
```

Each skill follows the [Agent Skills specification](https://agentskills.io/specification)
— browse the folders to see what's available. The root folders remain the
source of truth; `plugins/` is generated output and is never hand-edited.

## The Evolving Harness framework

Consult the **`using-evolving-harness`** router skill at the start of any
non-trivial task. It routes the work through a gated lifecycle (frame → design →
plan → test-first → build → review → land) and, before a session ends, runs the
evolution loop (save lessons, extract new skills, re-tune the repo).

### Bundles

| Bundle | What it's for |
|---|---|
| **harness-evolution** | The core self-improvement loop: extract skills from sessions, save learned lessons, analyze agent sessions, and evolve the repo. Includes the router and output-style setup. |
| **delivery-lifecycle** | Gated idea-to-shipped pipeline: plan, design, spec, test cases, autonomous build loop, review, verification, checkpoint — plus formal verification, functional-programming guidance, and site refinement. |
| **git-ops** | Git hygiene and delivery ops: linear history, fixup distribution, PR comment handling, shipped-state audits, secret-leak audits. |
| **thinking** | Reasoning and research toolkit: deep research, adversarial questioning, zero-assumption analysis, teaching, quick-wins triage. |

Every skill belongs to exactly one bundle; the flat catalog still lets you
install any skill individually.

### Install a bundle

```
/plugin marketplace add Harduex/skills
/plugin install harness-evolution@harduex
/reload-plugins
```

Swap `harness-evolution` for any bundle above. The marketplace is named
`harduex`. Use `/plugin list` and `/plugin marketplace list` to see
what's installed.

### Uninstall

```
/plugin uninstall harness-evolution@harduex
/plugin marketplace remove harduex
/reload-plugins
```

## Maintaining the bundles

`bundles.json` is the single source of truth for bundle membership and the
version. Regenerate the `plugins/` output after any change:

```
python3 scripts/generate_bundles.py          # regenerate plugins/
python3 scripts/generate_bundles.py --check   # validate only (used in CI)
```

Cut a release with:

```
python3 scripts/bump_version.py [major|minor|patch]
```

which bumps the version in `bundles.json`, prepends a `CHANGELOG.md` entry, and
prints the `git tag` command. Versioning: **major** = a skill removed/renamed or
a lifecycle change; **minor** = bundle membership change; **patch** = wording,
script, or CI fixes.

### Deploying a new or updated skill

Follow this exact order when a skill is added, edited, or renamed and you're
asked to deploy it. **Never hand-edit `plugins/`** — it is generated.

1. **Author the skill at the flat root** — a folder named exactly as the skill,
   containing `SKILL.md` with valid frontmatter (`name` matching the folder,
   non-empty `description`). See `write-a-skill/`. Editing an existing skill in
   place needs no other structural change.
2. **Decide bundle membership.** A *new* skill joins exactly one bundle in
   `bundles.json` (add its folder name to that bundle's `skills` list). Renames
   must be updated in `bundles.json` too. A pure edit to an existing skill
   changes nothing here.
3. **Regenerate, validate, and commit the change:**
   `python3 scripts/generate_bundles.py` then
   `python3 scripts/generate_bundles.py --check`; run `python3 -m unittest
   discover -s tests`. Commit the root skill change, `bundles.json`, and the
   regenerated `plugins/` together.
4. **Bump the version on the now-clean tree** (`bump_version.py` refuses a
   dirty tree so the bump stays an isolated, reviewable change):
   `python3 scripts/bump_version.py [major|minor|patch]` — a wording-only
   skill edit is a `patch` — then fill in the new `CHANGELOG.md` entry.
5. **Regenerate and commit the release:** rerun the generate/check/test
   commands from step 3, then commit `bundles.json`, `CHANGELOG.md`, and
   `plugins/` as the release commit. **Get the human's approval before
   pushing.**
6. **Push and tag** (human-gated): `git push origin master`, then push the tag
   the bump printed (`git tag vX.Y.Z && git push origin vX.Y.Z`) and, if
   desired, `gh release create vX.Y.Z`.

Both install paths pick the change up automatically: `npx skills add
Harduex/skills` sees the flat folder, and bundle users get it on their next
`/plugin` update of the affected bundle.

### Releasing the `agentic-notebook` plugin (cross-repo)

The `harduex` marketplace also serves
[`agentic-notebook`](https://github.com/Harduex/agentic-notebook), which lives
in its own repo. Its marketplace entry pins a commit `sha`, so a release there
does **not** reach users until the pin is updated here:

1. Release in the `agentic-notebook` repo as usual (its own version and history).
2. In `.claude-plugin/marketplace.json`, update the `agentic-notebook` entry's
   `sha` to the new release commit.
3. Commit and push this repo. Do **not** run `bump_version.py` — it governs only
   the four bundles' shared version, not this plugin.

## Creating skills

See the `write-a-skill/` folder for the authoring guide.

## License

[MIT](LICENSE)
