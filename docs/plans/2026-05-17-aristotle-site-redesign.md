# Aristotle Site Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restructure `index.html` and add `team.html` to match the executive credibility and section rhythm of eilla.ai, while preserving Aristotle's distinct Playfair/navy identity.

**Architecture:** Single-page static site at the repo root. Extract shared CSS into `styles.css` so the new `team.html` and the redesigned `index.html` stay in visual sync. Sections re-ordered to lead with proof (stat strip, employer logos) before narrative, then merge old "Our Offerings" into a new tabbed "Path to Compounding Growth" interaction. New sections: Insights placeholder, Q&A accordion, Decades-of-Expertise credibility block. Removed from homepage: dual hero CTA, hero badge, gradient text, counter animation, spinning flywheel rings, emoji icons, standalone Team section.

**Tech Stack:** Static HTML5 + vanilla CSS + vanilla JS. No build step. Fonts via Google Fonts (Playfair Display + Inter, already loaded). Inline SVG icons (no icon library).

**Reference:** `https://eilla.ai/` — match section rhythm and proof-first structure; do not copy copy verbatim. Aristotle keeps Playfair Display + navy palette.

**Verification model:** No automated tests. Each task ends with a manual browser check (open `index.html` in Chrome at desktop 1440px and mobile 375px). The task is complete only after the section renders correctly at both widths AND all links resolve to either a real anchor or `https://calendly.com/sam-aristotle/30min`.

**Working directory:** `/Users/rachit/Documents/ragarwal.io/`

---

## Section ordering (final)

After all tasks complete, `index.html` reads top-to-bottom as:

1. Nav (Approach · Why Us · Path to Growth · Insights · Team · Book a Meeting)
2. Hero (headline + single CTA + stat strip + Chicago video placeholder)
3. Backed by experience at (logo strip)
4. Value prop + horizontal 4-step process bar (replaces flywheel)
5. Path to Compounding Growth (tabbed: 4 tools → service mapping)
6. How We Are Different (comparison table, restyled)
7. Decades of Expertise (3 big stats + logos + sectors)
8. Case Studies (restyled, hairline dividers)
9. Insights (placeholder)
10. Q&A (accordion)
11. Final CTA (single Book a Meeting)
12. Footer (real links)

`team.html` is a single page: nav · page title · 3 rich cards (photo / name / role / bio / LinkedIn) · footer.

---

## Conventions used in this plan

- **No emojis anywhere in committed code.** All decorative icons are inline SVG.
- **No code comments** unless a non-obvious invariant requires one.
- **All CTAs say `Book a Meeting`** and point to `https://calendly.com/sam-aristotle/30min`.
- **TODO markers** use `<!-- TODO(content): … -->` so they're greppable.
- **Commit style** matches the repo's existing history (terse imperative, no scope prefix).
- **Co-author trailer** on every commit: `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`

---

## Task 1: Extract shared CSS into `styles.css`

**Files:**
- Create: `styles.css`
- Modify: `index.html` (replace `<style>…</style>` block with `<link rel="stylesheet" href="styles.css">`)

**Step 1: Copy CSS out**

Open `index.html`. Cut the entire contents between `<style>` (line 8) and `</style>` (line 895) — everything from `@import url(...)` through the last `}`. Paste into a new file `styles.css` at the repo root.

**Step 2: Replace the `<style>` block with a link**

In `index.html`, replace lines 8–895 (the `<style>…</style>` block) with:

```html
<link rel="stylesheet" href="styles.css">
```

**Step 3: Verify in browser**

Open `index.html` in Chrome. The page must look pixel-identical to before. If anything looks unstyled, the cut was off by one line.

**Step 4: Commit**

```bash
git add styles.css index.html
git commit -m "$(cat <<'EOF'
Extract inline CSS into styles.css

Prep for team.html sharing the same stylesheet.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Create `team.html` scaffold

**Files:**
- Create: `team.html`
- Modify: `styles.css` (append team-page styles)

**Step 1: Create `team.html`**

Write a new file `team.html` with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="images/favicon.png">
<title>Team — Aristotle</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>

<nav id="navbar">
  <a href="index.html" class="nav-logo">Aristotle</a>
  <ul class="nav-links">
    <li><a href="index.html#value">Approach</a></li>
    <li><a href="index.html#different">Why Us</a></li>
    <li><a href="index.html#path">Path to Growth</a></li>
    <li><a href="index.html#insights">Insights</a></li>
    <li><a href="team.html" class="nav-active">Team</a></li>
    <li><a href="https://calendly.com/sam-aristotle/30min" target="_blank" class="nav-cta">Book a Meeting</a></li>
  </ul>
</nav>

<section class="team-page">
  <div class="team-page-header">
    <div class="section-label">Leadership</div>
    <h1 class="team-page-title">The people behind Aristotle</h1>
    <p class="team-page-sub">Decades of strategy and engineering experience, applied to a single question: how do you make consulting compound?</p>
  </div>

  <div class="team-page-grid">
    <article class="team-bio-card">
      <div class="team-bio-photo"><img src="images/sam.jpeg" alt="Sam Garg"></div>
      <h2>Sam Garg</h2>
      <div class="team-bio-role">Founder</div>
      <p class="team-bio-text"><!-- TODO(content): Sam bio paragraph --></p>
      <a href="#" class="team-bio-linkedin" aria-label="Sam on LinkedIn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.86-3.04-1.86 0-2.15 1.45-2.15 2.95v5.66H9.34V9h3.41v1.56h.05c.48-.9 1.64-1.86 3.37-1.86 3.6 0 4.27 2.37 4.27 5.46v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.8 0 0 .77 0 1.72v20.56C0 23.23.8 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>
      </a>
      <!-- TODO(content): Sam LinkedIn URL in href above -->
    </article>

    <article class="team-bio-card">
      <div class="team-bio-photo"><img src="images/bia.jpeg" alt="Beatriz Abramof"></div>
      <h2>Beatriz Abramof</h2>
      <div class="team-bio-role">Chief of Staff</div>
      <p class="team-bio-text"><!-- TODO(content): Bea bio paragraph --></p>
      <a href="#" class="team-bio-linkedin" aria-label="Beatriz on LinkedIn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.86-3.04-1.86 0-2.15 1.45-2.15 2.95v5.66H9.34V9h3.41v1.56h.05c.48-.9 1.64-1.86 3.37-1.86 3.6 0 4.27 2.37 4.27 5.46v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.8 0 0 .77 0 1.72v20.56C0 23.23.8 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>
      </a>
      <!-- TODO(content): Bea LinkedIn URL in href above -->
    </article>

    <article class="team-bio-card">
      <div class="team-bio-photo"><img src="images/rachit.jpeg" alt="Rachit Agarwal"></div>
      <h2>Rachit Agarwal</h2>
      <div class="team-bio-role">Founding Engineer</div>
      <p class="team-bio-text"><!-- TODO(content): Rachit bio paragraph --></p>
      <a href="#" class="team-bio-linkedin" aria-label="Rachit on LinkedIn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.86-3.04-1.86 0-2.15 1.45-2.15 2.95v5.66H9.34V9h3.41v1.56h.05c.48-.9 1.64-1.86 3.37-1.86 3.6 0 4.27 2.37 4.27 5.46v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.8 0 0 .77 0 1.72v20.56C0 23.23.8 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>
      </a>
      <!-- TODO(content): Rachit LinkedIn URL in href above -->
    </article>
  </div>
</section>

<footer>
  <div class="footer-logo">Aristotle</div>
  <div class="footer-text">&copy; 2026 Aristotle. All rights reserved.</div>
  <ul class="footer-links">
    <li><a href="index.html">Home</a></li>
    <li><a href="https://calendly.com/sam-aristotle/30min" target="_blank">Book a Meeting</a></li>
  </ul>
</footer>

<script>
const nav = document.getElementById('navbar');
window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 60));
</script>

</body>
</html>
```

