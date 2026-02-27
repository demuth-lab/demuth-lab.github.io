#!/usr/bin/env python3
"""
Convert data/publications.bib -> _data/publications.yml
and conservatively add missing DOIs via Crossref.

Conservative policy:
- Only add DOI if title similarity is high AND year matches (if present)
  AND first-author surname matches (if present).
- Otherwise leave DOI blank and log to a report.
"""

from __future__ import annotations

import json
import re
import time
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "data" / "publications.bib"
OUT = ROOT / "_data" / "publications.yml"

CACHE_DIR = ROOT / ".cache"
CACHE_FILE = CACHE_DIR / "crossref_doi_cache.json"
REPORT = ROOT / "doi_lookup_report.txt"

# --- Very small BibTeX parser (good enough for Scholar exports) ---
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


# --- DOI lookup (Crossref) ---
def norm_title(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\{|\}", "", s)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, norm_title(a), norm_title(b)).ratio()


def first_author_surname(authors: str) -> str:
    # BibTeX author format often "Last, First and Last2, First2 ..."
    if not authors:
        return ""
    first = authors.split(" and ")[0].strip()
    if "," in first:
        return first.split(",")[0].strip().lower()
    # If "First Last"
    parts = first.split()
    return parts[-1].strip().lower() if parts else ""


def crossref_candidates(
    title: str, year: Optional[int], author_surname: str, mailto: Optional[str]
) -> List[dict]:
    url = "https://api.crossref.org/works"
    params = {
        "rows": 5,
        "query.bibliographic": title,
        # These two help a bit, but Crossref can be fuzzy anyway:
        "select": "DOI,title,author,issued,container-title,type,score,URL",
    }
    if author_surname:
        params["query.author"] = author_surname

    headers = {"User-Agent": "demuth-lab-site/1.0 (GitHub Actions)"}
    if mailto:
        params["mailto"] = mailto

    r = requests.get(url, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("message", {}).get("items", [])


def extract_year(item: dict) -> Optional[int]:
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
    first = authors[0]
    fam = (first.get("family") or "").strip().lower()
    return fam == target_surname


def best_doi_conservative(
    title: str,
    year: Optional[int],
    author_surname: str,
    mailto: Optional[str],
    min_sim: float = 0.92,
) -> Tuple[Optional[str], Optional[str], str]:
    """
    Returns: (doi, doi_url, reason)
    """
    items = crossref_candidates(title, year, author_surname, mailto)
    best = None
    best_sim = 0.0

    for it in items:
        it_title = (it.get("title") or [""])[0]
        sim = title_similarity(title, it_title)
        it_year = extract_year(it)

        # Conservative filters:
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
        return None, None, "no high-confidence match"

    doi = best.get("DOI")
    if not doi:
        return None, None, "match found but DOI missing in Crossref record"

    return doi, f"https://doi.org/{doi}", f"accepted (title_sim={best_sim:.3f})"


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


def bib_to_publications(entries: List[Dict[str, str]]) -> List[Dict[str, object]]:
    cache = load_cache()
    report_lines: List[str] = []
    pubs: List[Dict[str, object]] = []

    # Optional: set this to your email to be polite to Crossref
    # (or leave blank; it still works, but mailto is recommended)
    MAILTO = "jpdemuth@uta.edu"

    for e in entries:
        year_raw = e.get("year", "")
        year = int(year_raw) if year_raw.isdigit() else None

        title = e.get("title", "").replace("{", "").replace("}", "").strip()
        authors = e.get("author", "").strip()
        venue = (e.get("journal") or e.get("booktitle") or e.get("publisher") or "").strip()

        doi = (e.get("doi") or "").strip()
        url = (e.get("url") or "").strip()

        # If DOI missing, try Crossref (conservative)
        if not doi and title:
            cache_key = f"{norm_title(title)}|{year or ''}|{first_author_surname(authors)}"
            if cache_key in cache:
                cached = cache[cache_key]
                doi = cached.get("doi") or ""
                if doi:
                    report_lines.append(f"[CACHED] DOI added for: {title} -> {doi}")
                else:
                    report_lines.append(f"[CACHED] No DOI for: {title}")
            else:
                try:
                    doi_found, doi_url, reason = best_doi_conservative(
                        title=title,
                        year=year,
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

                # Be polite to Crossref
                time.sleep(0.2)

        pub: Dict[str, object] = {
            "year": int(year_raw) if year_raw.isdigit() else year_raw,
            "title": title,
            "authors": authors,
            "venue": venue,
        }

        if doi:
            pub["doi"] = doi
            pub["doi_url"] = f"https://doi.org/{doi}"
        elif url:
            pub["url"] = url

        pubs.append(pub)

    # Sort newest first if possible
    def sort_key(p: Dict[str, object]) -> int:
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
        raise SystemExit(f"BibTeX file not found: {BIB} (create it, then rerun)")

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
    print(f"Cache: {CACHE_FILE} (to reduce API calls)")


if __name__ == "__main__":
    main()
