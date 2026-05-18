#!/usr/bin/env python3
"""
Offline + online checks for the Aristotle site.

Offline checks run against the repo files. The optional --online flag also
fetches the live URLs to verify HTTP status, content type, and that the
deployed file matches the local file byte-for-byte.

Run:
    python3 tests/site_check.py            # offline checks only
    python3 tests/site_check.py --online   # also hit live URLs

Exit code is non-zero if any test fails. Designed for CI.
"""
from __future__ import annotations

import argparse
import html.parser
import os
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
CNAME = ROOT / "CNAME"

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"

failures: list[str] = []
passes: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        passes.append(name)
        print(f"  {PASS} {name}")
    else:
        msg = f"{name}" + (f" — {detail}" if detail else "")
        failures.append(msg)
        print(f"  {FAIL} {msg}")


# ---------- Parse helpers ----------


class IDCollector(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.imgs: list[tuple[str, str]] = []  # (src, alt)
        self.hrefs: list[str] = []
        self.tags_open: list[str] = []
        self.tag_counter: Counter[str] = Counter()
        self.section_h2s: list[str] = []
        self._in_h2 = False
        self._h2_buf: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
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

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self._in_h2:
            self._in_h2 = False
            self.section_h2s.append("".join(self._h2_buf).strip())
        if tag in {"div", "section", "nav", "footer", "header", "main", "article"}:
            if self.tags_open and self.tags_open[-1] == tag:
                self.tags_open.pop()
            else:
                self.errors.append(f"unbalanced </{tag}>")

    def handle_data(self, data: str) -> None:
        if self._in_h2:
            self._h2_buf.append(data)


def parse() -> IDCollector:
    text = INDEX.read_text(encoding="utf-8")
    p = IDCollector()
    p.feed(text)
    return p


# ---------- Tests ----------


def test_files_exist() -> None:
    print("\n[1] File existence")
    check("index.html exists", INDEX.is_file())
    check("CNAME exists", CNAME.is_file())
    check("images/ dir exists", (ROOT / "images").is_dir())
    for fname in ("favicon.png", "sam.jpeg", "bia.jpeg", "rachit.jpeg"):
        check(f"images/{fname} exists", (ROOT / "images" / fname).is_file())
    check(
        "no leftover aristotle-mockup.html",
        not (ROOT / "aristotle-mockup.html").exists(),
    )


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
    # Both are valid during launch transition: aristotletechnology.com (current
    # live domain) and thearistotle.ai (target domain on the redesign branch).
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
        "CNAME ends with newline (GH Pages convention)",
        raw.endswith(b"\n"),
        f"last bytes: {raw[-5:]!r}",
    )
    check(
        "CNAME is valid domain syntax",
        bool(re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", text)),
        f"got {text!r}",
    )


def test_html_head(p: IDCollector) -> None:
    print("\n[3] HTML head")
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


def test_anchors(p: IDCollector) -> None:
    print("\n[4] Anchor integrity")
    ids = set(p.ids)
    check("no duplicate IDs", len(p.ids) == len(ids), f"dupes: {[i for i,c in Counter(p.ids).items() if c>1]}")
    # Placeholder anchors that will become real URLs at launch
    known_placeholders = {"#meet", "#scan", "#privacy", "#terms", "#careers", "#linkedin"}
    anchors = [h for h in p.hrefs if h.startswith("#") and h != "#"]
    real_anchors = [a for a in anchors if a not in known_placeholders]
    missing = [a for a in real_anchors if a[1:] not in ids]
    check(
        f"all {len(real_anchors)} real internal anchors resolve",
        not missing,
        f"missing IDs: {sorted(set(missing))}",
    )
    placeholders_used = [a for a in anchors if a in known_placeholders]
    if placeholders_used:
        print(
            f"  \033[33m![/m] {len(placeholders_used)} placeholder anchors still in use "
            f"(replace before launch): {sorted(set(placeholders_used))}"
        )
    check("no empty hrefs", "" not in p.hrefs)
    check("no href='#' (lazy placeholder)", "#" not in p.hrefs, "found bare '#' link")
    check("no javascript: URLs", not any(h.lower().startswith("javascript:") for h in p.hrefs))


def test_images(p: IDCollector) -> None:
    print("\n[5] Images")
    for src, alt in p.imgs:
        if src.startswith(("http://", "https://", "data:")):
            continue
        path = ROOT / src
        check(f"image file exists: {src}", path.is_file())
        check(f"image has alt text: {src}", bool(alt.strip()), f"alt={alt!r}")


def test_required_sections(p: IDCollector) -> None:
    print("\n[6] Required sections present")
    text = INDEX.read_text(encoding="utf-8")
    expected_h2 = [
        ("comparison", "Old Consulting Model"),
        ("funnel", "Compounding Growth"),
        ("product", "Strategy Meets"),
        ("offerings", "Our Offerings"),
        ("credibility", "Decades of Expertise"),
        ("sectors", "Various Sectors"),
        ("cases", "Proven Results"),
        ("insights", "Insights"),
        ("leadership", "Who We Are"),
        ("qa", "Q&"),
    ]
    h2_text = " | ".join(p.section_h2s)
    for label, needle in expected_h2:
        check(f"section <{label}> headline contains {needle!r}", needle in h2_text, f"got: {h2_text}")

    expected_ids = ["offerings", "cases", "insights", "team"]
    for sid in expected_ids:
        check(f"section id='{sid}' exists", sid in set(p.ids))


def test_design_tokens() -> None:
    print("\n[7] Design tokens (plan-spec)")
    text = INDEX.read_text(encoding="utf-8")
    expected = {
        "--bg: #F7F8FB": "background light",
        "--navy: #0A2540": "navy",
        "--ink: #1A1A2E": "ink primary",
        "--ink-muted: #4A5568": "ink muted",
        "--line: #E6EAF2": "border",
        "--accent: #2E4BDB": "accent",
    }
    for token, label in expected.items():
        # tolerate optional whitespace differences
        pattern = re.escape(token).replace(r"\ ", r"\s*")
        check(f"{label} token: {token}", bool(re.search(pattern, text, re.IGNORECASE)))


def test_content_invariants() -> None:
    print("\n[8] Content invariants & regressions")
    text = INDEX.read_text(encoding="utf-8")

    # Stat band
    check("stat band: '40x'", ">40x<" in text or "40x" in text)
    check("stat band: '<6 wks'", "&lt;6 wks" in text or "<6 wks" in text)
    check("stat band: '$500M+'", "$500M+" in text)
    check("stat band: '25+ yrs'", "25+ yrs" in text)
    # Only flag 'No upfront fees' if it appears INSIDE the stat-band block
    stat_band = re.search(r'<section class="stat-band">.*?</section>', text, re.DOTALL)
    stat_band_text = stat_band.group(0) if stat_band else ""
    check(
        "regression: 'No upfront fees' removed from stat band",
        "No upfront fees" not in stat_band_text,
    )

    # Leadership
    check("Sam Garg present", "Sam Garg" in text)
    check("Bia Abramof present", "Bia Abramof" in text)
    check("Rachit Agarwal present", "Rachit Agarwal" in text)
    check("regression: no 'BlackRock' anywhere", "BlackRock" not in text and "Blackrock" not in text)

    # Hero dual CTA
    check("Hero CTA 1: 'Book a Meeting'", "Book a Meeting" in text)
    check("Hero CTA 2: 'See Case Studies'", "See Case Studies" in text)

    # Mobile sticky CTA
    check("mobile sticky CTA element present", 'id="mobileCta"' in text)

    # Comparison table column rename
    check("comparison: 'DIY / Internal' column present", "DIY / Internal" in text or "DIY/Internal" in text)
    check("comparison: 'No Advisor' column removed", "No Advisor" not in text)

    # Product headline
    check("product headline updated to 'AI Systems'", "AI Systems" in text)


def test_structural_counts() -> None:
    print("\n[9] Structural counts")
    text = INDEX.read_text(encoding="utf-8")

    funnel_rows = len(re.findall(r'class="funnel-row(?:[^"]*)"', text))
    check(f"funnel has 6 stages (got {funnel_rows})", funnel_rows == 6)

    stat_cells = len(re.findall(r'<div class="stat">', text))
    check(f"stat band has 4 cells (got {stat_cells})", stat_cells == 4)

    sectors = len(re.findall(r'<div class="sector">', text))
    check(f"sectors grid has 6 tiles (got {sectors})", sectors == 6)

    qa_items = len(re.findall(r"<details class=\"qa-item\">", text))
    check(f"Q&A has 6 entries (got {qa_items})", qa_items == 6)

    offerings = len(re.findall(r'<div class="offering-card">', text))
    check(f"offerings has 4 cards (got {offerings})", offerings == 4)

    cases = len(re.findall(r'<div class="case-card">', text))
    check(f"case studies has 4 cards (got {cases})", cases == 4)

    insights = len(re.findall(r'<div class="insight-card">', text))
    check(f"insights has 3 cards (got {insights})", insights == 3)

    leaders = len(re.findall(r'<div class="leader-card">', text))
    check(f"leadership has 3 cards (got {leaders})", leaders == 3)

    # Comparison table: header has 5 ths (1 empty + 4 cols), each row has 5 tds (label + 4 cells)
    # Match <th> or <th ...> but NOT <thead>
    header_ths = len(re.findall(r"<th(?:\s+[^>]*)?>", text.split("</thead>")[0]))
    check(f"comparison header has 5 cells (got {header_ths})", header_ths == 5)
    body_rows = re.findall(r"<tr>(.*?)</tr>", text.split("</tbody>")[0].split("<tbody>")[-1], re.DOTALL)
    for i, row in enumerate(body_rows):
        td_count = len(re.findall(r"<td[^>]*>", row))
        check(f"comparison row {i+1} has 5 cells", td_count == 5, f"got {td_count}")


def test_no_placeholders() -> None:
    print("\n[10] No placeholder leftovers")
    text = INDEX.read_text(encoding="utf-8")
    forbidden = ["lorem ipsum", "TODO", "FIXME", "XXX:", "PLACEHOLDER"]
    for needle in forbidden:
        check(f"no '{needle}'", needle.lower() not in text.lower())


def test_balanced_tags(p: IDCollector) -> None:
    print("\n[11] Tag balance")
    check("no unbalanced section/div/nav/footer", not p.tags_open, f"left open: {p.tags_open}")
    check("HTML parser had no errors", not p.errors, f"errors: {p.errors[:3]}")
    # <style> and </style> count
    text = INDEX.read_text(encoding="utf-8")
    check("<style> tags balanced", text.count("<style>") == text.count("</style>"))
    check("<script> tags balanced", text.count("<script>") == text.count("</script>"))


def test_online() -> None:
    print("\n[12] Online checks (raw.githubusercontent.com)")
    branch_url = (
        "https://raw.githubusercontent.com/ragarwal23/ragarwal.io/"
        "eilla_based_redesign/index.html"
    )
    main_cname_url = (
        "https://raw.githubusercontent.com/ragarwal23/ragarwal.io/main/CNAME"
    )
    try:
        with urllib.request.urlopen(branch_url, timeout=15) as r:
            remote = r.read()
        check("redesign branch index.html fetched", True)
        local = INDEX.read_bytes()
        check(
            "deployed branch index.html matches local",
            remote == local,
            f"local={len(local)}B remote={len(remote)}B",
        )
    except Exception as e:
        check("redesign branch index.html fetched", False, str(e))

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

    # Best-effort live-site check; allowed to fail if DNS not yet pointed.
    live = "https://thearistotle.ai/"
    try:
        with urllib.request.urlopen(live, timeout=10) as r:
            status = r.status
            body = r.read(4096).decode("utf-8", errors="replace")
        check(
            f"live site {live} returned 200",
            status == 200,
            f"status={status}",
        )
        check(
            "live site is the Aristotle page",
            "Aristotle" in body or "ARISTOTLE" in body,
            "headline marker missing",
        )
    except Exception as e:
        # Soft warning, not a failure — DNS / cert may not be ready yet
        print(f"  \033[33m![/m] live site {live} not yet reachable: {e}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--online", action="store_true")
    args = ap.parse_args()

    print(f"Aristotle site checks — repo: {ROOT}")

    p = parse()
    test_files_exist()
    test_cname()
    test_html_head(p)
    test_anchors(p)
    test_images(p)
    test_required_sections(p)
    test_design_tokens()
    test_content_invariants()
    test_structural_counts()
    test_no_placeholders()
    test_balanced_tags(p)
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
