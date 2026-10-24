"""Fetch the stage 2 corpus: titles and abstracts of openly licensed papers on drought indices.

The topic follows Sang's NCAR work (PDSI, SPI, SPEI). Candidates come from OpenAlex searches of titles and abstracts (a plain search matches full text and drifted
to papers on wildfire and mental health); a paper is
kept only if
- its title or abstract names a drought index (PDSI, Palmer, SPI, SPEI, or "drought index/indices"),
- its abstract has at least 80 words, and
- Crossref, the publisher's own record, lists a CC BY or CC BY-SA license (no NC, no ND). OpenAlex's own
  license field is not trusted on its own: in a sample of 8 it said cc-by for an Elsevier paper whose
  Crossref record has only a text-mining license, and for one with no license at all.

Each paper becomes one Markdown file: the title, the authors, the journal and year, the DOI, the license, and
the abstract. Files go in OUT/<license>/<docid>.md, so each license is one `p2 ingest` batch, and
OUT/sources.tsv maps every docid to its DOI and the Crossref license URL, for the manifest.

    uv run python scripts/fetch_drought_corpus.py ../p2-raw/drought --target 500
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

QUERIES = [
    "palmer drought severity index",
    "self-calibrating palmer drought severity index",
    "standardized precipitation evapotranspiration index",
    "standardized precipitation index drought",
    "drought index climate model projections",
    "drought index evapotranspiration thornthwaite penman-monteith",
    "drought indices comparison",
]
INDEX_TERMS = re.compile(r"\b(pdsi|scpdsi|palmer|spei|spi|drought (index|indices|indicator))\b", re.I)
CC = re.compile(r"creativecommons\.org/licenses/(by|by-sa)/(\d\.\d)", re.I)
PER_QUERY = 200  # candidates per query, most cited first


def get_json(url: str) -> dict:
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "p2-rag-system corpus fetch"}), timeout=60) as r:
                return json.load(r)
        except Exception as e:  # network hiccup or rate limit: back off and retry
            if attempt == 3:
                raise
            print(f"  retry after {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    return {}


def abstract(inverted: dict | None) -> str:
    if not inverted:
        return ""
    words = {}
    for word, positions in inverted.items():
        for p in positions:
            words[p] = word
    return " ".join(words[i] for i in sorted(words))


def openalex(query: str) -> list[dict]:
    out, cursor = [], "*"
    fields = "id,doi,title,publication_year,authorships,primary_location,abstract_inverted_index"
    while cursor and len(out) < PER_QUERY:
        url = (
            "https://api.openalex.org/works?filter=title_and_abstract.search:" + urllib.parse.quote(query)
            + ",best_oa_location.license:cc-by,has_abstract:true,type:article,has_doi:true"
            + f"&sort=cited_by_count:desc&per-page=100&select={fields}&cursor={urllib.parse.quote(cursor)}"
        )  # fmt: skip
        try:
            data = get_json(url)
        except Exception as e:  # OpenAlex refuses (401) once the shared free daily budget is spent
            print(f"  OpenAlex stopped this query: {e}", file=sys.stderr)
            break
        out += data.get("results", [])
        cursor = data.get("meta", {}).get("next_cursor")
        time.sleep(0.2)
    return out[:PER_QUERY]


def crossref_license(doi: str) -> str | None:
    """The CC BY or CC BY-SA license URL Crossref lists for a DOI (the version of record first), or None."""
    try:
        licenses = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi)).get("message", {}).get("license", [])
    except Exception:
        return None
    licenses.sort(key=lambda lic: lic.get("content-version") != "vor")
    for lic in licenses:
        url = lic.get("URL", "")
        if CC.search(url) and not re.search(r"-n[cd]", url, re.I):
            return url
    return None


def license_id(url: str) -> str:
    kind, version = CC.search(url).groups()
    return f"cc-{kind.lower()}-{version}"


def docid(doi: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", doi.lower()).strip("-")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--target", type=int, default=500)
    args = ap.parse_args()
    seen, kept, rows = set(), 0, []
    for query in QUERIES:
        works = openalex(query)
        print(f"{query!r}: {len(works)} candidates", file=sys.stderr)
        for w in works:
            if kept >= args.target:
                break
            doi = (w.get("doi") or "").replace("https://doi.org/", "")
            title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", w.get("title") or "")).strip()
            text = abstract(w.get("abstract_inverted_index"))
            if not doi or doi.lower() in seen or not title or len(text.split()) < 80 or not INDEX_TERMS.search(title + " " + text):
                continue
            seen.add(doi.lower())
            lic = crossref_license(doi)
            time.sleep(0.15)
            if not lic:
                continue
            authors = ", ".join(a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author"))
            source = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "unknown journal"
            ident = docid(doi)
            folder = args.out / license_id(lic)
            folder.mkdir(parents=True, exist_ok=True)
            body = (
                f"# {title}\n\n"
                f"Authors: {authors}\n"
                f"Published in {source}, {w.get('publication_year')}. DOI: {doi}. License: {lic}\n\n"
                f"{text}\n"
            )
            (folder / f"{ident}.md").write_text(body, encoding="utf-8", newline="\n")
            rows.append((ident, f"https://doi.org/{doi}", license_id(lic), lic))
            kept += 1
        print(f"  kept so far: {kept}", file=sys.stderr)
        if kept >= args.target:
            break
    with open(args.out / "sources.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("docid\tsource\tlicense\tcrossref_license\n")
        f.writelines("\t".join(r) + "\n" for r in rows)
    print(f"Kept {kept} papers in {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
