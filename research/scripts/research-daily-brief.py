"""
QNFO Research Briefing — Integrated arXiv + OpenAlex paper scanner.
Usage:
  python research-daily-brief.py --mode daily     (arXiv only, fast)
  python research-daily-brief.py --mode weekly    (arXiv + OpenAlex, comprehensive)

Daily mode: Fetches yesterday's arXiv papers, filters by QNFO keyword taxonomy.
Weekly mode: Same + OpenAlex (3-day window), catches journal papers arXiv misses.
"""
import urllib.request, urllib.parse, json, time, sys, re
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher

# ── Config ──
ARXIV_BASE = 'http://export.arxiv.org/api/query'
OPENALEX_BASE = 'https://api.openalex.org/works'
UA = 'Mozilla/5.0 (mailto:research@qnfo.org)'
POLITE = 2  # seconds between API calls

# arXiv categories to query
ARXIV_CATS = '(cat:quant-ph OR cat:math-ph OR cat:hep-th OR cat:math.NT OR cat:cs.IT OR cat:math.LO OR cat:math.CT OR cat:physics.soc-ph OR cat:physics.hist-ph)'

# OpenAlex search terms (space-separated = OR logic; filtering happens in Python)
OPENALEX_SEARCH = 'ultrametric p-adic adelic ostrowski bruhat-tits non-archimedean perfectoid berkovich langlands spencer-brown landauer bekenstein consilience quantum-error-correction quantum-foundations'

# ── Keyword Taxonomy (canonical from Obsidian _26217115844.md) ──
DAILY_KW = {
    'UMP': (5, [
        'ultrametric', 'p-adic', 'padic', 'adelic', 'adele', 'idele',
        'ostrowski', 'bruhat-tits', 'non-archimedean', 'nonarchimedean',
        'adelic-physics', 'ultrametric-physics', 'non-archimedean-physics',
        'p-adic-quantum', 'archimedean-completion', 'place-democracy',
        'ostrowski-theorem', 'product-formula', 'adele-ring', 'idele-class-group',
        'restricted-direct-product', 'strong-approximation', 'weak-approximation',
        'sagemath', 'pari-gp',
    ]),
    'RES': (4, [
        'consilience', 'cross-domain-consilience', 'interdisciplinary-synthesis',
        'transdisciplinary', 'unity-of-science', 'unification-physics',
        'measurement-stratigraphy', 'measurement-theory', 'metrology-foundations',
        'silent-radix', 'operationalism', 'epistemology-of-measurement',
        'ruliad', 'wolfram-physics', 'multiway-system', 'causal-invariance',
        'branchial-space', 'rulial-space', 'hypergraph-rewriting',
        'autaxys', 'quantum-coherence-biology', 'room-temperature-quantum-biology',
        'compton-bt', 'compton-bruhat-tits', 'frequency-valuation',
        'planck-scale-physics', 'quantum-gravity-phenomenology',
        'foundational-physics', 'theory-of-everything', 'quantum-foundations',
        'interpretation-of-quantum-mechanics', 'consistent-histories',
        'category-theory-physics', 'applied-category-theory',
    ]),
    'INM': (3, [
        'information-physics', 'physical-information', 'information-fundamental',
        'it-from-bit', 'bit-from-it', 'informational-universe',
        'landauer-principle', 'landauer-bound', 'landauer-limit',
        'bekenstein-bound', 'holographic-bound', 'bremermann-limit',
        'margolus-levitin',
        'shannon-entropy', 'kolmogorov-complexity',
        'algorithmic-information-theory', 'solomonoff-induction',
        'minimum-description-length', 'chaitin-constant',
        'thermodynamics-of-computation', 'maxwell-demon', 'szilard-engine',
        'reversible-computing', 'entropy-production',
        'information-geometry', 'fisher-information', 'amari-metric',
        'statistical-manifold', 'natural-gradient',
        'quantum-information', 'von-neumann-entropy', 'quantum-fisher',
        'holographic-entropy', 'entanglement-entropy', 'ryu-takayanagi',
        'free-energy-principle', 'bayesian-brain', 'predictive-coding',
        'active-inference', 'variational-free-energy',
        'integrated-information-theory', 'phi-measure', 'effective-information',
    ]),
    'QEC': (4, [
        'quantum error correction', 'surface code', 'stabilizer code',
        'topological code', 'qec decoder', 'quantum ldpc',
        'gkp code', 'concatenated code', 'quantum repeater',
        'toric code', 'color code', 'bacon shor',
        'flag qubit', 'magic state distillation',
        'quantum darwinism', 'error syndrome', 'decoding graph',
    ]),
    'SLB': (2, [
        'laws-of-form', 'spencer-brown', 'calculus-of-indications',
        'primary-algebra', 'primary-arithmetic', 'law-of-calling',
        'law-of-crossing', 'distinction-algebra', 'boundary-logic',
        'boundary-math', 'imaginary-boolean', 'self-reference-logic',
        'autopoiesis', 'second-order-cybernetics',
    ]),
    'CFE': (2, [
        'technology-forecasting', 'paradigm-forecasting', 'technology-roadmap',
        'strategic-foresight', 'cascading-foresight',
        'post-silicon-computing', 'beyond-cmos', 'novel-computing-substrate',
        'computing-paradigm', 'neuromorphic', 'photonic-computing',
        'quantum-computing-roadmap', 'dna-computing', 'molecular-computing',
        'technology-diffusion', 'bass-model', 'fisher-pry',
        'technology-readiness-level',
    ]),
}

