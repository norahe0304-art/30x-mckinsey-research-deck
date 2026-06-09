# -*- coding: utf-8 -*-
"""
McKinsey-style market-research deck engine (reusable).
============================================================
A data-driven generator for a 1280x720, page-turning HTML deck that also prints
to a clean per-slide PDF via headless Chrome.

HOW TO USE
  1. Put your research in <brand>-data.json (schema: references/methodology.md).
  2. Set BRAND, DATA_PATH, OUT_HTML below.
  3. Compose your deck in build() using the renderers (cover/divider/heroes/
     prose_slide/essay_slide/table_slide/decision_slide/sources_register).
  4. Run:  python3 deck_engine.py
     PDF:  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
           --disable-gpu --no-pdf-header-footer --print-to-pdf="<Brand>-Deck.pdf" "<Brand>-Deck.html"
  5. QC per references/qc-checklist.md (div diff must be 0).

DESIGN LAWS (see references/design-system.md) — do not violate:
  no eyebrow labels · action-title headlines · notes pinned bottom (margin-top:auto) ·
  nothing overlaps the footer · fill the page (<30% whitespace) · clipw() not raw [:n] ·
  flat (no shadows) · images = white-bg cutouts + mix-blend multiply + caption.
"""
import json, html, os, re

# ----------------------------------------------------------- config
PROJ      = os.path.dirname(os.path.abspath(__file__))
BRAND     = "BRAND NAME · CATEGORY"          # footer brand line
DATA_PATH = os.path.join(PROJ, "data.json")  # your <brand>-data.json
OUT_HTML  = os.path.join(PROJ, "Deck.html")
IMGREL    = "images"          # subject images: product cutouts, UI frames, or abstract motifs
D = json.load(open(DATA_PATH)) if os.path.exists(DATA_PATH) else {}

# ----------------------------------------------------------- helpers
def e(s): return html.escape(str(s))
def clipw(s, n):
    # word-boundary truncation: never cut mid-word; ellipsis only when shortened
    s = str(s).strip()
    if len(s) <= n: return s
    cut = s[:n]; sp = cut.rfind(' ')
    if sp > n * 0.55: cut = cut[:sp]
    return cut.rstrip(' ,.;:-') + '…'
def money(s):
    m = re.search(r'[\d.]+', str(s).replace(',', '')); return float(m.group()) if m else 0

PG = [1]  # running page number

# Universal "answer row" markers for decision exhibits — category-agnostic on purpose.
# Totals read the same in any category; category-specific result rows (LANDED COGS,
# CAC PAYBACK, NET VALUE, ...) are declared per deck via exhibit.boldKeys, never here.
RESULT_ROW_KEYS = ('TAM', 'SAM', 'SOM', 'TOTAL', 'SUBTOTAL', 'BLENDED', 'NET', 'PAYBACK',
                   'YEAR-1', 'YEAR 1')

