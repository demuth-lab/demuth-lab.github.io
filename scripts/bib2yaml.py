#!/usr/bin/env python3
"""
Convert data/publications.bib -> _data/publications.yml

What this script does:
- Parses Scholar-style BibTeX (lightweight parser, no external bibtex libs).
- If DOI is missing, uses Crossref conservatively to find it (high confidence only).
- Detects preprints (bioRxiv/medRxiv/arXiv/Research Square) and sets type: preprint.
- Merges manual per-publication extras from data/publication_extras.yml (software links, pdf, tags, overrides).
- Applies curated topic tags (many-to-many) from data/topics.yml keyed by DOI.
- Writes cache/report files to speed future runs:
    .cache/crossref_doi_cache.json
    doi_lookup_report.txt

Dependencies:
  pip install requests pyyaml
"""

from __future__ import annotations

import json
import re
import time
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]

BIB = ROOT / "data" / "publications.bib"
OUT = ROOT / "_data" / "publications.yml"

EXTRAS = ROOT / "_data" / "publication_extras.yml"
TOPICS = ROOT / "_data" / "topics.yml"

CACHE_DIR = ROOT / ".cache"
CACHE_FILE = CACHE_DIR / "crossref_doi_cache.json"
REPORT = ROOT / "doi_lookup_report.txt"

# -----------------------------
# Minimal BibTeX parser (Scholar-friendly)
# -----------------------------
ENTRY_RE = re.compile(
    r"@(?P<type>\w+)\s*\{\s*(?P<key>[^,]+)\s*,(?P<body>.*?)\n\}\s*",
    re.S,
)
FIELD_RE = re.compile(
    r"(?P<field>\w+)\s*=\s*(?P<value>\{.*?\}|\".*?\")\s*,?\s*",
    re.S,
)


def _clean(v: str) -> str:
    v = v.strip()
    if (v.startswith("{") and v.endswith("}")) or (v.startswith('"') and v.endswith('"')):
        v = v[1:-1]
    v = re.sub(r"\s+", " ", v).strip()
    return v


def parse_bibtex(text: str) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for m in ENTRY_RE.finditer(text):
        body = m.group("body")
        d: Dict[str, str] = {"_type": m.group("type"), "_key": m.group("key")}
        for fm in FIELD_RE.finditer(body):
            d[fm.group("field").lower()] = _clean(fm.group("value"))
        entries.append(d)
    return entries


# -----------------------------
# Helpers
# -----------------------------
def norm_title(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"\{|\}", "", s)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def slugify_title(s: str) -> str:
    s = norm_title(s).replace(" ", "-")
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def make_fallback_key(year: Any, title: str) -> str:
    y = str(year).strip() if year is not None else ""
    return f"{y}|{slugify_title(title)}"


def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, norm_title(a), norm_title(b)).ratio()


def first_author_surname(authors: str) -> str:
    # BibTeX authors are usually "Last, First and Last, First ..."
    if not authors:
        return ""
    first = authors.split(" and ")[0].strip()
    if "," in first:
        return first.split(",")[0].strip().lower()
    parts = first.split()
    return parts[-1].strip().lower() if parts else ""


def load_cache() -> Dict[str, dict]:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache: Dict[str, dict]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def load_extras() -> Dict[str, dict]:
    """
    Manual annotations keyed by DOI OR fallback key "<year>|<slugified-title>".
    If YAML is invalid, we warn and continue (do not fail the build).
    """
    if not EXTRAS.exists():
        return {}
    try:
        data = yaml.safe_load(EXTRAS.read_text(encoding="utf-8")) or {}
    except Exception as ex:
        print(f"WARNING: Could not parse {EXTRAS}: {ex}")
        return {}
    if not isinstance(data, dict):
        print(f"WARNING: {EXTRAS} must be a top-level mapping; ignoring.")
        return {}
    return data


def load_topics() -> Dict[str, dict]:
    """
    Curated topics file mapping:
      topic-id:
        label: "Human Label"
        dois:
          - "10.xxxx/yyy"
    A DOI may appear under multiple topics.
    If YAML is invalid, we warn and continue (do not fail the build).
    """
    if not TOPICS.exists():
        return {}
    try:
        data = yaml.safe_load(TOPICS.read_text(encoding="utf-8")) or {}
    except Exception as ex:
        print(f"WARNING: Could not parse {TOPICS}: {ex}")
        return {}
    if not isinstance(data, dict):
        print(f"WARNING: {TOPICS} must be a top-level mapping; ignoring.")
        return {}
    return data


