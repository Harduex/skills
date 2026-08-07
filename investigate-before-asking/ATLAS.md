# Investigation atlas — <org/project name>

Where truth lives for this project's integration unknowns, and how to reach it.
This file ships as a self-describing skeleton: replace the placeholders with your org's
map, in your project's copy of the skill. Keep entries as *pointers*, never findings —
findings belong in the design doc that needed them. Grow the atlas as investigations teach
you the map: every time a hunt discovers where a class of truth lives, add the row.

## Local checkouts first (`<local projects root>`)

| Path | What truth lives there | Before use |
|---|---|---|
| `<path>` | e.g. wire contracts under `src/api/`, schema/migrations, generated ERDs | e.g. `git pull` — must stay synced with the owning team |
| `<path>` | e.g. the client codebase: consumption conventions, math/units, upload clients | e.g. shallow clone — refresh with `git fetch --depth 1` |

## Remote sources

- **Org code host** `<host>` — the CLI/auth that works here, the blob-search incantation,
  and the size-check command to run *before any clone* (note host quirks, e.g. hidden
  statistics reading as 0).
- **Issue tracker** `<host>` — auth/id gotchas, and any structural quirks in how epics,
  mirrors, or links hide the real task breakdown.
- **Live databases** — which environment, through what tool/skill, and how far its data can
  be trusted (seeded? drifted? unmerged-branch rows?).

## Known truth map (who owns which fact)

| Question domain | Authoritative artifact |
|---|---|
| e.g. renderer/engine behavior | `<repo>` source — the shipped package is closed; the repo is the only window |
| e.g. wire contracts into our services | `<repo>/src/...` |
| e.g. product intent / scope | tracker epics + their children (note where they actually hang) |

## House rules that bit us before

- Rules earned from real misses in this org — one line each, with the command or check that
  prevents the repeat (e.g. "find local checkouts with `find <root> -maxdepth 3 -iname`
  before reaching for the host API"; "monorepo X is N GiB — sparse-clone only these dirs").