# ----------------------------------------------------------- CSS (the locked system)
CSS = """
:root{--navy:#051C2C;--blue:#1F6FB2;--ink:#23272E;--mute:#7B8593;--hair:#E3E6EB;--row:#F7F8FA;
--c1:#DCE9F3;--c2:#A9CCE6;--c3:#5E9BCB;--c4:#2E6FA8;--c5:#103A5E;
--serif:Georgia,'Times New Roman',serif;--sans:'Inter','Helvetica Neue',Arial,sans-serif;}
*{margin:0;padding:0;box-sizing:border-box}
@page{size:1280px 720px;margin:0}
body{background:#5b6675}
.bl{color:var(--blue)}
.slide{width:1280px;height:720px;background:#fff;position:relative;overflow:hidden;
  font-family:var(--sans);color:var(--ink);page-break-after:always;margin:0 auto}
.pad{padding:40px 50px 48px;height:100%;display:flex;flex-direction:column}
.kick{font-size:10.5px;letter-spacing:.14em;color:var(--mute);font-weight:600;text-transform:uppercase}
h1{font-family:var(--serif);font-size:26px;line-height:1.16;color:var(--navy);font-weight:400;margin-top:8px;max-width:1080px}
.deck{font-size:13.5px;color:var(--mute);margin-top:7px}
.hr{height:2px;background:var(--navy);margin:13px 0 0}
.heroes{display:grid;grid-template-columns:repeat(var(--n,4),1fr);margin:18px 0 18px;padding-bottom:20px;border-bottom:1px solid var(--hair)}
.hero{padding:0 24px;border-left:1px solid var(--hair)}
.hero:first-child{padding-left:0;border-left:none}
.hero .n{font-family:var(--serif);font-size:32px;color:var(--navy);line-height:1}
.hero .l{font-size:11px;color:var(--mute);margin-top:9px;line-height:1.4}
.body{flex:1;display:grid;gap:34px;min-height:0}
.col{display:flex;flex-direction:column;min-height:0}
.ct{font-size:11.5px;font-weight:700;color:var(--navy);margin-bottom:10px}
.ct .sub{color:var(--mute);font-weight:500}
.drv{font-size:12px;line-height:1.72;color:var(--ink)}
.drv b{color:var(--navy);font-weight:600}
ul.clean{list-style:none}
ul.clean li{font-size:11.5px;line-height:1.5;color:var(--ink);padding-left:15px;position:relative;margin-bottom:9px}
ul.clean li::before{content:"";position:absolute;left:0;top:7px;width:5px;height:5px;background:var(--ink)}
ul.clean li b{color:var(--navy)}
.themes{display:grid;gap:22px 52px;align-content:space-evenly;flex:1}
table.fill{flex:1}
table.fill td{vertical-align:middle}
.theme .h{font-size:var(--thfs,13.5px);font-weight:700;color:var(--navy);margin-bottom:7px;font-family:var(--sans)}
.theme p{font-size:var(--tfs,12.5px);line-height:var(--tlh,1.8);color:var(--ink)}
.theme p b{color:var(--navy);font-weight:600}
.essay{column-count:2;column-gap:44px;margin-top:4px}
.essay .lead{font-family:var(--serif);font-size:var(--elfs,16px);line-height:1.5;color:var(--navy);margin-bottom:14px;column-span:all;font-style:italic}
.essay p{font-size:var(--efs,12.5px);line-height:var(--elh,1.74);color:var(--ink);margin-bottom:var(--epm,13px);break-inside:avoid}
.essay p b{color:var(--navy);font-weight:600}
.essay p .lh{font-weight:700;color:var(--navy)}
table{border-collapse:collapse;width:100%}
th{background:var(--navy);color:#fff;font-size:10px;font-weight:600;text-align:left;padding:9px 9px;letter-spacing:.02em}
th.c{text-align:center}
td{font-size:10.5px;padding:11px 9px;border-bottom:1px solid var(--hair);color:var(--ink);vertical-align:top}
td.k{font-weight:600;color:var(--navy)}
td.c{text-align:center}
.cell{color:#fff;font-weight:600;text-align:center}
.donut-wrap{display:flex;flex-direction:column}
.donut-wrap svg,.donut-wrap .legend{align-self:center}
.legend{display:flex;flex-wrap:wrap;gap:7px 14px;margin-top:16px;justify-content:center}
.legend span{font-size:10.5px;color:var(--ink);display:flex;align-items:center;gap:6px}
.legend i{width:10px;height:10px;display:inline-block}
.bars{display:flex;align-items:flex-end;gap:14px;height:215px;padding-top:16px}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
.bar .v{font-size:10px;color:var(--navy);margin-bottom:5px;font-weight:600}
.bar .col2{width:74%;background:var(--navy)}
.bar .x{font-size:10px;color:var(--mute);margin-top:7px}
.imp{background:var(--row);border-left:3px solid var(--navy);padding:12px 15px;font-size:11.5px;line-height:1.5}
.imp b{color:var(--navy);text-transform:uppercase;letter-spacing:.07em;font-size:10px}
.foot{position:absolute;left:50px;right:50px;bottom:0;padding:10px 0 16px;border-top:1px solid var(--hair);
  display:flex;font-size:9px;color:var(--mute);letter-spacing:.04em}
.foot .b{font-weight:700;color:var(--navy);letter-spacing:.08em}
.foot .pg{margin-left:auto;color:var(--navy);font-weight:700}
.prodimg{display:flex;align-items:center;justify-content:center;flex:1;min-height:0}
.prodimg img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply}
.cap{font-size:8.5px;color:var(--mute);text-align:center;margin-top:6px;font-style:italic}
.pgrid{display:grid;gap:14px}
.pgrid .cell2{text-align:center}
.pgrid .cell2 img{width:100%;mix-blend-mode:multiply}
.pgrid .cell2 .nm{font-size:12px;color:var(--navy);font-weight:600;margin-top:7px}
.pgrid .cell2 .hex{font-size:9.5px;color:var(--mute);letter-spacing:.05em}
.navy{background:var(--navy);color:#fff;width:1280px;height:720px;position:relative;overflow:hidden;
  page-break-after:always;font-family:var(--sans)}
.navy .accent{position:absolute;left:0;top:0;bottom:0;width:6px;background:var(--blue)}
.cover-pad{padding:64px 70px}
.cover h1c{display:block;font-family:var(--serif);font-size:46px;color:#fff;font-weight:400;margin-top:18px;line-height:1.1}
.cover .sub{font-size:18px;color:#C7D2DE;margin-top:16px;font-family:var(--serif);font-style:italic}
.dv-pad{padding:0 70px;height:100%;display:flex;flex-direction:column;justify-content:center}
.dv .no{font-family:var(--serif);font-size:90px;color:#5AA9E0;line-height:1}
.dv h2{font-family:var(--serif);font-size:40px;color:#fff;font-weight:400;margin-top:6px}
.dv .pts{font-size:12.5px;color:#9FB1C4;line-height:1.9;margin-top:24px}
"""

