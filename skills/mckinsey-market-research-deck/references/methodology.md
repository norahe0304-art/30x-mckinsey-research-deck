# Research Methodology

How to do the research and what each section must contain. Every number gets a `sourceUrl`.

**Category-agnostic by design.** The spine, the decision pages, and the visual system are universal.
Only the *buildup arithmetic and the vocabulary* change with the subject. Three archetypes recur —
pick the one that fits and read its pattern where a section forks:

- **Physical goods** — priced SKUs, shelf prices, materials, landed cost, margin (e.g. kitchen tools).
- **Software / SaaS** — plans/tiers, ACV or ARPU, CAC, payback, gross margin on usage.
- **OSS / service / methodology-as-product** — free or open core, adoption funnel, conversion to a
  paid/managed surface, value-per-user instead of unit margin.

Never let one archetype's words leak into another's deck (no "shelf price" on a SaaS page, no "COGS"
on an open-source page). The skeleton is shared; the nouns are not.

## The source bar (quality first, then density)

Source count is a function of category evidence density (a goods deck cites one URL per shelf price
and lands at 150+; a software deck cites one pricing page per vendor and lands far lower) — so the
bar is rules, not a vanity number.

**Tier every source** (mentally, while researching):
- **T1 primary** — the subject itself: vendor pricing/docs pages, GitHub repo metrics, SEC filings,
  official proclamations/blogs (github.blog, devin.ai/pricing), the brand's own shelf listing.
- **T2 named research** — Gartner, McKinsey, government statistics, peer-reviewed/arXiv, named
  industry bodies; trade press reporting its OWN reporting (VentureBeat, InfoQ).
- **T3 practitioner** — named-author engineering blogs, HN/Reddit threads (as *pain evidence*,
  quoted verbatim with the venue named).
- **T4 aggregator** — SEO stat-roundup blogs, "X statistics 2026" pages, tool directories.

**Hard rules:**
1. **Prices and product facts: T1 only.** A competitor's price cited from anything but the vendor's
   own page (or a dated archive of it) is a defect. Capture date mandatory.
2. **Market size and adoption claims: T2 or better.** A T4 aggregator may appear only *alongside*
   the original study it aggregates, never as the sole support. If the original cannot be found,
   say "via <aggregator>" in the source line — visible honesty beats hidden weakness.
3. **Pain points: T3 minimum, verbatim.** A pain with no quotable human behind it gets cut.
4. **Load-bearing decision inputs** (the conversion rate, the penetration %, the velocity) need
   **two independent sources or an explicit "judgment call" label** — never one URL pretending
   to be enough.
5. **Density floor: ≥1.5 unique URLs per content page** (cover/dividers/thesis excluded), and
   **≥50% of the register at T1+T2**. Below the floor means the research is thin — go deeper or
   cut pages; never pad with URLs nothing in the deck actually uses (every register entry must be
   load-bearing for at least one number or quote).

## The single data file

Land all research in `<brand>-data.json`. The schema **adapts to the archetype** — keep `sourceUrl`
everywhere; rename the category-specific fields. Below is the physical-goods example; the neutral
field in brackets is what a software/service deck uses instead.

```jsonc
{
  "market": [                       // top-level market findings, one block per theme
    { "theme": "Market size",
      "findings": [ { "text": "...", "value": "$8.96B", "sourceUrl": "https://..." } ] }
  ],
  "subResults": [                   // one per subcategory / product line / module (aim 8–10, MECE:
                                    // no SKU/plan fits two subcategories, none fits zero — the
                                    // subcategory list must partition the whole category)
    { "subcategory": "Cooking Utensils",
      "competitors": [ { "brand": "OXO", "offer": "...",   // [offer] = product | plan | tool
                         "price": "$13.95",                // [price] = price | tier | "free / OSS"
                         "sourceUrl": "..." } ],
      "painPoints": [ { "issue": "Nylon heads melt", "evidence": "ATK: '...'", "sourceUrl": "..." } ] }
  ],
  "positioning": {
    "tier": "Better",                                      // Good | Better | Best — any category
    "anchors": [ { "position": "Budget floor (below X)",   // [anchors] = priceAnchors | tierAnchors
                   "benchmark": "Room Essentials 30pc set",
                   "value": "$20.00",                      // [value] = price | tier | cost-to-adopt
                   "heroVs": "our 10pc set is $30 vs ...", "sourceUrl": "..." } ]
  },
  "line": [                         // [line] = finalSkus | plans | modules — the recommendation
    { "name": "...", "tier": "Good|Better|Best",
      "spec": "...",                                       // [spec] = material | stack | capability
      "anchor": "$7.00",                                   // [anchor] = suggestedRetail | price | "free"
      "subcategory": "...", "keyFeatures": ["..."],
      "painPointAddressed": "...", "benchmark": "..." }     // [benchmark] = competitor it beats
  ]
}
```

