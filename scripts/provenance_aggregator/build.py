"""Render the provenance meta-aggregator (census schema 1.0): an index and one page per resource, from
data/provenance-census/census.json. Each page carries two JSON-LD nodes: the record (ours) and the entity it
describes (theirs). Every quoted field shows its source, the date read and the hash of the saved copy.
Run from the repository root: python3 scripts/provenance_aggregator/build.py"""
import json, html, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]
D = json.load(open(ROOT / "data/provenance-census/census.json", encoding="utf-8")); ROWS = D["rows"]; BY = {r["slug"]: r for r in ROWS}
SITE = "https://www.provenanceerasure.org"; BASE = SITE + "/aggregators/"
OUT = ROOT / "aggregators"
e = lambda s: html.escape(str(s), quote=True)
CSS = open(HERE / "style.css", encoding="utf-8").read()
BASIS = {"operator": ("op", "the operator's own statement"), "third-party": ("3p", "a third-party account"), "observed": ("obs", "our observation"), "reading": ("rd", "our reading")}
LINEAGE = {"media": "Media and images", "scholarly record": "The scholarly record", "training data": "Models and training data", "answer engines": "Answer engines",
           "computational lineage": "Computational lineage", "authorship and reuse": "Authorship and reuse", "manuscripts and books": "Manuscripts and books",
           "objects and art": "Objects and art"}
CAPS = ["expresses", "records", "tests"]
REL = {"part_of": "Part of", "has_part": "Has part", "neighbour": "Neighbours", "sibling": "Sibling record"}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">')
HEAD = FONTS + '<link rel="stylesheet" href="/assets/pe.css">'
NAV = [("Audit", "/module/"), ("Aggregators", "/aggregators/"), ("PER", "/#per"), ("Captures", "https://www.alexanarch.org/captures/")]

def topbar(on=""):
    nav = "".join(f'<a class="{"on" if n == on else ""}" href="{u}">{n}</a>' for n, u in NAV)
    return (f'<header class="top"><div class="in"><a class="wm" href="/"><i></i>Provenance Erasure</a><nav class="nav-top">{nav}</nav><div class="sp"></div>'
            f'<form class="srch" action="/aggregators/" method="get" role="search"><input name="q" type="search" placeholder="Search {len(ROWS)} resources" aria-label="Search the resources"></form></div></header>')

def bchip(r, f):
    v = r["evidence"].get(f)
    if not v: return ""
    ab, full = BASIS[v["basis"]]
    s = r["sources"][v["src"]]
    tip = full + (f' · “{v["quote"]}”' if v.get("quote") else "")
    return f' <a class="bl" href="#ev-{e(f)}" title="{e(tip)}"><span class="b">{ab}</span></a>'

def fold(title, inner, n=None, desc="", open_=False):
    if not inner: return ""
    return (f'<details class="sec"{" open" if open_ else ""}><summary><span class="st">{title}</span><span class="sd">{desc}</span>'
            + (f'<span class="sn">{n}</span>' if n else "") + f'</summary><div class="body">{inner}</div></details>')

def caps(r):
    return '<span class="cap">' + "".join(f'<span class="{"on" if c in r["capability"] else ""}">{c}</span>' for c in CAPS) + "</span>"

def chips(r):
    st = r["lifecycle"]["state"]; c = {"ended": "dead", "active": "live"}.get(st, "")
    return ('<div class="chips">' + f'<span class="chip">{e(LINEAGE.get(r["lineage"], r["lineage"]))}</span><span class="chip">{e(r["kind"])}</span>'
            + f'<span class="chip {c}">{e(st)}</span></div>')

def kernel(r):
    k = r["kind"]; art = "an" if k[:1].lower() in "aeiou" else "a"
    return f'{r["name"]}: {art} {k}. Operator: {r["operator"]}. The object it attaches provenance to: {r["provenance_object"]}.'

def cite_text(r):
    return f'Lee Sharks, ed. "{r["name"]}." Provenance meta-aggregator, Provenance Erasure, compiled {D["compiled"]}. {BASE}{r["slug"]}'

def bibtex(r):
    key = "pe-" + r["slug"].replace("-", "")[:24] + D["compiled"][:4]
    return (f'@misc{{{key},\n  editor = {{Sharks, Lee}},\n  title = {{{r["name"]}}},\n  howpublished = {{Provenance meta-aggregator, Provenance Erasure}},\n'
            f'  year = {{{D["compiled"][:4]}}},\n  note = {{Compiled {D["compiled"]}; every field sourced and dated}},\n  url = {{{BASE}{r["slug"]}}}\n}}')

