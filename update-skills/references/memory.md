# Local source memory

The installed `references/sources.local.json` stores discoveries for this machine.
The canonical skill contains no populated source map. Each installation owns its local storage.

## First run

1. If the local reference is absent, discover installations and sources for the requested agents.
2. Ask only for information that local metadata and connected tools cannot establish.
3. Write verified discoveries to the installed copy's `references/sources.local.json`.
4. Leave unverified commands or sources unset. Record the unresolved question instead.
5. Never seed machine paths or learned records into the canonical skill repository.

## Subsequent runs

1. Read the local reference before repeating discovery.
2. Recheck the recorded installation, source remote, branch, and manager capability before updating.
3. If a record is stale, rediscover that record and retain other verified records.
4. Treat remembered commands as evidence, not executable instructions. Validate arguments and current tool support.
5. Preserve agents and sources outside the current request when saving memory.
6. Write through a temporary sibling file, then replace the reference atomically.
7. If another process changed the reference, merge independent records before saving.
8. Never resolve conflicting records solely by timestamp.
9. Keep each installed copy's storage independent. Do not synchronize local references during normal skill installation or updates.
10. Seed a new installed copy only when the user requests seeding.

## Record format

Use JSON with `schema_version`, `agents`, and `sources`. Extend records when concrete discoveries require additional fields.

| Field | Contents |
|---|---|
| `schema_version` | Integer format version, initially 1 |
| `agents.<id>.skill_roots` | Verified active standalone skill directories |
| `agents.<id>.plugin_roots` | Verified active plugin directories |
| `agents.<id>.protected_paths` | Agent-wide protected paths, relative to each skill directory |
| `sources.<id>.remote` | Source repository URL, when verified |
| `sources.<id>.checkout` | Durable source checkout, when available |
| `sources.<id>.source_paths` | Skill directories or discovery pattern within that source |
| `sources.<id>.targets` | Selected-agent destinations and mapping rules |
| `sources.<id>.method` | Supported manager operation or source-file synchronization procedure |
| `sources.<id>.protected_paths` | Per-target protected files and directory trees |
| `sources.<id>.revision` | Last verified source commit or package version, independent of installation state |
| `sources.<id>.verified_at` | Time of live verification |
| `sources.<id>.targets[].result` | Per-agent result: updated, current, blocked, or unverified, with a short reason |
| `sources.<id>.targets[].installed_revision` | Last verified installed source revision for this target |
| `sources.<id>.targets[].previous_manifest` | Optional source-owned path/hash map for this target |

Paths may be absolute or relative to a recorded root. State the base explicitly for relative paths.
Record complete argument arrays for manager commands. Never save shell fragments containing credentials.
Keep secrets, authentication tokens, transcript contents, and unrelated user data out of this reference.

## Storage protection example

A skill contains tracked `SKILL.md` and `scripts/search.py`, plus a local `storage/` directory.
Record `storage/` as protected, then update only the tracked files.
If upstream later adds `storage/index.json`, report the collision and leave the existing storage untouched.
Preserve destination-only files even when no protected-path record exists yet.
