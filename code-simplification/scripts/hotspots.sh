#!/usr/bin/env bash
# hotspots.sh — rank files by change frequency × size, so a simplification scan
# starts where complexity is both high and paid for often. Read-only.
#
# Usage: hotspots.sh [path] [--since "<git date>"] [--top N]
#   path     limit to files under this path (default: whole repo)
#   --since  history window (default: "12 months ago" — older churn rarely
#            predicts where change lands next)
#   --top    rows to print (default: 20 — more than a scan can act on is noise)
#
# Output: score  commits  lines  path   (score = commits × lines, highest first)
# Line count is a cheap, language-neutral stand-in for complexity. Renames split
# a file's history, so a recently moved file may rank lower than it should.
#
# Exit codes:
#   0  ranking printed (possibly empty)
#   2  usage error, or not inside a git repository
set -u

path="."
since="12 months ago"
top=20

while [ $# -gt 0 ]; do
	case "$1" in
		--since) [ $# -ge 2 ] || { echo "error: --since needs a value" >&2; exit 2; }; since="$2"; shift 2 ;;
		--top)   [ $# -ge 2 ] || { echo "error: --top needs a value" >&2; exit 2; }; top="$2"; shift 2 ;;
		-h|--help) sed -n '2,17p' "$0"; exit 0 ;;
		-*) echo "error: unknown option: $1" >&2; exit 2 ;;
		*)  path="$1"; shift ;;
	esac
done

case "$top" in ''|*[!0-9]*) echo "error: --top must be a positive integer" >&2; exit 2 ;; esac
root="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "error: not inside a git repository" >&2; exit 2; }
[ -e "$path" ] || { echo "error: no such path: $path" >&2; exit 2; }

# Lockfiles, generated output, vendored code, docs, data and binary assets are
# not simplification targets — their churn and size say nothing about design.
skip='(^|/)(node_modules|vendor|dist|build|out|coverage|__generated__|generated|\.next)/|\.(lock|min\.js|map|snap|md|mdx|json|ya?ml|toml|csv|svg|png|jpe?g|gif|webp|ico|pdf|woff2?|ttf)$|(^|/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|go\.sum|Cargo\.lock|poetry\.lock)$|\.generated\.|\.gen\.'

rows="$(
	git log --since="$since" --format= --name-only --no-renames -- "$path" \
		| grep -v '^$' \
		| grep -Ev "$skip" \
		| sort | uniq -c \
		| while read -r commits file; do
			# git log prints root-relative paths. Deleted files still appear in
			# history; only live text files rank.
			[ -f "$root/$file" ] || continue
			grep -Iq . "$root/$file" 2>/dev/null || continue
			# Codegen tools stamp a marker in the file's opening comment block.
			head -n 5 "$root/$file" | grep -Eqi 'do not edit|@generated|code generated|auto-generated' && continue
			lines=$(wc -l < "$root/$file")
			printf '%d\t%d\t%d\t%s\n' "$((commits * lines))" "$commits" "$lines" "$file"
		done \
		| sort -t "$(printf '\t')" -k1,1nr
)"

if [ -z "$rows" ]; then
	echo "no ranked files: no commits since \"$since\" under $path (after excluding generated/data files)"
	exit 0
fi

printf 'score\tcommits\tlines\tpath\n'
printf '%s\n' "$rows" | head -n "$top"