**Step 2: Append team-page styles to `styles.css`**

Append to the end of `styles.css`:

```css
/* ─── TEAM PAGE ─── */
.nav-active { color: var(--white) !important; }

.team-page {
  padding: 160px 60px 120px;
  max-width: 1100px;
  margin: 0 auto;
}

.team-page-header {
  text-align: center;
  margin-bottom: 96px;
}

.team-page-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(40px, 5vw, 64px);
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin: 16px 0 24px;
}

.team-page-sub {
  font-size: 18px;
  color: var(--gray-300);
  max-width: 620px;
  margin: 0 auto;
  line-height: 1.6;
  font-weight: 300;
}

.team-page-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 48px;
}

.team-bio-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 40px 32px;
  text-align: center;
}

.team-bio-photo {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 28px;
  border: 1px solid rgba(65, 105, 225, 0.2);
}

.team-bio-photo img { width: 100%; height: 100%; object-fit: cover; display: block; }

.team-bio-card h2 {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  margin-bottom: 6px;
}

.team-bio-role {
  font-size: 14px;
  color: var(--blue-bright);
  letter-spacing: 0.04em;
  margin-bottom: 20px;
}

.team-bio-text {
  font-size: 14px;
  color: var(--gray-300);
  line-height: 1.7;
  margin-bottom: 24px;
  min-height: 84px;
}

.team-bio-linkedin {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(255,255,255,0.04);
  color: var(--gray-300);
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}

.team-bio-linkedin:hover { background: rgba(65, 105, 225, 0.15); color: var(--blue-bright); }

@media (max-width: 1024px) {
  .team-page-grid { grid-template-columns: 1fr; gap: 32px; max-width: 480px; margin: 0 auto; }
  .team-page { padding: 140px 24px 80px; }
}
```

**Step 3: Verify in browser**

Open `team.html` in Chrome. Page should show three placeholder cards with photos. Nav should have "Team" highlighted. Logo click goes back to `index.html`.

**Step 4: Commit**

```bash
git add team.html styles.css
git commit -m "$(cat <<'EOF'
Add team.html scaffold with placeholder bios

Bios and LinkedIn URLs left as TODOs.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Update homepage nav (Insights/Team links, unified CTA copy)

**Files:**
- Modify: `index.html` (the `<ul class="nav-links">` block)

**Step 1: Replace the nav links list**

Find the `<ul class="nav-links">` block. Replace it entirely with:

```html
<ul class="nav-links">
  <li><a href="#value">Approach</a></li>
  <li><a href="#different">Why Us</a></li>
  <li><a href="#path">Path to Growth</a></li>
  <li><a href="#insights">Insights</a></li>
  <li><a href="team.html">Team</a></li>
  <li><a href="https://calendly.com/sam-aristotle/30min" target="_blank" class="nav-cta">Book a Meeting</a></li>
</ul>
```

Note: `#path` and `#insights` will 404-scroll until Tasks 6 and 11 land. That's fine — leaves the nav anchored to its final IDs.

**Step 2: Verify in browser**

