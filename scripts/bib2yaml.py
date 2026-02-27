#!/usr/bin/env python3
"""Convert a BibTeX file into _data/publications.yml.

This is designed for an easy workflow:
1) Export/update publications in BibTeX (e.g., from Google Scholar, Zotero, or your reference manager).
2) Save to data/publications.bib
3) Run: python3 scripts/bib2yaml.py

No external dependencies required (very small BibTeX parser included).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "data" / "publications.bib"
OUT = ROOT / "_data" / "publications.yml"

ENTRY_RE = re.compile(r"@(?P<type>\w+)\s*\{\s*(?P<key>[^,]+)\s*,(?P<body>.*?)\n\}\s*", re.S)
FIELD_RE = re.compile(r"(?P<field>\w+)\s*=\s*(?P<value>\{.*?\}|\".*?\")\s*,?\s*", re.S)


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


def bib_to_publications(entries: List[Dict[str, str]]) -> List[Dict[str, object]]:
    pubs: List[Dict[str, object]] = []
    for e in entries:
        year = e.get("year", "")
        title = e.get("title", "").replace("{", "").replace("}", "")
        authors = e.get("author", "")
        venue = e.get("journal") or e.get("booktitle") or e.get("publisher") or ""

        doi = e.get("doi")
        url = e.get("url")

        pub: Dict[str, object] = {
            "year": int(year) if year.isdigit() else year,
            "title": title,
            "authors": authors,
            "venue": venue,
        }
        if doi:
            pub["doi"] = doi
        if url and (not doi or "doi.org" not in url):
            pub["url"] = url
        pubs.append(pub)

    # Sort by year descending when possible
    def sort_key(p):
        y = p.get("year")
        if isinstance(y, int):
            return y
        if isinstance(y, str) and y.isdigit():
            return int(y)
        return -1

    pubs.sort(key=sort_key, reverse=True)
    return pubs


def dump_yaml(pubs: List[Dict[str, object]]) -> str:
    def esc(s: str) -> str:
        # Escape backslashes first, then quotes (YAML double-quoted style)
        return str(s).replace("\\", "\\\\").replace('"', '\\"')

    def dump_list(items) -> str:
        # YAML inline list: ["a", "b", "c"]
        return "[{}]".format(", ".join(f'"{esc(x)}"' for x in items))

    lines: List[str] = []
    lines.append("# Generated from data/publications.bib")
    for p in pubs:
        lines.append("-")
        for k in ["year", "title", "authors", "venue", "doi", "url", "pdf", "tags"]:
            if k not in p:
                continue
            v = p[k]
            if isinstance(v, list):
                lines.append(f"  {k}: {dump_list(v)}")
            else:
                lines.append(f'  {k}: "{esc(v)}"')
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    if not BIB.exists():
        raise SystemExit(f"BibTeX file not found: {BIB} (create it, then rerun)")

    text = BIB.read_text(encoding="utf-8", errors="ignore")
    entries = parse_bibtex(text)
    pubs = bib_to_publications(entries)
    OUT.write_text(dump_yaml(pubs), encoding="utf-8")
    print(f"Wrote {OUT} with {len(pubs)} publications")


if __name__ == "__main__":
    main()