# ----------------------------------------------------------- primitives
def head(title, deck=None):
    # NO eyebrow/kicker — headline leads. title = full-sentence conclusion.
    h = f'<h1 style="margin-top:0">{e(title) if "<" not in title else title}</h1>'
    if deck: h += f'<div class="deck">{e(deck)}</div>'
    return h + '<div class="hr"></div>'

def foot(src, pg):
    return (f'<div class="foot"><span><span class="b">{e(BRAND)}</span> &nbsp;&nbsp;'
            f'Source: {e(src)}</span><span class="pg">{pg:02d}</span></div>')

def heroes(items):  # items = [(number_html, label), ...]
    cells = "".join(f'<div class="hero"><div class="n">{n}</div><div class="l">{l}</div></div>' for n, l in items)
    return f'<div class="heroes" style="--n:{len(items)}">{cells}</div>'

def hcell(v):  # heatmap cell
    bg = {'Low':'#DCE9F3','Med':'#A9CCE6','High':'#2E6FA8','Win':'#103A5E','—':'#F7F8FA'}.get(v, '#F7F8FA')
    fg = '#23272E' if v in ('Low','Med','—') else '#fff'
    return f'<td class="c cell" style="background:{bg};color:{fg}">{e(v)}</td>'

def donut_svg(segs, center_top, center_bot):
    # segs = [(pct, color), ...]
    out, off = [], 25.0
    for pct, col in segs:
        out.append(f'<circle cx="21" cy="21" r="15.9" fill="none" stroke="{col}" stroke-width="8" '
                   f'stroke-dasharray="{pct} {100-pct}" stroke-dashoffset="{off}"></circle>')
        off -= pct
    return (f'<svg width="172" height="172" viewBox="0 0 42 42">{"".join(out)}'
            f'<text x="21" y="22.4" text-anchor="middle" font-size="6" font-family="Georgia" fill="#051C2C">{center_top}</text>'
            f'<text x="21" y="26.4" text-anchor="middle" font-size="2.5" fill="#7B8593">{center_bot}</text></svg>')

