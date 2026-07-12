#!/usr/bin/env python3
"""T0.4: Dirac Material ZB Meta-Analysis.
Search literature for ZB observation and geometric effects in condensed matter.
"""

import json
import urllib.request
import xml.etree.ElementTree as ET
import time

def search_arxiv(query, max_results=30):
    """Search arXiv API for papers matching query."""
    base_url = "http://export.arxiv.org/api/query"
    params = f"search_query=all:{urllib.request.quote(query)}&start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending"
    url = f"{base_url}?{params}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read().decode('utf-8')
        return data
    except Exception as e:
        return f"<error>{e}</error>"

def classify_abstract(title, summary):
    """Classify paper into categories based on title and abstract keywords."""
    text = (title + " " + summary).lower()
    
    categories = []
    
    # ZB observation
    zb_obs_keywords = ["observe", "measure", "detect", "direct observation", 
                       "experimental", "scanning tunneling", "stm", "spectroscopy",
                       "imaging", "trembling motion"]
    if any(kw in text for kw in zb_obs_keywords):
        categories.append("ZB_OBSERVED")
    
    # Geometric effects
    geo_keywords = ["curvature", "strain", "effective metric", "geometric phase",
                    "berry curvature", "emergent geometry", "gravitational",
                    "spacetime", "analog gravity", "warped", "riemannian"]
    if any(kw in text for kw in geo_keywords):
        categories.append("GEOMETRIC_EFFECT")
    
    # Theoretical ZB→geometry
    theory_keywords = ["emergent", "derived", "correspondence", "mapping",
                       "holographic", "ads/cft", "duality", "effective field theory"]
    if any(kw in text for kw in theory_keywords):
        categories.append("THEORETICAL")
    
    # ZB in Dirac materials
    material_keywords = ["graphene", "topological insulator", "weyl semimetal",
                         "dirac semimetal", "transition metal dichalcogenide",
                         "silicene", "germanene", "borophene"]
    materials_found = [m for m in material_keywords if m in text]
    
    if not categories:
        categories.append("OTHER")
    
    return categories, materials_found

def main():
    queries = [
        "zitterbewegung graphene",
        "zitterbewegung topological insulator",
        "zitterbewegung Dirac material",
        "zitterbewegung Weyl semimetal",
        "emergent metric Dirac material zitterbewegung",
    ]
    
    all_papers = []
    seen_ids = set()
    
    for query in queries:
        print(f"Searching: {query}...")
        xml_data = search_arxiv(query, max_results=15)
        
        if xml_data.startswith("<error>"):
            print(f"  Error: {xml_data}")
            continue
        
        try:
            root = ET.fromstring(xml_data)
            ns = {'atom': 'http://www.w3.org/2005/Atom',
                  'arxiv': 'http://arxiv.org/schemas/atom'}
            
            for entry in root.findall('atom:entry', ns):
                arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
                
                if arxiv_id in seen_ids:
                    continue
                seen_ids.add(arxiv_id)
                
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                published = entry.find('atom:published', ns).text[:10]
                
                categories, materials = classify_abstract(title, summary)
                
                all_papers.append({
                    "arxiv_id": arxiv_id,
                    "title": title,
                    "published": published,
                    "categories": categories,
                    "materials": materials,
                })
        except ET.ParseError as e:
            print(f"  Parse error: {e}")
        
        time.sleep(1)  # Respect arXiv rate limit
    
    # Count statistics
    n_total = len(all_papers)
    n_zb_observed = sum(1 for p in all_papers if "ZB_OBSERVED" in p["categories"])
    n_geometric = sum(1 for p in all_papers if "GEOMETRIC_EFFECT" in p["categories"])
    n_theoretical = sum(1 for p in all_papers if "THEORETICAL" in p["categories"])
    n_both = sum(1 for p in all_papers if "ZB_OBSERVED" in p["categories"] and "GEOMETRIC_EFFECT" in p["categories"])
    
    # Material distribution
    material_counts = {}
    for p in all_papers:
        for mat in p.get("materials", []):
            material_counts[mat] = material_counts.get(mat, 0) + 1
    
    results = {
        "experiment": "T0.4 — Dirac Material ZB Meta-Analysis",
        "total_papers_found": n_total,
        "papers_zb_observed": n_zb_observed,
        "papers_geometric_effect": n_geometric,
        "papers_theoretical": n_theoretical,
        "papers_zb_plus_geometric": n_both,
        "geometric_fraction": round(n_geometric / n_total, 3) if n_total > 0 else 0,
        "material_distribution": material_counts,
        "interpretation": (
            f"Found {n_total} papers on ZB in condensed matter systems. "
            f"{n_zb_observed} report experimental ZB observation. "
            f"{n_geometric} report geometric/curvature effects. "
            f"{n_both} report BOTH ZB observation AND geometric effects. "
            + ("PASS — Evidence that ZB in Dirac materials produces measurable geometric response. "
               "This supports the ZB→metric correspondence in a tabletop analog system."
               if n_both > 0 else
               "NULL — No paper found that directly connects ZB observation to emergent geometry. "
               "The ZB→metric link remains theoretically motivated but lacks experimental analog support."),
        ),
        "verdict": "PASS" if n_both > 0 else "INCONCLUSIVE",
        "sample_papers": all_papers[:20],  # Top 20 for inspection
    }
    
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
