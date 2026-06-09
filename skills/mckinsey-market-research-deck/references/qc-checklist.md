# QC Checklist (mandatory self-run before delivery)

The user requires self-verification by rendering — never present unchecked. Run all of this, fix,
re-render, re-check.

## A. Structure (programmatic)
```bash
# 1. div balance must be 0 (an unclosed div silently breaks pagination)
python3 -c "h=open('<Brand>-Deck.html').read();print('div diff:',h.count('<div')-h.count('</div>'))"
# 2. page count matches intent
pdfinfo <Brand>-Deck.pdf | grep Pages
```

## B. Source register (programmatic)
Confirm every unique source URL renders, numbering is contiguous, no empty cells, header count matches.
Then audit against the source bar (methodology.md § The source bar):
- [ ] **Density**: unique URLs ÷ content pages ≥ 1.5 (exclude cover/dividers/thesis).
- [ ] **Quality mix**: ≥50% of register domains are T1 (vendor/primary) or T2 (named research).
- [ ] **No aggregator-only claims**: every market-size/adoption number traces to T2+, or its source
      line says "via <aggregator>" explicitly.
- [ ] **Prices are T1**: spot-check 5 competitor prices — each must resolve to the vendor's own page.
- [ ] **No padding**: spot-check 5 register entries — each must be load-bearing for a number or quote
      in the deck.
```python
import json,re
D=json.load(open('<brand>-data.json'))
urls=set()
# mirror the engine's dedup logic (findings + competitors + painPoints sourceUrl)
def walk(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='sourceUrl' and isinstance(v,str) and v.startswith('http'): urls.add(v)
            else: walk(v)
    elif isinstance(o,list):
        for x in o: walk(x)
walk(D); print('unique URLs:',len(urls))
html=open('<Brand>-Deck.html').read()
entries=re.findall(r'min-width:20px">(\d+)</span>',html)
print('rendered entries:',len(entries),'contiguous:',[int(x) for x in entries]==list(range(1,len(entries)+1)))
```

## C. Visual (render every page, eyeball)
```bash
pdftoppm -png -r 92 <Brand>-Deck.pdf _q   # then Read _q-*.png in batches
```
On each page check:
- [ ] **No overlap** — nothing touches/crosses the footer line; READ/notes sit clear above it.
- [ ] **No mid-word truncation** — every clipped string ends on a word + "…", never "…metal o".
- [ ] **Whitespace <30%** — no page is half-empty; sparse tables stretched (`table.fill`), prose spread.
- [ ] **Notes at uniform bottom** — READ/SO WHAT in the same position across pages.
- [ ] **Images blend** — no white box around cutouts, no drop shadow, caption present.
- [ ] **Cover** — title + subtitle only, hero image, no eyebrow / no date / no KPI band.
- [ ] **Dividers** — sky-blue number, no underline, duotone image seamless (no hard left edge).
- [ ] **No eyebrow labels** anywhere; headlines are full-sentence conclusions.
- [ ] **Numbers tie out** — decision-page totals match; figures consistent page to page; the §0
      pillar numbers equal the verified decision-page numbers exactly.

## C2. Storyline (read, don't render)
- [ ] **Horizontal logic** — read ONLY the action titles, cover to thesis: they must form one
      persuasive essay (SCQA arc), no headline that merely labels a topic, no page that doesn't
      advance the argument.
- [ ] **§0 elevator test** — the Answer page alone sells the recommendation in 30 seconds; governing
      thought is one sentence; every pillar is proven by a later section (vertical logic).

## D. Common defects seen before (check these first)
| Defect | Cause | Fix |
|---|---|---|
| 1–3 pages lost in pager | unclosed `<div>` (note opened `imp` without `</div>`) | balance divs = 0 |
| `&MIDDOT;` literal | `&middot;` passed through `e()` which escapes `&` | use the literal "·" char |
| image is a white box / shadow | not blended / shadow baked in | `mix-blend-mode:multiply`; whiten shadow with ImageMagick `-fuzz 13% -fill white -opaque white` |
| image overflows footer | fixed max-height | `.prodimg{flex:1;min-height:0}` + `img{max-height:100%;object-fit:contain}` |
| text cut mid-word | raw `[:n]` slice | `clipw(s,n)` |
| big void above bottom note | `align-content:start` + short content | `space-evenly` + `flex:1`, or `table.fill` |
| note/READ overlaps footer | content taller than page | trim standfirst to 1 line, tighten row padding, merge duplicate rows (e.g. "25% → 50%") |
| user "sees old layout" | stale browser tab | render PDF to verify; tell user Cmd+Shift+R |

## E. Sign-off
Only present when A+B pass clean, C is all-green, and every defect found is fixed and re-rendered.
Then deliver: `<Brand>-Deck.html` (review on screen) + `<Brand>-Deck.pdf` (share), and note the
hard-refresh.
