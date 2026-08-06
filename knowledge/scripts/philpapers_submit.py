#!/usr/bin/env python3
"""
PhilPapers Bulk Submission Guide & Automation
===============================================
How to get ALL QNFO Zenodo records indexed by PhilPapers.

TWO PATHS TO PHILPAPERS:

PATH 1: Organic Discovery (what happened to QUNTUF/QUNSAI)
  Zenodo -> DataCite -> CrossRef -> PhilPapers crawler
  Requirements: abstract + philosophy keywords + ORCID on Zenodo
  Timeline: days to weeks (depends on CrossRef/PhilPapers crawl cycles)

PATH 2: Direct Submission (guaranteed, faster)
  a) PhilArchive (https://philarchive.org) — PhilPapers' own preprint server
     Upload PDF + metadata -> indexed within days
  b) PhilPapers direct entry (https://philpapers.org/submit)
     Manual form submission per paper
  c) Bulk import via PhilPapers editor account
     Request editor status -> import multiple records

AUTOMATION SCRIPT:
  This script generates a CSV for PhilPapers bulk import
  and a JSON manifest suitable for PhilArchive API upload.

USAGE:
  python philpapers_submit.py --action generate-csv
  python philpapers_submit.py --action generate-manifest
"""

import json
import csv
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# KNOWN INDEXED PAPERS (for reference)
# ═══════════════════════════════════════════════════════════════

INDEXED_PAPERS = [
    {
        "philpapers_id": "QUNTUF",
        "title": "The Ultrametric Foundation: A Unified Thesis on Number, Time, Knowledge, and Computation",
        "doi": "10.5281/zenodo.21208346",
        "zenodo_url": "https://zenodo.org/records/21208346",
        "year": "2026",
        "abstract": "Positional notation is inherently an ultrametric tree of nested cycles. The Archimedean line is a derived abstraction. Recovering the native ultrametric resolves cascading errors across number, time, knowledge, and computation.",
        "keywords": ["ultrametric", "p-adic", "positional notation", "epistemology",
                      "cyclic time", "Zitterbewegung", "quantum computing", "Laws of Form"],
        "category": "Philosophy of Physical Science",
    },
    {
        "philpapers_id": "QUNSAI",
        "title": "Scaffolds and Invariants: An Epistemic Hygiene Audit of pi, Number Bases, and Geometric Centers",
        "doi": "10.5281/zenodo.21255344",
        "zenodo_url": "https://zenodo.org/records/21255344",
        "year": "2026",
        "abstract": "This paper applies epistemic hygiene -- the systematic separation of human-imposed conventions (scaffolds) from relational structures that persist across representations (invariants) -- to the foundations of mathematics. Through five critical experiments, we demonstrate that pi-the-constant is an invariant forced by the complex exponential period, while its association with planar circles, decimal digits, and Pi Day are pure scaffolds.",
        "keywords": ["epistemic hygiene", "scaffold", "invariant", "pi",
                      "number bases", "positional notation", "spherical geometry",
                      "philosophy of mathematics", "center-free geometry"],
        "category": "Philosophy of Mathematics",
    },
]

# PhilPapers subject categories relevant to QNFO work
QNFO_CATEGORIES = [
    "Philosophy of Physical Science",
    "Philosophy of Mathematics",
    "Metaphysics",
    "Epistemology",
    "General Philosophy of Science",
    "Philosophy of Computing and Information",
    "Philosophy of Probability",
    "Foundations of Physics",
    "Logic and Philosophy of Logic",
]


def generate_philpapers_csv(papers, output="philpapers_import.csv"):
    """Generate a CSV for PhilPapers bulk import."""

    fieldnames = [
        "title", "author", "year", "doi", "url", "abstract",
        "keywords", "category", "type", "publication_status"
    ]

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for paper in papers:
            row = {
                "title": paper.get("title", ""),
                "author": "Rowan Brad Quni-Gudzinas",
                "year": paper.get("year", "2026"),
                "doi": paper.get("doi", ""),
                "url": paper.get("zenodo_url", ""),
                "abstract": paper.get("abstract", ""),
                "keywords": "; ".join(paper.get("keywords", [])),
                "category": paper.get("category", "Philosophy of Physical Science"),
                "type": "preprint",
                "publication_status": "unpublished",
            }
            writer.writerow(row)

    print(f"Generated PhilPapers CSV: {output}")
    print(f"  {len(papers)} papers")
    print()
    print("NEXT STEPS:")
    print("  1. Go to https://philpapers.org/submit")
    print("  2. Or email editors@philpapers.org with CSV for bulk import")
    print("  3. Or upload individual papers to https://philarchive.org")
    return output