def topic_tags_for_doi(doi: str, topics: Dict[str, dict]) -> List[str]:
    if not doi:
        return []
    d = doi.strip().lower()
    tags: List[str] = []
    for topic_id, info in topics.items():
        if not isinstance(info, dict):
            continue
        dois = info.get("dois") or []
        if not isinstance(dois, list):
            continue
        dois_norm = [str(x).strip().lower() for x in dois]
        if d in dois_norm:
            tags.append(str(topic_id))
    return tags


# -----------------------------
# Preprint detection (includes Research Square)
# -----------------------------
PREPRINT_VENUE_KEYWORDS = ["biorxiv", "medrxiv", "arxiv", "research square"]
PREPRINT_URL_KEYWORDS = ["biorxiv.org", "medrxiv.org", "arxiv.org", "researchsquare.com"]


def is_preprint_entry(entry: Dict[str, str], venue: str, url: str) -> bool:
    v = (venue or "").lower()
    u = (url or "").lower()

    if any(k in v for k in PREPRINT_VENUE_KEYWORDS):
        return True
    if any(k in u for k in PREPRINT_URL_KEYWORDS):
        return True

    # BibTeX arXiv-style fields
    arch = (entry.get("archiveprefix") or "").lower()
    if arch == "arxiv":
        return True

    return False


