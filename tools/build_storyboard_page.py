#!/usr/bin/env python3
"""Stitch the per-film STORYBOARD.md files and their frames into one review page.

Reads <film_dir>/storyboard/STORYBOARD.md and <film_dir>/storyboard/frames/*_small.jpg
for every film listed in FILMS, and writes:
    docs/STORYBOARDS_<date>.md    (concatenated markdown with image links)
    docs/STORYBOARDS_<date>.html  (self-contained: frames embedded as base64 JPEG)
    docs/STORYBOARDS_<date>.pdf   (via headless Chromium, if playwright is installed)

Usage: python tools/build_storyboard_page.py [YYYY-MM-DD]
"""
import base64
import re
import sys
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
FILMS = [
    ("01", "Giraffe Manor", "giraffe_manor"),
    ("02", "The Fifth Avenue Hotel", "fifth_avenue"),
    ("03", "Passalacqua", "passalacqua"),
    ("04", "Airelles Le Grand Contrôle, Versailles", "versailles"),
    ("05", "North Island", "north_island"),
    ("06", "Miavana", "miavana"),
    ("07", "Necker Island", "necker_island"),
    ("08", "22 Club", "club22"),
]

CSS = """
:root{--bg:#fff;--fg:#111;--muted:#555;--accent:#FFB020;--rule:#ddd;--code:#f3f3f3}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#000;--fg:#eee;--muted:#aaa;--rule:#333;--code:#151515}}
:root[data-theme="dark"]{--bg:#000;--fg:#eee;--muted:#aaa;--rule:#333;--code:#151515}
html,body{background:var(--bg);color:var(--fg);margin:0}
body{font-family:"Space Grotesk",system-ui,sans-serif;font-size:14px;line-height:1.45;padding:32px 16px;max-width:1200px;margin:0 auto}
h1,h2,h3{font-family:"Martian Mono",monospace;letter-spacing:-.01em;line-height:1.2}
h1{font-size:24px;border-left:6px solid var(--accent);padding-left:12px}
h2{font-size:20px;margin-top:2.4em;border-bottom:1px solid var(--rule);padding-bottom:4px;page-break-before:always}
h2.first,.intro h2{page-break-before:auto}
h3{font-size:14px;margin-top:1.4em}
table{border-collapse:collapse;width:100%;font-size:12px;margin:12px 0}
th,td{border:1px solid var(--rule);padding:4px 6px;vertical-align:top;text-align:left}
th{background:var(--code);font-family:"Martian Mono",monospace;font-weight:600;font-size:11px}
code{font-family:"Martian Mono",monospace;font-size:11px;background:var(--code);padding:1px 4px}
.frames{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin:14px 0}
.frames figure{margin:0}
.frames img{width:100%;display:block;border:1px solid var(--rule)}
.frames figcaption{font-family:"Martian Mono",monospace;font-size:11px;color:var(--muted);padding:4px 0}
.meta{color:var(--muted);font-size:12px}
@media print{body{padding:0;font-size:10.5px;max-width:none} h1{font-size:18px} h2{font-size:15px} table{font-size:8.5px} tr{page-break-inside:avoid} .frames{grid-template-columns:repeat(3,1fr)} :root{--bg:#fff;--fg:#000;--rule:#bbb;--code:#f0f0f0}}
"""


def b64(p: Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()


def main():
    day = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    out_md, out_html = ROOT / "docs" / f"STORYBOARDS_{day}.md", ROOT / "docs" / f"STORYBOARDS_{day}.html"
    md_parts = [f"# Theria Hotel Animations — Storyboards for review\nBoarded {day} · RTFX Design · one section per film, frames built from the real assets.\n"]
    html_parts = []
    intro = ROOT / "docs" / "storyboards_intro.md"
    if intro.exists():
        itxt = intro.read_text(encoding="utf-8")
        md_parts.append(itxt)
        html_parts.append("<div class=intro>" + markdown.markdown(itxt, extensions=["tables", "sane_lists"]) + "</div>")
    missing = []
    for num, title, d in FILMS:
        sb = ROOT / d / "storyboard" / "STORYBOARD.md"
        fr = sorted((ROOT / d / "storyboard" / "frames").glob("*_small.jpg"))
        if not sb.exists():
            missing.append(title)
            md_parts.append(f"\n## {num} · {title}\n\n_Not boarded yet._\n")
            html_parts.append(f"<h2>{num} · {title}</h2><p class=meta>Not boarded yet.</p>")
            continue
        text = sb.read_text(encoding="utf-8")
        text = re.sub(r"^# .*\n", "", text, count=1)          # drop the film's own H1
        text = re.sub(r"^## ", "### ", text, flags=re.M)       # demote its H2s
        gallery_md = "\n".join(f"![{p.stem}]({Path('..') / d / 'storyboard' / 'frames' / p.name})" for p in fr)
        md_parts.append(f"\n## {num} · {title}\n\n{gallery_md}\n\n{text}\n")
        figs = "".join(f"<figure><img src='{b64(p)}' alt='{p.stem}'><figcaption>{p.stem.replace('_small', '')}</figcaption></figure>" for p in fr)
        html_parts.append(f"<h2{' class=first' if num == '01' else ''}>{num} · {title}</h2><div class=frames>{figs}</div>"
                          + markdown.markdown(text, extensions=["tables", "sane_lists"]))
    out_md.write_text("\n".join(md_parts), encoding="utf-8")
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Theria Storyboards {day}</title>
<link href="https://fonts.googleapis.com/css2?family=Martian+Mono:wght@400;600&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<h1>Theria Hotel Animations — Storyboards for review</h1>
<p class=meta>Boarded {day} · RTFX Design · frames built from the real assets in the Drive folder; orange tags mark placeholders and shots still to generate.</p>
{''.join(html_parts)}
<p class=meta>Generated by tools/build_storyboard_page.py · Artifex Machina</p></body></html>"""
    out_html.write_text(html, encoding="utf-8")
    print(f"wrote {out_md.name} and {out_html.name} ({len(html)/1e6:.1f} MB); not boarded: {missing or 'none'}")
    try:
        import asyncio
        from playwright.async_api import async_playwright

        async def pdf():
            async with async_playwright() as p:
                exe = "/opt/pw-browsers/chromium" if Path("/opt/pw-browsers/chromium").exists() else None
                b = await p.chromium.launch(executable_path=exe)
                pg = await b.new_page()
                await pg.goto(out_html.resolve().as_uri(), wait_until="networkidle")
                await pg.emulate_media(media="print")
                await pg.pdf(path=str(out_html.with_suffix(".pdf")), format="A4", landscape=True, print_background=True,
                             margin={"top": "12mm", "bottom": "12mm", "left": "10mm", "right": "10mm"})
                await b.close()
        asyncio.run(pdf())
        print("wrote", out_html.with_suffix(".pdf").name)
    except ImportError:
        print("playwright not installed; PDF skipped")


if __name__ == "__main__":
    main()
