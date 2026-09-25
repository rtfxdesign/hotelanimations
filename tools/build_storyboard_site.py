#!/usr/bin/env python3
"""Build the single-page storyboard site in the rtfx design system.

Per film: the client's beats first (verbatim from the brief), then the expanded
board: one illustrated card per beat, built from <film>/storyboard/STORYBOARD.md
(beat table, "Decisions taken", "Assets still needed") and the 960x540 frame
previews. Everything is embedded (base64), so the file is self-contained.

Usage: python tools/build_storyboard_site.py [out.html]
"""
import base64
import html
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "theria_storyboards.html"

FILMS = [
    ("01", "Giraffe Manor", "Nairobi, Kenya", "giraffe_manor", [
        "Start with image of the giraffe",
        "The giraffe manor logo appears under its feet",
        "Another giraffe walks into frame",
        "The logo disappears but the manor in the background appears",
        "Both giraffes turn and walk towards the manor and put their heads in the window"]),
    ("02", "The Fifth Avenue Hotel", "New York", "fifth_avenue", [
        "Start with image of the gold tortoise",
        "Add the fifth ave logo in gold (no background under its feet)",
        "The logo disappears",
        "Add the people walking the tortoise",
        "Have the people moving very slowly"]),
    ("03", "Passalacqua", "Lago di Como", "passalacqua", [
        "Start with their logo of 3 outlines of golden fishes",
        "Add the logo underneath",
        "The logo disappears as the fish become real golden fish - colored in",
        "The fish then become alive",
        "Add the background of the villa and the fish jumping out of the water"]),
    ("04", "Airelles Le Grand Contrôle", "Château de Versailles", "versailles", [
        "Start with the cake on the table with the chandelier",
        "The background appears with the lavish finishing in the background",
        "The logo for the hotel appears under the table",
        "The chandelier turns into a guillotine",
        "The logo disappears",
        "The guillotine comes down fast and cuts the cake",
        "The cake it cut up into many pieces"]),
    ("05", "North Island", "Seychelles", "north_island", [
        "Start with the gold turtle logo",
        "Have the background change to water",
        "Have the gold turtles start to swim",
        "Have them land on a beach",
        "Then back to sea, back to blue, back to white"]),
    ("06", "Miavana", "Nosy Ankao, Madagascar", "miavana", [
        "Start with the logo with the Lemers (better positions)",
        "Have the last one holding a mango throwing it to the other lemur",
        "The hotel appears in the background and the lemurs are in the palm trees",
        "Hotel disappears back to the logo and lemurs in places"]),
    ("07", "Necker Island", "British Virgin Islands", "necker_island", [
        "Art is a flamingo",
        "The flamingo takes flight",
        "It zooms out as an island comes into view with Richard Branson kite surfing (change in the photo to a blonde man)",
        "And a Lemers are playing Tennis with each other"]),
    ("08", "22 Club", "", "club22", [
        "Start with the The logo with the 22 club",
        "The 22 turns on its back and becomes vinyl record player with spinning records",
        "A spot light appears",
        "The numbers turn back around and then go back to normal",
        "Music is very sexy techno"]),
]