# ----------------------------------------------------------- slide renderers
def cover(title_html, subtitle):
    PG[0] += 1
    f = os.path.join(PROJ, IMGREL, "cover-hero.png")
    bg = f"background:var(--navy) url('{IMGREL}/cover-hero.png') no-repeat center/cover" if os.path.exists(f) else ""
    return (f'<div class="navy cover" style="{bg}"><div class="accent"></div>'
            f'<div class="cover-pad" style="max-width:680px;height:100%;display:flex;flex-direction:column;justify-content:center">'
            f'<h1c>{title_html}</h1c><div class="sub">{e(subtitle)}</div></div></div>')

def divider(no, title, points):
    PG[0] += 1
    pts = "".join(f'{e(p)}<br>' for p in points)
    f = os.path.join(PROJ, IMGREL, f"divider-{no}.png")
    # duotone image bleeds off bottom-right; left edge faded so the square dissolves into navy.
    # NOTE: keep height<=100% so the PDF does not clip the subject (see qc-checklist "divider image").
    fade = "-webkit-mask-image:linear-gradient(to right,transparent 0%,#000 42%);mask-image:linear-gradient(to right,transparent 0%,#000 42%)"
    img = (f'<img src="{IMGREL}/divider-{no}.png" style="position:absolute;right:0;bottom:0;height:100%;width:auto;{fade}">'
           if os.path.exists(f) else "")
    return (f'<div class="navy dv"><div class="accent"></div>{img}'
            f'<div class="dv-pad" style="max-width:680px;position:relative;z-index:1">'
            f'<div class="no">{no}</div><h2>{e(title)}</h2><div class="pts">{pts}</div></div></div>')

def prose_slide(title, deck, themes, src, cols=2, note=None):
    # themes = [(bold_heading, paragraph_html), ...]   — the reference "bold theme + paragraph" style
    pg = PG[0]; PG[0] += 1
    blocks = "".join(f'<div class="theme"><div class="h">{e(h)}</div><p>{p}</p></div>' for h, p in themes)
    extra = f'<div class="imp" style="margin-top:auto"><b>Read.</b> {e(note)}</div>' if note else ""
    n = len(re.sub(r'<[^>]+>', '', ''.join(h + str(p) for h, p in themes)))
    thfs, tfs, tlh = (('15px', '13.8px', '2.0') if n < 1100 else
                      ('14.2px', '13px', '1.9') if n < 1800 else
                      ('13.5px', '12.5px', '1.8'))
    body = (f'<div class="themes" style="grid-template-columns:repeat({cols},1fr);'
            f'--thfs:{thfs};--tfs:{tfs};--tlh:{tlh}">{blocks}</div>')
    return (f'<div class="slide"><div class="pad">{head(title, deck)}'
            f'<div class="body" style="display:flex;flex-direction:column;margin-top:18px">{body}{extra}</div></div>{foot(src, pg)}</div>')

def essay_slide(title, deck, lead, paras, src, side=None):
    pg = PG[0]; PG[0] += 1
    # 自适应排版: 短文自动升档 (字大行疏) 填满页面, 长文维持密排 — 稀疏页不再顶部拥挤+底部留白
    n = len(re.sub(r'<[^>]+>', '', lead + ''.join(paras)))
    elfs, efs, elh, epm = (('19px', '14.2px', '2.05', '20px') if n < 1050 else
                           ('17.5px', '13.4px', '1.92', '16px') if n < 1500 else
                           ('16px', '12.5px', '1.74', '13px'))
    sty = f'--elfs:{elfs};--efs:{efs};--elh:{elh};--epm:{epm}'
    body = f'<div class="essay" style="{sty}">' + f'<div class="lead">{lead}</div>' + ''.join(f'<p>{p}</p>' for p in paras) + '</div>'
    if side:
        body = f'<div class="col">{body}</div><div class="col">{side}</div>'; grid = "1.5fr 1fr"
    else:
        grid = "1fr"
    return (f'<div class="slide"><div class="pad">{head(title, deck)}'
            f'<div class="body" style="grid-template-columns:{grid};margin-top:14px">{body}</div></div>{foot(src, pg)}</div>')

