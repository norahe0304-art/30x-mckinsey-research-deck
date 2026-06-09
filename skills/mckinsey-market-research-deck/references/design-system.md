# McKinsey Visual Design System (the locked contract)

The deck is 1280×720 slides, flat, editorial. The full working CSS lives in the canonical engine
`../mckinsey-deck/assets/deck_engine.py` (the `CSS` constant) — this file explains the *intent* so
you can extend without breaking it.

## Palette
| Token | Hex | Use |
|---|---|---|
| `--navy` | `#051C2C` | headlines, cover/divider bg, table headers, structure |
| `--blue` | `#1F6FB2` | accent, highlighted numbers, the subject's highlighted series in a comparison bar |
| sky blue | `#5AA9E0` | divider section numbers, inline emphasis on navy |
| `--ink` | `#23272E` | body text |
| `--mute` | `#7B8593` | captions, standfirsts, footnotes |
| `--hair` | `#E3E6EB` | hairline rules / table separators |
| heatmap ramp | `#DCE9F3 → #A9CCE6 → #5E9BCB → #2E6FA8 → #103A5E` | demand/fit heatmap cells |

Flat only — no shadows/bevels (navy cover & divider are the only places a subtle image shadow is OK).
Color is rationed: navy structure + grays, blue/sky as small high-value accents.

## Type
- **Headlines:** Georgia, navy, ~26px, weight 400, tight leading. The headline IS the takeaway
  (a full sentence conclusion).
- **Standfirst/deck:** ~13.5px, muted, one line under the headline.
- **Body:** Inter. Prose 12.5px / line-height 1.8. Table cells 10.5px.
- **Adaptive density (engine-automatic):** `essay_slide` and `prose_slide` measure visible text and
  pick one of 3 type tiers — sparse pages get larger type and looser leading (up to 14.2px/2.05) so
  they fill naturally; dense pages keep the 12.5px default. If a page still sits under ~70% full at
  the top tier, the fix is MORE CONTENT (add a paragraph), never more font.
- **Cover title:** Georgia 46px. **Divider title:** Georgia 40px; section number Georgia 90px sky-blue.

## Page-type catalog (renderers in deck_engine.py)
- `cover()` — navy hero image bg, title + one italic subtitle only. Nothing else.
- `answer_slide(title,deck,governing,pillars,src)` — the §0 executive summary, right after the
  cover. Governing thought in serif behind a blue left-rule; 3–4 pillars under thin navy top-rules,
  each = serif key stat (blue) + bold mini-conclusion + one support line. White page, flat; the only
  page allowed to preview later sections' numbers (they must match the verified ones exactly).
- `divider(no,title,points)` — full navy, big sky-blue number, title, point list; optional duotone
  image anchored bottom-right with a left-fade mask (no hard seam).
- hero stat strip `heroes([(num,label)...])` — 4-up serif numbers with hairline dividers.
- `prose_slide(...)` — "bold theme + flowing paragraph" blocks in a grid, `space-evenly` to fill.
- `essay_slide(...)` — flowing two-column prose + a side rail (donut + stat tiles + SO WHAT).
- table slides — navy header row, hairline separators, first column bold navy. **Row heights are
  sacred and uniform deck-wide: header 34px, data rows 52px, never stretched.** A sparse table does
  not balloon to fill the page — the page is filled by composition: pass `extra=` (a `heroes()`
  stat strip, a widened READ) to `table_slide`. Tables answer for truth, not for layout.
- heatmap table — cells colored by the ramp to show intensity (e.g. demand pull by tier).
- charts — `donut_block(segs,top,bot,legend,title=)` + `bars_chart([(x,value,label)...],title=)` +
  `heatmap_block([corner,col…],[(row,[v…])…],title=)` (v ∈ Low/Med/High/Win/—); flat, no gridlines,
  navy→light-blue ramp. **Chart titles are always centered** above the chart (pass `title=`; the
  engine centers it — never hand-place a left-aligned `.ct` over a chart). **Default placement:
  embedded in a content page's right rail** via `essay_slide(..., side=...)` — charts ride *beside*
  the prose that reads them, never alone on a page. **A deck carries ≥4 charts that each earn their
  place** (a real finding, not filler). `charts_slide(...)` exists only for the rare full-page
  exhibit; do not reach for it just to show a chart.
- `decision_slide(page)` — renders a verified decision page (buildup/breakdown/scenarios table +
  key-assumptions 2-col + READ note). Bolds the answer rows the exhibit declares (`exhibit.boldKeys`);
  defaults to universal totals only (TAM/SAM/SOM/TOTAL/PAYBACK) — no category finance term is baked in.
- sources register — selected-notes table (use `table.fill`) + paginated full URL list (numbered).

## Layout laws (these are the ones that bite)
1. **`.pad` reserves bottom clearance** (`padding:40px 50px 48px`) so content never hits the footer.
2. **Footer is absolute** at the bottom; **notes/READ use `margin-top:auto`** → identical bottom
   position on every page.
3. **Fill by composition, not by stretching.** Sparse prose → `space-evenly`; sparse tables →
   `extra=` content (heroes stat strip / widened READ) or more rows from deeper research. Stretching
   an element to hide thin content is cheating; >30% whitespace means the page needs more CONTENT.
4. **No mid-word truncation** — `clipw(s,n)` cuts at a word boundary and adds "…" only if shortened.
5. **Images:** `.prodimg img{object-fit:contain;mix-blend-mode:multiply}` blends a white-bg cutout
   invisibly onto the white slide. Every image gets a `.cap` italic caption.
6. **Cover/divider images** are set via an absolutely-positioned `<img>` with a left-edge gradient
   mask (`mask-image:linear-gradient(to right,transparent,#000 42%)`) so the square image dissolves
   into the navy with no visible seam.
7. **Div balance:** after every build, `html.count('<div') - html.count('</div>')` must be 0.

## The pager (screen vs print)
- One HTML file does both. `@media screen` shows one `.on` slide centered & scaled (`--s` transform),
  with keyboard (←/→/space/Home/End), click-left/right halves, and a page counter.
- `@media print` restores all slides as a normal 1280×720 page-per-slide flow for the PDF.
- Render PDF with headless Chrome `--no-pdf-header-footer --print-to-pdf`.
- **Browser caching trap:** `open`-ing an already-open file only refocuses the stale tab. Always
  verify by rendering the PDF page, and tell the user to hard-refresh (Cmd+Shift+R).

## Anti-patterns the user explicitly rejects
- Eyebrow/kicker small-caps labels (anywhere, including the cover).
- Decorative vertical lines / over-engineered "AI-looking" cards.
- Gimmicky stacked-bar/stat cards that add no information.
- Terse bullet points where the reference uses prose paragraphs.
- Cover metadata clutter (KPI band, method/evidence, "Prepared <date>").
- Forced large gaps (space-between) — prefer even rhythm or genuine fill.
- **Standalone chart pages** — a donut/bar alone on its own slide. Charts belong in the side rail of
  the content page that interprets them, not isolated from their analysis.
