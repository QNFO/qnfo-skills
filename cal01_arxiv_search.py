#!/usr/bin/env python3
"""CAL-01 Phase 0: Literature Survey — arXiv API search for transmon anharmonicity."""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
import sys

ARXIV_API = "http://export.arxiv.org/api/query"
NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom'
}

def search_arxiv(query, max_results=15, sort_by='relevance'):
    """Search arXiv API and return parsed entries."""
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': sort_by
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    
    print(f"=== Searching: {query[:80]}... ===")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CAL01-Literature-Survey/1.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode('utf-8')
    except Exception as e:
        print(f"  ERROR: {e}")
        return []
    
    root = ET.fromstring(data)
    entries = []
    for entry in root.findall('atom:entry', NS):
        title = entry.find('atom:title', NS)
        summary = entry.find('atom:summary', NS)
        published = entry.find('atom:published', NS)
        authors = entry.findall('atom:author', NS)
        links = entry.findall('atom:link', NS)
        arxiv_id = None
        doi = None
        
        for link in links:
            href = link.attrib.get('href', '')
            if 'arxiv.org/abs/' in href:
                arxiv_id = href.split('/abs/')[-1]
            if link.attrib.get('title') == 'doi':
                doi = href.split('doi.org/')[-1] if 'doi.org/' in href else href
        
        author_names = []
        for a in authors:
            name = a.find('atom:name', NS)
            if name is not None and name.text:
                author_names.append(name.text)
        
        entries.append({
            'title': title.text.strip() if title is not None and title.text else 'N/A',
            'authors': ', '.join(author_names[:3]) + (' et al.' if len(author_names) > 3 else ''),
            'published': published.text[:10] if published is not None and published.text else 'N/A',
            'arxiv_id': arxiv_id or 'N/A',
            'doi': doi or 'N/A',
            'summary': (summary.text[:300] + '...') if summary is not None and summary.text else 'N/A'
        })
    
    print(f"  Found: {len(entries)} results\n")
    return entries

def fetch_paper(arxiv_id):
    """Fetch metadata for a specific arXiv paper."""
    params = {'id_list': arxiv_id, 'max_results': 1}
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CAL01-Literature-Survey/1.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode('utf-8')
    except Exception as e:
        print(f"  ERROR fetching {arxiv_id}: {e}")
        return None
    
    root = ET.fromstring(data)
    entry = root.find('atom:entry', NS)
    if entry is None:
        return None
    
    title = entry.find('atom:title', NS)
    summary = entry.find('atom:summary', NS)
    published = entry.find('atom:published', NS)
    authors = entry.findall('atom:author', NS)
    
    author_names = []
    for a in authors:
        name = a.find('atom:name', NS)
        if name is not None and name.text:
            author_names.append(name.text)
    
    return {
        'title': title.text.strip() if title is not None and title.text else 'N/A',
        'authors': ', '.join(author_names),
        'published': published.text[:10] if published is not None and published.text else 'N/A',
        'summary': summary.text if summary is not None and summary.text else 'N/A'
    }


# === MAIN ===

print("=" * 70)
print("CAL-01 Phase 0: TRANSMON ANHARMONICITY LITERATURE SURVEY")
print("=" * 70)
print()

# Query 1: Systematic transmon anharmonicity surveys
q1 = search_arxiv("transmon anharmonicity systematic E_J/E_C", max_results=15)

# Query 2: Transmon anharmonicity + deep transmon + E_J/E_C ratio  
q2 = search_arxiv("transmon anharmonicity scaling E_J over E_C deep transmon", max_results=15)

# Query 3: Relative anharmonicity measurement transmon
q3 = search_arxiv("relative anharmonicity transmon measurement alpha_r nu", max_results=15)

# Query 4: Koch transmon anharmonicity validation experiment
q4 = search_arxiv("Koch transmon anharmonicity experimental validation", max_results=15)

# Query 5: Purkayastha 2026 specific
print("=== Fetching Purkayastha et al. (2026) — arXiv:2603.26895 ===")
purk = fetch_paper("2603.26895")
if purk:
    print(f"  Title: {purk['title']}")
    print(f"  Authors: {purk['authors']}")
    print(f"  Published: {purk['published']}")
    print(f"  Summary: {purk['summary'][:500]}...")
else:
    print("  NOT FOUND on arXiv")
print()

# Deduplicate and print summary
all_results = {}
for q_results in [q1, q2, q3, q4]:
    for r in q_results:
        key = r['arxiv_id']
        if key not in all_results:
            all_results[key] = r

print("=" * 70)
print(f"UNIQUE RESULTS: {len(all_results)}")
print("=" * 70)

# Sort by relevance (paper year)
for i, (aid, r) in enumerate(sorted(all_results.items(), key=lambda x: x[1]['published'], reverse=True)):
    print(f"\n[{i+1}] {r['title']}")
    print(f"    Authors: {r['authors']}")
    print(f"    Published: {r['published']} | arXiv: {aid} | DOI: {r['doi']}")
    print(f"    Abstract: {r['summary'][:200]}...")

print("\nDone.")