def jsonld(r):
    rec, ent = BASE + r["slug"], BASE + r["slug"] + "#entity"
    sch = {"database": "Dataset", "monitor": "Dataset", "registry": "Dataset", "benchmark": "Dataset", "test series": "CreativeWorkSeries",
           "tracing tool": "SoftwareApplication", "algorithm and API": "SoftwareApplication"}.get(r["kind"], "CreativeWork")
    entity = {"@id": ent, "@type": sch, "name": r["name"], "alternateName": r.get("aka", []), "url": r["url"],
              "creator": {"@type": "Organization", "name": r["operator"]}}
    if r["evidence"].get("self_description", {}).get("quote"): entity["description"] = r["evidence"]["self_description"]["quote"]
    for x in r.get("relations", []):
        if x["rel"] == "part_of": entity["isPartOf"] = {"@id": BASE + x["target"] + "#entity"}
    record = {"@id": rec, "@type": "WebPage", "name": f'{r["name"]} — provenance meta-aggregator record', "mainEntity": {"@id": ent}, "about": {"@id": ent},
              "abstract": kernel(r), "dateCreated": D["compiled"], "dateModified": D["compiled"],
              "publisher": {"@type": "Organization", "name": "Provenance Erasure", "url": SITE + "/"},
              "editor": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
              "isPartOf": {"@type": "Dataset", "name": "Provenance meta-aggregator", "url": BASE},
              "citation": [s["url"] for s in r["sources"].values()], "license": "https://creativecommons.org/licenses/by/4.0/"}
    return json.dumps({"@context": "https://schema.org", "@graph": [record, entity]}, ensure_ascii=False, indent=1).replace("</", "<\\/")

def link(slug):
    x = BY.get(slug); return f'<a href="/aggregators/{slug}">{e(x["name"])}</a>' if x else e(slug)

