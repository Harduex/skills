# Engines: install, invoke, and when to use

Read this after Step 1 of SKILL.md has chosen a tier. Each entry lists when it fits, how to
install, and how to run it. Prefer the cheapest tier that covers the stated property. Always
confirm the exact current install/usage against the tool's own docs — versions drift.

## Table of contents
- Tier 1: off-the-shelf linters (no encoding)
- Tier 2: SMT solving (Z3 / MCP Solver)
- Tier 2: logic programming (Datalog / Prolog)
- Tier 2: contract verification (Dafny)
- Tier 3: property-based testing

---

## Environment setup (read this first)

Engines are NOT vendored — binaries are platform-specific (a `manylinux_x86_64` wheel is broken on
macOS/ARM) and too large for a synced skill repo. Install on demand and cache. The friction is
never "the tool is missing" — it is the install path on a locked-down box. The principles, learned
the hard way:

- **No root.** Assume you cannot `sudo apt`/`snap`. Prefer, in order: `uv` (Python) · `npx`
  (JS) · prebuilt release binary unzipped to a cache dir · `docker` · `go install`.
- **Python is PEP 668 + may lack `ensurepip`.** Do NOT `--break-system-packages` the system
  Python, and don't rely on `python3 -m venv` (often has no ensurepip). **`uv` is the answer** —
  it bundles its own pip and builds a clean venv. `scripts/setup-engine.sh` provisions the Python
  engines via uv and prints the interpreter to use. (Fallback for a box with no `uv`: a no-install
  wheel via `PYTHONPATH`, which the script also handles for Z3.)

**`scripts/setup-engine.sh` usage** — provisions a shared uv venv and echoes the interpreter:

```bash
PY="$(bash scripts/setup-engine.sh z3-solver clingo hypothesis)"   # any pip pkgs; default z3-solver
"$PY" my_spec.py            # uv path: $PY is the venv python
# (no-uv fallback for z3 only: $PY is a PYTHONPATH, run: PYTHONPATH="$PY" python3 my_spec.py)
```

**Verified optimal no-root command per engine** (Linux x86_64, tools: uv/npx/go/docker; checked
2026 — versions drift, reconfirm). "via setup-engine.sh" = the script above.

| Engine | Tier | Optimal no-root command |
|--------|------|--------------------------|
| **Z3** (SMT, lib) | B | `bash scripts/setup-engine.sh z3-solver` → run with returned `$PY` |
| **clingo** (ASP, lib+CLI) | C | `bash scripts/setup-engine.sh clingo` · or `uvx --from clingo clingo` |
| **Hypothesis** (PBT, lib) | E | `bash scripts/setup-engine.sh hypothesis pytest` |
| **Semgrep** (SAST, CLI) | A | `uvx semgrep scan` (needs glibc ≥ 2.34; else `docker run --rm -v "$PWD:/src" semgrep/semgrep semgrep scan`) |
| **migration-lint** (CLI) | A | `uvx migration-lint` |
| **Squawk** (SQL lint, CLI) | A | `npx squawk-cli@latest path/to/migration.sql` |
| **fast-check** (PBT, lib) | E | `npm i -D fast-check` (library; drive via `npx vitest`/`jest`) |
| **Atlas** (migrate lint) | A | `curl -fsSL -o "$HOME/.cache/formal-verification/bin/atlas" https://release.ariga.io/atlas/atlas-linux-amd64-latest && chmod +x "$_"` — **NOT `go install`** (officially deprecated, ships a crippled binary). Docker: `arigaio/atlas:latest`. |
| **CodeQL** (SAST) | A | release bundle, unzip-and-run (~770 MB): `wget https://github.com/github/codeql-action/releases/latest/download/codeql-bundle-linux64.tar.gz && tar -xzf codeql-bundle-*.tar.gz && export PATH="$PWD/codeql:$PATH"` |
| **SWI-Prolog** (Prolog) | C | **Docker only** (no no-root binary/AppImage): `docker run --rm -it -v "$PWD:/work" -w /work swipl:stable swipl` |
| **Soufflé** (Datalog) | C | **No clean no-root path** — GitHub ships only `.deb`/`.rpm` (need root) and no official Docker image. **Prefer `clingo` (ASP) for reachability/transitive closure**; reach for Soufflé only where you can `apt install` or build a container. |
| **Dafny** (contract) | D | **No clean no-root path here** — the Linux zip is framework-dependent (needs .NET 8; not installed) and there is no verified official Docker image. Reserve for crown-jewel logic; if truly needed, bootstrap .NET to `~/.dotnet` via `dotnet-install.sh` first, or build a container. |

For the heavier/awkward engines (Soufflé, SWI-Prolog, Dafny, CodeQL), confirm the property can't be
discharged by a cheaper tier first — clingo or Z3 usually can.

---

## Tier 1 — off-the-shelf linters (zero encoding)

Use when the property is a *known anti-pattern* in a common artifact. These require no
formalization: point them at files and read the findings. They cannot find bespoke,
project-specific invariants — only what a rule already covers.

### SQL migrations
- **Squawk** (Postgres) — flags blocking/destructive schema changes: locking constraint
  creation, adding NOT NULL columns, `CREATE INDEX` without `CONCURRENTLY`, column drops.
  Run (no install footprint): `npx squawk-cli@latest path/to/migration.sql`. Has a GitHub PR
  integration for CI. **For the Maui Hasura migrations, Squawk is the first-line Tier-1 check.**
- **Atlas migrate lint** — multi-database; detects destructive operations, breaking changes,
  and lock/rewrite risks. Run: `atlas migrate lint --dev-url <db-url> --git-base main`. Install
  via the matrix above (release binary — **not `go install`**).
