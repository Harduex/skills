#!/usr/bin/env python3
"""Re-render every generated example in SHOWCASE.md from diagram.py.

The showcase is the gallery people copy configs out of, so a rendered block
that no longer matches what the generator produces is worse than no gallery at
all. Running this makes drift impossible to miss: each example is regenerated
from the config the page itself publishes.

    python3 scripts/regen_showcase.py           # rewrite SHOWCASE.md in place
    python3 scripts/regen_showcase.py --check   # exit 1 if anything drifted

Each generated example is marked by an HTML comment before its fenced block:

    <!-- regen: self -->            render the ```python block that follows it
    <!-- regen: default -->         render diagram.py's own built-in example
    <!-- regen: LR -->              reuse the config from the "## LR" section
    <!-- regen: TB, STAGGER=8 -->   that config, with a constant overridden

Blocks with no marker (the hand-drawn hub-and-spoke) are left alone.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOWCASE = HERE.parent / "SHOWCASE.md"
GENERATOR = HERE / "diagram.py"
MARKER = re.compile(r"<!--\s*regen:\s*([^>]*?)\s*-->\s*\n```\n(.*?)\n```", re.S)


def configs_by_section(text):
    """Every '## <NAME> …' section's python config block, keyed by NAME."""
    out = {}
    for m in re.finditer(r"\n#{2,3} (\S+)[^\n]*\n(.*?)(?=\n#{2,3} |\Z)", text, re.S):
        cfg = re.search(r"```python\n(.*?)```", m.group(2), re.S)
        if cfg:
            out.setdefault(m.group(1), cfg.group(1))
    return out


def render(config, overrides):
    """Run diagram.py with `config` spliced over its own COLUMNS/EDGES block.

    `config` is None for the generator's own built-in example. Overrides are
    appended AFTER the config, never patched into the header — a config block
    that sets the same constant would otherwise silently win and the override
    would render as a no-op."""
    src = GENERATOR.read_text(encoding="utf-8")
    tail = src[src.index("\nFOOTPRINT = ORIENTATION"):]
    if config is None:
        head, config = src[: src.index("\nFOOTPRINT = ORIENTATION")], ""
    else:
        head = src[: src.index("COLUMNS = [")]
        if orient := re.search(r'ORIENTATION = "(\w+)"', config):
            head = re.sub(r'^ORIENTATION = "\w+"',
                          f'ORIENTATION = "{orient.group(1)}"', head,
                          count=1, flags=re.M)
        for name in ("EDGES", "SKIP_EDGES"):
            if f"\n{name} =" not in "\n" + config:
                config += f"\n{name} = []\n"
    config += "\n" + "".join(f"{k} = {v}\n" for k, v in overrides.items())
    scratch = HERE / "_regen_tmp.py"
    scratch.write_text(head + config + tail, encoding="utf-8")
    try:
        done = subprocess.run([sys.executable, str(scratch)],
                              capture_output=True, text=True)
    finally:
        scratch.unlink(missing_ok=True)
    if done.returncode:
        sys.exit(f"generator failed for {overrides or 'self'}:\n{done.stderr}")
    return done.stdout.rstrip("\n")


def main():
    check = "--check" in sys.argv
    text = SHOWCASE.read_text(encoding="utf-8")
    sections = configs_by_section(text)
    drifted, out, last = [], [], 0

    for m in MARKER.finditer(text):
        directive, shown = m.group(1), m.group(2)
        source, *rest = [p.strip() for p in directive.split(",")]
        overrides = dict(p.split("=", 1) for p in rest)
        if source == "self":
            config = re.search(r"```python\n(.*?)```", text[m.end():], re.S).group(1)
        elif source == "default":
            config = None                      # the generator's own built-in example
        else:
            config = sections[source]
        got = render(config, overrides)
        if got != shown:
            drifted.append(directive)
        out.append(text[last:m.start(2)])
        out.append(got)
        last = m.end(2)
    out.append(text[last:])

    if check:
        print("\n".join(f"  drifted: {d}" for d in drifted) or "  all examples current")
        return 1 if drifted else 0
    SHOWCASE.write_text("".join(out), encoding="utf-8")
    print(f"regenerated {len(MARKER.findall(text))} example(s); "
          f"{len(drifted)} were stale")
    return 0


if __name__ == "__main__":
    sys.exit(main())