def page(r):
    vt = "; ".join(f"{k.replace('_', ' ')}: {v}" for k, v in (r.get("version_and_time") or {}).items())
    cnt = f'{e(r["count"]["value"])} <span class="d">(as of {e(r["count"]["as_of"])})</span>' if r.get("count") else ""
    CARRY = [("provenance_object", "What receives provenance", e(r["provenance_object"])),
             ("relation_types", "Relations carried", e("; ".join(r["relation_types"]))),
             ("provenance_carrier", "Carrier", e(r["provenance_carrier"])),
             ("capability", "Expresses · records · tests", caps(r)),
             ("transformations_tested", "Operations tested", e("; ".join(r.get("transformations_tested") or [])) or '<span class="d">none</span>'),
             ("retention_results", "What survived", e(r.get("retention_results") or "not tested")),
             ("authority_dependencies", "Depends on", e("; ".join(r.get("authority_dependencies") or [])))]
    ENT = [("name", "Canonical name", e(r["name"])), ("aka", "Also known as", e(", ".join(r.get("aka", [])))),
           ("url", "Address", f'<a href="{e(r["url"])}">{e(r["url"])}</a>'), ("operator", "Operator", e(r["operator"])),
           ("founded", "Founded", e(r.get("founded") or "")), ("kind", "Kind", e(r["kind"])), ("unit", "Unit", e(r["unit"])),
           ("lifecycle", "Lifecycle", e(r["lifecycle"]["state"] + (f' — {r["lifecycle"]["detail"]}' if r["lifecycle"].get("detail") else ""))),
           ("count", "Count", cnt), ("cadence", "Cadence", e(r.get("cadence") or "")), ("intake", "Intake", e(r.get("intake") or "")),
           ("data_access", "Data access", e(r.get("data_access") or "")), ("license", "Licence", e(r.get("license") or "")),
           ("version_and_time", "Versions and dates", e(vt)), ("observed", "Observation", e(f'{r["observed"]["on"]}: {r["observed"]["fetch"]}'))]
    tbl = lambda F: "".join(f'<tr><td>{k}</td><td>{v}{bchip(r, f)}</td></tr>' for f, k, v in F if v)
    own = r["evidence"].get("self_description")
    ownq = f'<blockquote class="q">{e(own["quote"])}</blockquote><p class="d">{"In its own words" if own["basis"] == "operator" else "As a third party describes it"}: <a href="{e(r["sources"][own["src"]]["url"])}">{e(r["sources"][own["src"]]["url"])}</a>, read {e(r["sources"][own["src"]]["read"])}</p>' if own and own.get("quote") else ""
    ev = "".join(f'<li id="ev-{e(f)}"><b>{e(re.sub(r"_[0-9]+$", "", f).replace("_", " "))}</b> <span class="b">{BASIS[v["basis"]][0]}</span>'
                 + (f'<div class="q">{e(v["quote"])}</div>' if v.get("quote") else f'<div class="d">{e(v.get("note") or "")}</div>')
                 + f'<div class="d"><a href="{e(r["sources"][v["src"]]["url"])}">{e(r["sources"][v["src"]]["url"])}</a> · read {e(r["sources"][v["src"]]["read"])} · saved copy sha256 <code>{e(r["sources"][v["src"]]["sha256"][:16])}…</code></div></li>'
                 for f, v in r["evidence"].items())
    rels = list(r.get("relations", [])) + [{"rel": "has_part", "target": x["slug"]} for x in ROWS if any(y["rel"] == "part_of" and y.get("target") == r["slug"] for y in x.get("relations", [])) and not any(z.get("target") == x["slug"] for z in r.get("relations", []))]
    groups = {}
    for x in rels: groups.setdefault(x["rel"], []).append(x)
    def item(x):
        if x.get("target"): return f'<li>{link(x["target"])}' + (f'<div class="d">{e(x["note"])}</div>' if x.get("note") else "") + "</li>"
        head = f'<a href="{e(x["url"])}">{e(x["label"])}</a>' if x.get("url") else e(x["label"])
        return f'<li>{head}<div class="d">{e(x.get("note") or "")}</div></li>'
    relhtml = "".join(f'<h3>{REL[k]}</h3><ul>{"".join(item(x) for x in v)}</ul>' for k, v in groups.items())
    dis = "".join(f'<tr><td>{link(n["neighbour"]) if n.get("neighbour") else e(n["label"])}</td><td>{e(n["context"])}</td></tr>' for n in r.get("disambiguation", []))
    neg = "".join(f"<li>{e(t)}</li>" for t in r.get("negative_tags", []))
    src = "".join(f'<li><a href="{e(s["url"])}">{e(s["url"])}</a><div class="d">read {e(s["read"])} · HTTP {e(s["http"])} · sha256 <code>{e(s["sha256"][:16])}…</code></div></li>' for s in r["sources"].values())
    unc = "".join(f"<li>{e(u)}</li>" for u in r.get("unchecked", []))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(r["name"])} — provenance meta-aggregator</title><meta name="description" content="{e(kernel(r))}"><link rel="canonical" href="{BASE}{r["slug"]}">