def answer_slide(title, deck, governing, pillars, src, note=None):
    # 金字塔原理执行摘要页：governing thought（一句话答案）先行，3–4 支柱结论支撑。
    # pillars = [(mini_conclusion_html, support_html[, stat, stat_label]), ...]
    pg = PG[0]; PG[0] += 1
    gov = (f'<div style="border-left:3px solid var(--blue);padding:4px 0 4px 18px;margin-top:10px">'
           f'<div style="font-family:var(--serif);font-size:20px;color:var(--navy);line-height:1.55">{governing}</div></div>')
    cells = ""
    for p in pillars:
        c, s = p[0], p[1]
        stat = p[2] if len(p) > 2 else None
        sl = p[3] if len(p) > 3 else ""
        num = (f'<div style="font-family:var(--serif);font-size:30px;color:var(--blue);line-height:1.1">{stat}</div>'
               f'<div style="font-size:10px;color:var(--mute);margin:2px 0 8px">{e(sl)}</div>') if stat else ""
        cells += (f'<div style="border-top:2px solid var(--navy);padding-top:10px">{num}'
                  f'<div style="font-size:12px;font-weight:700;color:var(--navy);line-height:1.45">{c}</div>'
                  f'<p style="font-size:11.5px;line-height:1.7;color:var(--ink);margin-top:6px">{s}</p></div>')
    grid = f'<div style="display:grid;grid-template-columns:repeat({len(pillars)},1fr);gap:22px;margin-top:26px">{cells}</div>'
    extra = f'<div class="imp" style="margin-top:auto"><b>Read.</b> {e(note)}</div>' if note else ""
    return (f'<div class="slide"><div class="pad">{head(title, deck)}'
            f'<div class="body" style="display:flex;flex-direction:column;margin-top:6px">{gov}{grid}{extra}</div></div>{foot(src, pg)}</div>')

def table_slide(title, deck, columns, rows, src, note=None, fill=True, bold_keys=()):
    # rows = [[c0, c1, ...], ...]; bold_keys = substrings that mark a highlighted total/result row.
    pg = PG[0]; PG[0] += 1
    th = "".join(f'<th{"" if i == 0 else " class=c"}>{e(c)}</th>' for i, c in enumerate(columns))
    trs = ""
    for r in rows:
        hl = any(k in str(r[0]).upper() for k in bold_keys)
        rst = ' style="background:#EAF1F8"' if hl else ''
        tds = ""
        for i, c in enumerate(r):
            base = 'k' if i == 0 else 'c'
            extra = ';font-weight:700;color:var(--navy)' if hl else ''
            tds += f'<td class="{base}" style="padding:6px 9px;font-size:10.5px{extra}">{e(c)}</td>'
        trs += f'<tr{rst}>{tds}</tr>'
    cls = ' class="fill"' if fill else ''
    table = f'<table{cls}><tr>{th}</tr>{trs}</table>'
    extra = f'<div class="imp" style="margin-top:auto"><b>Read.</b> {e(note)}</div>' if note else ""
    return (f'<div class="slide"><div class="pad">{head(title, deck)}'
            f'<div class="body" style="display:flex;flex-direction:column;margin-top:14px">{table}{extra}</div></div>{foot(src, pg)}</div>')

def _chart_title(t):
    # Chart titles are ALWAYS centered above the chart (sits on the chart's vertical axis).
    # `t` is raw HTML (may carry a `<span class="sub">` qualifier) — passed through, not escaped.
    return f'<div class="ct" style="text-align:center;margin-bottom:8px">{t}</div>' if t else ''

def donut_block(segs, center_top, center_bot, legend, title=None):
    # segs = [(pct, color), ...]; legend = [(label, color), ...]. Centered title + donut + legend.
    leg = "".join(f'<span><i style="background:{c}"></i>{e(l)}</span>' for l, c in legend)
    return (f'{_chart_title(title)}<div class="donut-wrap">{donut_svg(segs, center_top, center_bot)}'
            f'<div class="legend">{leg}</div></div>')