Open `index.html`. Nav should show the new link set. Clicking "Team" navigates to `team.html`. "Book a Meeting" opens Calendly in a new tab. Old "Offerings", "Case Studies" anchors are gone from nav (the sections still exist; they're just no longer in nav).

**Step 3: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Update nav: add Insights and Team, unify CTA copy

Team links to team.html. Insights anchor resolves once Task 11 adds the section.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Hero refactor (drop badge, gradient, tagline, dual CTA; add stat strip + media slot)

**Files:**
- Modify: `index.html` (the `<section class="hero">` block)
- Modify: `styles.css` (hero rules + new stat-strip + media-slot rules)

**Step 1: Replace the hero section markup**

Find `<section class="hero" id="hero">` and replace the entire section through its closing `</section>` with:

```html
<section class="hero" id="hero">
  <div class="hero-inner">
    <h1>Consulting that builds <span class="accent">capabilities.</span><br>Not dependencies.</h1>
    <p class="hero-sub">MBB-grade insight, embedded in your team — so the capability stays after we leave.</p>
    <div class="hero-ctas">
      <a href="https://calendly.com/sam-aristotle/30min" target="_blank" class="btn-primary">Book a Meeting <span aria-hidden="true">→</span></a>
    </div>
  </div>

  <div class="hero-media">
    <!-- TODO(media): Drop Chicago video into images/hero-chicago.mp4 and uncomment below.
    <video autoplay muted loop playsinline poster="images/hero-chicago-poster.jpg">
      <source src="images/hero-chicago.mp4" type="video/mp4">
    </video>
    -->
    <div class="hero-media-placeholder">Chicago — hero media slot</div>
  </div>

  <div class="hero-strip">
    <div class="hero-strip-item">
      <div class="hero-strip-stat">25%</div>
      <div class="hero-strip-label">Higher value captured vs. status quo</div>
    </div>
    <div class="hero-strip-item">
      <div class="hero-strip-stat">&lt;6 wks</div>
      <div class="hero-strip-label">From kickoff to first results</div>
    </div>
    <div class="hero-strip-item">
      <div class="hero-strip-stat">$2B+</div>
      <div class="hero-strip-label">Growth opportunities identified to date</div>
    </div>
    <div class="hero-strip-item">
      <div class="hero-strip-stat">Tied to impact</div>
      <div class="hero-strip-label">No seven-figure fixed fees</div>
    </div>
  </div>
</section>
```

**Step 2: Update hero styles**

In `styles.css`, find the `/* ─── HERO ─── */` block. Replace everything from `.hero {` through (and including) the `.scroll-indicator`/`@keyframes scrollPulse` rules with:

```css
/* ─── HERO ─── */
.hero {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 140px 60px 0;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: -40%;
  left: 50%;
  transform: translateX(-50%);
  width: 900px;
  height: 900px;
  background: radial-gradient(circle, rgba(40, 81, 164, 0.12) 0%, transparent 70%);
  pointer-events: none;
}

.hero-inner {
  max-width: 900px;
  position: relative;
}

.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(48px, 6.5vw, 88px);
  font-weight: 600;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin-bottom: 28px;
  animation: fadeUp 0.8s ease-out 0.2s both;
}

.hero h1 .accent { color: var(--blue-light); }

.hero-sub {
  font-size: 20px;
  font-weight: 300;
  color: var(--gray-300);
  max-width: 620px;
  margin: 0 auto 40px;
  line-height: 1.6;
  animation: fadeUp 0.8s ease-out 0.4s both;
}

.hero-ctas {
  display: flex;
  justify-content: center;
  margin-bottom: 64px;
  animation: fadeUp 0.8s ease-out 0.6s both;
}

.hero-media {
  width: 100%;
  max-width: 1080px;
  aspect-ratio: 16 / 7;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 56px;
  background: linear-gradient(135deg, var(--navy-mid) 0%, var(--navy-deep) 100%);
  border: 1px solid rgba(255,255,255,0.06);
  position: relative;
  animation: fadeUp 0.8s ease-out 0.8s both;
}

.hero-media video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.hero-media-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  color: var(--gray-500);
  letter-spacing: 0.15em;
  text-transform: uppercase;
}

.hero-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  width: 100%;
  max-width: 1200px;
  padding: 40px 0;
  border-top: 1px solid rgba(255,255,255,0.06);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  animation: fadeUp 0.8s ease-out 1s both;
}

.hero-strip-item {
  text-align: center;
  padding: 0 24px;
  border-right: 1px solid rgba(255,255,255,0.06);
}

.hero-strip-item:last-child { border-right: none; }

.hero-strip-stat {
  font-family: 'Playfair Display', serif;
  font-size: clamp(28px, 3.2vw, 40px);
  font-weight: 600;
  color: var(--white);
  margin-bottom: 8px;
  line-height: 1;
}

.hero-strip-label {
  font-size: 13px;
  color: var(--gray-400);
  line-height: 1.5;
}

@media (max-width: 768px) {
  .hero { padding: 110px 24px 0; }
  .hero-strip { grid-template-columns: repeat(2, 1fr); gap: 24px 0; padding: 28px 0; }
  .hero-strip-item { padding: 8px 16px; }
  .hero-strip-item:nth-child(2) { border-right: none; }
  .hero-strip-item:nth-child(odd) { border-right: 1px solid rgba(255,255,255,0.06); }
}
```

**Step 3: Verify in browser**

Open `index.html`. Hero should show: headline (with solid blue "capabilities." — no gradient), one short sub, single CTA, dark media placeholder rectangle, and a 4-column stat strip with hairline dividers. No badge. No scroll-indicator. No italic tagline.

**Step 4: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Hero refactor: single CTA, stat strip, media slot

Drops the keyword-stuffed badge, gradient accent text, italic tagline, and
secondary CTA. Adds a 4-up stat strip and a 16:7 media placeholder for the
Chicago video.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Add "Backed by experience at" logo strip section

**Files:**
- Modify: `index.html` (insert new section immediately after `</section>` of hero)
- Modify: `styles.css` (append logo-strip rules)

**Step 1: Insert the section**

Immediately after the hero's closing `</section>` (and before the `<div class="section-divider"></div>`), insert:

```html
<section class="logo-strip" aria-label="Prior firms our team has worked at">
  <p class="logo-strip-caption">Decades of experience at the firms shaping global commerce</p>
  <div class="logo-strip-grid">
    <!-- TODO(content): Drop monochrome SVG/PNG logos into images/logos/ and uncomment below.
    <img src="images/logos/mckinsey.svg" alt="McKinsey & Company">
    <img src="images/logos/bcg.svg" alt="Boston Consulting Group">
    <img src="images/logos/blackrock.svg" alt="BlackRock">
    <img src="images/logos/bain.svg" alt="Bain & Company">
    <img src="images/logos/jpmorgan.svg" alt="JPMorgan">
    -->
    <div class="logo-strip-placeholder">McKinsey</div>
    <div class="logo-strip-placeholder">BCG</div>
    <div class="logo-strip-placeholder">BlackRock</div>
    <div class="logo-strip-placeholder">Bain</div>
    <div class="logo-strip-placeholder">JPMorgan</div>
  </div>
</section>
```

**Step 2: Append styles**

Append to `styles.css`:

```css
/* ─── LOGO STRIP ─── */
.logo-strip {
  background: var(--navy-deepest);
  padding: 80px 60px;
  text-align: center;
}

.logo-strip-caption {
  font-size: 13px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gray-400);
  margin-bottom: 36px;
}

.logo-strip-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 56px;
  max-width: 1100px;
  margin: 0 auto;
}

.logo-strip-grid img {
  height: 28px;
  width: auto;
  opacity: 0.55;
  filter: grayscale(100%) brightness(2);
  transition: opacity 0.3s, filter 0.3s;
}

.logo-strip-grid img:hover { opacity: 1; filter: none; }

.logo-strip-placeholder {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  color: var(--gray-400);
  letter-spacing: 0.02em;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .logo-strip { padding: 56px 24px; }
  .logo-strip-grid { gap: 32px; }
  .logo-strip-grid img { height: 22px; }
}
```

**Step 3: Verify in browser**

Open `index.html`. Immediately under the hero stat strip should be a new dark section with the caption "DECADES OF EXPERIENCE AT THE FIRMS SHAPING GLOBAL COMMERCE" and 5 placeholder logo wordmarks in a row.

**Step 4: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Add 'Backed by experience at' logo strip section

Placeholder wordmarks until monochrome logo assets ship.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Replace flywheel with horizontal 4-step process bar

**Files:**
- Modify: `index.html` (the `.flywheel-visual` block inside `.value-prop`)
- Modify: `styles.css` (delete `.flywheel*` rules, add `.process-bar` rules)

**Step 1: Replace the visual markup**

In `index.html`, find `<div class="flywheel-visual reveal reveal-delay-2">` through its matching `</div>` (the entire flywheel block — about 12 lines). Replace with:

```html
<div class="process-bar reveal reveal-delay-2">
  <div class="process-step">
    <div class="process-step-num">01</div>
    <div class="process-step-title">Engage</div>
    <div class="process-step-text">Diagnose the revenue lever with the highest ROI in weeks, not months.</div>
  </div>
  <div class="process-step">
    <div class="process-step-num">02</div>
    <div class="process-step-title">Build</div>
    <div class="process-step-text">Stand up the AI system unique to your data, your products, your buyers.</div>
  </div>
  <div class="process-step">
    <div class="process-step-num">03</div>
    <div class="process-step-title">Embed</div>
    <div class="process-step-text">Hand the keys to your team. Train them to run, iterate, and extend.</div>
  </div>
  <div class="process-step">
    <div class="process-step-num">04</div>
    <div class="process-step-title">Iterate</div>
    <div class="process-step-text">Returns compound as the system learns and your team applies it to new questions.</div>
  </div>
</div>
```

**Step 2: Delete the flywheel CSS**

In `styles.css`, delete every rule whose selector starts with `.flywheel` (there are 7: `.flywheel-visual`, `.flywheel`, `.flywheel-ring`, `.flywheel-ring:nth-child(1/2/3)`, `.flywheel-node`, `.flywheel-node:nth-child(4/5/6/7)`, `.flywheel-center`) AND the `@keyframes spin` block.

**Step 3: Append process-bar CSS**

Append to `styles.css`:

```css
/* ─── PROCESS BAR ─── */
.process-bar {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px 32px;
  width: 100%;
}

.process-step {
  padding: 24px 0;
  border-top: 1px solid rgba(65, 105, 225, 0.2);
}

.process-step-num {
  font-family: 'Playfair Display', serif;
  font-size: 14px;
  color: var(--blue-bright);
  letter-spacing: 0.1em;
  margin-bottom: 12px;
}

.process-step-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: var(--white);
  margin-bottom: 8px;
}

.process-step-text {
  font-size: 14px;
  color: var(--gray-300);
  line-height: 1.6;
}

@media (max-width: 768px) {
  .process-bar { grid-template-columns: 1fr; }
}
```

**Step 4: Update the value-prop grid layout to make room**

In `styles.css`, find `.value-grid` and change `gap: 80px` to `gap: 64px`. (The process bar is denser than the flywheel — slightly tighter gap reads better.)

**Step 5: Verify in browser**

Open `index.html`. The Approach section should now show the stats on the left and a 2x2 grid of numbered process steps on the right. No spinning rings.

**Step 6: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Replace flywheel with restrained 4-step process bar

Engage / Build / Embed / Iterate as static numbered steps. Drops the rotating
concentric ring visual which read as a SaaS template.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Build "Path to Compounding Growth" tabbed section (merging old Offerings)

**Files:**
- Modify: `index.html` (delete `<section class="offerings">`, insert new `<section id="path">` in its place)
- Modify: `styles.css` (delete `.offerings*` rules, add `.path*` rules)
- Modify: `index.html` `<script>` block (append tab JS)

**Step 1: Delete the old Offerings section markup**

In `index.html`, delete the entire `<section class="offerings" id="offerings">…</section>` block including its inner `.offerings-header` and `.offerings-grid`.

**Step 2: Insert the new Path section in its place**

```html
<section class="path" id="path">
  <div class="path-header">
    <div class="section-label reveal">Our Platform</div>
    <h2 class="section-title reveal reveal-delay-1">Path to Compounding Growth</h2>
    <p class="section-desc reveal reveal-delay-2">Four AI capabilities, applied in concert. Each one stands alone — together they make consulting compound.</p>
  </div>

  <div class="path-tabs" role="tablist">
    <button class="path-tab active" role="tab" aria-selected="true" data-target="tab-opportunity">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      Opportunity Identification
    </button>
    <button class="path-tab" role="tab" aria-selected="false" data-target="tab-geospatial">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-7-7-12a7 7 0 1 1 14 0c0 5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>
      Geospatial Mapping
    </button>
    <button class="path-tab" role="tab" aria-selected="false" data-target="tab-pricing">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 6H9a3 3 0 0 0 0 6h6a3 3 0 0 1 0 6H7"/></svg>
      Pricing Engine
    </button>
    <button class="path-tab" role="tab" aria-selected="false" data-target="tab-forecast">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5-5 4 4 7-9"/><path d="M14 7h6v6"/></svg>
      Demand Forecasting
    </button>
  </div>

  <div class="path-panels">
    <div class="path-panel active" id="tab-opportunity" role="tabpanel">
      <div class="path-panel-content">
        <h3>Surface the growth no one's looked for.</h3>
        <p>Scan markets, adjacencies, and acquisition targets at a depth that used to take a six-month engagement. Output: ranked opportunities with sizing and rationale.</p>
        <div class="path-panel-meta">
          <div class="path-panel-meta-label">Engaged via</div>
          <div class="path-panel-meta-value">Growth Strategy · Commercial Due Diligence</div>
        </div>
      </div>
      <div class="path-panel-visual">
        <!-- TODO(media): screenshot or product mock of opportunity dashboard -->
        <div class="path-panel-placeholder">Opportunity scan output</div>
      </div>
    </div>

    <div class="path-panel" id="tab-geospatial" role="tabpanel" hidden>
      <div class="path-panel-content">
        <h3>See your market the way it actually behaves.</h3>
        <p>Map demand, competitors, and white space at the ZIP, county, or trade-area level. Built for industrials, retail, and services where geography determines the play.</p>
        <div class="path-panel-meta">
          <div class="path-panel-meta-label">Engaged via</div>
          <div class="path-panel-meta-value">Growth Strategy · Commercial Due Diligence</div>
        </div>
      </div>
      <div class="path-panel-visual">
        <div class="path-panel-placeholder">Geospatial demand map</div>
      </div>
    </div>

    <div class="path-panel" id="tab-pricing" role="tabpanel" hidden>
      <div class="path-panel-content">
        <h3>Capture the value you're leaving on the table.</h3>
        <p>Customer- and quote-level pricing models that surface leaks and recommend moves. Then we embed it so the team can run pricing refreshes without us.</p>
        <div class="path-panel-meta">
          <div class="path-panel-meta-label">Engaged via</div>
          <div class="path-panel-meta-value">Pricing</div>
        </div>
      </div>
      <div class="path-panel-visual">
        <div class="path-panel-placeholder">Pricing engine output</div>
      </div>
    </div>

    <div class="path-panel" id="tab-forecast" role="tabpanel" hidden>
      <div class="path-panel-content">
        <h3>Forecasts that stay sharp after we leave.</h3>
        <p>Customer-by-SKU forecasts that learn from every cycle. Built into your S&amp;OP flow, owned by your team.</p>
        <div class="path-panel-meta">
          <div class="path-panel-meta-label">Engaged via</div>
          <div class="path-panel-meta-value">Demand Forecasting</div>
        </div>
      </div>
      <div class="path-panel-visual">
        <div class="path-panel-placeholder">Forecast accuracy dashboard</div>
      </div>
    </div>
  </div>
</section>
```

**Step 3: Delete old Offerings styles, add Path styles**

In `styles.css`, delete every rule starting with `.offerings`, `.offering-card`, `.offering-icon`, `.offering-link`, `.offering-link .arrow`. Then append:

```css
/* ─── PATH TO GROWTH ─── */
.path {
  background: var(--navy-deep);
}

.path-header {
  text-align: center;
  margin-bottom: 64px;
}

.path-header .section-desc { margin: 16px auto 0; }

.path-tabs {
  display: flex;
  justify-content: center;
  gap: 0;
  max-width: 1100px;
  margin: 0 auto 56px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.path-tab {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 18px 28px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--gray-400);
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s;
  margin-bottom: -1px;
}

.path-tab:hover { color: var(--gray-200); }

.path-tab.active {
  color: var(--white);
  border-bottom-color: var(--blue-accent);
}

.path-panels {
  max-width: 1100px;
  margin: 0 auto;
}

.path-panel {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
  animation: fadeUp 0.5s ease-out;
}

.path-panel[hidden] { display: none; }

.path-panel-content h3 {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  line-height: 1.2;
  margin-bottom: 20px;
}

.path-panel-content p {
  font-size: 16px;
  color: var(--gray-300);
  line-height: 1.7;
  margin-bottom: 32px;
}

.path-panel-meta {
  padding-top: 24px;
  border-top: 1px solid rgba(255,255,255,0.08);
}

.path-panel-meta-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gray-400);
  margin-bottom: 6px;
}

.path-panel-meta-value {
  font-size: 14px;
  color: var(--blue-bright);
  font-weight: 500;
}

.path-panel-visual {
  aspect-ratio: 4 / 3;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--navy-mid) 0%, var(--navy-deepest) 100%);
  border: 1px solid rgba(255,255,255,0.06);
  display: flex;
  align-items: center;
  justify-content: center;
}

.path-panel-placeholder {
  font-size: 12px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gray-500);
}

@media (max-width: 1024px) {
  .path-tabs { flex-wrap: wrap; }
  .path-panel { grid-template-columns: 1fr; gap: 32px; }
}

@media (max-width: 768px) {
  .path-tab { padding: 14px 16px; font-size: 13px; }
  .path-tab svg { width: 16px; height: 16px; }
}
```

**Step 4: Add tab JS**

In `index.html` `<script>` block, append:

```javascript
// ─── PATH TABS ───
const pathTabs = document.querySelectorAll('.path-tab');
const pathPanels = document.querySelectorAll('.path-panel');
pathTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const targetId = tab.dataset.target;
    pathTabs.forEach(t => {
      const active = t === tab;
      t.classList.toggle('active', active);
      t.setAttribute('aria-selected', String(active));
    });
    pathPanels.forEach(p => {
      const show = p.id === targetId;
      p.classList.toggle('active', show);
      p.hidden = !show;
    });
  });
});
```

**Step 5: Verify in browser**

Open `index.html`. The old "Our Offerings" 4-card grid is gone. In its place: a Path-to-Growth header, 4 tabs with line-stroke icons, and the active tab's panel shows a headline + paragraph + "Engaged via" mapping + placeholder visual. Click each tab — content swaps in. The active tab has a blue underline.

**Step 6: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Merge Offerings into Path to Compounding Growth tabs

Four AI capability tabs (Opportunity ID / Geospatial / Pricing / Demand
Forecasting), each mapping back to a service category. Replaces the
4-card emoji-iconed Offerings grid.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Restyle Differentiators table (Aristotle column emphasis)

**Files:**
- Modify: `styles.css` (the `/* ─── DIFFERENTIATORS ─── */` rules)

**Step 1: Replace the diff-table styles**

In `styles.css`, find the differentiators block. Replace the rules from `.diff-row {` through `.diff-aristotle {` with:

```css
.diff-row {
  display: grid;
  grid-template-columns: 220px 1fr 1fr;
  gap: 0;
  border-bottom: 1px solid rgba(15, 27, 51, 0.08);
}

.diff-row.header {
  border-bottom: 2px solid rgba(15, 27, 51, 0.15);
  margin-bottom: 0;
}

.diff-cell {
  padding: 32px 32px;
  font-size: 15px;
  line-height: 1.55;
}

.diff-row:not(.header) .diff-cell:last-child {
  background: rgba(40, 81, 164, 0.06);
}

.diff-label {
  font-weight: 600;
  color: var(--navy);
  font-size: 14px;
  letter-spacing: 0.02em;
}

.diff-trad {
  color: var(--gray-500);
  font-weight: 400;
}

.diff-aristotle {
  color: var(--navy);
  font-weight: 600;
}
```

**Step 2: Tweak header cell weight**

Find `.diff-header-cell` and change `color: var(--gray-400);` to `color: var(--navy);` so the column headers read with more authority. Also add `padding-bottom: 20px;` (replacing `16px`).

For the Aristotle column header, we want it to stand out. Update markup in `index.html` — find the header row in the differentiators section:

```html
<div class="diff-row header reveal">
  <div class="diff-cell diff-header-cell"></div>
  <div class="diff-cell diff-header-cell">Traditional Consulting</div>
  <div class="diff-cell diff-header-cell diff-header-aristotle">Aristotle</div>
</div>
```

Append CSS:

```css
.diff-header-aristotle { background: rgba(40, 81, 164, 0.06); color: var(--blue-primary); }
```

**Step 3: Verify in browser**

Open `index.html`. The "How We Are Different" table should now have a subtle blue tint highlighting the entire Aristotle column (header included), with bolder header text.

**Step 4: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Restyle differentiators: highlight Aristotle column

Subtle blue tint on the winning column, bolder header weight, slightly wider
cell padding for breathing room.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Add "Decades of Expertise" credibility section (with sectors strip)

**Files:**
- Modify: `index.html` (insert new section after the differentiators section)
- Modify: `styles.css` (append rules)

**Step 1: Insert the section**

Between `</section>` of differentiators and `<section class="case-studies" id="cases">`, insert:

```html
<section class="expertise" id="expertise">
  <div class="expertise-header">
    <div class="section-label">By the Numbers</div>
    <h2 class="section-title">Decades of expertise. Backed by technology that delivers.</h2>
  </div>

  <div class="expertise-stats">
    <div class="expertise-stat">
      <div class="expertise-stat-num">$2B+</div>
      <div class="expertise-stat-text">in growth opportunities identified in under a week</div>
    </div>
    <div class="expertise-stat">
      <div class="expertise-stat-num">40x</div>
      <div class="expertise-stat-text">average ROI on a single Aristotle engagement</div>
    </div>
    <div class="expertise-stat">
      <div class="expertise-stat-num">10x</div>
      <div class="expertise-stat-text">faster than the traditional consulting cycle</div>
    </div>
  </div>

  <div class="expertise-sectors">
    <div class="expertise-sectors-label">Sectors we serve</div>
    <div class="expertise-sectors-grid">
      <div class="expertise-sector">Industrials &amp; Manufacturing</div>
      <div class="expertise-sector">Semiconductors</div>
      <div class="expertise-sector">Financial Services</div>
      <div class="expertise-sector">Technology</div>
      <div class="expertise-sector">Consumer &amp; Retail</div>
      <div class="expertise-sector">Private Equity</div>
    </div>
  </div>
</section>
```

**Step 2: Append styles**

```css
/* ─── EXPERTISE ─── */
.expertise {
  background: var(--gray-100);
  color: var(--navy-deep);
}

.expertise-header {
  text-align: center;
  margin-bottom: 80px;
}

.expertise-header .section-label { color: var(--blue-primary); }

.expertise-header .section-title {
  color: var(--navy-deep);
  max-width: 820px;
  margin: 20px auto 0;
}

.expertise-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  max-width: 1100px;
  margin: 0 auto 96px;
  border-top: 1px solid rgba(15, 27, 51, 0.1);
  border-bottom: 1px solid rgba(15, 27, 51, 0.1);
}

.expertise-stat {
  padding: 56px 32px;
  text-align: center;
  border-right: 1px solid rgba(15, 27, 51, 0.1);
}

.expertise-stat:last-child { border-right: none; }

.expertise-stat-num {
  font-family: 'Playfair Display', serif;
  font-size: clamp(48px, 5.5vw, 72px);
  font-weight: 600;
  color: var(--blue-primary);
  line-height: 1;
  margin-bottom: 16px;
}

.expertise-stat-text {
  font-size: 15px;
  color: var(--gray-500);
  line-height: 1.5;
  max-width: 240px;
  margin: 0 auto;
}

.expertise-sectors {
  max-width: 1100px;
  margin: 0 auto;
  text-align: center;
}

.expertise-sectors-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gray-500);
  margin-bottom: 28px;
}

.expertise-sectors-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
}

.expertise-sector {
  padding: 18px 16px;
  background: var(--white);
  border: 1px solid rgba(15, 27, 51, 0.08);
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  color: var(--navy);
}

@media (max-width: 1024px) {
  .expertise-stats { grid-template-columns: 1fr; }
  .expertise-stat { border-right: none; border-bottom: 1px solid rgba(15, 27, 51, 0.1); }
  .expertise-stat:last-child { border-bottom: none; }
  .expertise-sectors-grid { grid-template-columns: repeat(2, 1fr); }
}
```

**Step 3: Verify in browser**

Open `index.html`. After "How We Are Different" (light section), you should see another light section with three big Playfair numbers in a row, hairline dividers, and a 6-column sector grid below.

**Step 4: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Add Decades-of-Expertise credibility section

Three flagship stats and a sector grid on a light background. Provides the
proof-block ILA leans on to convert skeptics.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: Restyle Case Studies (hairline dividers, gold result accent)

**Files:**
- Modify: `styles.css` (the `/* ─── CASE STUDIES ─── */` block)

**Step 1: Replace the case-card rules**

Find and replace the case-studies block (from `.case-studies {` through `.case-result-text {`) with:

```css
/* ─── CASE STUDIES ─── */
.case-studies {
  background: var(--navy-deepest);
}

.cases-header {
  text-align: center;
  margin-bottom: 72px;
}

.cases-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0;
  max-width: 1100px;
  margin: 0 auto;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.case-card {
  padding: 48px 40px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  border-right: 1px solid rgba(255,255,255,0.06);
  background: transparent;
  border-radius: 0;
}

.case-card:nth-child(2n) { border-right: none; }

.case-card:hover { background: rgba(255,255,255,0.02); }

.case-tag {
  display: inline-block;
  padding: 4px 12px;
  background: transparent;
  color: var(--blue-bright);
  border: 1px solid rgba(91, 141, 239, 0.3);
  border-radius: 100px;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.05em;
  margin-bottom: 20px;
}

.case-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 8px;
  line-height: 1.3;
}

.case-meta {
  font-size: 12px;
  color: var(--gray-500);
  margin-bottom: 24px;
  letter-spacing: 0.02em;
}

.case-section { margin-bottom: 18px; }

.case-section-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--gray-400);
  margin-bottom: 6px;
}

.case-section-text {
  font-size: 14px;
  color: var(--gray-300);
  line-height: 1.6;
}

.case-result {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.case-result-text {
  font-size: 15px;
  font-weight: 600;
  color: var(--gold);
  line-height: 1.5;
  letter-spacing: 0.01em;
}
```

**Step 2: Verify in browser**

Case studies should now read as a 2x2 grid with hairline dividers (no rounded card backgrounds). Result line should be gold. Outline-only tag pill.

**Step 3: Commit**

```bash
git add styles.css
git commit -m "$(cat <<'EOF'
Restyle case studies: hairline grid, gold result accent

Drops floating card backgrounds for an editorial 2x2 grid with thin
dividers. Result line uses the existing --gold token for accent.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 11: Add Insights placeholder section

**Files:**
- Modify: `index.html` (insert new section after case-studies)
- Modify: `styles.css` (append insights rules)

**Step 1: Insert the section**

After case-studies' closing `</section>`, before the team section, insert:

```html
<section class="insights" id="insights">
  <div class="insights-header">
    <div class="section-label">Insights</div>
    <h2 class="section-title">Notes from the field</h2>
    <p class="section-desc">Field-tested perspectives on revenue, pricing, and where AI is actually moving the needle.</p>
  </div>
  <div class="insights-grid">
    <article class="insight-card">
      <div class="insight-tag">Pricing</div>
      <h3>Why your pricing model expires the day you ship it</h3>
      <div class="insight-meta">Coming soon</div>
    </article>
    <article class="insight-card">
      <div class="insight-tag">Growth Strategy</div>
      <h3>Adjacency scans: the cheapest growth lever most companies skip</h3>
      <div class="insight-meta">Coming soon</div>
    </article>
    <article class="insight-card">
      <div class="insight-tag">AI in Consulting</div>
      <h3>The hand-off problem: why consulting capabilities don't stick</h3>
      <div class="insight-meta">Coming soon</div>
    </article>
  </div>
  <!-- TODO(content): swap placeholder titles for real posts; link to /insights/<slug>.html when ready -->
</section>
```

**Step 2: Append styles**

```css
/* ─── INSIGHTS ─── */
.insights {
  background: var(--navy-deep);
}

.insights-header {
  text-align: center;
  margin-bottom: 64px;
}

.insights-header .section-desc { margin: 16px auto 0; }

.insights-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1100px;
  margin: 0 auto;
}