WEEKLY_KW = {
    'UMP-DEEP': (5, [
        'berkovich', 'perfectoid', 'rigid-geometry', 'tate-algebra',
        'formal-group', 'lubin-tate', 'p-divisible', 'dieudonne',
        'crystalline-cohomology', 'etale-cohomology',
        'galois-representation', 'local-field', 'global-field',
        'class-field-theory', 'valuation-theory', 'valued-field',
        'arithmetic-dynamics', 'p-adic-dynamics', 'berkovich-dynamics',
        'p-adic-hodge', 'fontaine', 'de-rham', 'crystalline', 'semistable',
        'breuil-kisin',
        'langlands-program', 'automorphic-form', 'shimura-variety',
        'modular-form', 'elliptic-curve', 'l-function', 'selberg-trace',
    ]),
    'RES-DEEP': (4, [
        'monoidal-category', 'symmetric-monoidal', 'string-diagram',
        'decorated-cospan', 'operad', 'categorical-quantum',
        'decoherence', 'quantum-darwinism', 'einselection',
        'complex-systems', 'emergence', 'self-organized-criticality',
        'power-law', 'scale-free-network', 'integrated-information',
    ]),
}


# ── Helpers ──
def sleep():
    time.sleep(POLITE)


def norm(s):
    """Normalize text: lowercase, replace hyphens with spaces."""
    return s.lower().replace('-', ' ')


def title_similarity(t1, t2):
    """Rough dedup: check if titles are similar enough to be the same paper."""
    t1n = norm(t1)[:80]
    t2n = norm(t2)[:80]
    return SequenceMatcher(None, t1n, t2n).ratio()


# ── arXiv ──
def fetch_arxiv(date_start, date_end):
    """Fetch arXiv papers in date range."""
    date_filter = f'submittedDate:[{date_start.strftime("%Y%m%d")}0000 TO {date_end.strftime("%Y%m%d")}2359]'
    full = f'({ARXIV_CATS}) AND {date_filter}'
    sleep()
    params = urllib.parse.urlencode({
        'search_query': full, 'start': 0, 'max_results': 200,
        'sortBy': 'submittedDate', 'sortOrder': 'descending'
    })
    url = f'{ARXIV_BASE}?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            data = r.read().decode('utf-8')
            root = ET.fromstring(data)
            ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
            entries = root.findall('atom:entry', ns)
            papers = []
            for e in entries:
                t = e.find('atom:title', ns)
                title = t.text.strip().replace('\n', ' ') if t is not None and t.text else 'Untitled'
                aid = e.find('atom:id', ns)
                aid = aid.text.split('/abs/')[-1] if aid is not None and aid.text else ''
                pub = e.find('atom:published', ns)
                pub = pub.text[:10] if pub is not None and pub.text else ''
                s = e.find('atom:summary', ns)
                summary = s.text.strip().replace('\n', ' ') if s is not None and s.text else ''
                authors = []
                for a in e.findall('atom:author', ns):
                    n = a.find('atom:name', ns)
                    if n is not None and n.text:
                        authors.append(n.text)
                cat = e.find('arxiv:primary_category', ns)
                cat = cat.get('term', '') if cat is not None else ''
                papers.append({
                    'id': aid, 'title': title, 'published': pub,
                    'summary': summary, 'authors': authors,
                    'primary_cat': cat, 'source': 'arXiv',
                })
            print(f'  [arXiv] {len(papers)} papers ({date_start.strftime("%Y-%m-%d")} → {date_end.strftime("%Y-%m-%d")})', flush=True)
            return papers
    except Exception as e:
        print(f'  [arXiv] FAILED: {e}', flush=True)
        return []