def bars_chart(items, maxv=None, title=None):
    # items = [(x_label, value_number, value_label), ...]. Centered title + flat navy bars, value on top.
    vals = [v for _, v, _ in items] or [1]
    mx = maxv or max(vals)
    cells = "".join(
        f'<div class="bar"><div class="v">{e(vl)}</div>'
        f'<div class="col2" style="height:{(v / mx * 100) if mx else 0:.1f}%"></div>'
        f'<div class="x">{e(l)}</div></div>' for l, v, vl in items)
    return f'{_chart_title(title)}<div class="bars">{cells}</div>'

def heatmap_block(columns, rows, title=None):
    # columns = [corner_label, col1, col2, ...]; rows = [(row_label, [v, v, ...]), ...]
    # each v in {'Low','Med','High','Win','—'} colored via hcell(). Centered title. Compact for a rail.
    th = "".join(f'<th{"" if i == 0 else " class=c"} style="font-size:9px;padding:6px 7px">{e(c)}</th>'
                 for i, c in enumerate(columns))
    trs = ""
    for label, vals in rows:
        cells = "".join(hcell(v).replace('class="c cell" style="',
                                         'class="c cell" style="padding:7px;font-size:9.5px;') for v in vals)
        trs += (f'<tr><td class="k" style="font-size:9.5px;padding:7px">{e(label)}</td>{cells}</tr>')
    return f'{_chart_title(title)}<table style="width:100%">{f"<tr>{th}</tr>"}{trs}</table>'

def charts_slide(title, deck, left, right, src, left_title=None, right_title=None, note=None):
    # EXCEPTION renderer — a full-page two-up exhibit. DEFAULT is to embed charts in a content page's
    # right rail via essay_slide(side=donut_block(...)+bars_chart(...)); a chart rides beside the prose
    # that reads it, not alone on a page. Use this only when a chart genuinely needs the whole canvas.
    pg = PG[0]; PG[0] += 1
    def col(t, body):
        h = f'<div class="ct">{e(t)}</div>' if t else ''
        return f'<div class="col" style="justify-content:center">{h}{body}</div>'
    grid = (f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:34px;flex:1;min-height:0">'
            f'{col(left_title, left)}{col(right_title, right)}</div>')
    extra = f'<div class="imp" style="margin-top:auto"><b>Read.</b> {e(note)}</div>' if note else ""
    return (f'<div class="slide"><div class="pad">{head(title, deck)}'
            f'<div class="body" style="display:flex;flex-direction:column;margin-top:16px">{grid}{extra}</div>'
            f'</div>{foot(src, pg)}</div>')

