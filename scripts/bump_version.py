#!/usr/bin/env python3
"""Bump the Evolving Harness version.

Updates the single semver in ``bundles.json``, prepends a stub entry to
``CHANGELOG.md``, and prints the ``git tag`` command to run once the change is
committed. Refuses to run on a dirty git tree so the bump is an isolated,
reviewable change.

Versioning policy:
- ``major`` - a skill was removed/renamed, or the lifecycle changed;
- ``minor`` - bundle membership changed;
- ``patch`` - wording, script, or CI fixes.

Stdlib only.
"""
import argparse
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLES_FILE = os.path.join(REPO_ROOT, "bundles.json")
CHANGELOG_FILE = os.path.join(REPO_ROOT, "CHANGELOG.md")


def git_dirty():
    out = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    return bool(out.stdout.strip())


def bump(version, level):
    major, minor, patch = (int(p) for p in version.split("."))
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def prepend_changelog(text, version):
    entry = f"## v{version}\n\n- _describe changes_\n\n"
    idx = text.find("## v")
    if idx == -1:
        return text.rstrip() + "\n\n" + entry
    return text[:idx] + entry + text[idx:]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Bump the harness version.")
    parser.add_argument("level", choices=["major", "minor", "patch"])
    args = parser.parse_args(argv)

    if git_dirty():
        print("error: git tree is dirty; commit or stash before bumping.",
              file=sys.stderr)
        return 1

    with open(BUNDLES_FILE, encoding="utf-8") as f:
        spec = json.load(f)
    old = spec["version"]
    new = bump(old, args.level)
    spec["version"] = new
    with open(BUNDLES_FILE, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        f.write("\n")

    with open(CHANGELOG_FILE, encoding="utf-8") as f:
        changelog = f.read()
    with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
        f.write(prepend_changelog(changelog, new))

    print(f"bumped {old} -> {new}")
    print("next: edit the new CHANGELOG.md entry, then regenerate:")
    print("  python3 scripts/generate_bundles.py")
    print("after committing, tag the release:")
    print(f"  git tag v{new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