.insight-card {
  padding: 36px 32px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px;
  transition: border-color 0.2s, background 0.2s;
}

.insight-card:hover {
  background: rgba(255,255,255,0.04);
  border-color: rgba(65, 105, 225, 0.2);
}

.insight-tag {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--blue-bright);
  margin-bottom: 20px;
}

.insight-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  line-height: 1.35;
  margin-bottom: 24px;
  min-height: 80px;
}

.insight-meta {
  font-size: 12px;
  color: var(--gray-500);
  letter-spacing: 0.05em;
}

@media (max-width: 1024px) {
  .insights-grid { grid-template-columns: 1fr; }
  .insight-card h3 { min-height: 0; }
}
```

**Step 3: Verify in browser**

Open `index.html`. Scroll to where the old team section used to be (it's still there for now). Just above it should now be an Insights section with 3 placeholder post cards.

**Step 4: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Add Insights placeholder section

Three coming-soon post tiles, linked to nav #insights anchor. Real posts
land in a follow-up.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 12: Add Q&A accordion section

**Files:**
- Modify: `index.html` (insert section between insights and CTA; remove the existing `<section class="team">` block)
- Modify: `styles.css` (append Q&A rules; remove team rules later in Task 13)
- Modify: `<script>` (append accordion JS)

**Step 1: Insert the Q&A section**

After the insights section's `</section>`, insert:

```html
<section class="qa" id="qa">
  <div class="qa-header">
    <div class="section-label">Q&amp;A</div>
    <h2 class="section-title">Common questions</h2>
  </div>

  <div class="qa-list">
    <details class="qa-item">
      <summary>How is Aristotle different from a traditional consulting firm?</summary>
      <div class="qa-answer">We deliver MBB-grade insight in weeks, not months — then we embed the AI systems and trained team so the capability stays after we leave. Traditional firms ship a deck and a bill; we ship a working system you own.</div>
    </details>
    <details class="qa-item">
      <summary>What does "tied to impact" mean for fees?</summary>
      <div class="qa-answer">Our commercials are structured around the outcome we deliver, not a fixed seven-figure engagement fee. We win when you win.</div>
    </details>
    <details class="qa-item">
      <summary>What size of company do you typically work with?</summary>
      <div class="qa-answer"><!-- TODO(content): confirm revenue band --> Mid-market through enterprise — typically $200M–$5B in revenue, in industries where revenue decisions are driven by pricing, geography, or demand complexity.</div>
    </details>
    <details class="qa-item">
      <summary>How quickly can we see results?</summary>
      <div class="qa-answer">Initial findings in under six weeks. Most engagements show measurable revenue impact within the first quarter and compound from there as the embedded system iterates.</div>
    </details>
    <details class="qa-item">
      <summary>Who owns the AI system you build?</summary>
      <div class="qa-answer">You do. Code, models, dashboards, and documentation all live in your environment. We provide ongoing support, but the capability is yours to run.</div>
    </details>
    <details class="qa-item">
      <summary>Is my data secure?</summary>
      <div class="qa-answer">Yes. We work inside your security perimeter where possible, and use enterprise-grade controls otherwise. NDAs and DPAs are standard.</div>
    </details>
  </div>
