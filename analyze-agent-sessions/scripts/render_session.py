#!/usr/bin/env python3
"""Render one Claude Code transcript to cheap-to-grep text.

Usage:
    render_session.py <session.jsonl>

USER turns and ASSISTANT prose are printed in full; tool calls collapse to a
single line; tool results and thinking are truncated. Pipe THIS to grep/less —
never `cat` the raw JSONL (transcripts are ~1MB+ and will overflow context).

Schema notes: routes on top-level `type` ("user"/"assistant"); `message.content`
may be a plain string OR a list of blocks (text/thinking/tool_use/tool_result).
Does NOT rely on `isSidechain` (uniformly false in some CC versions) — detect
subagents via Agent/Task tool_use lines and the task-notification user turns
they return.
"""
import sys, json

TRUNC = 240
META_USER_PREFIXES = (
    "Base directory for this skill", "<command-name>", "<local-command", "Caveat:",
)


def trunc(s, n=TRUNC):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[:n] + "…"


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            b.get("text", "") for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def tool_oneliner(name, inp):
    inp = inp or {}
    if name == "Bash":
        return f"$ {trunc(inp.get('command', ''), 300)}"
    if name in ("Read", "Edit", "Write", "NotebookEdit"):
        return f"{name} {inp.get('file_path', '')}"
    if name in ("Grep", "Glob"):
        return f"{name} {inp.get('pattern', inp.get('query', ''))}"
    if name in ("Agent", "Task"):
        what = inp.get("description") or inp.get("prompt", "")
        return f"Agent[{inp.get('subagent_type', '')}] {trunc(what, 120)}"
    return f"{name} {trunc(json.dumps(inp), 120)}"


for line in open(sys.argv[1], errors="replace"):
    try:
        o = json.loads(line)
    except ValueError:
        continue
    typ = o.get("type")
    ts = o.get("timestamp", "")[:16].replace("T", " ")
    content = o.get("message", {}).get("content")

    if typ == "user":
        text = text_of(content)
        if text.strip() and not text.lstrip().startswith(META_USER_PREFIXES):
            print(f"\n### USER {ts}\n{text.strip()}")
        if isinstance(content, list):
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    rc = b.get("content", "")
                    if isinstance(rc, list):
                        rc = "".join(x.get("text", "") for x in rc if isinstance(x, dict))
                    print(f"  [result] {trunc(rc)}")

    elif typ == "assistant":
        blocks = content if isinstance(content, list) else (
            [{"type": "text", "text": content}] if isinstance(content, str) else []
        )
        for b in blocks:
            if not isinstance(b, dict):
                continue
            bt = b.get("type")
            if bt == "text" and b.get("text", "").strip():
                print(f"\n### ASSISTANT {ts}\n{b['text'].strip()}")
            elif bt == "thinking":
                print(f"  [thinking] {trunc(b.get('thinking', ''))}")
            elif bt == "tool_use":
                print(f"  → {tool_oneliner(b.get('name'), b.get('input'))}")