# ── OpenAlex ──
def fetch_openalex(date_start, date_end):
    """Fetch recent OpenAlex works matching QNFO search terms."""
    # OpenAlex date filter: from_publication_date
    from_date = date_start.strftime('%Y-%m-%d')
    # OpenAlex search: use + for OR, encode properly
    search_q = urllib.parse.quote(OPENALEX_SEARCH, safe='')
    url = (f'{OPENALEX_BASE}?search={search_q}'
           f'&filter=from_publication_date:{from_date}'
           f'&sort=publication_date:desc&per-page=50'
           f'&mailto=research@qnfo.org')
    sleep()
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
            results = d.get('results', [])
            papers = []
            for w in results:
                title = w.get('display_name', 'Untitled')
                pub_date = w.get('publication_date', '') or ''
                doi = w.get('doi', '') or ''
                if doi:
                    doi = doi.replace('https://doi.org/', '')
                abstract = ''
                # Try to get abstract from inverted abstract
                inv = w.get('abstract_inverted_index')
                if inv:
                    words = sorted((pos, word) for word, positions in inv.items() for pos in positions)
                    abstract = ' '.join(w for _, w in words)
                venue = (w.get('primary_location', {}) or {}).get('source', {}) or {}
                venue_name = venue.get('display_name', '')
                cited = w.get('cited_by_count', 0) or 0
                authors = []
                for a in (w.get('authorships', []) or []):
                    auth = a.get('author', {}) or {}
                    name = auth.get('display_name', '')
                    if name:
                        authors.append(name)
                papers.append({
                    'id': doi or str(w.get('id', '')),
                    'title': title,
                    'published': pub_date,
                    'summary': abstract,
                    'authors': authors,
                    'primary_cat': venue_name,
                    'source': 'OpenAlex',
                    'cited': cited,
                })
            print(f'  [OpenAlex] {len(papers)} papers (from {from_date})', flush=True)
            return papers
    except Exception as e:
        print(f'  [OpenAlex] FAILED: {e}', flush=True)
        return []


# ── Dedup ──
def dedup(arxiv_papers, oa_papers):
    """Remove OpenAlex papers that are duplicates of arXiv papers."""
    if not oa_papers:
        return arxiv_papers
    result = list(arxiv_papers)
    for oa in oa_papers:
        is_dup = False
        for arx in arxiv_papers:
            sim = title_similarity(oa['title'], arx['title'])
            if sim > 0.75:
                is_dup = True
                break
        if not is_dup:
            result.append(oa)
    return result


# ── Keyword Matching ──
def match_keywords(papers, kw_config):
    """Score and rank papers by keyword matches."""
    results = []
    for p in papers:
        text = norm(f"{p['title']} {p['summary']}")
        p_matches = {}
        total = 0
        best_prog = None
        best_w = 0
        for prog, (weight, kws) in kw_config.items():
            hits = [kw for kw in kws if norm(kw) in text]
            if hits:
                s = len(hits) * weight
                total += s
                p_matches[prog] = hits
                if weight > best_w:
                    best_w = weight
                    best_prog = prog
        if total > 0:
            results.append({**p, 'matches': p_matches, 'score': total, 'primary_program': best_prog})
    results.sort(key=lambda x: -x['score'])
    return results


