# Plan — Rebuild "Where Strategy Meets AI" around deck content

**Date:** 2026-05-20
**Scope:** [index.html:209-307](../../index.html#L209-L307) — the `.platform` band inside `.path-merged`

## Goal

Today the section is a single hand-coded growth-opportunities table mock + 4 accordion blurbs. Rebuild it so each of the 4 pillars is backed by **multiple** visual artifacts pulled from real (already-redacted) client decks:

1. **Opportunity Identification** — value chain mapping (BB Logistics), whitespace matrices, sized plays
2. **Pricing Engine** — segmentation, price-volume curves, leak quantification, quote-level recommendations
3. **Demand Forecasting** — accuracy baselining, segment-specific models, S&OP integration
4. **Geospatial Mapping** — market study logistics, demand heatmaps, trade-area whitespace

## Design decisions (locked)

- **Source delivery:** user pastes slides as images in chat, one pillar at a time.
- **Structure:** tab nav (4 pillars) + horizontal carousel of slides per active pillar.
- **Render approach:** native HTML/CSS rebuild for charts/tables/matrices; images only for things genuinely hard to recreate (maps, schematics, photo-realistic visuals). Target ~70/30 native/image.
- **Confidentiality:** decks are pre-sanitized; use as-is. Still flag anything that looks like a real client identifier when rebuilding.
- **No build step:** stay consistent with the rest of the site — vanilla HTML, SCSS-free CSS in `styles.css`, inline `<script>` at bottom of `index.html`.

## New DOM structure

Replace the existing `.product-grid` (lines 214-305) with:

```
.platform
  h3.platform-h3 "Where Strategy Meets AI"
  p.platform-lead
  .pillar-deck
    .pillar-tabs[role=tablist]
      button.pillar-tab.is-active (Opportunity Identification)
      button.pillar-tab (Pricing Engine)
      button.pillar-tab (Demand Forecasting)
      button.pillar-tab (Geospatial Mapping)
    .pillar-panels
      .pillar-panel.is-active[data-pillar=opportunity]
        .carousel
          button.carousel-prev
          .carousel-track
            .carousel-slide
              .slide-visual (native HTML or <img>)
              .slide-caption
                .slide-title
                .slide-insight
            .carousel-slide ...
          button.carousel-next
          .carousel-dots
      .pillar-panel[data-pillar=pricing] ...
      .pillar-panel[data-pillar=forecasting] ...
      .pillar-panel[data-pillar=geospatial] ...
```

- Each carousel slide is self-contained HTML — easy to add/remove/reorder as user pastes more material.
- `data-pillar` attributes drive the tab↔panel association.

## JS behavior (extend existing inline `<script>`)

Follows the same pattern as the existing capability accordion at the bottom of [index.html](../../index.html):

1. **Tab switching:** click pillar tab → toggle `is-active` on tab + matching `.pillar-panel`. ARIA: `aria-selected`, `aria-controls`, `role=tab`/`role=tabpanel`.
2. **Carousel per panel:** prev/next buttons step through slides via `transform: translateX()` on `.carousel-track`. Dot indicators reflect current index.
3. **Keyboard:** left/right arrows when focus is on tab → switch pillar; left/right on carousel area → step slides.
4. **Touch/swipe (optional, defer if scope tightens):** basic touch handler for mobile.
5. **Reset on tab switch:** when switching pillars, reset that panel's carousel to index 0 (or keep last index — decide during build).

## CSS (`styles.css`)

Add a new section after the existing `.capability-list` styles (~line 380):

- `.pillar-deck` — outer container, dark band styling matching `.platform`
- `.pillar-tabs` — flex row, underline-on-active indicator (mirror the existing `.product-mock .bar .tab.active` underline treatment for consistency)
- `.carousel` — relative positioned, overflow hidden, arrow buttons absolutely positioned
- `.carousel-track` — flex row, `transition: transform 300ms ease`
- `.carousel-slide` — `flex: 0 0 100%`, padding, two-column on desktop (visual left / caption right), stacked on mobile
- `.slide-visual` — light-on-dark chart container; sub-styles for each visual type (matrix, bars, curves, map)
- `.slide-caption .slide-title` — uses existing Playfair Display heading style
- `.slide-caption .slide-insight` — body sans, accent number callouts
- Dots: small circles, `.is-active` filled
- Responsive: <768px → carousel slides stack visual above caption; tabs become horizontally scrollable

## Execution checklist

- [ ] **1. Skeleton** — replace `.product-grid` with `.pillar-deck` shell; 4 empty panels with placeholder "slides will go here" text. Tab switching works end-to-end. JS + CSS in place.
- [ ] **2. Carousel mechanics** — prev/next + dots working on placeholder slides (3 dummy slides per panel). Verify keyboard + responsive.
- [ ] **3. Slide content — iteration loop** (one pass per pillar):
  - User pastes slide image(s) in chat
  - I propose: rebuild as native HTML/CSS OR embed as `<img>` with a brief justification
  - I draft the slide block (visual + 1-sentence title + 1-2 sentence insight)
  - User approves / edits
  - Commit slide to the right panel
  - Repeat until pillar has its full set
- [ ] **4. Polish pass** — typography rhythm, spacing, hover/focus states, motion (fade between tabs?), check all responsive breakpoints
- [ ] **5. Verify** — open in browser, click through every pillar + every slide, keyboard nav, mobile viewport, check tests/site_check.py if relevant
- [ ] **6. Cleanup** — remove the old `.product-mock` table and `.capability-list` from index.html; remove their orphaned CSS from styles.css

## Open questions to resolve as we go

- **Slide count per pillar:** suggest aiming for 3-5 per pillar. Fewer = thin; more = carousel fatigue. Will recalibrate after seeing source material.
- **Where does the rebuilt growth-opportunities table go?** It's a strong visual that currently lives at the top of `.product-grid`. Option A: retire it (the pillar carousel replaces it). Option B: keep it as the first slide of "Opportunity Identification." Lean B unless the deck has something stronger.
- **Animation between tabs:** simple opacity crossfade vs hard cut. Decide in polish pass.
- **Deep linking:** should `#pricing` open the Pricing tab? Probably nice-to-have, not critical.

## Out of scope

- Changing the surrounding `.path-merged` section (funnel, pillars, partner cards).
- Reworking the navbar's "Platform" anchor target.
- New imagery for sections outside `.platform`.

## Notes on source material handling

- Each slide image you paste, I'll: (a) describe what I see, (b) propose native rebuild vs image embed, (c) draft the slide HTML, (d) show you the result.
- If a deck has a narrative arc (e.g., BB Logistics value chain → whitespace → sized plays), preserve that order in the carousel so the slides build on each other.
- Keep the slide *insight text* short — one punchy sentence per slide. The visual carries the weight, not the prose.