## Section content requirements

Each section: the **universal requirement** first, then how it forks by archetype.

**0. The Answer (executive summary)** — one `answer_slide()` immediately after the cover.
- **Governing thought**: the full recommendation in ONE sentence — what to do, at what scale, why
  it wins (e.g. "Launch a 44-SKU design-led Better line: the $X market has no design-forward player
  between the budget floor and premium, and the economics clear a Y% margin bar").
- **3–4 pillars**, each a mini action-title + one supporting line + the key number. The pillars ARE
  the deck's sections in miniature (market shift / competitive gap / economics / the line) — vertical
  logic: every pillar is proven by a later section; nothing appears here that the deck doesn't prove.
- Built as SCQA compressed: situation+complication live in the governing thought's "because" clause,
  the answer is the imperative. Drafted in Phase 1.5 from the Day-1 hypothesis, **rewritten last**
  after the decision pages verify — the numbers on this page must match the verified ones exactly.
- Must pass the **elevator test**: a partner reading only this page can decide.

**1. Market Overview** — size today → forecast + CAGR, the structural shift that reframes the category,
a maturity signal, and a demand split. Headline = the shift ("design and online now drive growth" /
"foundation models reset GTM every six months"), not "market overview".
- *Physical*: channel split & faster-growing channel, household penetration, private-label share.
- *Software/SaaS*: segment split, adoption/penetration of the new motion, build-vs-buy share.
- *OSS/service*: formation rate of the buyer population, the channel shift (e.g. agent-native), the
  gap incumbents leave open.
Exhibit: one donut (segment/mix) + one bar (size trajectory) + a Good/Better/Best demand heatmap.
Charts are required here, not optional; never ship a market overview as text only. **Default: embed
the donut/bar in the analysis page's right rail** via `essay_slide(..., side=donut_block(...) +
bars_chart(...))` — the chart rides *beside* the prose that interprets it, never on a page of its own.
Reserve a full-page `charts_slide(...)` for the rare exhibit that genuinely needs the whole canvas.

**Charts budget: ≥4 across the deck, each load-bearing.** A finished deck carries at least four charts
(mix donut / bar / heatmap), each earning its place with a real finding — e.g. §1 a resourcing-mix
donut + a trajectory bar, §2 a Good/Better/Best × forces heatmap, §3–4 a price/exposure bar. Pass
`title=` to every chart (the engine centers it). Charts that only decorate get cut, not counted.

**2. Brand / Offer Landscape** — Good/Better/Best table (tiers × players × band × position) + a
comparison bar on a shared axis so the premium/gap reads visually + a player-by-player profile table
(name / tier / one-line brief / one-line position), subject highlighted.
- *Physical*: band = price band. *Software*: band = plan price / ACV. *OSS*: band = cost-and-openness
  (free templates → open scaffold → paid managed).

**3. Product Categories / Modules** — one page per subcategory/line/module: left = the competitor
ladder (sorted low→high on the category's axis) + top sourced pain points; right = the subject's
lineup table + a clean image with caption. Headline names the gap the subject wins.
- *Physical*: ladder = price ladder (shelf prices); lineup = SKU / tier / MSRP.
- *Software*: ladder = plan/tier ladder; lineup = plan / tier / price.
- *OSS/service*: ladder = cost-and-openness ladder; lineup = module / tier / what-it-ships.

**4. Customer Pain Points** — dense tables, grouped by subcategory, "what customers report, in their
words" with sourced evidence. Each page ends with a SO WHAT linking failures → the subject's fixes.
Universal across archetypes (the only thing that changes is the source: reviews/ATK for goods,
forums/churn-reasons/changelogs for software).

**5. Opportunities** — 3–4 numbered moves, each: the pain it answers (italic) + the fix + a "why it
wins" defensibility line. Sequence by defensibility. Universal.

**6. The Solution** — positioning (the lane it owns, with hero stats), the line plan, **the three
decision pages**, the thesis (full-navy single statement), then the source register.
- *Physical*: pricing anchored to real shelf prices, colorway/design grid, SKU allocation table.
- *Software*: tier design anchored to competitor ACV, the plan ladder, packaging table.
- *OSS/service*: the adoption order of modules, open-core boundary, what accrues value.

## Decision pages (the senior differentiator)

Most market research stops at "market + competition + consumer". Three pages turn it into a deck a
partner can act on. Build each as a **checkable-arithmetic exhibit**. The *questions* are universal;
the *buildup* is per-archetype. Set `exhibit.boldKeys` to mark the answer rows (the engine bolds only
universal totals by default — TAM/SAM/SOM/TOTAL/PAYBACK).

**Decision 1 · Bottom-up market sizing (TAM/SAM/SOM)** — never borrow a top-down number as the answer.
Build it from a multiplication chain, then reconcile to the top-down figure as a *consistency check*.
State the load-bearing judgment call honestly. Exhibit = a "buildup" table, one row per step.
- *Physical*: households × penetration × annual spend on THIS subcategory → TAM; × tier share → SAM;
  × channel share × in-store capture → SOM.
- *Software/SaaS*: target accounts × adoption rate × ACV → TAM; × segment-we-serve → SAM; × realistic
  win rate × ramp → SOM.
- *OSS/service*: addressable user/org population × activation rate → reachable base; × conversion to
  the paid/managed surface × price → revenue SOM. (Adoption, not units.)

**Decision 2 · Economics** — *validate*, don't assume, the value/margin claim. The result row is the
"answer"; declare it in `boldKeys`.
- *Physical*: landed-cost stack — materials, tooling amortization, labor/overhead, freight, duties
  (model the load-bearing one, e.g. tariff on metal content only) → landed COGS → gross margin.
  `boldKeys:["LANDED COGS","GROSS MARGIN"]`.
- *Software/SaaS*: CAC by channel + payback + gross margin on usage cost (inference/compute) → unit
  contribution. `boldKeys:["CAC","PAYBACK","GROSS MARGIN"]`.
- *OSS/service*: adoption → conversion → value-per-converted-user (or cost-to-serve for managed) →
  contribution per logo. `boldKeys:["NET VALUE","CONTRIBUTION"]`.

**Decision 3 · Business case** — investment + 3-scenario revenue (conservative/base/optimistic) ×
validated economics → return → payback. Sanity-check base revenue against the SOM (should roughly
agree; flag that it agrees "by construction", not independently). Verdict = go/no-go + the condition.
- *Physical*: investment = per-SKU tooling × N + initial inventory + launch; revenue = units/SKU/door
  velocity. *Software/OSS*: investment = build + GTM; revenue = logos × ACV (or converted users ×
  price) by scenario.
- **Competitive-response stress test (mandatory)**: McKinsey's own market-entry research finds ~60%
  of failed entries underestimated the competition. The conservative scenario must price in the
  incumbents' most likely counter (price cut / fast-follow / shelf-space defense / bundling), named
  explicitly in the assumptions — never model competitors as static.

### Verify pattern (Workflow)
Run a `pipeline` over the 3 pages: stage 1 an analyst agent emits the page as structured JSON (force a
schema); stage 2 an **adversarial verifier** (skeptical EM) re-derives every number, checks no
double-counting, the load-bearing assumption, conclusion-follows-from-table, and returns the corrected
page. Be tough on rosy numbers (margin, win rate, velocity, payback, conversion). Persist each verified
page as `_decision_<id>.json`. CRITICAL prompt line for both stages: *"your final answer MUST be a
single StructuredOutput tool call"* — agents otherwise ramble and skip it. Keep schemas flat-ish;
deeply nested schemas fail more often. If a verify agent fails to emit structured output, rerun just
that item with a firmer instruction.

## Honesty rules
- Label every assumption; surface the load-bearing one explicitly.
- Reconcile, don't average, conflicting market scopes (averaging inflates a niche).
- If a claim only holds under a condition (a tariff regime, a model-price floor, a conversion rate),
  say so in the takeaway.
- Quote the *defensible* number to the client, not the rosiest.