# ── Briefing ──
def briefing(papers, date_str, mode):
    """Format briefing output."""
    label = 'Weekly Deep Scan (arXiv + OpenAlex)' if mode == 'weekly' else 'Daily Briefing (arXiv)'
    out = [f'📋 QNFO Research {label}', f'═══════════════════════════════════════════════════════']

    if not papers:
        out.append('\n⚪ No new papers matched QNFO keywords.')
        return '\n'.join(out)

    high = [p for p in papers if p['score'] >= 10]
    med = [p for p in papers if 5 <= p['score'] < 10]
    low = [p for p in papers if p['score'] < 5]

    for tier_name, group, emoji in [
        ('HIGH RELEVANCE', high, '🔴'),
        ('MEDIUM', med, '🟡'),
        ('LOW — SKIMMABLE', low, '⚪'),
    ]:
        if not group:
            continue
        out.append(f'\n{emoji} {tier_name} ({len(group)})')
        for p in group:
            prog = p['primary_program'] or ''
            authors = ', '.join(p['authors'][:2])
            if len(p['authors']) > 2:
                authors += ' et al.'
            all_kws = set()
            for kws in p['matches'].values():
                all_kws.update(kws[:3])
            kws_str = ', '.join(sorted(all_kws)[:5])
            src_tag = f' [{p["source"]}]' if p.get('source') == 'OpenAlex' else ''
            out.append(f'  [{prog}{src_tag}] {p["title"][:110]}')
            out.append(f'         {authors} | {p["id"]} | {p["published"]}')
            if kws_str:
                out.append(f'         Keywords: {kws_str}')
            if p.get('cited'):
                out.append(f'         Cited: {p["cited"]}x | Venue: {p["primary_cat"]}')
            out.append('')

    progs = {p['primary_program'] for p in papers if p['primary_program']}
    arxiv_n = sum(1 for p in papers if p.get('source') == 'arXiv')
    oa_n = sum(1 for p in papers if p.get('source') == 'OpenAlex')
    out.append('─' * 60)
    sources_str = f'{arxiv_n} arXiv, {oa_n} OpenAlex' if oa_n else f'{arxiv_n} arXiv'
    out.append(f'📊 {len(papers)} papers in {len(progs)} programs ({sources_str}): {", ".join(sorted(progs))}')
    return '\n'.join(out)


# ── Main ──
def main():
    import argparse
    ap = argparse.ArgumentParser(description='QNFO Research Daily Briefing')
    ap.add_argument('--mode', choices=['daily', 'weekly'], default='daily',
                    help='daily = arXiv only | weekly = arXiv + OpenAlex (default: daily)')
    ap.add_argument('--days', type=int, default=1,
                    help='Days to scan (daily defaults to 1, weekly to 3)')
    args = ap.parse_args()

    # Date range
    if args.mode == 'weekly':
        days = args.days if args.days != 1 else 3  # weekly defaults to 3 days
    else:
        days = args.days

    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    date_start = today - timedelta(days=days)
    date_end = today - timedelta(seconds=1)

    print(f'QNFO Research Briefing — mode={args.mode}, window={date_start.strftime("%Y-%m-%d")} → {date_end.strftime("%Y-%m-%d")}', flush=True)
    print()

    # ── Fetch arXiv ──
    arxiv_papers = fetch_arxiv(date_start, date_end)

    # ── Fetch OpenAlex (weekly only) ──
    oa_papers = []
    if args.mode == 'weekly':
        oa_papers = fetch_openalex(date_start, date_end)

    # ── Dedup ──
    all_papers = dedup(arxiv_papers, oa_papers)
    dup_count = len(arxiv_papers) + len(oa_papers) - len(all_papers)
    print(f'\nTotal: {len(all_papers)} unique papers (arXiv: {len(arxiv_papers)}, OpenAlex: {len(oa_papers)}, deduped: {dup_count})', flush=True)

    # ── Keyword matching ──
    kw_config = dict(DAILY_KW)
    if args.mode == 'weekly':
        kw_config.update(WEEKLY_KW)

    matched = match_keywords(all_papers, kw_config)
    print(f'Matched: {len(matched)} papers', flush=True)

    # ── Print briefing ──
    print()
    print(briefing(matched, date_start.strftime('%Y-%m-%d'), args.mode))


if __name__ == '__main__':
    main()