def decision_slide(page, src, headline=None, read=None):
    # page = verified _decision_<id>.json:
    #   {title,standfirst,exhibit:{columns,rows,note,boldKeys?},assumptions[],takeaway}
    # CATEGORY-AGNOSTIC: which row is the "answer row" is data, not engine. The default
    # marks only the universal totals (a sizing row is TAM/SAM/SOM/TOTAL in any category);
    # what an economics result row is called differs by category — LANDED COGS for goods,
    # CAC PAYBACK for SaaS, NET VALUE for a service — so the deck declares it via
    # exhibit.boldKeys. No physical-goods finance term is baked into the engine.
    pg = PG[0]; PG[0] += 1
    ex = page['exhibit']
    bold = tuple(k.upper() for k in ex.get('boldKeys', RESULT_ROW_KEYS))
    cols = ex['columns']; rows = ex['rows']
    th = "".join(f'<th{"" if i == 0 else " class=c"}>{e(c)}</th>' for i, c in enumerate(cols))
    trs = ""
    for r in rows:
        hl = any(k in str(r[0]).upper() for k in bold)
        rst = ' style="background:#EAF1F8"' if hl else ''
        tds = "".join(f'<td class="{"k" if i==0 else "c"}" style="padding:3px 9px;font-size:10px'
                      f'{";font-weight:700;color:var(--navy)" if hl else ""}">{e(c)}</td>' for i, c in enumerate(r))
        trs += f'<tr{rst}>{tds}</tr>'
    enote = ex.get('note', '')
    notehtml = f'<div class="cap" style="text-align:left;margin-top:6px;line-height:1.45">{e(enote)}</div>' if enote else ''
    table = f'<table><tr>{th}</tr>{trs}</table>{notehtml}'
    acells = "".join(
        f'<div style="font-size:9.5px;line-height:1.4"><span style="font-weight:700;color:var(--navy)">'
        f'{e(a["label"])} &mdash; {e(a["value"])}.</span> <span style="color:var(--mute)">{e(clipw(a["basis"],118))}</span></div>'
        for a in page['assumptions'])
    assum = (f'<div style="margin-top:12px"><div class="ct">Key assumptions and the judgment calls behind them</div>'
             f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px 36px;margin-top:6px">{acells}</div></div>')
    note = f'<div class="imp" style="margin-top:auto"><b>Read.</b> {e(read or page["takeaway"])}</div>'
    body = f'<div class="body" style="display:flex;flex-direction:column;margin-top:14px">{table}{assum}{note}</div>'
    return (f'<div class="slide"><div class="pad">{head(headline or page["title"], page["standfirst"])}{body}</div>{foot(src, pg)}</div>')

def sources_register(url_set, selected_rows, src, perpage=96):
    # selected_rows = [(area, primary_sources, how_used), ...]
    from urllib.parse import urlparse
    out = []
    pg = PG[0]; PG[0] += 1
    tr = "".join(f'<tr><td class="k" style="width:20%">{e(a)}</td><td style="width:40%">{e(b)}</td><td>{e(c)}</td></tr>'
                 for a, b, c in selected_rows)
    body = (f'<table class="fill"><tr><th>Evidence area</th><th>Primary sources</th><th>How it is used</th></tr>{tr}</table>'
            f'<div class="cap" style="text-align:left;margin-top:12px">Every source URL is listed in full on the following pages.</div>')
    out.append(f'<div class="slide"><div class="pad">{head("Selected source notes","")}'
               f'<div class="body" style="display:flex;flex-direction:column;margin-top:14px">{body}</div></div>{foot(src, pg)}</div>')
    dom = lambda u: (urlparse(u).netloc.replace('www.', '') or u)
    allu = sorted(url_set, key=lambda u: (dom(u), u))
    def disp(u):
        d = dom(u); path = u.split(d, 1)[-1] if d in u else u; s = d + path
        return s[:78] + '…' if len(s) > 79 else s
    chunks = [allu[i:i+perpage] for i in range(0, len(allu), perpage)]
    for ci, ch in enumerate(chunks):
        pg2 = PG[0]; PG[0] += 1; start = ci * perpage
        items = "".join(
            f'<div style="font-size:8px;line-height:1.5;color:var(--ink);padding:2px 0;border-bottom:1px solid #EEF0F3;'
            f'display:flex;gap:6px"><span style="color:var(--blue);font-weight:600;min-width:20px">{start+j+1}</span>'
            f'<a href="{e(u)}" style="color:var(--ink);text-decoration:none;word-break:break-all">{e(disp(u))}</a></div>' for j, u in enumerate(ch))
        sub = f"Complete source register, {len(allu)} unique URLs · part {ci+1} of {len(chunks)}"
        out.append(f'<div class="slide"><div class="pad">{head("Full source register", sub)}'
                   f'<div class="body" style="margin-top:6px;display:block"><div style="columns:3;column-gap:34px">{items}</div></div></div>{foot(src, pg2)}</div>')
    return out

def collect_source_urls(data):
    urls = set()
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'sourceUrl' and isinstance(v, str) and v.startswith('http'): urls.add(v)
                else: walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(data); return urls

# ----------------------------------------------------------- pager (screen) + assembler
PAGER_CSS = """
@media screen{
  html,body{height:100%;margin:0;background:#3a3f45;overflow:hidden}
  #deck{position:fixed;inset:0}
  #deck>div{position:absolute;top:50%;left:50%;display:none;
    transform:translate(-50%,-50%) scale(var(--s,1));transform-origin:center center;
    box-shadow:0 14px 50px rgba(0,0,0,.5);page-break-after:auto;margin:0}
  #deck>div.on{display:block}
  #nav{position:fixed;inset:0;z-index:40;display:flex}
  #nav .h{flex:1;cursor:pointer}
  #pg{position:fixed;right:16px;bottom:14px;z-index:50;background:rgba(5,28,44,.86);
    color:#cfe0ee;font:600 12px/1 'Inter',Arial,sans-serif;padding:8px 13px;border-radius:20px;letter-spacing:.04em;user-select:none}
  #hint{position:fixed;left:16px;bottom:15px;z-index:50;color:#aebccb;
    font:500 11px/1 'Inter',Arial,sans-serif;letter-spacing:.03em;user-select:none}
}
@media print{
  #nav,#pg,#hint{display:none!important}
  #deck>div{transform:none!important;box-shadow:none!important;display:block!important;position:relative!important}
}
"""
PAGER_JS = """
(function(){
  var d=document.getElementById('deck');
  var s=[].slice.call(d.children),i=0,pg=document.getElementById('pg');
  function fit(){var k=Math.min(innerWidth/1280,innerHeight/720)*0.97;
    s.forEach(function(el){el.style.setProperty('--s',k)});}
  function show(n){i=Math.max(0,Math.min(s.length-1,n));
    s.forEach(function(el,j){el.classList.toggle('on',j===i)});
    pg.textContent=(i+1)+' / '+s.length;history.replaceState(null,'','#'+(i+1));}
  addEventListener('keydown',function(ev){
    if(['ArrowRight','PageDown','ArrowDown',' '].indexOf(ev.key)>=0){ev.preventDefault();show(i+1);}
    else if(['ArrowLeft','PageUp','ArrowUp'].indexOf(ev.key)>=0){ev.preventDefault();show(i-1);}
    else if(ev.key==='Home'){show(0);}else if(ev.key==='End'){show(s.length-1);}});
  document.getElementById('navL').onclick=function(){show(i-1)};
  document.getElementById('navR').onclick=function(){show(i+1)};
  addEventListener('resize',fit);fit();
  show((parseInt((location.hash||'').slice(1))||1)-1);
})();
"""

def render(slides, out_html=OUT_HTML):
    doc = (f'<!doctype html><html><head><meta charset="utf-8">'
           f'<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
           f'<style>{CSS}</style><style>{PAGER_CSS}</style></head>'
           f'<body><div id="deck">{"".join(slides)}</div>'
           f'<div id="nav"><div class="h" id="navL"></div><div class="h" id="navR"></div></div>'
           f'<div id="pg"></div><div id="hint">&larr; &rarr; / space &middot; Home / End &middot; click left or right</div>'
           f'<script>{PAGER_JS}</script></body></html>')
    open(out_html, 'w').write(doc)
    diff = doc.count('<div') - doc.count('</div>')
    print(f"slides: {len(slides)} | div diff: {diff}  {'OK' if diff == 0 else '!! UNBALANCED'}")

# ----------------------------------------------------------- EXAMPLE build (replace with your deck)
def build():
    S = []
    S.append(cover("Brand<br>Category", "Market sizing, competitive landscape, and a line recommendation"))
    S.append(divider("01", "Market Overview",
                     ["Market size and trajectory", "Consumer and material preferences",
                      "Trends, competition, and challenges", "Where the opportunity sits"]))
    # ... s_market(), essay_slide(...), prose_slide(...) for sections 1–5 ...
    # Section 6 decision pages (verified JSON produced by the Workflow pipeline):
    for fid, src in [("_decision_tam.json", "Bottom-up build"),
                     ("_decision_econ.json", "Bottom-up economics model"),
                     ("_decision_biz.json", "Line plan; verified economics")]:
        p = os.path.join(PROJ, fid)
        if os.path.exists(p): S.append(decision_slide(json.load(open(p)), src))
    # sources last:
    if D:
        S.extend(sources_register(collect_source_urls(D),
                 [("Market sizing", "Primary source", "How used")], "Source register"))
    render(S)

if __name__ == "__main__":
    build()
