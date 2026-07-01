#!/usr/bin/env python3
"""
render-graph.py — inject a graph data model into the self-contained force-graph
template and write a standalone, browser-openable HTML file (no server, no CDN).

Usage:
  python3 render-graph.py DATA.json [-o OUT.html] [-t TEMPLATE.html]

Defaults: template = ../assets/graph.template.html (next to this script);
          out      = docs/<DATA-stem>.html  (dir created if missing).

Validates referential integrity (edge endpoints exist, every node.cat points to an
anchor, exactly one core) and prints a summary to stderr. Exits non-zero on a
structural error so a broken data model never ships silently. stdout = output path.
"""
import argparse, json, os, sys
import html as _htmlesc

def die(m): print("error:", m, file=sys.stderr); sys.exit(1)
def warn(m): print("warn: ", m, file=sys.stderr)

ap = argparse.ArgumentParser(description="Render a graph data model to a standalone HTML file.")
ap.add_argument('data', help='path to the graph data JSON')
ap.add_argument('-o', '--out', help='output HTML path (default: docs/<data-stem>.html)')
ap.add_argument('-t', '--template', help='template path (default: ../assets/graph.template.html)')
args = ap.parse_args()

here = os.path.dirname(os.path.abspath(__file__))
tpl  = args.template or os.path.join(here, '..', 'assets', 'graph.template.html')
if not os.path.isfile(tpl): die(f"template not found: {tpl}")
try:
    data = json.load(open(args.data, encoding='utf-8'))
except Exception as e:
    die(f"cannot parse {args.data}: {e}")

nodes = data.get('nodes', []); edges = data.get('edges', []); kinds = data.get('kinds', {})
if not nodes: die("data has no nodes")
ids = {}
for i, n in enumerate(nodes):
    if 'id' not in n: die(f"node #{i} has no id")
    if 'k'  not in n: die(f"node {n['id']} has no kind (k)")
    if n['id'] in ids: die(f"duplicate node id: {n['id']}")
    ids[n['id']] = n
anchors = {nid for nid, n in ids.items() if n.get('anchor')}
cores   = [nid for nid, n in ids.items() if n.get('core')]
if len(cores) == 0: warn("no core node (core:true) — the graph will have no centre")
if len(cores) > 1:  warn(f"{len(cores)} core nodes; expected 1")
if not anchors:     warn("no anchor nodes (anchor:true) — members will not cluster")
for nid, n in ids.items():
    if n.get('core') or n.get('anchor'): continue
    cat = n.get('cat')
    if not cat:            warn(f"node {nid} has no cat — it will not attach to a layer")
    elif cat not in anchors: die(f"node {nid} cat '{cat}' is not an anchor node")
    if kinds and n['k'] not in kinds: warn(f"node {nid} kind '{n['k']}' missing from kinds (auto-neutral)")
for i, e in enumerate(edges):
    if len(e) < 3: die(f"edge #{i} needs [from,to,rel]: {e}")
    if e[0] not in ids: die(f"edge #{i} from '{e[0]}' is not a node id")
    if e[1] not in ids: die(f"edge #{i} to '{e[1]}' is not a node id")

payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
html = open(tpl, encoding='utf-8').read()
if '__GRAPH_DATA__' not in html: die("template has no __GRAPH_DATA__ placeholder")
html = html.replace('__GRAPH_DATA__', payload)
if data.get('title'):
    html = html.replace('<title>System Graph</title>', '<title>'+_htmlesc.escape(str(data['title']))+'</title>', 1)

out = args.out or os.path.join('docs', os.path.splitext(os.path.basename(args.data))[0] + '.html')
os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
open(out, 'w', encoding='utf-8').write(html)
struct = sum(1 for nid,n in ids.items() if not n.get('core') and not n.get('anchor') and n.get('cat') in anchors) + (len(anchors) if cores else 0)
print(f"ok: {len(nodes)} nodes, {len(edges)} semantic edges (+{struct} structural drawn), {len(anchors)} anchors, {len(cores)} core", file=sys.stderr)
print(f"wrote {out} — open file://{os.path.abspath(out)} in a browser", file=sys.stderr)
print(os.path.abspath(out))