<meta name="citation_title" content="{e(r["name"])} — provenance meta-aggregator record"><meta name="citation_editor" content="Lee Sharks"><meta name="citation_date" content="{D["compiled"]}"><meta name="citation_public_url" content="{BASE}{r["slug"]}">
<script type="application/ld+json">{jsonld(r)}</script>{HEAD}</head><body>{topbar("Aggregators")}<div class="wrap">
<div class="crumb"><a href="/aggregators/">Provenance meta-aggregator</a> / {e(LINEAGE.get(r["lineage"], r["lineage"]))}</div><h1>{e(r["name"])}</h1>{chips(r)}<div class="kernel">{e(kernel(r))}</div>
<div class="act"><a class="btn" href="{e(r["url"])}">{("Its landing page ↗ (" + e(r["lifecycle"]["state"]) + ")") if (r.get("lifecycle") or {}).get("state") == "ended" else ("Visit " + e(r["name"]) + " ↗")}</a><a class="btn ghost" href="/module/">Run an erasure audit</a><button class="btn ghost" type="button" data-copy="cite">Copy citation</button></div>
{ownq}
<h2>What it carries</h2><table>{tbl(CARRY)}</table><p class="legend">op the operator's own statement · 3p a third-party account · obs our observation · rd our reading. Hover a tag for its quote; each opens below with its source.</p>
<h2>Entity</h2><table>{tbl(ENT)}</table>
<h2>Relations</h2>{relhtml or '<p class="pend">None recorded yet.</p>'}
<div style="margin-top:34px">{fold("Evidence", f'<ul class="ev">{ev}</ul>', len(r["evidence"]), "every field's quote, its source and the hash of the saved copy")}{fold("Disambiguation", f'<table>{dis}</table>' if dis else '', len(r.get("disambiguation", [])), "the names it can be confused with")}{fold("Negative tags", f'<ul>{neg}</ul>' if neg else '', len(r.get("negative_tags", [])), "what it is not")}{fold("Sources", f'<ul>{src}</ul>', len(r["sources"]), "every source read, with its date and hash")}{fold("Not yet checked", f'<ul>{unc}</ul>' if unc else '', len(r.get("unchecked", [])), "what remains to read")}</div>
<h2>Cite this record</h2><div class="cite"><p id="cite">{e(cite_text(r))}</p><p class="d">Record {BASE}{r["slug"]} · entity {BASE}{r["slug"]}#entity · <a href="/data/provenance-census/census.json">the census as data</a></p></div><pre class="bib">{e(bibtex(r))}</pre>
<div class="foot">Editor: Lee Sharks (<a href="https://orcid.org/0009-0000-1599-0703">ORCID 0009-0000-1599-0703</a>). This page is the provenance meta-aggregator's record of the resource above: its reading and fields are ours, and each field carries its source, its basis and the hash of the copy read. Compiled {D["compiled"]}. CC BY 4.0.</div></div>
<script>document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=()=>{{const t=document.getElementById(b.dataset.copy).innerText;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{{const o=b.textContent;b.textContent='Copied';setTimeout(()=>b.textContent=o,1600)}}).catch(()=>{{}})}})</script></body></html>"""

SVG = lambda d: f'<svg viewBox="0 0 32 32" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'
FLOW = [("what", "What provenance", "the object it attaches to", '<rect x="7" y="6" width="18" height="20" rx="2"/><path d="M11 12h10M11 16h10M11 20h6"/>',
         "<b>What provenance</b>: the object that receives it (a file, a dataset, an assertion, a token, a manuscript, a work of art), the relations carried (creation, credit, rights, ownership, derivation, support) and what carries them (embedded metadata, a signed manifest, a graph, a revision history, a transcribed document)."),
        ("op", "Through which operation", "upload, publication, generation", '<path d="M6 16h14"/><path d="M16 11l5 5-5 5"/><circle cx="25" cy="16" r="2"/>',
         "<b>Through which operation</b>: the transformations the resource actually tested, each with its date: an upload and a download, publication through a news pipeline, every edit of an article, a model's generation."),
        ("whose", "On whose assertion", "operator, third party, observation", '<circle cx="16" cy="11" r="4.5"/><path d="M7 26c1.5-5 5-7.5 9-7.5s7.5 2.5 9 7.5"/>',
         "<b>On whose assertion</b>: every field is tagged with its basis: the operator's own statement, a third-party account, our observation, or our reading. Each quote opens with its source and the hash of the copy read."),
        ("survive", "With what evidence of survival", "what was kept, lost or untested", '<path d="M6 22l6-6 5 5 9-11"/><path d="M20 10h6v6"/>',
         "<b>With what evidence of survival</b>: what a dated test shows surviving. A resource that expresses or records provenance without testing it reads <i>not tested</i>, never a failure.")]

def index():
    lin = sorted({r["lineage"] for r in ROWS}, key=lambda x: list(LINEAGE).index(x) if x in LINEAGE else 99)
    rows = "".join(f'<div class="row" data-lin="{e(r["lineage"])}" data-cap="{e(" ".join(r["capability"]))}" data-text="{e((r["name"] + " " + " ".join(r.get("aka", [])) + " " + r["operator"] + " " + kernel(r)).lower())}">'
                   f'<div class="n"><a href="{r["slug"]}">{e(r["name"])}</a></div>{chips(r)}<div class="k">{e(kernel(r))}</div><div style="margin-top:10px">{caps(r)}</div></div>'
                   for r in sorted(ROWS, key=lambda r: r["name"].lower()) if not any(x["rel"] == "part_of" for x in r.get("relations", [])))
    steps = '<span class="arrow" aria-hidden="true"></span>'.join(f'<button type="button" class="step" aria-expanded="false" aria-controls="x-{k}">{SVG(d)}<b>{t}</b><span>{u}</span></button>' for k, t, u, d, _ in FLOW)
    xs = "".join(f'<p id="x-{k}" class="x" hidden>{x}</p>' for k, _, _, _, x in FLOW)
    trav = "".join(f'<tr><td><a href="{r["slug"]}">{e(r["name"])}</a></td>' + "".join(f'<td>{"●" if c in r["capability"] else "<span class=d>·</span>"}</td>' for c in CAPS)
                   + f'<td>{e("; ".join(r.get("transformations_tested") or [])) or "<span class=d>none</span>"}</td></tr>' for r in sorted(ROWS, key=lambda r: r["name"].lower()))
    btn = lambda key, vals, lab: "".join(f'<button data-{key}="{e(v)}">{e(lab(v))}</button>' for v in vals)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Provenance meta-aggregator — Provenance Erasure</title>
<meta name="description" content="The resources that carry, record and test provenance, across disciplines, each formalized as an entity with sourced, dated fields."><link rel="canonical" href="{BASE[:-1]}">{HEAD}</head><body>{topbar("Aggregators")}<div class="wrap">
<div class="crumb"><a href="/">Provenance Erasure</a> / aggregators</div><h1>Provenance meta-aggregator</h1>
<div class="kernel">The resources that carry, record and test provenance, from art history and manuscript studies to media credentials and model training data, each formalized as an entity. Every record answers one question: {e(D["organizing_question"][0].lower() + D["organizing_question"][1:])} {len(ROWS)} resources, compiled {D["compiled"]}.</div>
<div class="flow" role="group" aria-label="The organizing question">{steps}</div><div class="flow-x">{xs}</div><noscript><style>.flow-x .x{{display:block!important}}</style></noscript>
<p class="fig-cap">Each record keeps apart what a resource can <b>express</b>, what it <b>records</b>, and what it <b>tests</b>. Tap a step for the fields that answer it.</p>
<div class="f"><button class="on" data-all="1">all</button>{btn("lin", lin, lambda v: LINEAGE.get(v, v))}</div><div class="f">{btn("cap", CAPS, lambda v: v)}</div>
<div id="L" class="grid">{rows}</div><p class="none" id="none">No resource matches.</p>
<h2>Traverse by capability</h2><div class="tw"><table class="tv"><tr><td></td>{"".join(f"<td>{c}</td>" for c in CAPS)}<td>operations tested</td></tr>{trav}</table></div>
<p class="legend">The census as data: <a href="/data/provenance-census/census.json">census.json</a>, with every saved source in <a href="https://github.com/leesharks000/provenance-erasure/tree/main/data/provenance-census/sources">data/provenance-census/sources</a>.</p>
<div class="foot">Provenance Erasure · provenanceerasure.org · editor Lee Sharks (<a href="https://orcid.org/0009-0000-1599-0703">ORCID 0009-0000-1599-0703</a>) · a sibling of the <a href="https://www.machinemediation.org/aggregators/">MMRS meta-aggregator</a></div></div>
<script>let fs={{}};const qi=document.querySelector('.srch input');qi.value=new URLSearchParams(location.search).get('q')||'';document.querySelector('.srch').onsubmit=ev=>{{ev.preventDefault();apply()}};qi.oninput=()=>apply();
function apply(){{const q=qi.value.trim().toLowerCase();let n=0;document.querySelectorAll('.f button').forEach(x=>{{const k=x.dataset.lin?'lin':x.dataset.cap?'cap':'all';x.classList.toggle('on',k==='all'?!fs.lin&&!fs.cap:fs[k]===x.dataset[k])}});
document.querySelectorAll('#L .row').forEach(r=>{{const ok=(!fs.lin||r.dataset.lin===fs.lin)&&(!fs.cap||r.dataset.cap.split(' ').includes(fs.cap))&&(!q||q.split(' ').filter(Boolean).every(w=>r.dataset.text.includes(w)));r.style.display=ok?'':'none';n+=ok}});document.getElementById('none').style.display=n?'none':'block'}}
document.querySelectorAll('.f button').forEach(b=>b.onclick=()=>{{if(b.dataset.all){{fs={{}}}}else{{const k=b.dataset.lin?'lin':'cap',v=b.dataset[k];fs[k]=fs[k]===v?undefined:v}}apply()}});apply();
document.querySelectorAll('.flow .step').forEach(b=>b.onclick=()=>{{const on=b.getAttribute('aria-expanded')!=='true';document.querySelectorAll('.flow .step').forEach(x=>{{x.setAttribute('aria-expanded','false');document.getElementById(x.getAttribute('aria-controls')).hidden=true}});if(on){{b.setAttribute('aria-expanded','true');document.getElementById(b.getAttribute('aria-controls')).hidden=false}}}})</script></body></html>"""