def b64(p: Path, mime="image/jpeg") -> str:
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def inline_md(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def parse_table(lines):
    """Return (headers, rows) for a markdown table given its lines."""
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    headers = [h.lower() for h in rows[0]]
    body = [r for r in rows[2:] if any(r)]
    return headers, body


def find_beat_table(md: str):
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            cells = [c.strip().lower() for c in lines[i].strip().strip("|").split("|")]
            has_frame = any(c == "frame" or c.startswith("frame") for c in cells)
            has_beat = any(c in ("#", "beat", "beat #", "#/beat") or c.startswith("on screen") or c.startswith("beat") for c in cells)
            if has_frame and has_beat and j - i >= 3:
                return parse_table(lines[i:j])
            i = j
        else:
            i += 1
    return None, []


def col(headers, *keys):
    """Column index whose header cell equals / starts with / contains a key, in that priority."""
    for pred in (lambda h, k: h == k, lambda h, k: h.startswith(k), lambda h, k: k in h):
        for k in keys:
            for idx, h in enumerate(headers):
                if pred(h, k):
                    return idx
    return None


def section_bullets(md: str, title_regex: str):
    m = re.search(r"^#{2,3}\s+(" + title_regex + r")[^\n]*\n(.*?)(?=^#{2,3}\s|\Z)", md, re.S | re.M | re.I)
    if not m:
        return []
    out = []
    for ln in m.group(2).splitlines():
        ln = ln.strip()
        if re.match(r"^([-*]|\d+[.)])\s+", ln):
            out.append(re.sub(r"^([-*]|\d+[.)])\s+", "", ln))
    return out


def header_meta(md: str):
    """TRT / fps line from the header table or first paragraph."""
    m = re.search(r"TRT[^|\n]*\|\s*([^|\n]+)", md)
    if m:
        return re.sub(r"\*", "", m.group(1)).strip()
    m = re.search(r"TRT\**[^0-9\n]{0,24}(\d+(?:\.\d+)?\s*s[^|\n]{0,80})", md)
    if m:
        return re.sub(r"\*", "", m.group(1)).strip()
    m = re.search(r"(\d+(?:\.\d+)?\s*s\s*/\s*f?\d+[^|\n]*)", md)
    return m.group(1).strip() if m else ""


def frame_key(cell: str):
    """First backticked or bare token like 01_hold from a Frame cell."""
    m = re.findall(r"`?([0-9]{2}[a-z]?_[A-Za-z0-9_\-]+)`?", cell)
    return m[0] if m else None


def load_svg(name):
    p = ROOT / "assets" / "rtfx" / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


CSS = """
:root{--bg:#000;--fg:#FAFAFA;--muted:#9a9a9a;--dim:#5c5c5c;--rule:#262626;--panel:#0d0d0d;--amber:#FFB020;--ch:12px}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--fg)}
body{font-family:"Space Grotesk",system-ui,sans-serif;font-size:15px;line-height:1.5;padding:0 16px 96px}
h1,h2,h3,.mono{font-family:"Martian Mono",monospace;letter-spacing:-.01em}
a{color:inherit}
code{font-family:"Martian Mono",monospace;font-size:.85em;color:var(--amber)}
.wrap{max-width:1280px;margin:0 auto}
.chamfer{clip-path:polygon(var(--ch) 0,100% 0,100% calc(100% - var(--ch)),calc(100% - var(--ch)) 100%,0 100%,0 var(--ch))}
.tick{height:9px;margin:28px 0;background:linear-gradient(#333,#333) 0 8px/100% 1px no-repeat,repeating-linear-gradient(90deg,#3a3a3a 0 1px,transparent 1px 32px) 0 0/100% 9px no-repeat}
header{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;padding:40px 0 24px;flex-wrap:wrap}
header .logo svg{height:30px;width:auto;display:block}
header h1{font-size:20px;margin:14px 0 4px;font-weight:600}
header .sub{color:var(--muted);font-size:13px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font-family:"Martian Mono",monospace;font-size:11px;letter-spacing:.04em;text-transform:uppercase;padding:6px 10px;border:1px solid var(--rule);color:var(--muted);background:var(--panel)}
.chip.amber{color:#000;background:var(--amber);border-color:var(--amber)}
nav.films{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin:12px 0 0}
nav.films a{display:block;text-decoration:none;padding:10px 12px;background:var(--panel);border:1px solid var(--rule);font-family:"Martian Mono",monospace;font-size:12px;color:var(--fg)}
nav.films a span{color:var(--amber);margin-right:8px}
nav.films a:hover{border-color:var(--amber)}
.intro{color:var(--muted);max-width:820px}
.intro strong{color:var(--fg)}
section.film{padding-top:8px}
.filmhead{display:flex;align-items:baseline;gap:18px;flex-wrap:wrap;margin:36px 0 6px}
.filmhead .num{font-family:"Martian Mono",monospace;font-size:44px;color:var(--amber);line-height:1}
.filmhead h2{font-size:26px;margin:0;font-weight:600}
.filmhead .place{color:var(--muted);font-family:"Martian Mono",monospace;font-size:12px;text-transform:uppercase;letter-spacing:.06em}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 18px}
.label{font-family:"Martian Mono",monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);margin:0 0 10px}
.brief{background:var(--panel);border:1px solid var(--rule);padding:18px 20px;max-width:900px}
.brief ol{margin:0;padding:0;list-style:none;counter-reset:b}
.brief li{counter-increment:b;display:grid;grid-template-columns:34px minmax(0,1fr);gap:10px;padding:6px 0;border-top:1px solid var(--rule);font-family:"Martian Mono",monospace;font-size:13px}
.brief li:first-child{border-top:0}
.brief li::before{content:counter(b,decimal-leading-zero);color:var(--amber)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(400px,1fr));gap:16px}
.card{background:var(--panel);border:1px solid var(--rule);display:flex;flex-direction:column}
.card img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#111}
.card .body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px}
.card .beat{font-family:"Martian Mono",monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--amber)}
.card .beat .t{color:var(--muted);margin-left:10px;text-transform:none;letter-spacing:0}
.card .brieftxt{font-family:"Martian Mono",monospace;font-size:12px;color:var(--muted)}
.card .on{font-size:15px}
.card .motion{font-size:13.5px;color:#cfcfcf}
.card .foot{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
.card .foot .chip{font-size:10px;padding:4px 8px}
.card .foot .chip.gen{color:var(--amber);border-color:#5a3d00}
.card .foot .chip.ready{color:#8fd694;border-color:#1f4a24}
.card .foot .chip.comp{color:#9dc1ff;border-color:#1f3556}
.aside{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.aside .box{background:var(--panel);border:1px solid var(--rule);padding:14px 16px}
.aside ul{margin:0;padding-left:18px;font-size:13.5px;color:#cfcfcf}
.aside li{margin:4px 0}
footer{margin-top:64px;color:var(--dim);font-family:"Martian Mono",monospace;font-size:11px;display:flex;align-items:center;gap:14px}
footer svg{height:22px;width:auto}
@media (max-width:700px){.cards{grid-template-columns:1fr}.aside{grid-template-columns:1fr}.filmhead .num{font-size:32px}.filmhead h2{font-size:20px}}
"""


def status_class(s: str):
    u = s.upper()
    if "GENERATE" in u:
        return "gen"
    if "READY" in u:
        return "ready"
    if "COMP" in u:
        return "comp"
    return ""


def build():
    parts = []
    wordmark = load_svg("rtfx-wordmark-white.svg")
    mark = load_svg("rtfx-mark-x-white.svg")
    today = date.today().isoformat()
    parts.append(f"""<header class=wrap>
<div><div class=logo>{wordmark}</div><h1>THERIA · HOTEL ANIMATIONS · STORYBOARDS</h1>
<div class=sub>v2 · {today} · eight films · one 16:9 HD master · 24 fps · every film loops on its first frame</div></div>
<div class=chips><span class="chip amber">For review</span><span class=chip>Client beats first</span><span class=chip>Expanded board below</span></div>
</header>
<div class=wrap><nav class=films>{''.join(f'<a href="#f{n}"><span>{n}</span>{html.escape(t)}</a>' for n, t, _, _, _ in FILMS)}</nav>
<div class=tick></div>
<p class=intro>Each film: the client's beats as written in the brief, then the expanded board. One card per beat, illustrated with a frame built from the supplied assets. <strong>Amber tags</strong> on a frame mean comp work or a shot still to generate; untagged frames are real assets as-is. Nothing is animated yet.</p></div>""")

    for num, title, place, d, brief in FILMS:
        sb = ROOT / d / "storyboard" / "STORYBOARD.md"
        frames_dir = ROOT / d / "storyboard" / "frames"
        md = sb.read_text(encoding="utf-8") if sb.exists() else ""
        headers, rows = find_beat_table(md)
        trt = header_meta(md)
        smalls = {p.stem.replace("_small", ""): p for p in sorted(frames_dir.glob("*_small.jpg"))} if frames_dir.exists() else {}

        cards = []
        used = set()
        if headers:
            c_beat = col(headers, "#", "beat", "beat #")
            c_brief = col(headers, "brief line", "brief line served", "brief")
            c_time = col(headers, "in – out", "in–out", "in-out", "in – out (frames)", "in – out (s)", "in–out (s)", "timing", "time", "in ")
            c_frame = col(headers, "frame", "frame file", "frame(s)")
            c_on = col(headers, "on screen", "on-screen", "screen")
            c_motion = col(headers, "motion")
            c_trans = col(headers, "transition")
            c_assets = col(headers, "asset")
            c_status = col(headers, "status")
            for r in rows:
                get = lambda i: (r[i] if i is not None and i < len(r) else "")
                key = frame_key(get(c_frame))
                img = ""
                if key:
                    # prefer exact stem, else the first small whose stem starts with key
                    p = smalls.get(key) or next((v for k, v in smalls.items() if k.startswith(key)), None)
                    if p:
                        img = f"<img src='{b64(p)}' alt='{html.escape(key)}' loading=lazy>"
                        used.add(p.stem.replace("_small", ""))
                status = re.sub(r"\*", "", get(c_status))
                foot = ""
                if get(c_trans):
                    foot += f"<span class=chip>{inline_md(get(c_trans))}</span>"
                if status:
                    foot += f"<span class='chip {status_class(status)}'>{inline_md(status[:90])}</span>"
                cards.append(f"""<article class="card chamfer">{img}<div class=body>
<div class=beat>Beat {inline_md(get(c_beat))}<span class=t>{inline_md(get(c_time))}</span></div>
{f'<div class=brieftxt>{inline_md(get(c_brief))}</div>' if get(c_brief) else ''}
<div class=on>{inline_md(get(c_on))}</div>
{f'<div class=motion>{inline_md(get(c_motion))}</div>' if get(c_motion) else ''}
{f'<div class=foot>{foot}</div>' if foot else ''}
{f'<div class=brieftxt style="opacity:.7">{inline_md(get(c_assets))}</div>' if get(c_assets) else ''}
</div></article>""")
        # frames not referenced by any beat row (alternates, extra tweens) get a plain card
        for k, p in smalls.items():
            if k not in used and not k.startswith("contact"):
                cards.append(f"<article class='card chamfer'><img src='{b64(p)}' alt='{html.escape(k)}' loading=lazy><div class=body><div class=beat>{html.escape(k.replace('_', ' '))}</div></div></article>")

        print(f'{d}: rows={len(rows)} frames={len(smalls)} matched={len(used)} extra={len(smalls)-len(used)}')
        decisions = section_bullets(md, r"Decisions taken|Decisions")
        needed = section_bullets(md, r"Assets still needed|Assets needed")
        aside = ""
        if decisions or needed:
            aside = "<div class=aside>"
            if decisions:
                aside += "<div class='box chamfer'><p class=label>Decisions taken</p><ul>" + "".join(f"<li>{inline_md(x)}</li>" for x in decisions) + "</ul></div>"
            if needed:
                aside += "<div class='box chamfer'><p class=label>Still to make</p><ul>" + "".join(f"<li>{inline_md(x)}</li>" for x in needed) + "</ul></div>"
            aside += "</div>"

        parts.append(f"""<section class="film wrap" id="f{num}">
<div class=tick></div>
<div class=filmhead><span class=num>{num}</span><h2>{html.escape(title)}</h2><span class=place>{html.escape(place)}</span></div>
<div class=meta>{f'<span class=chip>{inline_md(trt)}</span>' if trt else ''}<span class=chip>{len(brief)} client beats</span><span class=chip>{len(cards)} board frames</span></div>
<p class=label>Client beats · from the brief</p>
<div class="brief chamfer"><ol>{''.join(f'<li><span>{html.escape(b)}</span></li>' for b in brief)}</ol></div>
<p class=label style="margin-top:26px">Expanded board</p>
<div class=cards>{''.join(cards)}</div>
{aside}
</section>""")

    parts.append(f"<footer class=wrap>{mark}<span>RTFX DESIGN · ARTIFEX MACHINA · built from the Drive assets, {today}</span></footer>")
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Theria Storyboards</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Martian+Mono:wght@400;600&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(parts)}</body></html>"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT} ({len(doc)/1e6:.1f} MB)")


if __name__ == "__main__":
    build()
