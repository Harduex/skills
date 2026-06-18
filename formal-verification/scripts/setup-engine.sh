#!/usr/bin/env bash
# Provision the Python verification engines (Z3 / clingo / Hypothesis, or any pip package)
# the cheapest no-root way that works on this box, and print on the LAST stdout line the
# interpreter to run specs with. All progress goes to stderr so stdout stays clean.
#
# Usage:
#   PY="$(bash scripts/setup-engine.sh)"                       # default: z3-solver
#   PY="$(bash scripts/setup-engine.sh z3-solver clingo hypothesis)"
#   "$PY" my_spec.py            # $PY is a venv python (uv path) ...
#   PYTHONPATH="$PY" python3 my_spec.py   # ... or a PYTHONPATH (wheel fallback, z3-only)
#
# Strategy: `uv` is the right tool on a PEP 668 / no-ensurepip box — it bundles its own
# pip and builds a venv with no system packages. We fall back to a no-install wheel loaded
# via PYTHONPATH only when uv is absent (and only for z3-solver).
set -euo pipefail
log() { echo "[setup-engine] $*" >&2; }

PKGS=("$@"); [ ${#PKGS[@]} -eq 0 ] && PKGS=("z3-solver")
CACHE="${FV_CACHE:-$HOME/.cache/formal-verification}"
VENV="$CACHE/venv"

# --- Preferred path: uv ---
if command -v uv >/dev/null 2>&1; then
  [ -x "$VENV/bin/python" ] || { log "creating uv venv at $VENV"; uv venv "$VENV" >&2; }
  log "uv pip install ${PKGS[*]}"
  uv pip install --python "$VENV/bin/python" "${PKGS[@]}" >&2
  log "ready: $("$VENV/bin/python" -c 'import sys;print(sys.version.split()[0])') @ $VENV"
  echo "$VENV/bin/python"; exit 0
fi

# --- Fallback (no uv): no-install wheel via PYTHONPATH. z3-solver only. ---
log "uv not found — falling back to wheel-into-cache (z3-solver only)"
if [ "${PKGS[*]}" != "z3-solver" ]; then
  log "ERROR: without uv I can only provision z3-solver, not: ${PKGS[*]}. Install uv (https://docs.astral.sh/uv/)."
  exit 1
fi
Z3LIB="$CACHE/z3lib"; mkdir -p "$Z3LIB/dl"
if python3 -c "import z3" 2>/dev/null; then echo ""; exit 0; fi
if PYTHONPATH="$Z3LIB" python3 -c "import z3" 2>/dev/null; then echo "$Z3LIB"; exit 0; fi
ls "$Z3LIB"/dl/z3_solver-*.whl >/dev/null 2>&1 || { log "downloading z3-solver wheel"; pip download z3-solver --no-deps -d "$Z3LIB/dl" --quiet; }
unzip -qo "$Z3LIB"/dl/z3_solver-*.whl -d "$Z3LIB"
PYTHONPATH="$Z3LIB" python3 -c "import z3" 2>/dev/null && { log "ready via wheel at $Z3LIB"; echo "$Z3LIB"; exit 0; }
log "ERROR: could not provision z3"; exit 1
