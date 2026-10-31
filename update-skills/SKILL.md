---
name: update-skills
description: Update installed agent skills. Use when asked to refresh skills for Codex, Antigravity, or another coding agent.
---

# Update Skills

Refresh installed skills from their verified sources. Keep learned installation details in local reference storage.

## Choose agents and load memory

1. Resolve the agents named in the current request.
2. If no agents are named, ask which agents to update before making changes.
3. Treat "all agents" as all discovered installations, then state that scope before proceeding.
4. Read [references/memory.md](references/memory.md) and this installed copy's `references/sources.local.json`, when present.
5. Never infer current target agents from the previous run or the agent hosting this conversation.
6. Check remembered paths, repository remotes, branches, and update methods against live state.
7. Keep valid records. Rediscover only missing, changed, or invalid details.

## Discover sources

1. Enumerate standalone skills and enabled skill plugins for the selected agents.
2. Distinguish active installations from download caches, disabled plugins, and application built-ins.
3. Find source repositories, package metadata, lockfiles, configured marketplaces, and existing update helpers.
4. Resolve each installed skill to its owner and source subdirectory.
5. Prefer the user's Git-tracked source copies over installed mirrors.
6. Keep local canonical commits, including unpublished commits. Fetch upstream without discarding local history.
7. If ownership remains ambiguous, ask about that source and continue independent updates.
8. Save verified discoveries to local memory, even when an update is blocked.

## Protect local storage

1. Read the installed skill's instructions and inventory its files before changing that skill.
2. Identify source-owned files from the repository or package manifest.
3. Identify storage from the skill instructions, existing local records, and destination-only files.
4. Preserve local memory, indexes, databases, generated assets, caches, and user-added files.
5. Preserve `references/sources.local.json` when updating this skill itself.
6. Record protected paths explicitly. A directory entry protects all descendants.
7. Never copy source files onto protected paths, even when upstream introduces the same name.
8. If source and storage paths collide, skip the conflicting writes and report the conflict.
9. Never mirror-delete a destination directory or replace an entire skill tree.
10. Remove obsolete files only when a previous source manifest proves source ownership and local content is unchanged.
11. For skills with storage, update only source-owned skill files. Do not migrate, reset, or replace the storage.
12. Apply the same protection to package-manager updates. Check replacement behavior before invoking the manager.
13. If a manager cannot preserve storage, stop that package update and explain the limitation.

## Apply updates

1. Inspect repository instructions, status, and installed differences before writing.
2. Fetch the configured upstream. Fast-forward clean checkouts when possible.
3. If branches diverge or tracked files have local edits, preserve those changes and report the affected source.
4. Prefer a supported update command when that command preserves local storage.
5. For file installations, copy source-owned files from the verified source.
6. Compare differing installed files against Git history or the previous source manifest.
7. Treat recognized older source versions as updates. Preserve unrecognized edits for review.
8. Back up replaced files outside the installed skill tree.
9. Update only the selected agents. Do not install additional standalone skills unless requested.
10. Keep package adapters and agent-specific configuration intact.
11. Never push, publish, or post as part of a skill update without explicit approval.

## Verify and remember

1. Re-enumerate active installations after updating.
2. Compare updated source-owned files with the selected source using content hashes.
3. Confirm protected file hashes and protected directory contents remain unchanged.
4. Check source manifests or package versions for manager-owned installations.
5. Record verified sources, protected paths, source revisions, update methods, and results in local memory.
6. Update memory after storage verification as the explicit exception for this skill's own learned records.
7. Report updated, current, conflicted, and unverified items separately, with stable IDs for follow-up.
8. State when an application reload is needed. Do not restart an application without authorization.
