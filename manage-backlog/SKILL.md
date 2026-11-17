---
name: manage-backlog
description: "Gives a short, linked, ranked overview of the user's open tasks and triages them with the user, in whatever tracker the project uses. Use when the user asks to see, list, review, rank, prioritize, or triage their tasks, tickets, issues, backlog, or roadmap (in Jira, Notion, Linear, GitHub Issues, a roadmap file in the repository, or another tracker), asks what to work on next, asks which open tickets are already done or stale, wants stale tickets closed, or wants to set up where a project's tasks are tracked. Not for writing a ticket or planning the work inside one."
---

# Manage Backlog

Show the user's open tasks as a short, linked, ranked list, and triage that list with the user.
The skill learns each tracker on first use. It remembers the setup and the user's decisions between runs.

## Storage

Keep all state in `${XDG_CONFIG_HOME:-$HOME/.config}/skills/manage-backlog/`:

- `trackers.json` holds the setup: how to reach each tracker, and which folders use it.
- `decisions.json` holds the user's ranking, notes, and the last run's list.

Read [references/storage.md](references/storage.md) before the first read or write of either file.
Never write state inside the skill folder or the skill repository.

## 1. Pick the tracker and the mode

1. If the user names a tracker, use it. If that tracker is not in `trackers.json`, run Setup for it.
2. Otherwise, match the current folder's git remote against `folders` in `trackers.json`. Then try the folder's absolute path.
3. If nothing matches, run Setup.
4. Run the Triage when the user asks to rank, prioritize, triage, or close items, and on the first run. Otherwise, run only the Overview.

## 2. Reach the tracker (every run)

1. Use a connector, a CLI, or file access. Find the connector by the service that the user named or `trackers.json` records, not by a tool name.
2. If nothing reaches the tracker, tell the user how to connect it, then stop. Never scrape a web page or drive a browser instead.
3. If the connector reaches several sites or workspaces, ask which one.
4. Check the saved query against the live tracker before use. If a detail fails, rediscover only that detail. Set `verified_at` when the check passes.

## 3. Setup (first run in a folder)

1. Ask where this project's tasks live: any tracker, a file in the repository, or a tracker already in `trackers.json`.
2. Reach the tracker as section 2 says.
3. For a repository roadmap, adopt the existing roadmap file and keep its format. If none exists, offer to create `docs/ROADMAP.md`: one entry per item, with a stable ID, a status, and a group. A roadmap file is its own ranking home: the order of its entries is the ranking. If the roadmap separates approved work from proposed or deferred ideas, triage only the approved, not-started entries.
4. Discover these details from the tracker, then show them to the user and confirm:
   - the query for open, not-started items in scope (default: assigned to the user), with its result count
   - how to close an item: statuses, transitions, and required resolutions
   - the link format for one item (for a file: an anchor in the file, through the repository URL when a remote exists)
   - the code repositories where the work lands (propose candidates from local git history)
5. For any other tracker, ask whether it is personal or shared with a team. Propose the ranking home: the tracker itself when it is personal and has a field for the group, otherwise `decisions.json`. Apply it only after the user agrees.
6. Offer the default groups: Do next, Soon, Later, Waiting on a product decision, Blocked. Save the names the user picks.
7. Save the setup. Match this folder by its git remote, or by its absolute path when it has no remote. Offer to map the folders of the code repositories to the same tracker.
8. Fetch the live list, run the Triage, then show the Overview with the agreed ranking. Say that no earlier run exists to compare.

## 4. Overview

1. Fetch the live list with the saved query.
2. Group the items by the saved ranking. Put unranked items under **New**. Skip empty groups.
3. Show one line per item: the link, then a plain summary. Number the items in the user's first group, because that order says what to start next. Use bullets in every other group, including **New**.
4. Add "Changed since last run": new items, items gone with their new status, and items moved into the current sprint or iteration.
5. Before you remove a gone item from the ranking, look it up by its key. If the item is still open, the saved query is stale: recheck the query and keep the ranking. Remove only items that are closed or deleted.
6. Save `last_run`.

```
**Do next**
1. [PROJ-12](https://tracker.example/PROJ-12) Add a dark mode toggle
2. [PROJ-15](https://tracker.example/PROJ-15) Export reports as CSV (needs PROJ-12)

**Soon**
- [PROJ-21](https://tracker.example/PROJ-21) Fix the date format on invoices

**Changed since last run**
- [PROJ-9](https://tracker.example/PROJ-9) moved to Code Review, off the list
```

## 5. Triage

1. Check whether the work on each item is already done:
   - Search every item cheaply first: the code repositories by the feature's own names and symptoms, not only the item key. A fix often lands under another key.
   - Look deeper only where that search finds a lead. Treat a matching commit as a lead, not as proof.
   - Call an item done only after someone saw the change work: the user, or you by running or driving the changed behavior.
   - If a lead exists but nobody saw the change work, list the item as "looks done, needs a look". Say which items you checked.
2. Bring evidence to the ranking, not a formula: the current sprint, blockers, dependencies, waiting on others, age, and past decisions (in `decisions.json` and in your memory, if you have one).
3. Propose a ranking. Apply the user's changes exactly. The user's order wins over yours.
4. Save the agreed ranking to `decisions.json` or the roadmap file. Agreeing to the ranking is the yes for that save. Save the notes that the user agreed to, with their item keys.

## 6. Writes

1. Writing the ranking into an external tracker needs its own yes. Name each item that moves and its new group.
2. Get the user's yes for each other write to a tracker: a close, a status change, or a comment. Name the item and the change.
3. Close an item with the resolution that fits, such as done, won't do, or cannot reproduce. Use the names recorded in Setup. In a roadmap file, set the status and keep the entry and its ID.
4. When a note belongs on the item itself, offer to add it there.
5. Commit only the roadmap file, locally, with the repository's own identity and commit conventions. Never push.