def generate_philarchive_manifest(papers, output="philarchive_manifest.json"):
    """Generate a JSON manifest for PhilArchive API upload."""

    manifest = {
        "submitter": {
            "name": "Rowan Brad Quni-Gudzinas",
            "orcid": "0009-0002-4317-5604",
            "email": "SET_YOUR_EMAIL",
        },
        "papers": []
    }

    for paper in papers:
        manifest["papers"].append({
            "title": paper.get("title", ""),
            "authors": [{"name": "Rowan Brad Quni-Gudzinas", "orcid": "0009-0002-4317-5604"}],
            "abstract": paper.get("abstract", ""),
            "doi": paper.get("doi", ""),
            "year": paper.get("year", "2026"),
            "keywords": paper.get("keywords", []),
            "categories": [paper.get("category", "Philosophy of Physical Science")],
            "type": "preprint",
            "license": "CC-BY-4.0",
        })

    with open(output, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Generated PhilArchive manifest: {output}")
    print(f"  {len(manifest['papers'])} papers")
    return output


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PhilPapers Submission Tools")
    parser.add_argument("--action", choices=["generate-csv", "generate-manifest", "info", "strategy"],
                       default="strategy")
    args = parser.parse_args()

    if args.action == "strategy" or args.action == "info":
        print("=" * 70)
        print("  PHILPAPERS SUBMISSION STRATEGY")
        print("=" * 70)
        print()
        print("HOW YOUR PAPERS GOT INDEXED:")
        print("  Zenodo registers DOI -> DataCite metadata -> CrossRef propagation")
        print("  PhilPapers crawler finds papers with philosophy-domain keywords")
        print()
        print("WHY ONLY 2 OF ~293 GOT INDEXED:")
        print("  ✓ QUNTUF: has keywords (epistemology, ultrametric, etc.) + abstract")
        print("  ✓ QUNSAI: has keywords (philosophy of mathematics, etc.) + abstract")
        print("  ✗ Others: missing keywords, missing abstracts, or both")
        print()
        print("IMMEDIATE ACTIONS (ranked by ROI):")
        print()
        print("  1. ORCID LINKING (5 min)")
        print("     Your ORCID: 0009-0002-4317-5604")
        print("     Action: Add ORCID to ALL Zenodo records")
        print("     Effect: DataCite propagates ORCID -> all aggregators link to you")
        print("     Impact: ★★★★★")
        print()
        print("  2. KEYWORD INJECTION (30 min with script)")
        print("     Add philosophy-domain keywords to all 293 records:")
        print("     - 'philosophy of physics', 'epistemology', 'metaphysics'")
        print("     - 'foundations of quantum mechanics', 'ontology'")
        print("     - 'philosophy of mathematics', 'consilience'")
        print("     Use: python zenodo_philpapers_optimizer.py --fix --token YOUR_TOKEN")
        print("     Impact: ★★★★★")
        print()
        print("  3. ABSTRACT ENRICHMENT (1-2 hours)")
        print("     Ensure every record has 200+ word abstract with philosophy terms")
        print("     The two indexed papers both have substantial abstracts")
        print("     Impact: ★★★★☆")
        print()
        print("  4. PHILARCHIVE DIRECT UPLOAD (1 hour for top 10 papers)")
        print("     Upload to https://philarchive.org -> guaranteed indexing in days")
        print("     Prioritize papers with philosophy-heavy content")
        print("     Impact: ★★★★★ (instant)")
        print()
        print("  5. CROSS-REFERENCING (ongoing)")
        print("     Add references/related_identifiers between your Zenodo papers")
        print("     Builds citation graph -> PhilPapers values citation networks")
        print("     Impact: ★★★☆☆")
        print()
        print("  6. ZENODO COMMUNITY (5 min)")
        print("     Add all papers to a Zenodo community (e.g., 'qnfo')")
        print("     Community pages are crawled by aggregators")
        print("     Impact: ★★★☆☆")
        print()
        print("  7. GOOGLE SCHOLAR + SEMANTIC SCHOLAR (30 min)")
        print("     Claim author profiles on both platforms")
        print("     Link ORCID -> auto-sync from Zenodo")
        print("     These feed into discovery chains that reach PhilPapers")
        print("     Impact: ★★★★☆")
        print("=" * 70)

    elif args.action == "generate-csv":
        generate_philpapers_csv(INDEXED_PAPERS)

    elif args.action == "generate-manifest":
        generate_philarchive_manifest(INDEXED_PAPERS)


if __name__ == "__main__":
    main()