(ROOT / "assets").mkdir(exist_ok=True); (ROOT / "assets/pe.css").write_text(CSS, encoding="utf-8")
OUT.mkdir(exist_ok=True); (OUT / "index.html").write_text(index(), encoding="utf-8")
for r in ROWS:
    p = OUT / r["slug"]; p.mkdir(exist_ok=True); (p / "index.html").write_text(page(r), encoding="utf-8")
sm = ROOT / "sitemap.xml"; st = sm.read_text(encoding="utf-8")
add = "".join(f'  <url><loc>{u}</loc><lastmod>{D["compiled"]}</lastmod><priority>0.7</priority></url>\n' for u in [BASE[:-1]] + [BASE + r["slug"] for r in ROWS] if f"<loc>{u}</loc>" not in st)
sm.write_text(st.replace("</urlset>", add + "</urlset>"), encoding="utf-8")
lp = ROOT / "llms.txt"; lt = lp.read_text(encoding="utf-8")
blk = ("<!-- PROVENANCE-AGGREGATOR-START -->\n## Provenance meta-aggregator\n\nThe resources that carry, record and test provenance, each formalized as an entity with sourced, dated fields: "
       f"{BASE[:-1]} (census as data: {SITE}/data/provenance-census/census.json)\n\n"
       + "".join(f'- {r["name"]} ({r["kind"]}; {LINEAGE.get(r["lineage"], r["lineage"])}; {"/".join(r["capability"])}): {BASE}{r["slug"]}\n' for r in sorted(ROWS, key=lambda r: r["name"].lower()))
       + "<!-- PROVENANCE-AGGREGATOR-END -->\n")
