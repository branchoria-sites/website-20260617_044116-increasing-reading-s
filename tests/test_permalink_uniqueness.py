"""Falsifier for the increasing-re-852ca6 subtopic-index permalink collision cure.

Before the cure, 72 level-3 ``*_index.md`` files across 12 subtopic families
shared 12 truncated permalinks (six claimants each), so only one document per
family was reachable at its URL and five were shadowed. The cure keeps the
live winner at each shared route and gives every shadowed index a unique
``-<slugified index title>`` suffixed permalink (hex fragment fallback when
two cured titles slugify alike).
"""
import io
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"
FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
PERMALINK = re.compile(r"^permalink:\s*[\"']?([^\s\"'#]+)[\"']?\s*$", re.M)


def page_permalinks():
    out = {}
    for p in PAGES.glob("*.md"):
        m = FRONT_MATTER.match(p.read_text(encoding="utf-8", errors="replace"))
        if not m:
            continue
        pm = PERMALINK.search(m.group(1))
        if pm:
            out[p.name] = pm.group(1)
    return out


FAMILIES = [
    "dense-materia", "honest-skimmi", "inner-voice-r", "measure-readi",
    "phrase-readin", "purpose-based", "reading-speed", "repeated-read",
    "rereading-reg", "rsvp-reading", "speed-reading", "vocabulary-ba",
]
SHARED_SLUGS = {f"/increasing-re-852ca6-{f}/" for f in FAMILIES}

EXPECTED_CURED = {
    "/increasing-re-852ca6-dense-texts/",
    "/increasing-re-852ca6-expertise/",
    "/increasing-re-852ca6-legalese/",
    "/increasing-re-852ca6-paper-preview/",
    "/increasing-re-852ca6-signal-words/",
    "/increasing-re-852ca6-visual-span/",
    "/increasing-re-852ca6-baseball-study/",
    "/increasing-re-852ca6-rereading-c42398/",
}


class TestPermalinkUniqueness(unittest.TestCase):
    def test_all_permalinks_unique(self):
        pls = page_permalinks()
        counts = Counter(pls.values())
        dups = {k: v for k, v in counts.items() if v > 1}
        owners = {k: sorted(n for n, v in pls.items() if v == k) for k in dups}
        self.assertEqual({}, owners)

    def test_shared_family_slugs_claimed_by_one_document(self):
        pls = page_permalinks()
        for slug in SHARED_SLUGS:
            owners = sorted(n for n, v in pls.items() if v == slug)
            self.assertEqual(1, len(owners), f"{slug} claimed by {owners}")

    def test_expected_cured_index_routes_exist(self):
        pls = set(page_permalinks().values())
        self.assertEqual(set(), EXPECTED_CURED - pls)

    def test_manifest_canonical_urls_match_front_matter(self):
        manifest = json.loads(io.open(ROOT / "phoenix-manifest.json", encoding="utf-8").read())
        stem_to_pl = {p[:-3]: v for p, v in page_permalinks().items()}
        bad = []
        for page in manifest.get("pages", []):
            lid = page.get("logical_id", "")
            cu = page.get("canonical_url", "")
            if lid in stem_to_pl and cu.endswith("/"):
                route = cu[cu.index(".com") + 4:]
                if route != stem_to_pl[lid]:
                    bad.append((lid, route, stem_to_pl[lid]))
        self.assertEqual([], bad)

    def test_index_bodies_link_only_existing_routes(self):
        existing = set(page_permalinks().values())
        dangling = []
        for p in PAGES.glob("*_index.md"):
            for m in re.finditer(r"\{\{\s*'(/[^']*?)'\s*\|\s*relative_url", p.read_text(encoding="utf-8", errors="replace")):
                if m.group(1) not in existing:
                    dangling.append((p.name, m.group(1)))
        self.assertEqual([], dangling)


if __name__ == "__main__":
    unittest.main()
