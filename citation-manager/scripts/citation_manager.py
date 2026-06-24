#!/usr/bin/env python3
# citation_manager.py v1.0 -- Verify academic citations
# Part of the citation-manager skill. Usage: python citation_manager.py --paper paper.md

import argparse, json, re, sys, urllib.request
from datetime import datetime, timezone

def extract_citations(text: str) -> list[str]:
    keys = set()
    for group in re.findall(r'\[@(\w+(?:[,;\s]+@\w+)*)\]', text):
        for key in re.findall(r'@(\w+)', f"@{group}"): keys.add(key)
    return sorted(keys)

def extract_bib_keys(bib_text: str) -> dict[str, str]:
    entries = {}
    for match in re.finditer(r'```(?:bibtex)?\s*\n(.*?)```', bib_text, re.DOTALL):
        entry = match.group(1).strip()
        km = re.search(r'@\w+\{(\w+),', entry)
        if km: entries[km.group(1)] = entry
    for match in re.finditer(r'@\w+\{(\w+),\s*\n?(.*?)\n\}', bib_text, re.DOTALL):
        key = match.group(1)
        if key not in entries: entries[key] = match.group(0).strip()
    return entries

def generate_bibtex_from_doi(doi: str) -> str | None:
    url = f"https://api.crossref.org/works/{doi.strip()}/transform/application/x-bibtex"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/x-bibtex")
    req.add_header("User-Agent", "QNFO-CitationManager/1.0 (mailto:rwnquni@outlook.com)")
    try:
        return urllib.request.urlopen(req, timeout=10).read().decode("utf-8").strip()
    except Exception as e:
        print(f"[WARN] DOI lookup failed for {doi}: {e}", file=sys.stderr)
        return None

def run_audit(paper_path: str, bib_path: str = None) -> dict:
    with open(paper_path, 'r', encoding='utf-8') as f: paper_text = f.read()
    cited_keys = extract_citations(paper_text)
    if bib_path:
        with open(bib_path, 'r', encoding='utf-8') as f: bib_text = f.read()
    else:
        bs = re.search(r'##\s+(?:References?|Bibliography|Works Cited)\s*\n(.*?)(?=\n##\s|\Z)', paper_text, re.DOTALL | re.IGNORECASE)
        bib_text = bs.group(1) if bs else ""
    bib_entries = extract_bib_keys(bib_text)
    cited_set, bib_set = set(cited_keys), set(bib_entries.keys())
    missing, unused, matched = cited_set - bib_set, bib_set - cited_set, cited_set & bib_set
    repaired = {}
    for key in missing:
        dm = re.search(rf'\[@{re.escape(key)}\][\s\S]*?doi[:\s]*([^\s\n,]+)', paper_text, re.IGNORECASE)
        if dm:
            bibtex = generate_bibtex_from_doi(dm.group(1).rstrip('.,;:'))
            if bibtex:
                repaired[key] = bibtex
                print(f"[REPAIRED] @{key} from DOI")
    return {"total_cited": len(cited_set), "total_bib_entries": len(bib_set), "matched_count": len(matched), "missing_count": len(missing), "unused_count": len(unused), "matched": sorted(matched), "missing": sorted(missing), "unused": sorted(unused), "repaired": repaired, "status": "PASS" if not missing else ("REPAIRED" if repaired else "FAIL")}

def format_report(audit: dict) -> str:
    lines = ["# CITATION AUDIT REPORT", f"**Date:** {datetime.now(timezone.utc).isoformat()}", "", "## Summary", "", f"| Metric | Count |", f"|:-------|:-----:|", f"| Citations in text | {audit['total_cited']} |", f"| Bibliography entries | {audit['total_bib_entries']} |", f"| Matched | {audit['matched_count']} |", f"| Missing (cited, no entry) | **{audit['missing_count']}** |", f"| Unused (entry, not cited) | {audit['unused_count']} |", f"| Auto-repaired | {len(audit.get('repaired', {}))} |"]
    if audit["missing"]:
        lines.extend(["", "## MISSING CITATIONS", ""])
        for key in audit["missing"]:
            s = "[AUTO-REPAIRED]" if key in audit.get("repaired", {}) else "[NEEDS MANUAL ENTRY]"
            lines.append(f"- `@{key}` -- {s}")
        if audit.get("repaired"):
            lines.extend(["", "### Auto-Repaired BibTeX", "", "```bibtex"])
            for k, v in audit["repaired"].items(): lines.append(f"% @{k}\n{v}\n")
            lines.append("```")
    if audit["status"] == "PASS": lines.extend(["", "## ALL CITATIONS VERIFIED", f"All {audit['total_cited']} citations have matching bibliography entries."])
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser(description="Verify academic citations")
    p.add_argument("--paper", "-p", required=True); p.add_argument("--bib", "-b")
    p.add_argument("--output", "-o", default="citation-audit.md"); p.add_argument("--json", action="store_true")
    args = p.parse_args()
    audit = run_audit(args.paper, args.bib)
    if args.json:
        print(json.dumps(audit, indent=2, ensure_ascii=False))
        return
    report = format_report(audit)
    with open(args.output, "w", encoding="utf-8") as f: f.write(report)
    print(report)
    print(f"\n[{'PASS' if audit['status']=='PASS' else 'ACTION NEEDED'}] -> {args.output}")
    if audit["status"] == "FAIL": sys.exit(1)

if __name__ == "__main__": main()
