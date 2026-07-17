#!/usr/bin/env python3
"""Generate Claude Code plugin bundles from bundles.json.

Reads bundles.json at the repo root and (re)generates ``plugins/<bundle>/`` for
each bundle:

- ``.claude-plugin/plugin.json`` with the bundle name, description, and the
  single semver stamped from ``bundles.json``;
- ``skills/<skill>`` relative symlinks into the flat root catalog
  (``../../../<skill>``), so a fresh clone resolves them;
- ``hooks/hooks.json`` copied from the file a bundle names in its ``hooks``
  field, when present.

Validation runs in both modes: a missing skill folder or SKILL.md is an error
(exit 1); the same skill in more than one bundle is a warning. Generation is
idempotent - each bundle directory is rebuilt from scratch.

Stdlib only. No arguments generates; ``--check`` validates without writing.
"""
import argparse
import json
import os
import shutil
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_bundles(root):
    with open(os.path.join(root, "bundles.json"), encoding="utf-8") as f:
        return json.load(f)


def validate(spec, root):
    """Return (errors, warnings). Errors block generation; warnings do not."""
    errors = []
    warnings = []
    seen = {}
    for bundle in spec["bundles"]:
        name = bundle["name"]
        for skill in bundle["skills"]:
            seen.setdefault(skill, []).append(name)
            skill_dir = os.path.join(root, skill)
            if not os.path.isdir(skill_dir):
                errors.append(f"{name}: skill folder missing: {skill}/")
            elif not os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
                errors.append(f"{name}: SKILL.md missing: {skill}/SKILL.md")
        hooks = bundle.get("hooks")
        if hooks and not os.path.isfile(os.path.join(root, hooks)):
            errors.append(f"{name}: hooks file missing: {hooks}")
    for skill, bundles in seen.items():
        if len(bundles) > 1:
            warnings.append(
                f"skill {skill!r} appears in multiple bundles: "
                + ", ".join(bundles)
            )
    return errors, warnings


def generate(spec, root):
    version = spec["version"]
    plugins_dir = os.path.join(root, "plugins")
    for bundle in spec["bundles"]:
        name = bundle["name"]
        bdir = os.path.join(plugins_dir, name)
        if os.path.isdir(bdir):
            shutil.rmtree(bdir)

        meta_dir = os.path.join(bdir, ".claude-plugin")
        os.makedirs(meta_dir)
        plugin = {
            "name": name,
            "description": bundle["description"],
            "version": version,
        }
        with open(os.path.join(meta_dir, "plugin.json"), "w", encoding="utf-8") as f:
            json.dump(plugin, f, indent=2)
            f.write("\n")

        skills_dir = os.path.join(bdir, "skills")
        os.makedirs(skills_dir)
        for skill in bundle["skills"]:
            # Relative so the link resolves from a fresh clone:
            # plugins/<bundle>/skills/<skill> -> ../../../<skill>
            os.symlink(os.path.join("..", "..", "..", skill),
                       os.path.join(skills_dir, skill))

        hooks = bundle.get("hooks")
        if hooks:
            hooks_dir = os.path.join(bdir, "hooks")
            os.makedirs(hooks_dir)
            shutil.copyfile(os.path.join(root, hooks),
                            os.path.join(hooks_dir, "hooks.json"))


def main(argv=None, root=None):
    root = root or REPO_ROOT
    parser = argparse.ArgumentParser(
        description="Generate plugin bundles from bundles.json.")
    parser.add_argument("--check", action="store_true",
                        help="validate only; do not write anything")
    args = parser.parse_args(argv)

    spec = load_bundles(root)
    errors, warnings = validate(spec, root)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 1

    if args.check:
        print(f"check passed: {len(spec['bundles'])} bundles, all skills resolve")
        return 0

    generate(spec, root)
    print(f"generated {len(spec['bundles'])} bundles into plugins/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
