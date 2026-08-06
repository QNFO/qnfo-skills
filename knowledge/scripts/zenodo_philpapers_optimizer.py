#!/usr/bin/env python3
"""
Zenodo Bulk Metadata Optimizer — PhilPapers Discoverability Engine
===================================================================
Fixes metadata gaps across ALL QNFO Zenodo records to maximize
discoverability by PhilPapers, Google Scholar, Semantic Scholar, etc.

STRATEGY:
  Zenodo -> DataCite -> CrossRef -> PhilPapers crawler
  The trigger: abstract + philosophy-domain keywords + ORCID

USAGE:
  python zenodo_philpapers_optimizer.py --token ZENODO_API_TOKEN [--dry-run]

  Get your Zenodo API token at: https://zenodo.org/account/settings/applications/

  --dry-run: Only audit, don't modify anything
  --orcid 0009-0002-4317-5604  (override default ORCID)
  --community qnfo              (override default community)
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

ORCID = "0009-0002-4317-5604"
AUTHOR_CANONICAL = "Rowan Brad Quni-Gudzinas"
ZENODO_COMMUNITY = "qnfo"  # Create if doesn't exist

# Philosophy-domain keywords that trigger PhilPapers indexing.
# These get ADDED to existing keywords, not replacing them.
PHILOSOPHY_KEYWORDS = [
    "philosophy of physics",
    "philosophy of mathematics",
    "philosophy of science",
    "epistemology",
    "metaphysics",
    "ontology",
    "foundations of quantum mechanics",
    "structural realism",
    "measurement theory",
    "philosophy of information",
    "consilience",
    "paradigm theory",
    "foundations of mathematics",
    "number theory",
    "ultrametric physics",
]

# Zenodo API
ZENODO_API = "https://zenodo.org/api"

HEADERS_TEMPLATE = {
    "User-Agent": "QNFO/PhilPapers-Optimizer/1.0",
    "Content-Type": "application/json",
}


def get_all_records(token, query="Rowan Quni", size=250):
    """Fetch all QNFO records from Zenodo."""
    headers = {**HEADERS_TEMPLATE, "Authorization": f"Bearer {token}"}
    all_hits = []
    page = 1

    while True:
        url = f"{ZENODO_API}/records?q={urllib.request.quote(query)}&size={size}&page={page}&access_token={token}"
        req = urllib.request.Request(url, headers={"User-Agent": HEADERS_TEMPLATE["User-Agent"]})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            raw = e.read().decode('utf-8', errors='ignore')
            print(f"  HTTP {e.code} on page {page}: {raw[:200]}")
            # Try alternative query
            if page == 1:
                print("  Retrying with broader query...")
                return get_all_records(token, query="QNFO OR QWAV OR ultrametric", size=size)
            break
        except Exception as e:
            print(f"  Error on page {page}: {e}")
            break

        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            break

        # Filter to Quni-authored papers
        for hit in hits:
            creators = hit.get("metadata", {}).get("creators", [])
            is_quni = any("Quni" in c.get("name", "") or "Rowan" in c.get("name", "") for c in creators)
            if is_quni:
                all_hits.append(hit)

        total = data.get("hits", {}).get("total", 0)
        fetched = page * size
        print(f"  Page {page}: fetched {fetched}/{total}, Quni matches: {len(all_hits)} cumulative")

        if fetched >= total:
            break
        page += 1
        time.sleep(0.5)

    return all_hits


def audit_record(record):
    """Audit a single record for PhilPapers readiness."""
    meta = record.get("metadata", {})
    title = meta.get("title", "N/A")
    doi = meta.get("doi", "N/A")
    keywords = meta.get("keywords", [])
    abstract = (meta.get("description", "") or "")
    creators = meta.get("creators", [])
    orcid = creators[0].get("orcid", "") if creators else ""
    communities = [c.get("id", "") for c in meta.get("communities", [])]
    refs = meta.get("references", [])
    related = meta.get("related_identifiers", [])
    pubdate = meta.get("publication_date", "N/A")

    has_abstract = len(abstract) > 50
    has_keywords = len(keywords) > 0
    has_orcid = bool(orcid)
    has_community = len(communities) > 0
    has_refs = len(refs) > 0

    # Check for philosophy keywords specifically
    has_phil_kw = any(
        any(pkw in kw.lower() for pkw in ["philosophy", "epistemology", "metaphysics", "ontology", "foundation"])
        for kw in keywords
    )

    author_name = creators[0].get("name", "") if creators else ""
    name_consistent = author_name == AUTHOR_CANONICAL

    score = sum([has_abstract, has_keywords, has_orcid, has_community, has_refs])

    return {
        "record": record,
        "title": title,
        "doi": doi,
        "keywords": keywords,
        "abstract": abstract,
        "abstract_len": len(abstract),
        "orcid": orcid,
        "author_name": author_name,
        "communities": communities,
        "refs": refs,
        "related": related,
        "pubdate": pubdate,
        "has_abstract": has_abstract,
        "has_keywords": has_keywords,
        "has_orcid": has_orcid,
        "has_community": has_community,
        "has_refs": has_refs,
        "has_phil_kw": has_phil_kw,
        "name_consistent": name_consistent,
        "score": score,
        "needs_fix": score < 5,
    }


def generate_fixes(audit):
    """Generate the metadata diff needed to fix a record."""
    fixes = {}

    if not audit["has_keywords"]:
        # Add philosophy keywords
        fixes["keywords"] = PHILOSOPHY_KEYWORDS.copy()
    elif not audit["has_phil_kw"]:
        # Append philosophy keywords to existing ones
        existing = audit["keywords"].copy()
        existing.extend(PHILOSOPHY_KEYWORDS)
        fixes["keywords"] = list(dict.fromkeys(existing))  # dedupe

    if not audit["has_orcid"]:
        fixes["orcid"] = ORCID

    if not audit["name_consistent"]:
        fixes["author_name"] = AUTHOR_CANONICAL

    if not audit["has_community"]:
        fixes["community"] = ZENODO_COMMUNITY

    return fixes


def apply_fixes(record, audit, fixes, token, dry_run=False):
    """Apply metadata fixes to a Zenodo record via API."""
    rec_id = record.get("id")
    if not rec_id:
        return False

    meta = record.get("metadata", {})

    # Build updated metadata
    if "keywords" in fixes:
        meta["keywords"] = fixes["keywords"]

    if "orcid" in fixes:
        if meta.get("creators"):
            meta["creators"][0]["orcid"] = fixes["orcid"]

    if "author_name" in fixes:
        if meta.get("creators"):
            meta["creators"][0]["name"] = fixes["author_name"]

    if "community" in fixes:
        if "communities" not in meta:
            meta["communities"] = []
        meta["communities"] = [{"identifier": fixes["community"]}]

    payload = {"metadata": meta}

    if dry_run:
        return {
            "would_update": True,
            "fixes_applied": list(fixes.keys()),
            "title": audit["title"],
            "doi": audit["doi"],
        }

    headers = {
        **HEADERS_TEMPLATE,
        "Authorization": f"Bearer {token}",
    }

    url = f"{ZENODO_API}/records/{rec_id}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="PUT")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
        return {
            "success": True,
            "fixes_applied": list(fixes.keys()),
            "title": audit["title"],
            "doi": audit["doi"],
        }
    except urllib.error.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')[:200]}",
            "title": audit["title"],
            "doi": audit["doi"],
        }


def print_report(audits):
    """Print a comprehensive audit report."""
    total = len(audits)

    ready = sum(1 for a in audits if a["score"] >= 4)
    missing_kw = sum(1 for a in audits if not a["has_keywords"])
    missing_abs = sum(1 for a in audits if not a["has_abstract"])
    missing_orcid = sum(1 for a in audits if not a["has_orcid"])
    missing_com = sum(1 for a in audits if not a["has_community"])
    missing_refs = sum(1 for a in audits if not a["has_refs"])
    missing_phil_kw = sum(1 for a in audits if not a["has_phil_kw"])
    name_mismatch = sum(1 for a in audits if not a["name_consistent"])

    print()
    print("=" * 70)
    print("  ZENODO → PHILPAPERS DISCOVERABILITY AUDIT")
    print("=" * 70)
    print(f"  Total records audited:  {total}")
    print(f"  PhilPapers-ready (≥4/5): {ready}/{total}")
    print()
    print("  GAPS:")
    print(f"    Missing keywords:         {missing_kw}/{total}")
    print(f"    Missing philosophy KW:    {missing_phil_kw}/{total}")
    print(f"    Missing abstracts:        {missing_abs}/{total}")
    print(f"    Missing ORCID:            {missing_orcid}/{total}")
    print(f"    Missing Zenodo community: {missing_com}/{total}")
    print(f"    Missing references:       {missing_refs}/{total}")
    print(f"    Author name inconsistency:{name_mismatch}/{total}")
    print()

    if audits:
        print("  WORST OFFENDERS (score=0):")
        for a in audits:
            if a["score"] == 0:
                print(f"    ✗ {a['title'][:70]}")
                print(f"      DOI: {a['doi']}")

    print("=" * 70)
    return {
        "total": total,
        "ready": ready,
        "missing_kw": missing_kw,
        "missing_abs": missing_abs,
        "missing_orcid": missing_orcid,
        "missing_com": missing_com,
        "missing_refs": missing_refs,
        "missing_phil_kw": missing_phil_kw,
        "name_mismatch": name_mismatch,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Zenodo → PhilPapers Metadata Optimizer")
    parser.add_argument("--token", help="Zenodo API token (required for writes)")
    parser.add_argument("--dry-run", action="store_true", help="Audit only, no modifications")
    parser.add_argument("--orcid", default=ORCID, help=f"ORCID iD (default: {ORCID})")
    parser.add_argument("--community", default=ZENODO_COMMUNITY, help="Zenodo community slug")
    parser.add_argument("--fix", action="store_true", help="Apply fixes (requires --token)")
    parser.add_argument("--output", help="Save audit JSON to file")

    args = parser.parse_args()

    if args.fix and not args.token:
        print("ERROR: --fix requires --token ZENODO_API_TOKEN")
        print("Get your token at: https://zenodo.org/account/settings/applications/")
        sys.exit(1)

    print("Zenodo → PhilPapers Metadata Optimizer")
    print(f"ORCID: {args.orcid}")
    print(f"Community: {args.community}")
    print(f"Mode: {'DRY RUN (audit only)' if args.dry_run else 'FIX MODE' if args.fix else 'AUDIT ONLY'}")
    print()

    # Step 1: Fetch all records
    print("Step 1: Fetching Zenodo records...")
    token = args.token or ""
    records = get_all_records(token)
    print(f"  Found {len(records)} Quni-authored records")

    if not records:
        print("  No records found. Check query or API access.")
        # Try to fetch without auth for public records
        print("  Attempting public-only fetch...")
        records = get_all_records("", query="Rowan Quni", size=250)
        print(f"  Found {len(records)} public Quni records")

    # Step 2: Audit
    print("\nStep 2: Auditing metadata...")
    audits = []
    for rec in records:
        audit = audit_record(rec)
        audits.append(audit)
        status = "✓" if not audit["needs_fix"] else "✗"
        print(f"  [{status}] {audit['score']}/5 | {audit['title'][:60]}...")

    # Step 3: Report
    report = print_report(audits)

    # Step 4: Fix (if requested)
    if args.fix and args.token:
        print("\nStep 3: Applying fixes...")
        fixed = 0
        failed = 0

        for audit in audits:
            if not audit["needs_fix"]:
                continue

            fixes = generate_fixes(audit)
            if not fixes:
                continue

            print(f"  Fixing: {audit['title'][:60]}...")
            print(f"    Fixes: {list(fixes.keys())}")

            result = apply_fixes(audit["record"], audit, fixes, args.token, dry_run=args.dry_run)

            if result.get("success") or result.get("would_update"):
                print(f"    ✓ Applied")
                fixed += 1
            else:
                print(f"    ✗ Failed: {result.get('error', 'unknown')}")
                failed += 1

            time.sleep(0.5)  # Rate limit

        print(f"\n  Fixed: {fixed}, Failed: {failed}")

    # Step 5: Save results
    if args.output:
        output_data = {
            "report": report,
            "audits": [
                {
                    "title": a["title"],
                    "doi": a["doi"],
                    "score": a["score"],
                    "has_abstract": a["has_abstract"],
                    "has_keywords": a["has_keywords"],
                    "has_orcid": a["has_orcid"],
                    "has_community": a["has_community"],
                    "has_refs": a["has_refs"],
                    "has_phil_kw": a["has_phil_kw"],
                    "name_consistent": a["name_consistent"],
                    "abstract_len": a["abstract_len"],
                    "kw_count": len(a["keywords"]),
                    "needs_fix": a["needs_fix"],
                }
                for a in audits
            ],
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\nAudit saved to: {args.output}")

    print("\nDone.")


if __name__ == "__main__":
    main()
