---
name: mckinsey-deck
description: >
  Turn any content into a top-tier McKinsey-style deck — a 1280×720 page-turning HTML
  presentation that also prints to a clean per-slide PDF. Use when the user wants a
  "McKinsey-style deck / presentation", a polished slide deck or PDF from notes/content,
  an executive/board/investor deck, or to "make slides / a deck / a PDF report" with a
  premium consulting look. (For full market research with sizing + competitor + business
  case, use mckinsey-market-research-deck instead.)
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# McKinsey-Style Deck (the style + engine skill)

Build a research-grade-looking, page-turning deck from content the user gives you.
Reviewed on screen as an HTML presentation; shared as a print-clean PDF. The whole engine
is one file — `assets/deck_engine.py` — copy it into the project and compose `build()`.

**This skill owns the canonical engine.** `mckinsey-market-research-deck` (and any future
deck skill) consumes `assets/deck_engine.py` from HERE — engine fixes land in this file only,
never in a project-local or sibling-skill fork. One engine, zero drift.

## How to use

1. Copy `assets/deck_engine.py` into the working dir. Set `BRAND` (the footer line) and `OUT_HTML`.
2. Compose the deck inside `build()` using the renderers (below). Feed them the user's content
   directly, or load from a JSON if the content is structured.
3. Render + export:
   ```bash
   python3 deck_engine.py
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
     --no-pdf-header-footer --print-to-pdf="Deck.pdf" "Deck.html"
   ```
   (Windows/Linux: swap the Chrome path for `chrome`/`google-chrome`.)
4. QC (below), fix, re-render, then deliver.

## Renderers (all in deck_engine.py)
- `cover(title_html, subtitle)` — navy hero (uses `product-images/cover-hero.png` if present), title + one subtitle.
- `answer_slide(title, deck, governing, pillars, src)` — the executive-summary page (Pyramid Principle: answer first). One-sentence governing thought + 3–4 pillar conclusions, each optionally with a serif key stat. Place right after the cover; reading only the headlines from here to the end must form one persuasive essay (horizontal logic).
- `divider(no, title, points)` — full-navy section break; big sky-blue number; optional duotone image (`divider-<no>.png`).
- `heroes([(num, label), ...])` — 4-up serif stat strip.
- `prose_slide(title, deck, themes, src, cols=2, note=None)` — "bold theme + paragraph" blocks (the McKinsey prose page). `themes=[(heading, paragraph_html), ...]`.
- `essay_slide(title, deck, lead, paras, src, side=None)` — flowing two-column prose + optional side rail.
- `table_slide(title, deck, columns, rows, src, note=None, fill=True, bold_keys=(), extra=None)` — navy-header table, uniform row heights (header 34px / rows 52px, never stretched); `bold_keys` highlights total rows; `extra=` takes a content block (e.g. `heroes([...])`) to fill a sparse page by composition.
- `decision_slide(page, src)` — renders a structured exhibit (buildup/breakdown/scenarios + assumptions + READ).
- `donut_block(...)`, `bars_chart(...)`, `heatmap_block(...)` — titled chart blocks for a page's side rail (charts ride beside their analysis; never alone on a page); `charts_slide(...)` for the rare full-canvas exhibit. Low-level: `donut_svg(...)`, heatmap `hcell(...)`.
- `sources_register(url_set, selected_rows, src)` — the numbered, clickable source appendix.
- `render(slides)` — assembles the page-turning HTML and prints the div-balance check.

Headline = a full-sentence conclusion (the takeaway), never a topic label.

## Hard design laws (never violate)
- **No eyebrow/kicker labels** — no small letter-spaced ALL-CAPS tags above titles or on the cover.
- **Cover is minimal:** title + one italic subtitle only. No KPI band, no date, no method block.
- **Action-title headlines** — the headline states the conclusion.
- **Notes pinned to a uniform bottom** (`margin-top:auto`) on every page.
- **Nothing overlaps the footer.** `.pad` reserves bottom clearance.
- **Fill by composition, not by stretching.** Essay/prose type auto-scales across 3 tiers by
  content length. **Table row heights are uniform deck-wide (header 34px / rows 52px) and never
  stretch** — fill a sparse table page via `table_slide(..., extra=heroes([...]))` or more rows.
  If a page is still thin at the top tier, add content — never inflate type or rows.
- **No mid-word truncation** — use `clipw()`, never raw `[:n]`.
- **Flat** — no shadows/bevels (navy cover/divider are the only image-shadow exception).
- **Images** — clean cutout on pure white, no shadow, blended via `mix-blend-mode:multiply`; every image gets an italic caption. Cover/divider images: anchored bottom-right, `height:100%` (never >100%, or the PDF clips the subject), left-edge gradient mask so the square dissolves into navy.

## Palette (baked into the engine CSS)
navy `#051C2C` · blue `#1F6FB2` · sky `#5AA9E0` · ink `#23272E` · muted `#7B8593` · hairline `#E3E6EB`.
Headlines Georgia; body Inter. Color is rationed: navy structure + grays, blue/sky as small accents.

## QC before delivery (always self-run)
```bash
# structure — must be 0, or an unclosed div breaks pagination
python3 -c "h=open('Deck.html').read();print('div diff:',h.count('<div')-h.count('</div>'))"
pdfinfo Deck.pdf | grep Pages
# visual — render every page and eyeball
pdftoppm -png -r 92 Deck.pdf _q   # then look at _q-*.png
```
Check each page: no footer overlap · no mid-word "…metal o" cuts · <30% whitespace · notes at a
uniform bottom · images blended with captions · cover has no eyebrow/date. Fix, re-render, re-check.

**Browser caching trap:** `open`-ing an already-open HTML only refocuses the stale tab — verify by
rendering the PDF, and tell the user to hard-refresh (Cmd+Shift+R).

## Make links clickable
If you list URLs (sources/appendix), wrap each in `<a href="<full-url>">…</a>` — Chrome's
`--print-to-pdf` turns them into clickable PDF link annotations (verify: the PDF bytes contain `/URI`).