</section>
```

**Step 2: Append Q&A styles**

```css
/* ─── Q&A ─── */
.qa {
  background: var(--navy-deepest);
}

.qa-header {
  text-align: center;
  margin-bottom: 64px;
}

.qa-list {
  max-width: 820px;
  margin: 0 auto;
}

.qa-item {
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.qa-item summary {
  list-style: none;
  cursor: pointer;
  padding: 28px 8px;
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 500;
  color: var(--white);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  transition: color 0.2s;
}

.qa-item summary::-webkit-details-marker { display: none; }

.qa-item summary::after {
  content: '+';
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  font-weight: 300;
  color: var(--blue-bright);
  transition: transform 0.2s;
}

.qa-item[open] summary::after { transform: rotate(45deg); }

.qa-item summary:hover { color: var(--blue-light); }

.qa-answer {
  padding: 0 8px 28px;
  font-size: 16px;
  color: var(--gray-300);
  line-height: 1.7;
  max-width: 720px;
}
```

**Step 3: Verify in browser**

Open `index.html`. Q&A section appears with 6 collapsible items. Clicking expands the answer and rotates the `+` to an `x`. Default state: all closed.

**Step 4: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Add Q&A accordion section

Native <details>/<summary> for accessibility — no JS needed. Six common
questions, one TODO on revenue band.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 13: Remove Team section from index.html; restyle final CTA + footer

**Files:**
- Modify: `index.html` (delete `<section class="team">`, update CTA and footer)
- Modify: `styles.css` (delete `.team*` rules from homepage section, keep team-page rules from Task 2)

**Step 1: Delete the homepage Team section**

In `index.html`, delete the entire `<section class="team" id="team">…</section>` block (the one with `.team-grid` and 3 `.team-card` entries).

**Step 2: Delete the corresponding CSS**

In `styles.css`, delete the rules from `/* ─── TEAM ─── */` through `.team-card .role { … }`. (Do NOT touch the `/* ─── TEAM PAGE ─── */` block added in Task 2.)

**Step 3: Update the CTA section**

Find `<section class="cta" id="contact">` and replace with:

```html
<section class="cta" id="contact">
  <h2 class="section-title">Business decisions are too important for stale spreadsheets and consulting decks.</h2>
  <p class="cta-sub">Book a 30-minute call. We'll show you what compounding consulting looks like for your team.</p>
  <a href="https://calendly.com/sam-aristotle/30min" target="_blank" class="btn-primary">Book a Meeting <span aria-hidden="true">→</span></a>
</section>
```

**Step 4: Update the footer**

Replace the existing `<footer>` block with:

```html
<footer>
  <div class="footer-logo">Aristotle</div>
  <div class="footer-text">&copy; 2026 Aristotle. Chicago, IL.</div>
  <ul class="footer-links">
    <li><a href="team.html">Team</a></li>
    <li><a href="#insights">Insights</a></li>
    <li><a href="https://calendly.com/sam-aristotle/30min" target="_blank">Book a Meeting</a></li>
    <li><a href="mailto:sam@aristotle.ai">Contact</a></li>
  </ul>
</footer>
<!-- TODO(content): confirm sam@aristotle.ai or correct contact email -->
```

**Step 5: Verify in browser**

Open `index.html`. Team section is gone from homepage. Footer shows 4 real links. CTA copy is updated. Click "Team" in nav or footer — navigates to `team.html`.

**Step 6: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Move Team off homepage; polish CTA and footer

Team lives at team.html now. Footer replaces placeholder # links with
team / insights / book / contact.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 14: Typography + button polish (Inter on numbers, flat buttons, drop counter animation)

**Files:**
- Modify: `index.html` (remove the counter `data-target`/`data-suffix` attrs)
- Modify: `index.html` `<script>` (delete the counter IIFE)
- Modify: `styles.css` (button + stat-number rules)

**Step 1: Drop the counter animation**

In `index.html`, find the value-prop stat cards. Replace the 4 stat-card divs to render static numbers (no counter animation):

```html
<div class="stat-card">
  <div class="stat-number">40x</div>
  <div class="stat-label">Typical ROI on engagement</div>
</div>
<div class="stat-card">
  <div class="stat-number">80+</div>
  <div class="stat-label">Growth targets identified per scan</div>
</div>
<div class="stat-card">
  <div class="stat-number">$500M+</div>
  <div class="stat-label">Growth opportunities identified</div>
</div>
<div class="stat-card">
  <div class="stat-number">10x</div>
  <div class="stat-label">Faster than traditional consulting</div>
</div>
```

In the `<script>` block, delete the entire `// ─── COUNTER ANIMATION ───` section (the `counters` constant, the `counterObserver`, and the `counters.forEach(...)` line).

**Step 2: Switch stat numbers to Inter**

In `styles.css`, find `.stat-number` and change `font-family: 'Playfair Display', serif;` to `font-family: 'Inter', sans-serif;`. Add `font-feature-settings: 'tnum' 1;` for tabular alignment. Also reduce `font-size: 36px` to `font-size: 32px` and `font-weight: 600` stays.

Same treatment for `.hero-strip-stat`: change font-family from Playfair to Inter. Keep `font-weight: 600`. Add `font-feature-settings: 'tnum' 1;`.

(Leave `.expertise-stat-num` and Path/team headings in Playfair — those are decorative section anchors, not data points.)

**Step 3: Flatten buttons**

In `styles.css`, find `.btn-primary:hover`. Replace its body with:

```css
.btn-primary:hover {
  background: var(--blue-bright);
}
```

(Removes the `transform` and `box-shadow`.)

Same for `.btn-secondary:hover` — leave as background only. (`.btn-secondary` exists but is unused after Task 4; safe to leave the rule.)

Same for `.nav-cta:hover`:

```css
.nav-cta:hover {
  background: var(--blue-bright);
}
```

(Removes the `transform`.)

Same for `.cta .btn-primary:hover`:

```css
.cta .btn-primary:hover {
  background: var(--gray-100);
}
```

**Step 4: Reduce stat-card hover lift**

In `styles.css`, find `.stat-card:hover`. Replace with:

```css
.stat-card:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(65, 105, 225, 0.18);
}
```

(Drops the `transform: translateY` lift.)

**Step 5: Verify in browser**

Open `index.html`. Stats render immediately as final values (no count-up). Numbers should look slightly tighter and more data-like (Inter, tabular). Hover on buttons just shifts background — no movement, no shadow. Hover on stat cards just changes background tint.

**Step 6: Commit**

```bash
git add index.html styles.css
git commit -m "$(cat <<'EOF'
Polish pass: flat buttons, Inter on numbers, no counter animation

Data renders as fact, not performance. Hover states drop transforms and
shadows for an editorial feel.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 15: Final QA pass

**Files:** none modified unless issues found.

**Step 1: Desktop pass at 1440px**

Open `index.html` in Chrome at window width 1440px. Scroll top to bottom. Confirm:
- Hero: solid blue accent, single CTA, media placeholder, 4-stat strip with hairline dividers.
- Logo strip: 5 placeholder wordmarks centered.
- Approach: stats grid (left) + 2x2 process steps (right), no spinning rings.
- Path to Growth: 4 tabs with SVG icons, blue underline on active tab, tabs swap content correctly.
- How We Are Different: Aristotle column has subtle blue tint.
- Decades of Expertise: light section, 3 big Playfair numbers, sector grid.
- Case Studies: 2x2 hairline grid, gold result lines.
- Insights: 3 dark card placeholders.
- Q&A: 6 collapsible items, `+` rotates to `x` on open.
- CTA: single Book a Meeting button.
- Footer: 4 real links (Team / Insights / Book / Contact).

**Step 2: Mobile pass at 375px**

Resize Chrome to 375px (DevTools device toolbar, iPhone SE). Scroll top to bottom. Confirm:
- Hero strip: 2x2 grid (not 1x4).
- Process bar: vertical stack.
- Path tabs: wrap if needed; panels stack vertically.
- Differentiators table: stacks per-row (label hidden).
- Expertise stats: stack vertically.
- Sector grid: 2-column.
- Insights: 1-column.
- Q&A: full-width, summary stays tappable.

**Step 3: Link audit**

Click every nav link, every CTA, every footer link. Confirm:
- All `Book a Meeting` CTAs open `https://calendly.com/sam-aristotle/30min` in a new tab.
- "Team" in nav and footer goes to `team.html`.
- "Insights" in nav scrolls to the insights section.
- `index.html` → `team.html` → click "Aristotle" logo → returns to `index.html`.

**Step 4: TODO sweep**

Run `grep -n 'TODO' index.html team.html styles.css`. Confirm all TODOs are intentional (content placeholders) and nothing accidentally shipped.

**Step 5: Open `team.html` standalone**

Confirm nav active state on "Team". Three cards render with photos. LinkedIn icons present (currently `href="#"` placeholders).

**Step 6: Commit any fixes (if needed)**

If anything is broken at this point, fix and commit:

```bash
git add -- <files>
git commit -m "$(cat <<'EOF'
QA fixes from final pass

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

If everything passes, no commit needed — Task 15 is verification only.

---

## Out of scope (deliberately)

The following were considered and deferred:
- **`/insights.html` dedicated blog page** — placeholder section only; build when first post is ready.
- **Real logo SVGs** — markup is staged; drop files into `images/logos/` and uncomment the `<img>` block.
- **Chicago hero video** — `<video>` markup is staged in a comment; drop the file into `images/hero-chicago.mp4` and uncomment.
- **Case study expansion / case-study detail pages** — homepage section restyled only.
- **Light theme for individual pages** — `team.html` deliberately matches the homepage dark theme for visual consistency.
- **Analytics / Plausible / GA** — not added.
- **Open Graph / Twitter Card meta tags** — not added; consider in a follow-up alongside the favicon work.
- **`prefers-reduced-motion` media query** — animations are subtle and time-limited; revisit if accessibility audit demands it.

---

## Content TODO list (for the user to fill in after implementation)

After implementation, search `grep -rn 'TODO(content)' .` and provide:
- Sam / Bea / Rachit one-paragraph bios for `team.html`
- LinkedIn URLs for all three team members
- Real Q&A revenue band confirmation
- Confirmation or replacement of `sam@aristotle.ai` contact email
- 5–6 monochrome logo files (`images/logos/*.svg` or `*.png`)
- Chicago hero video file (`images/hero-chicago.mp4` ~2–5 MB) + poster image
- Real numbers for the three Decades-of-Expertise stats (current values are educated guesses pulled from existing homepage stats)
- Real Insights post titles + dates when blog launches

