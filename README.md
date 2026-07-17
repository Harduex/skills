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
| **harness-evolution** | The core self-improvement loop: extract skills from sessions, save learned lessons, analyze agent sessions, and evolve the repo. Includes the router and the session-start nudge hook. |
| **delivery-lifecycle** | Gated idea-to-shipped pipeline: plan, design, spec, test cases, autonomous build loop, review, verification, checkpoint. |
| **git-ops** | Git hygiene and delivery ops: linear history, fixup distribution, PR comment handling, shipped-state audits, secret-leak audits. |
| **thinking** | Reasoning and research toolkit: deep research, adversarial questioning, zero-assumption analysis, teaching, quick-wins triage. |

Some skills stay root-only (installable individually, not part of a bundle):
`functional-programming`, `formal-verification`, `site-refiner`,
`set-output-style`, `continuous-chat-loop`.

### Install a bundle

```
/plugin marketplace add Harduex/skills
/plugin install harness-evolution@evolving-harness
/reload-plugins
```

Swap `harness-evolution` for any bundle above. The marketplace is named
`evolving-harness`. Use `/plugin list` and `/plugin marketplace list` to see
what's installed.

### Uninstall

```
/plugin uninstall harness-evolution@evolving-harness
/plugin marketplace remove evolving-harness
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
2. **Decide bundle membership.** A *new* skill either joins one bundle in
   `bundles.json` (add its folder name to that bundle's `skills` list) or stays
   root-only (installable individually, listed under "root-only" in this
   README). Renames must be updated in `bundles.json` too. A pure edit to an
   existing skill changes nothing here.
3. **Bump the version** to match what changed (only if `bundles.json` or a skill
   name changed — a wording-only skill edit is a `patch`):
   `python3 scripts/bump_version.py [major|minor|patch]`, then fill in the new
   `CHANGELOG.md` entry.
4. **Regenerate and validate:** `python3 scripts/generate_bundles.py` then
   `python3 scripts/generate_bundles.py --check`; run `python3 -m unittest
   discover -s tests`.
5. **Commit** the root skill change, `bundles.json`, `CHANGELOG.md`, and the
   regenerated `plugins/` together. **Get the human's approval before pushing.**
6. **Push and tag** (human-gated): `git push origin master`, then push the tag
   the bump printed (`git tag vX.Y.Z && git push origin vX.Y.Z`) and, if
   desired, `gh release create vX.Y.Z`.

Both install paths pick the change up automatically: `npx skills add
Harduex/skills` sees the flat folder, and bundle users get it on their next
`/plugin` update of the affected bundle.

## Creating skills

See the `write-a-skill/` folder for the authoring guide.

## License

[MIT](LICENSE)