lt = re.sub(r"<!-- PROVENANCE-AGGREGATOR-START -->.*?<!-- PROVENANCE-AGGREGATOR-END -->\n", lambda m: blk, lt, flags=re.S) if "PROVENANCE-AGGREGATOR-START" in lt else lt.rstrip("\n") + "\n\n" + blk
lp.write_text(lt, encoding="utf-8")
print(len(ROWS), "pages")

# the landing page's aggregator block, between its markers, after the audit
def front_block():
    top = [r for r in sorted(ROWS, key=lambda r: r["name"].lower()) if not any(x["rel"] == "part_of" for x in r.get("relations", []))]
    li = "".join(f'<a class="mini" href="/aggregators/{r["slug"]}"><b>{e(r["name"])}</b><span>{e(LINEAGE.get(r["lineage"], r["lineage"]))} · {e("/".join(r["capability"]))}</span></a>' for r in top)
    return ("<!-- PE-AGGREGATOR-START (generated by scripts/provenance_aggregator/build.py from data/provenance-census/census.json) -->\n"
            f'<section class="section" id="aggregators"><h2>Provenance meta-aggregator</h2><p class="section">The resources that carry, record and test provenance, across disciplines, each formalized as an entity with sourced, dated fields: '
            f'what provenance it carries, through which operation, on whose assertion, with what evidence of survival. {len(ROWS)} resources, compiled {D["compiled"]}.</p>'
            f'<div class="minis">{li}</div><p class="section" style="margin-top:12px"><a href="/aggregators/">All {len(ROWS)}, with the capability table</a> · <a href="/data/provenance-census/census.json">the census as data</a></p></section>\n'
            "<!-- PE-AGGREGATOR-END -->")
lp = ROOT / "index.html"; lt = lp.read_text(encoding="utf-8")
if "<!-- PE-AGGREGATOR-START" in lt:
    lt = re.sub(r"<!-- PE-AGGREGATOR-START.*?<!-- PE-AGGREGATOR-END -->", lambda m: front_block(), lt, count=1, flags=re.S)
elif "<!-- PE-AUDIT-END -->" in lt:
    lt = lt.replace("<!-- PE-AUDIT-END -->", "<!-- PE-AUDIT-END -->\n" + front_block(), 1)
lp.write_text(lt, encoding="utf-8")
