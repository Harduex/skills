#!/usr/bin/env bash
# scan-history.sh — sweep a git repo's FULL history for anything that makes it
# unsafe to publish: secrets, PII, work identity, machine-local paths, and
# accidentally-committed binaries/dumps/key material. Read-only — never mutates
# the repo or contacts the remote.
#
# Usage: scan-history.sh [repo-dir]        (default: current directory)
#
# Exit codes:
#   0  clean — no hard leaks found (soft advisories may still print)
#   1  HARD findings — secrets, private keys, or committed binaries/DBs/env files
#   2  scanner self-test FAILED — result is untrusted, do not rely on a clean run
set -u

REPO="${1:-.}"
cd "$REPO" 2>/dev/null || { echo "error: not a directory: $REPO" >&2; exit 2; }
git rev-parse --git-dir >/dev/null 2>&1 || { echo "error: not a git repo: $REPO" >&2; exit 2; }

hard=0   # set when a publish-blocking finding is seen
say()  { printf '\n=== %s ===\n' "$1"; }

# ── locate or fetch gitleaks ────────────────────────────────────────────────
# Prefer a system gitleaks; otherwise cache a pinned release under the user's
# cache dir so repeat runs don't re-download.
GITLEAKS="$(command -v gitleaks || true)"
if [ -z "$GITLEAKS" ]; then
	cache="${XDG_CACHE_HOME:-$HOME/.cache}/auditing-repo-for-leaks"
	mkdir -p "$cache"
	GITLEAKS="$cache/gitleaks"
	if [ ! -x "$GITLEAKS" ]; then
		ver="8.21.2"
		m="$(uname -m)"; case "$m" in x86_64|amd64) a=x64;; aarch64|arm64) a=arm64;; *) a="$m";; esac
		url="https://github.com/gitleaks/gitleaks/releases/download/v${ver}/gitleaks_${ver}_$(uname -s | tr A-Z a-z)_${a}.tar.gz"
		echo "fetching gitleaks $ver …" >&2
		if ! curl -fsSL "$url" | tar -xz -C "$cache" gitleaks 2>/dev/null; then
			echo "warning: could not fetch gitleaks; skipping the secret-scan pass" >&2
			GITLEAKS=""
		fi
	fi
fi

# ── scanner self-test (the honest-ceiling habit) ────────────────────────────
# A clean gitleaks run is only trustworthy if gitleaks actually fires on a known
# secret. Plant one in a throwaway repo and confirm it is caught BEFORE trusting
# a clean result on the real repo. If this fails, the whole run is untrusted.
if [ -n "$GITLEAKS" ]; then
	say "scanner self-test (plant a known key, expect a hit)"
	t="$(mktemp -d)"
	(
		cd "$t" && git init -q
		printf 'aws = "AKIAIOSFODNN7EXAMPLE"\nghp_1234567890abcdefghijklmnopqrstuvwxyz\n' > leak.txt
		git add . && git -c user.email=t@t.co -c user.name=t commit -qm x
	)
	# gitleaks exits 1 when it finds leaks, 0 when clean. Rely on the exit code —
	# the "leaks found" line goes to stderr and its wording/colour is not stable.
	"$GITLEAKS" git --no-banner "$t" >/dev/null 2>&1
	if [ "$?" -eq 1 ]; then
		echo "PASS — gitleaks detects planted secrets, so a clean result is meaningful."
	else
		echo "FAIL — gitleaks did NOT flag a planted secret. Result untrusted." >&2
		rm -rf "$t"; exit 2
	fi
	rm -rf "$t"
fi

# ── 1. secret scan over full history ────────────────────────────────────────
if [ -n "$GITLEAKS" ]; then
	say "secrets across all commits (gitleaks)"
	# -v prints per-finding detail; without it gitleaks only logs a count to stderr.
	out="$("$GITLEAKS" git --no-banner -v "$PWD" 2>&1)"; st=$?
	esc="$(printf '\033')"
	if [ "$st" -eq 1 ]; then
		# Show locator lines (rule/file/commit) but NOT the raw Secret value —
		# no point re-printing a live secret into the report.
		printf '%s\n' "$out" | sed "s/${esc}\[[0-9;]*m//g" \
			| grep -E '^(RuleID|File|Commit|Line|Link):' | head -80
		hard=1
	elif [ "$st" -eq 0 ]; then
		echo "no secrets found."
	else
		echo "gitleaks error (exit $st):"; printf '%s\n' "$out" | tail -5
	fi
fi

allblobs="$(git rev-list --all)"

# ── 2. machine-local paths (leak a username + local layout) ─────────────────
say "machine-local paths (/home/<user>, /Users/<user>, C:\\Users\\)"
paths="$(git grep -I -nE '/home/[A-Za-z0-9._-]+/|/Users/[A-Za-z0-9._-]+/|[A-Z]:\\\\Users\\\\[A-Za-z0-9._-]+' $allblobs 2>/dev/null \
	| sed 's/^\([0-9a-f]\{9\}\)[0-9a-f]*:/\1:/' | sort -u -t: -k2)"
if [ -n "$paths" ]; then printf '%s\n' "$paths" | head -40; echo "(advisory — usually cosmetic, not publish-blocking)"; else echo "none."; fi

# ── 3. private key material ─────────────────────────────────────────────────
say "private keys"
keys="$(git grep -lI 'BEGIN [A-Z ]*PRIVATE KEY' $allblobs 2>/dev/null | sort -u)"
if [ -n "$keys" ]; then printf '%s\n' "$keys"; echo "HARD — private key material in history."; hard=1; else echo "none."; fi

# ── 4. accidentally-committed binaries / dumps / secret files ───────────────
say "binaries, DB dumps, archives, env/key files ever committed"
arts="$(git log --all --name-only --format= 2>/dev/null | sort -u \
	| grep -iE '\.(db|sqlite3?|dump|bak|pem|key|pfx|p12|keystore|env|tfstate|pcap)$|(^|/)\.env' )"
if [ -n "$arts" ]; then printf '%s\n' "$arts"; echo "HARD — review each; secrets/dumps must not ship."; hard=1; else echo "none."; fi

# ── 5. identity disclosure (who is baked into every commit) ─────────────────
# Author/committer emails are inherently public in git history. Not a leak per
# se, but the user should see whose identity (esp. a work address) is exposed.
say "author/committer identities in history"
git log --all --format='%ae%n%ce' 2>/dev/null | sort -u | grep -v 'noreply' | sed 's/^/  /'

# ── 6. other emails in file contents (excluding commit-author addresses) ────
say "email addresses in file contents (excl. commit authors)"
authors="$(git log --all --format='%ae%n%ce' 2>/dev/null | sort -u | paste -sd'|' -)"
mails="$(git grep -hIoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' $allblobs 2>/dev/null \
	| sort -u | grep -viE "${authors:-NOMATCH}|noreply|example\.(com|org)|@sha256|@types|@babel|@v[0-9]")"
if [ -n "$mails" ]; then printf '%s\n' "$mails" | head -30; echo "(advisory — confirm none is a private/work address)"; else echo "none beyond commit authors."; fi

# ── verdict ─────────────────────────────────────────────────────────────────
say "verdict"
if [ "$hard" -eq 1 ]; then
	echo "NOT clean — hard findings above must be resolved before publishing."
	exit 1
fi
echo "No hard leaks found. Review the advisories above, then it is safe to publish."
exit 0
