#!/usr/bin/env python3
"""Chronologically index Claude Code session transcripts.

Usage:
    index_sessions.py <file1.jsonl> [file2.jsonl ...]

Prints one line per session, sorted by first timestamp:
    YYYY-MM-DD HH:MM | <short-id> | br=<gitBranch> | u=<user-turns> | <first real user message>

`gitBranch` is usually the strongest relevance signal; the first real user
message tells you what the session was about. Harness/meta first messages are
skipped so a skill preamble isn't mistaken for the topic.
"""
import sys, json, os

NOISE_PREFIXES = (
    "<", "[Request interrupted", "Caveat:", "Base directory for this skill",
    "<command-name>", "<local-command",
)


def content_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            b.get("text", "") for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def is_noise(text):
    t = (text or "").strip()
    return len(t) < 15 or t.startswith(NOISE_PREFIXES)


rows = []
for path in sys.argv[1:]:
    first_ts = branch = topic = None
    users = 0
    try:
        fh = open(path, errors="replace")
    except OSError:
        continue
    with fh:
        for line in fh:
            try:
                o = json.loads(line)
            except ValueError:
                continue
            if not first_ts and o.get("timestamp"):
                first_ts = o["timestamp"]
            if not branch and o.get("gitBranch"):
                branch = o["gitBranch"]
            if o.get("type") == "user":
                txt = content_text(o.get("message", {}).get("content"))
                if txt.strip():
                    users += 1
                    if topic is None and not is_noise(txt):
                        topic = " ".join(txt.split())[:90]
    short = os.path.basename(path).split(".")[0][:13]
    rows.append((first_ts or "", short, branch or "?", users, topic or ""))

rows.sort(key=lambda r: r[0])
for ts, short, branch, users, topic in rows:
    tsf = ts[:16].replace("T", " ") if ts else "?"
    print(f"{tsf} | {short} | br={branch} | u={users:3d} | {topic}")