- **migration-lint** — works with Django, Alembic, and raw SQL; flags backward-incompatible and
  unsafe operations. Run: `uvx migration-lint`.

### Application / backend code
- **Semgrep** — fast, 30+ languages; pattern-based with custom rules you can write in an hour;
  catches some business-logic flaws (e.g. IDOR, broken authorization) beyond pure structure.
  Run: `uvx semgrep scan` (or `semgrep --config auto .`). Write project-specific rules in YAML
  for your own anti-patterns.
- **CodeQL** — GitHub's semantic engine; treats the codebase as a queryable relational database
  and you query it in QL (a logic/Datalog-family language). Deeper but heavier; best when you
  need custom structural queries. Install the bundle per the matrix, then `codeql database
  create` → `codeql database analyze` with a query pack.

When a linter covers the property, stop here — it is the cheapest correct answer.

---

## Tier 2 — SMT solving (Z3 / MCP Solver)

Use for property shape (B): "can data/state ever satisfy a forbidden condition?" over booleans,
integers, reals, bitvectors, enums, and strings. This is the workhorse for permissions, access
rules, config consistency, and rule contradictions.

Two equivalent ways to run it:

1. **Z3 directly via code execution** (the default — simplest and headless-safe) — provision with
   `scripts/setup-engine.sh z3-solver` and write a short Python script. No connector setup.
2. **MCP Solver** (optional, interactive only) — `szeider/mcp-solver` exposes Z3 (+ MiniZinc,
   PySAT, ASP) over MCP for a persistent, structured solving session. Install **from source via
   uv** (`git clone … && uv venv && uv pip install -e ".[all]"`) — *not* `pip install mcp-solver`
   (PyPI is stale). Do NOT make this the default: MCP connectors may be ABSENT in headless/cron
   runs, and local Z3 covers the same ground with a one-line install.

Core pattern (detailed in `encoding-patterns.md`): encode each rule as a constraint, assert the
*negation of the property* (the violation), and check satisfiability.
- `unsat` → the violation is impossible → property PROVED within the model.
- `sat` → `model()` gives the concrete counterexample.

MiniZinc / PySAT / ASP (Clingo) modes of MCP Solver are alternatives when the problem is pure
combinatorial optimization (MiniZinc) or hard combinatorial search (ASP) rather than logical
satisfiability.

---

## Tier 2 — logic programming (Datalog / Prolog)

Use for property shape (C): relational, transitive, reachability, and effective-set questions
(role inheritance, dependency/call graphs, data-flow).

- **clingo** (ASP — Answer Set Programming) — the **preferred Datalog/reachability engine on a
  no-root box**: it installs as a Python wheel (`scripts/setup-engine.sh clingo`), needs no system
  packages, and expresses transitive closure / effective-set queries directly. Use this before
  reaching for Soufflé.
- **Soufflé** (Datalog) — high-performance; the engine family behind serious static analyzers.
  But there is **no clean no-root install** (only `.deb`/`.rpm`, no official Docker image), so on a
  locked-down box prefer clingo above and reserve Soufflé for when you can `apt install` or build a
  container.
- **SWI-Prolog** — more general (relational logic + `CLP(FD)`). No no-root binary; run via Docker
  (`swipl:stable`, see matrix). Run: `swipl`.
- **prolog-reasoner** (MCP, optional) — a real, maintained-but-niche Prolog MCP server
  (`rikarazome/prolog-reasoner`, PyPI v0.2.2; `uvx prolog-reasoner`). Saves stable rule bases by
  name and feeds per-case facts, with a natural-language→Prolog self-correction loop. Caveat: it
  needs a working SWI-Prolog on PATH (itself awkward no-root, above) and connectors may be absent
  in headless runs — treat as an optional interactive front-end, not a default.

Pattern: load the world as facts (`has_direct_access(role, table).`, `relationship(t1, t2).`),
write rules for the derived relation (`reachable/2`), then query and compare against an
allow-list. Save the rules once; only the per-case facts change.

---

## Tier 2 — contract verification (Dafny)

Use for property shape (D): functional correctness of an algorithm or state machine against an
explicit contract, where a proof is worth significant effort (e.g. a money/balance invariant, a
core authorization engine — AWS rebuilt theirs in Dafny while proving behavior was preserved).

- Write code with `requires` (preconditions), `ensures` (postconditions), and loop `invariant`s;
  the verifier translates them to SMT formulas (Z3) and proves them. Run: `dafny verify file.dfy`.
- Install caveat (see matrix): there is **no clean no-root install** without .NET — the Linux zip
  is framework-dependent and no official Docker image is verified. Reserve for crown-jewel logic.
- Caveat: Dafny verifies code written *in Dafny*, so you model the logic in it — you do not point
  it at existing TypeScript/Python. It can also demand proofs of seemingly trivial facts due to
  solver heuristics. Reserve it for crown-jewel logic, not everyday code.

---

## Tier 3 — property-based testing

Use for property shape (E): breadth and cheap counterexamples when a proof is not required. This
is the best low-cost complement to every tier above — turn it on even when you also use a solver.

- **Hypothesis** (Python) — `scripts/setup-engine.sh hypothesis pytest`; define strategies
  (generators) and assert the invariant inside a `@given` test.
- **fast-check** (JS/TS) — `npm i -D fast-check`; `fc.assert(fc.property(...))`. The natural choice
  for this repo's TS code (drive via the project's Jest/Vitest runner).
- **QuickCheck** (Haskell) and ports — the original.

Pattern: describe the space of valid inputs, state the invariant as an assertion, let the tool
generate hundreds of cases and shrink any failure to a minimal counterexample. Not a proof, but
it finds real bugs fast and requires no formal model.
