"""Provenance Erasure landing layout (2026-10-30). Operator: "provenanceerasure has some nearly invisible text, and both provenance erasure and
labor vector need some serious help with organization, visual flow, space between sections, collapsed expandables" — and, to the proposal, "yup, lets".

The page already folds its eight method sections and five record plates. This pass gives each method section a one-line summary under its title,
closes the one that opened by default (the Self-Audit Module), puts the older Empty Bracket panel's heading in the page's dim ink (it was #999,
contrast 2.85), squares the field panels, and sets the spacing. Nothing is removed: words and links are counted before and after.
Idempotent.  python3 scripts/provenance_aggregator/landing_layout.py"""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "index.html"
t = P.read_text(encoding="utf-8")
if 'id="pe-layout"' in t:
    print("already laid out"); sys.exit(0)


def words(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    return len(re.sub(r"<[^>]+>", " ", s).split())


def links(s):
    return sorted(re.findall(r'<a\s[^>]*href="([^"]+)"', s))


W0, L0 = words(t), links(t)
SUM = {
 "The PER Metric": "What a composition retains of a work's provenance against what it requires: one minus retained over required.",
 "Erasure Skew (Ω)": "The same rate, two different losses: which way the loss falls, and on whom.",
 "Three Dimensions": "PER-M, PER-C and PER-D: the loss of basic attribution, of the framework that made the meaning, and of lineage.",
 "The Self-Audit Module — recovered, and executable": "The module removed from Zenodo with the account on 19 June 2026, kept here in five versions and executable.",
 "Three Domains": "AI composition, historical and cultural erasure, and AI-mediated production.",
 "Process Provenance": "The third dimension beside artifact and semantic provenance: what was prompted, rejected, revised and decided.",
 "Canonical Sources": "The deposits that define PER, Ω and their companions, with their DOIs.",
 "Field Measurements: Live PER Batteries": "PER run live on Google AI Overview: the Self-Audit Module dissolved, and the Empty Bracket.",
}
n = 0
for title, line in SUM.items():
    pat = re.compile(r'(<details class="sec"[^>]*>\s*<summary>\s*<h2>' + re.escape(title) + r'</h2>)(\s*</summary>)')
    t, k = pat.subn(lambda m: m.group(1) + f'<span class="sd">{line}</span>' + m.group(2), t, count=1)
    n += k
if n != len(SUM):
    sys.exit(f"refused: {n} of {len(SUM)} summaries placed")
assert t.count('<details class="sec" id="module" open>') == 1
t = t.replace('<details class="sec" id="module" open>', '<details class="sec" id="module">')
assert t.count('<h3 style="margin-top: 0; color: #999;">') == 1
t = t.replace('<h3 style="margin-top: 0; color: #999;">', '<h3 style="margin-top: 0; color: var(--dim);">')

CSS = """<style id="pe-layout">/* landing layout (2026-10-30): one line under each folded section, room between them, square panels */
details.sec{border-top:1px solid var(--border);scroll-margin-top:70px}
details.sec:last-of-type{border-bottom:1px solid var(--border)}
details.sec>summary{padding:18px 2px 16px;cursor:pointer;display:flex;flex-wrap:wrap;align-items:baseline;row-gap:4px}
details.sec>summary h2{flex:1 1 70%}
details.sec>summary h2{font-size:1.28em!important}
details.sec>summary .sd{display:block;flex:1 1 100%;order:3;font-family:var(--serif);font-style:italic;font-size:.98em;color:var(--dim);line-height:1.45;margin-top:4px;text-transform:none;letter-spacing:0}
details.sec[open]>summary{border-bottom:1px dashed var(--border);margin-bottom:18px}
details.sec>*:last-child{margin-bottom:30px}
details.sec+hr{display:none}details.sec:last-of-type{border-bottom:none}details.sec+:not(details){margin-top:28px}
.fieldpanel{border-radius:4px!important;background:var(--soft)!important}
.lvagg,.audit{margin-bottom:28px}
.pplate{margin-top:3rem}
.pnav a{border-radius:3px!important}
</style>"""
t = t.replace("</head>", CSS + "\n</head>", 1)
W1, L1 = words(t), links(t)
added = sum(len(x.split()) for x in SUM.values())
if W1 - added != W0 or L1 != L0:
    sys.exit(f"refused: words {W0} → {W1} (added {added}); links {len(L0)} → {len(L1)}")
P.write_text(t, encoding="utf-8")
print(f"laid out: words {W0} + {added} = {W1}; links {len(L1)} unchanged; {n} summaries; the module section closed")
