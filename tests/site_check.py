#!/usr/bin/env python3
"""
Offline + online checks for the Aristotle site.

Offline checks run against the repo files. The optional --online flag also
fetches the live URLs to verify HTTP status and content type.

Run:
    python3 tests/site_check.py            # offline checks only
    python3 tests/site_check.py --online   # also hit live URLs

Exit code is non-zero if any test fails. Designed for CI.
"""
from __future__ import annotations

import argparse
import html.parser
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
TEAM = ROOT / "team.html"
STYLES = ROOT / "styles.css"
CNAME = ROOT / "CNAME"

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"

failures: list[str] = []
passes: list[str] = []

HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        passes.append(name)
        print(f"  {PASS} {name}")
    else:
        msg = f"{name}" + (f" — {detail}" if detail else "")
        failures.append(msg)
        print(f"  {FAIL} {msg}")


def strip_comments(text: str) -> str:
    """Return HTML with comments removed so placeholder markers inside comments
    don't trip user-visible content checks."""
    return HTML_COMMENT_RE.sub("", text)


# ---------- Parse helpers ----------


class IDCollector(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.imgs: list[tuple[str, str]] = []
        self.hrefs: list[str] = []
        self.tags_open: list[str] = []
        self.tag_counter: Counter[str] = Counter()
        self.section_h2s: list[str] = []
        self._in_h2 = False
        self._h2_buf: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        self.tag_counter[tag] += 1
        if "id" in attr and attr["id"]:
            self.ids.append(attr["id"])
        if tag == "img":
            self.imgs.append((attr.get("src") or "", attr.get("alt") or ""))
        if tag == "a" and "href" in attr and attr["href"]:
            self.hrefs.append(attr["href"])
        if tag == "h2":
            self._in_h2 = True
            self._h2_buf = []
        if tag in {"div", "section", "nav", "footer", "header", "main", "article"}:
            self.tags_open.append(tag)

    def handle_endtag(self, tag):
        if tag == "h2" and self._in_h2:
            self._in_h2 = False
            self.section_h2s.append("".join(self._h2_buf).strip())
        if tag in {"div", "section", "nav", "footer", "header", "main", "article"}:
            if self.tags_open and self.tags_open[-1] == tag:
                self.tags_open.pop()
            else:
                self.errors.append(f"unbalanced </{tag}>")

    def handle_data(self, data):
        if self._in_h2:
            self._h2_buf.append(data)


def parse(path: Path) -> IDCollector:
    p = IDCollector()
    p.feed(path.read_text(encoding="utf-8"))
    return p


# ---------- Tests ----------


def test_files_exist() -> None:
    print("\n[1] File existence")
    check("index.html exists", INDEX.is_file())
    check("team.html exists", TEAM.is_file())
    check("styles.css exists", STYLES.is_file())
    check("CNAME exists", CNAME.is_file())
    check("images/ dir exists", (ROOT / "images").is_dir())
    for fname in ("favicon.png", "sam.jpeg", "bia.jpeg", "rachit.jpeg"):
        check(f"images/{fname} exists", (ROOT / "images" / fname).is_file())
    for logo in ("mckinsey.svg", "nyu.svg", "umich.svg"):
        check(f"images/logos/{logo} exists", (ROOT / "images" / "logos" / logo).is_file())


def test_cname() -> None:
    print("\n[2] CNAME format")
    raw = CNAME.read_bytes()
    text = CNAME.read_text(encoding="utf-8").strip()
    check("CNAME is not empty", bool(text), repr(raw))
    check(
        "CNAME has exactly one domain",
        len(text.splitlines()) == 1,
        f"got {len(text.splitlines())} lines",
    )
    valid_domains = {"aristotletechnology.com", "thearistotle.ai"}
    check(
        f"CNAME is one of {sorted(valid_domains)}",
        text in valid_domains,
        f"got {text!r}",
    )
    check(
        "CNAME has no leading/trailing whitespace on the domain",
        not (text != text.strip() or text.startswith(" ") or text.endswith(" ")),
    )
    check(
        "CNAME is valid domain syntax",
        bool(re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", text)),
        f"got {text!r}",
    )


def test_html_head(p: IDCollector) -> None:
    print("\n[3] HTML head (index.html)")
    text = INDEX.read_text(encoding="utf-8")
    check("has DOCTYPE", text.lstrip().lower().startswith("<!doctype html>"))
    check("html lang attr present", 'lang="en"' in text)
    check("has <title>", "<title>" in text and "</title>" in text)
    check(
        "title mentions Aristotle",
        bool(re.search(r"<title>[^<]*Aristotle[^<]*</title>", text)),
    )
    check("has meta viewport", 'name="viewport"' in text)
    check("has favicon link", 'rel="icon"' in text)
    check("references favicon.png", "images/favicon.png" in text)
    check("links external styles.css", 'href="styles.css"' in text)


def test_anchors(p: IDCollector) -> None:
    print("\n[4] Anchor integrity (index.html)")
    ids = set(p.ids)
    check(
        "no duplicate IDs",
        len(p.ids) == len(ids),
        f"dupes: {[i for i,c in Counter(p.ids).items() if c>1]}",
    )
    anchors = [h for h in p.hrefs if h.startswith("#") and h != "#"]
    missing = [a for a in anchors if a[1:] not in ids]
    check(
        f"all {len(anchors)} internal anchors resolve",
        not missing,
        f"missing IDs: {sorted(set(missing))}",
    )
    check("no empty hrefs", "" not in p.hrefs)
    check("no href='#' (lazy placeholder)", "#" not in p.hrefs, "found bare '#' link in index.html")
    check("no javascript: URLs", not any(h.lower().startswith("javascript:") for h in p.hrefs))


def test_images(p: IDCollector, where: str) -> None:
    print(f"\n[5] Images ({where})")
    for src, alt in p.imgs:
        if src.startswith(("http://", "https://", "data:")):
            continue
        path = ROOT / src
        check(f"image file exists: {src}", path.is_file())
        check(f"image has alt text: {src}", bool(alt.strip()), f"alt={alt!r}")


def test_required_sections(p: IDCollector) -> None:
    print("\n[6] Required sections present (index.html)")
    h2_text = " | ".join(p.section_h2s)
    expected_h2 = [
        ("path", "Path to Compounding Growth"),
        ("differentiators", "How We Are Different"),
        ("expertise", "Decades of expertise"),
        ("cases", "Case Studies"),
        ("insights", "Notes from the field"),
        ("qa", "Common questions"),
    ]
    for label, needle in expected_h2:
        check(
            f"section <{label}> headline contains {needle!r}",
            needle in h2_text,
            f"got: {h2_text}",
        )

    expected_ids = ["hero", "value", "path", "different", "expertise", "cases", "insights", "qa", "contact"]
    actual_ids = set(p.ids)
    for sid in expected_ids:
        check(f"section id='{sid}' exists", sid in actual_ids)


def test_design_tokens() -> None:
    print("\n[7] Design tokens (styles.css)")
    text = STYLES.read_text(encoding="utf-8")
    expected = {
        "--navy-deepest": r"--navy-deepest:\s*#[0-9A-Fa-f]{3,8}",
        "--navy-deep": r"--navy-deep:\s*#[0-9A-Fa-f]{3,8}",
        "--navy": r"--navy:\s*#[0-9A-Fa-f]{3,8}",
        "--blue-accent": r"--blue-accent:\s*#[0-9A-Fa-f]{3,8}",
        "--blue-bright": r"--blue-bright:\s*#[0-9A-Fa-f]{3,8}",
        "--white": r"--white:\s*#[0-9A-Fa-f]{3,8}",
        "--gold": r"--gold:\s*#[0-9A-Fa-f]{3,8}",
    }
    for name, pattern in expected.items():
        check(f"token defined: {name}", bool(re.search(pattern, text)))


def test_content_invariants() -> None:
    print("\n[8] Content invariants (index.html)")
    text = INDEX.read_text(encoding="utf-8")
    visible = strip_comments(text)

    # Hero strip
    check("hero strip: '25%'", "25%" in visible)
    check("hero strip: '&lt;6 wks' or '<6 wks'", "&lt;6 wks" in visible or "<6 wks" in visible)
    check("hero strip: '$2B+'", "$2B+" in visible)
    check("hero strip: 'Tied to impact'", "Tied to impact" in visible)

    # Value-prop stats
    check("value stats: '40x'", "40x" in visible)
    check("value stats: '80+'", "80+" in visible)
    check("value stats: '$500M+'", "$500M+" in visible)
    check("value stats: '10x'", "10x" in visible)

    # Expertise stats
    check("expertise: '$2B+'", "$2B+" in visible)

    # Path-to-Growth tabs
    for tab in ("Opportunity Identification", "Geospatial Mapping", "Pricing Engine", "Demand Forecasting"):
        check(f"path tab present: {tab!r}", tab in visible)

    # Hero CTA
    check("hero CTA: 'Book a Meeting'", "Book a Meeting" in visible)

    # Comparison columns
    check("comparison: 'Traditional Consulting'", "Traditional Consulting" in visible)
    check("comparison: 'Aristotle' column", "diff-header-aristotle" in text)

    # Regressions
    check("regression: no 'BlackRock'", "BlackRock" not in visible and "Blackrock" not in visible)
    check("regression: no old 'Start a Conversation' CTA", "Start a Conversation" not in visible)
    check("regression: no flywheel remnants", "flywheel" not in text.lower())


def test_team_page(p: IDCollector) -> None:
    print("\n[8b] Team page (team.html)")
    text = TEAM.read_text(encoding="utf-8")
    visible = strip_comments(text)
    check("Sam Garg present", "Sam Garg" in visible)
    check("Beatriz Abramof present", "Beatriz Abramof" in visible)
    check("Rachit Agarwal present", "Rachit Agarwal" in visible)
    check("team-bio-card count is 3", text.count('"team-bio-card"') == 3)
    check("nav links back to index.html", 'href="index.html"' in text)


def test_structural_counts() -> None:
    print("\n[9] Structural counts (index.html)")
    text = INDEX.read_text(encoding="utf-8")

    process_steps = len(re.findall(r'<div class="process-step">', text))
    check(f"process bar has 4 steps (got {process_steps})", process_steps == 4)

    path_tabs = len(re.findall(r"<button class=\"path-tab", text))
    check(f"path section has 4 tabs (got {path_tabs})", path_tabs == 4)

    path_panels = len(re.findall(r"<div class=\"path-panel(?: active)?\"", text))
    check(f"path section has 4 panels (got {path_panels})", path_panels == 4)

    hero_strip = len(re.findall(r'class="hero-strip-item"', text))
    check(f"hero strip has 4 items (got {hero_strip})", hero_strip == 4)

    stat_cards = len(re.findall(r'class="stat-card"', text))
    check(f"value-prop has 4 stat cards (got {stat_cards})", stat_cards == 4)

    qa_items = len(re.findall(r'<details class="qa-item">', text))
    check(f"Q&A has 6 entries (got {qa_items})", qa_items == 6)

    case_cards = len(re.findall(r'class="case-card', text))
    check(f"case studies has 4 cards (got {case_cards})", case_cards == 4)

    insights = len(re.findall(r'<article class="insight-card">', text))
    check(f"insights has 3 cards (got {insights})", insights == 3)

    expertise_stats = len(re.findall(r'<div class="expertise-stat">', text))
    check(f"expertise has 3 big stats (got {expertise_stats})", expertise_stats == 3)

    expertise_sectors = len(re.findall(r'<div class="expertise-sector">', text))
    check(f"expertise has 6 sector tiles (got {expertise_sectors})", expertise_sectors == 6)

    diff_data_rows = len(re.findall(r'<div class="diff-row reveal', text))
    check(f"differentiators has 3 data rows (got {diff_data_rows})", diff_data_rows == 3)

    logo_imgs = len(re.findall(r'<img src="images/logos/', text))
    check(f"logo strip has at least 3 real logos (got {logo_imgs})", logo_imgs >= 3)


def test_no_visible_placeholders() -> None:
    print("\n[10] No visible placeholder text")
    # Strip HTML comments first — intentional TODO markers live in comments and
    # are documented in the plan. We only care about placeholders the user sees.
    # Uppercase markers are matched exactly (PLACEHOLDER as a class-name token
    # like `hero-media-placeholder` is fine; PLACEHOLDER as visible copy is not).
    case_insensitive = ["lorem ipsum"]
    case_sensitive = ["FIXME", "XXX:", "PLACEHOLDER", "TBD"]
    for path in (INDEX, TEAM):
        visible = strip_comments(path.read_text(encoding="utf-8"))
        for needle in case_insensitive:
            check(
                f"{path.name}: no visible '{needle}'",
                needle.lower() not in visible.lower(),
            )
        for needle in case_sensitive:
            check(
                f"{path.name}: no visible '{needle}'",
                needle not in visible,
            )


def test_balanced_tags(p: IDCollector, where: str) -> None:
    print(f"\n[11] Tag balance ({where})")
    check("no unbalanced section/div/nav/footer", not p.tags_open, f"left open: {p.tags_open}")
    check("HTML parser had no errors", not p.errors, f"errors: {p.errors[:3]}")
    text = (INDEX if where == "index.html" else TEAM).read_text(encoding="utf-8")
    check("<style> tags balanced", text.count("<style>") == text.count("</style>"))
    check("<script> tags balanced", text.count("<script>") == text.count("</script>"))


def test_online() -> None:
    print("\n[12] Online checks")
    # Verify the styles.css link on raw GitHub is fetchable for this branch.
    branch_url = (
        "https://raw.githubusercontent.com/ragarwal23/ragarwal.io/"
        "redesign-eilla/index.html"
    )
    try:
        with urllib.request.urlopen(branch_url, timeout=15) as r:
            r.read(1024)
        check("redesign-eilla branch index.html fetched", True)
    except Exception as e:
        check("redesign-eilla branch index.html fetched", False, str(e))

    main_cname_url = (
        "https://raw.githubusercontent.com/ragarwal23/ragarwal.io/main/CNAME"
    )
    try:
        with urllib.request.urlopen(main_cname_url, timeout=15) as r:
            cname_main = r.read().decode().strip()
        check(
            "main CNAME is a known domain",
            cname_main in {"aristotletechnology.com", "thearistotle.ai"},
            f"got {cname_main!r}",
        )
    except Exception as e:
        check("main CNAME fetch", False, str(e))

    # Best-effort live-site check.
    live = "https://thearistotle.ai/"
    try:
        with urllib.request.urlopen(live, timeout=10) as r:
            status = r.status
            body = r.read(4096).decode("utf-8", errors="replace")
        check(f"live site {live} returned 200", status == 200, f"status={status}")
        check(
            "live site is the Aristotle page",
            "Aristotle" in body or "ARISTOTLE" in body,
            "headline marker missing",
        )
    except Exception as e:
        print(f"  \033[33m![/m] live site {live} not yet reachable: {e}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--online", action="store_true")
    args = ap.parse_args()

    print(f"Aristotle site checks — repo: {ROOT}")

    index_p = parse(INDEX)
    team_p = parse(TEAM)

    test_files_exist()
    test_cname()
    test_html_head(index_p)
    test_anchors(index_p)
    test_images(index_p, "index.html")
    test_images(team_p, "team.html")
    test_required_sections(index_p)
    test_design_tokens()
    test_content_invariants()
    test_team_page(team_p)
    test_structural_counts()
    test_no_visible_placeholders()
    test_balanced_tags(index_p, "index.html")
    test_balanced_tags(team_p, "team.html")
    if args.online:
        test_online()

    print()
    print(f"  {len(passes)} passed, {len(failures)} failed")
    if failures:
        print("\nFailures:")
        for f in failures:
            print(f"  {FAIL} {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())