# -----------------------------
# Crossref DOI lookup (conservative)
# -----------------------------
def crossref_candidates(title: str, author_surname: str, mailto: Optional[str]) -> List[dict]:
    url = "https://api.crossref.org/works"
    params = {
        "rows": 5,
        "query.bibliographic": title,
        "select": "DOI,title,author,issued,container-title,type,score,URL",
    }
    if author_surname:
        params["query.author"] = author_surname
    if mailto:
        params["mailto"] = mailto

    headers = {"User-Agent": "demuth-lab-site/1.0 (GitHub Actions)"}
    r = requests.get(url, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json().get("message", {}).get("items", [])


def extract_year_from_crossref(item: dict) -> Optional[int]:
    issued = item.get("issued", {})
    parts = issued.get("date-parts", [])
    if parts and parts[0] and isinstance(parts[0][0], int):
        return parts[0][0]
    return None


def author_surname_matches(item: dict, target_surname: str) -> bool:
    if not target_surname:
        return True
    authors = item.get("author") or []
    if not authors:
        return False
    fam = (authors[0].get("family") or "").strip().lower()
    return fam == target_surname


def best_doi_conservative(
    title: str,
    year: Optional[int],
    author_surname: str,
    mailto: Optional[str],
    min_sim: float = 0.92,
) -> Tuple[Optional[str], str]:
    """
    Returns (doi, reason). Only accepts DOI if it's a high-confidence match.
    """
    items = crossref_candidates(title, author_surname, mailto)
    best = None
    best_sim = 0.0

    for it in items:
        it_title = (it.get("title") or [""])[0]
        sim = title_similarity(title, it_title)
        it_year = extract_year_from_crossref(it)

        if sim < min_sim:
            continue
        if year is not None and it_year is not None and it_year != year:
            continue
        if not author_surname_matches(it, author_surname):
            continue

        if sim > best_sim:
            best_sim = sim
            best = it

    if not best:
        return None, "no high-confidence match"

    doi = best.get("DOI")
    if not doi:
        return None, "match found but DOI missing in Crossref record"

    return str(doi).strip().lower(), f"accepted (title_sim={best_sim:.3f})"


# -----------------------------
# Merge extras + topics
# -----------------------------
def merge_extras(pub: Dict[str, Any], extras: Dict[str, dict]) -> None:
    """
    Extras can be keyed by:
      - DOI (preferred): "10.xxxx/yyy"
      - fallback: "<year>|<slugified-title>"

    Merge behavior:
      - scalar fields overwrite (pdf, url, type, venue, etc.)
      - tags: union (preserve pub order)
      - software: append
    """
    doi = (pub.get("doi") or "").strip().lower()
    fallback_key = make_fallback_key(pub.get("year"), pub.get("title", ""))

    extra: Optional[dict] = None
    if doi and doi in extras:
        extra = extras[doi]
    elif fallback_key in extras:
        extra = extras[fallback_key]

    if not extra or not isinstance(extra, dict):
        return

    # Scalars/other dict fields
    for k, v in extra.items():
        if k in ("tags", "software"):
            continue
        pub[k] = v

    # tags union
    if "tags" in extra and isinstance(extra["tags"], list):
        existing = pub.get("tags")
        if not isinstance(existing, list):
            existing = []
        for t in extra["tags"]:
            if t not in existing:
                existing.append(t)
        pub["tags"] = existing

    # software append
    if "software" in extra and isinstance(extra["software"], list):
        existing_sw = pub.get("software")
        if not isinstance(existing_sw, list):
            existing_sw = []
        pub["software"] = existing_sw + extra["software"]


def add_topic_tags(pub: Dict[str, Any], topics: Dict[str, dict]) -> None:
    doi = (pub.get("doi") or "").strip().lower()
    if not doi:
        return

    tags_to_add = topic_tags_for_doi(doi, topics)
    if not tags_to_add:
        return

    existing = pub.get("tags")
    if not isinstance(existing, list):
        existing = []

    for t in tags_to_add:
        if t not in existing:
            existing.append(t)

    pub["tags"] = existing


# -----------------------------
# Main conversion
# -----------------------------
def bib_to_publications(entries: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    cache = load_cache()
    extras = load_extras()
    topics = load_topics()

    report_lines: List[str] = []
    pubs: List[Dict[str, Any]] = []

    # Crossref polite-pool email (set to your email)
    MAILTO = "jpdemuth@uta.edu"

    for e in entries:
        year_raw = e.get("year", "").strip()
        year_int = int(year_raw) if year_raw.isdigit() else None

        title = e.get("title", "").replace("{", "").replace("}", "").strip()
        authors = e.get("author", "").strip()
        venue = (e.get("journal") or e.get("booktitle") or e.get("publisher") or "").strip()

        url = (e.get("url") or "").strip()
        doi = (e.get("doi") or "").strip().lower()

        # Default type
        pub_type = "preprint" if is_preprint_entry(e, venue, url) else "article"

        # Conservative DOI enrichment if missing
        if not doi and title:
            cache_key = f"{norm_title(title)}|{year_int or ''}|{first_author_surname(authors)}"
            if cache_key in cache:
                cached = cache[cache_key]
                doi = (cached.get("doi") or "").strip().lower()
                if doi:
                    report_lines.append(f"[CACHED] DOI added: {title} -> {doi}")
                else:
                    report_lines.append(f"[CACHED] No DOI: {title}")
            else:
                try:
                    doi_found, reason = best_doi_conservative(
                        title=title,
                        year=year_int,
                        author_surname=first_author_surname(authors),
                        mailto=MAILTO,
                    )
                    if doi_found:
                        doi = doi_found
                        report_lines.append(f"[OK] {reason}: {title} -> {doi}")
                        cache[cache_key] = {"doi": doi}
                    else:
                        report_lines.append(f"[SKIP] {reason}: {title}")
                        cache[cache_key] = {"doi": None, "reason": reason}
                except Exception as ex:
                    report_lines.append(f"[ERROR] {title}: {ex}")
                    cache[cache_key] = {"doi": None, "reason": str(ex)}

                time.sleep(0.2)  # polite delay

        pub: Dict[str, Any] = {
            "year": int(year_raw) if year_raw.isdigit() else year_raw,
            "title": title,
            "authors": authors,
            "venue": venue,
            "type": pub_type,
        }

        if doi:
            pub["doi"] = doi
        # Keep url if present (useful sometimes even if doi exists)
        if url and url != "":
            pub["url"] = url

        # Merge manual extras (software/pdf/tags/type overrides/etc.)
        merge_extras(pub, extras)

        # Apply curated topics by DOI (many-to-many)
        add_topic_tags(pub, topics)

        pubs.append(pub)

    # Sort newest first
    def sort_key(p: Dict[str, Any]) -> int:
        y = p.get("year")
        if isinstance(y, int):
            return y
        if isinstance(y, str) and y.isdigit():
            return int(y)
        return -1

    pubs.sort(key=sort_key, reverse=True)

    save_cache(cache)
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    return pubs


def main() -> None:
    if not BIB.exists():
        raise SystemExit(f"BibTeX file not found: {BIB}")

    text = BIB.read_text(encoding="utf-8", errors="ignore")
    entries = parse_bibtex(text)
    pubs = bib_to_publications(entries)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        yaml.safe_dump(pubs, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    print(f"Wrote {OUT} with {len(pubs)} publications")
    print(f"Wrote {REPORT} (DOI lookup report)")
    print(f"Cache: {CACHE_FILE}")


if __name__ == "__main__":
    main()
