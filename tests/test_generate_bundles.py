"""Tests for scripts/generate_bundles.py.

Each test builds a self-contained fake repo in a temp directory so nothing here
depends on the real catalog.
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import generate_bundles  # noqa: E402


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def make_repo(tmp, spec, skills, hooks_file=None):
    write(os.path.join(tmp, "bundles.json"), json.dumps(spec))
    for s in skills:
        write(os.path.join(tmp, s, "SKILL.md"),
              f"---\nname: {s}\ndescription: test\n---\n")
    if hooks_file:
        write(os.path.join(tmp, hooks_file), '{"hooks": {}}\n')


def snapshot(plugins_dir):
    """Map every path under plugins/ to ('link', target) or ('file', bytes)."""
    entries = {}
    for dirpath, dirnames, filenames in os.walk(plugins_dir):
        for name in list(dirnames):
            p = os.path.join(dirpath, name)
            if os.path.islink(p):
                entries[os.path.relpath(p, plugins_dir)] = ("link", os.readlink(p))
        for name in filenames:
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, plugins_dir)
            if os.path.islink(p):
                entries[rel] = ("link", os.readlink(p))
            else:
                with open(p, "rb") as f:
                    entries[rel] = ("file", f.read())
    return entries


class GenerateBundlesTest(unittest.TestCase):
    def test_generation_succeeds_and_symlinks_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = {"version": "1.2.3", "bundles": [{
                "name": "b1", "description": "d1",
                "hooks": "hooks/session-start.json",
                "skills": ["alpha", "beta"],
            }]}
            make_repo(tmp, spec, ["alpha", "beta"],
                      hooks_file="hooks/session-start.json")

            self.assertEqual(generate_bundles.main([], root=tmp), 0)

            pj = os.path.join(tmp, "plugins", "b1", ".claude-plugin", "plugin.json")
            with open(pj, encoding="utf-8") as f:
                meta = json.load(f)
            self.assertEqual(meta["name"], "b1")
            self.assertEqual(meta["description"], "d1")
            self.assertEqual(meta["version"], "1.2.3")

            for s in ["alpha", "beta"]:
                link = os.path.join(tmp, "plugins", "b1", "skills", s)
                self.assertTrue(os.path.islink(link), f"{s} should be a symlink")
                self.assertEqual(os.readlink(link),
                                 os.path.join("..", "..", "..", s))
                # Every symlink resolves to a real SKILL.md.
                self.assertTrue(os.path.isfile(os.path.join(link, "SKILL.md")))

            self.assertTrue(os.path.isfile(
                os.path.join(tmp, "plugins", "b1", "hooks", "hooks.json")))

    def test_check_exits_1_on_missing_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = {"version": "0.1.0", "bundles": [{
                "name": "b1", "description": "d", "skills": ["ghost"],
            }]}
            # ghost/ is intentionally never created.
            write(os.path.join(tmp, "bundles.json"), json.dumps(spec))
            self.assertEqual(generate_bundles.main(["--check"], root=tmp), 1)

    def test_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = {"version": "0.1.0", "bundles": [{
                "name": "b1", "description": "d", "skills": ["alpha"],
            }]}
            make_repo(tmp, spec, ["alpha"])
            plugins_dir = os.path.join(tmp, "plugins")

            self.assertEqual(generate_bundles.main([], root=tmp), 0)
            first = snapshot(plugins_dir)
            self.assertEqual(generate_bundles.main([], root=tmp), 0)
            second = snapshot(plugins_dir)

            self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
