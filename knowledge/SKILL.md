---
name: knowledge
description: QNFO Knowledge Graph and durable memory management -- graph querying for due diligence and impact analysis (stats, nodes, neighbors, impact, query endpoints), ultrametric clustering and taxonomy edge seeding, semantic memory search via Vectorize, persistent fact storage in D1/Vectorize, cross-system discovery, and paper context retrieval. Use for remembering, recalling, and discovering knowledge across the QNFO ecosystem.
version: 2.8
triggers: ["knowledge graph", "KG", "graph", "graph-api", "dependencies", "impact", "neighbors", "nodes", "edges", "due diligence", "memory", "remember", "recall", "durable learning", "semantic search", "Vectorize", "D1 memory", "fact storage", "discovery", "cross-system", "ultrametric", "p-adic", "taxonomy", "impact analysis", "what exists", "who depends", "ecosystem", "paper search", "memory search", "fact", "knowledge base"]
related: ["qnfo-core"]
priority: 1
platform: cloudflare
autonomous: true
self_sufficient: true
---
> **v2.8 UPDATE (2026-08-06, PhilPapers discoverability pipeline):**
> Red-team: direct parent-agent audit of session 1tz85-vMiqh2TyFySznBA (IPR KG deployment).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **Stale cached baseline removed from authoritative positions** — the body's
>     "Last verified: 2026-07-28 live (2,500 nodes, 1,492 edges, 1,569 Paper nodes)" and
>     Step 0b's identical claim contradicted this skill's OWN v2.6 banner (2026-08-04 baseline:
>     2,569/908) and the live tool description (2,518/831). Cached numbers now reference the
>     v2.6 reconciliation baseline with an explicit "always query live" caveat.
> (2) [SOFT] **N-2 frontmatter fixed** — frontmatter said 2.5 while header/footer said 2.6.
> Cross-reference: kaizen v1.20, research v2.65, qnfo-core N-2, KIF-23,
> session 1tz85-vMiqh2TyFySznBA.

# KNOWLEDGE — v2.8
> **v2.6 UPDATE (2026-08-04, kaizen — staleness sweep + KG-D1 reconciliation result):**
> Red-team: direct parent-agent audit (session C8CxG7CWs3AOR9w37Q5c8).
> HARD: 0. SOFT: 2. DESIGN: 1.
> Changes:
> (1) [SOFT] **Staleness sweep**: 16 days since last kaizen (2026-07-21).
> (2) [SOFT] **KIF-23 reconciliation note**: 11 D1-only Paper nodes seeded into
>     KG today via graph-api /sync (acrp04/acrp07/acrp08/adelic-cross-domain/
>     compton-ontology/frequency-valuation/kkr-coarse/odr-thesis/ostrowski/
>     ultrametric-p-adic/wbs-6). KG paper-slug sync now 952/952 (100%).
> (3) [DESIGN] **KG baseline updated**: 2,569 nodes / 908 edges / 14
>     GovernancePolicy nodes (2026-08-04). Edge-type distribution: 57 types,
>     BELONGS_TO dominant (378, 41.6%), OWNS (143). Edge count 908 vs prior
>     ~1,433 baseline reflects paper-sync node growth without edge seeding —
>     document in reconciliation runs, not data loss.
> Cross-reference: kaizen v1.18, research v2.62, KIF-23.





> **API-FAILURE PROTOCOL (HARD, cross-ref):** When any API call returns 403/401/404,
> run the API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6):
> STOP -> VERIFY your HTTP method/headers -> COMPARE with curl -> THEN consider
> infrastructure. The bug is ALWAYS your code until proven otherwise (kaizen BLAME-EXTERNAL-1).

> **v2.3 UPDATE (2026-08-04, kaizen — zenodo_doi ownership gate):**
> Red-team: blanket `zenodo_url` backfill incident (session dXXJ3TxRQ1VHzGdAyp-lo)
> created 1,245+ fake D1 links to external citations. The KG 4-D seed script writes
> `zenodo_doi` — it must NOT write DOIs that are not QNFO-owned.
> Changes:
> (1) [HARD] **zenodo_doi ownership gate added to the 4-D seed section** — verify
>     DOI ownership against the live Zenodo API (creator search + person-name
>     variant) before writing `zenodo_doi` to any KG Paper node.
> (2) [SOFT] Anti-pattern row added: ZENODO-KG-OWNERSHIP-1.
> Cross-reference: research v2.54 (P5.OWNERSHIP), kaizen v1.13,
> session dXXJ3TxRQ1VHzGdAyp-lo.

> **v2.2 UPDATE (2026-07-29, Cloudflare MCP kaizen):**
> Added references to `cloudflare-autorag-mcp-server` (automated RAG with Workers AI +
> Vectorize) as the preferred method for building RAG pipelines over manual Vectorize
> insert + query calls. Added `cloudflare-ai-gateway` as the canonical AI query logging
> source for memory operations. Updated Cross-System Discovery Hierarchy to include
> MCP-first retrieval paths. See `cloudflare` skill v3.9 §MCP-Driven Operations.

## KNOWLEDGE — v2.7 (Ultra-Consolidated KG + Memory + AutoRAG)

> **v2.1 UPDATE (2026-07-21, phantom-claim audit):** Added the
> **Tool-Call Execution Mandate** section below. A KG edge/node write or a
> `remember_fact` call is not "stored" until re-queried and shown present
> in this turn.

> **Merges 2:** knowledge-graph + memory-management
> **Related:** Always load with `qnfo-core` for Due Diligence Protocol (§3) -- KG-First Discovery Gate.
> **Cloudflare Full-Stack:** KG API runs on Cloudflare Workers. Memories persist in D1 + Vectorize (768-dim cosine). All knowledge infrastructure is Cloudflare-native.

## execute_plan

update_plan([
  {"step": "Query KG /stats for ecosystem overview (nodes, edges, labels)", "status": "pending"},
  {"step": "Query KG /nodes or /neighbors for specific entity discovery", "status": "pending"},
  {"step": "Query D1 + Vectorize for durable memories and paper context", "status": "pending"},
  {"step": "Perform impact analysis or store new facts as needed", "status": "pending"},
  {"step": "Seed taxonomy edges for orphaned KG nodes (minimum 1 edge per entity)", "status": "pending"},
])

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY)

Claiming a fact is "remembered", a KG edge is "seeded", or a D1 row is
"stored" without an invoked tool call showing evidence in this turn is a
PHANTOM CLAIM (`qnfo-core` §9.11 Rule 14) — BLOCKED.

1. **`remember_fact`** — after storing, re-run `recall_facts` or `search_memories` with a matching keyword/query and show the stored entry in the response, not just the write call's ack.
2. **KG edge seeding** — after seeding, re-query `/neighbors/{entity}` and show neighbor count > 0; a POST/insert success response alone does not confirm the edge exists.
3. **D1 writes** — re-run a `SELECT` against the exact row just written before claiming "stored" or "synced".
4. **"Comprehensive"/"all" discovery claims** — must be preceded by an actual `query_graph('stats')` call in this turn; a claim of completeness from memory/assumption alone is BLOCKED per the KG-First Discovery Gate below.
5. If re-verification cannot be run in this turn, say `[NOT-VERIFIED: reason]` instead of "stored"/"remembered"/"seeded".

---

## Knowledge Graph API

All endpoints accessible via `query_graph()` tool.

### /stats -- Ecosystem Overview
```python
# Who am I working with? What's out there?
stats = query_graph('stats')
# Returns: totalNodes, totalEdges, nodeLabels (with counts), relationshipTypes (with counts)
print(f"KG: {stats['totalNodes']} nodes, {stats['totalEdges']} edges")
for label in stats.get('nodeLabels', []):
    print(f"  {label['label']}: {label['count']}")
```

**Current state (live):** Query at session start via `query_graph('stats')`. DO NOT rely on static cached numbers — KG state evolves across sessions. Last verified: 2026-08-04 live (2,569 nodes / 908 edges / 14 GovernancePolicy per v2.6 reconciliation baseline). NOTE: edge count 908 vs ~1,433 prior reflects paper-sync node growth without edge seeding — document in reconciliation runs, not data loss. Tool description may report a newer snapshot (e.g. 2,518/831) — always query live, never cite these cached numbers as current..

## Reusable Scripts

### D1 KG 4-D Seed Script
```js
// _kg_seed_4d.js — Seed Knowledge Graph Paper nodes with 4-D distribution properties
const T = process.env.CLOUDFLARE_API_TOKEN; // requires D1:Edit permission
const ACCOUNT = '...'; // Cloudflare account ID
const DB = '...'; // qnfo-graph database UUID

// === Seed single node ===
const props = {
  distribution_status: 'complete', // draft|published|distributed|durable|complete
  ipfs_cid: 'bafkrei...',
  arweave_tx: 'CFC5MQLe...',
  dns_link: '_dnslink.mypaper.mydomain.org',
  zenodo_doi: '10.5281/zenodo.XXXXX',
  internet_archive: 'https://web.archive.org/web/...',
  distribution_date: new Date().toISOString().split('T')[0]
};

const sql = `UPDATE nodes SET properties = json_set(
  COALESCE(properties,'{}'),
  '$.distribution_status', ?1,
  '$.ipfs_cid', ?2,
  '$.arweave_tx', ?3,
  '$.dns_link', ?4,
  '$.zenodo_doi', ?5,
  '$.internet_archive', ?6,
  '$.distribution_date', ?7
) WHERE id = 'node-id'`;

await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/d1/database/' + DB + '/query', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json' },
  body: JSON.stringify({ sql, params: [props.distribution_status, props.ipfs_cid, props.arweave_tx, props.dns_link, props.zenodo_doi, props.internet_archive, props.distribution_date] })
});

// === Bulk seed all draft nodes ===
await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/d1/database/' + DB + '/query', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json' },
  body: JSON.stringify({ sql: "UPDATE nodes SET properties = json_set(COALESCE(properties,'{}'), '$.distribution_status', 'draft') WHERE label = 'Paper' AND (properties IS NULL OR properties NOT LIKE '%distribution_status%')" })
});

// === Verify ===
const r = await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/d1/database/' + DB + '/query', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json' },
  body: JSON.stringify({ sql: "SELECT COUNT(*) as c FROM nodes WHERE label = 'Paper' AND properties LIKE '%distribution_status%'" })
});
const d = await r.json();
console.log('Papers with 4-D properties:', d.result[0].results[0].c);
```
When seeding or updating KG Paper nodes, include 4-D distribution properties:
```json
{
  "distribution_status": "draft|published|distributed|durable|complete",
  "ipfs_cid": "bafkreicod...",
  "filecoin_cid": "bafybeid6z...",
  "arweave_tx": "WCauEwD...",
  "dns_link": "_dnslink.{slug}.qnfo.org",
  "internet_archive": "https://web.archive.org/web/...",
  "zenodo_doi": "10.5281/zenodo.XXXXX"
}
```
**GATE:** Paper nodes without 4-D properties are `distribution_status: "draft"` — not published.

**zenodo_doi OWNERSHIP GATE (v2.3, HARD — added 2026-08-04):** Before writing
`zenodo_doi` (or any Zenodo URL/DOI) to a KG Paper node or D1 row, verify the DOI is
QNFO-owned against the LIVE Zenodo API. Build the owned-DOI set from BOTH
`metadata.creators.person_or_org.name:QNFO` AND the person-name variant
`"Rowan Brad Quni-Gudzinas"` (mis-attributed records are invisible to the QNFO
creator search). NEVER write `zenodo_doi` derived from a raw `doi LIKE '%zenodo%'`
match — D1 `papers`/`paper_ids` contain EXTERNAL citations. Canonical incident:
session dXXJ3TxRQ1VHzGdAyp-lo blanket backfill created 1,245+ fake links.
Enforcement script: `research/scripts/zenodo-ownership-check.py`.
Cross-ref: research v2.54 P5.OWNERSHIP, kaizen v1.13.

### /nodes -- Query by Label
```python
# Find all papers, projects, concepts...
papers = query_graph('nodes', {'label': 'Paper'})
projects = query_graph('nodes', {'label': 'Project'})
rqs = query_graph('nodes', {'label': 'ResearchQuestion'})

# Search by name
results = query_graph('nodes', {'label': 'Paper', 'search': 'quantum'})
# Returns: [{id, name, slug, doi, ev_score, ...}, ...]
```

### /neighbors/{id} -- What's Connected?
```python
# What depends on this? What does it depend on?
neighbors = query_graph('neighbors', {'id': 'paper-cfpe-forecast'})
# Returns: [{id, name, label, relationship}, ...]
```

### /impact/{id} -- Impact Analysis
```python
# What would break if this changed?
impact = query_graph('impact', {'id': 'project-qnfo-gov'})
# Returns: upstream dependencies, downstream dependents, total impact score
print(f"Impact: {impact.get('totalDependents', 0)} downstream dependents")
```

### /query -- Raw Graph Queries
```python
# Custom traversal
results = query_graph('query', {
    'query': "MATCH (p:Paper)-[:BELONGS_TO]->(c:Concept) WHERE p.slug CONTAINS 'quantum' RETURN p, c"
})
```

---

## Due Diligence Gate (MANDATORY -- KG-First Discovery)

**Before ANY task involving "what exists" or ecosystem discovery:**

### Step 0a: KG /stats (MANDATORY first API call)
The Knowledge Graph is the canonical ecosystem registry. MUST query `/stats` before claiming "comprehensive" or "all" discovery.

### Step 0b: KG Label Counts
Query live labels at session start. Last verified 2026-08-04 live (baseline per v2.6 banner — 2,569 nodes / 908 edges; per-label counts below are the 2026-07-28 snapshot, superseded by live query):
```
Paper: 1569, CloudflareAsset: 120, R2Object: 105, Project: 94
Concept: 66, Skill: 60, ResearchQuestion: 49, Finding: 45
Decision: 39, GovernancePolicy: 14, OpenItem: 25
```
**DO NOT rely on static numbers — run `query_graph('stats')` live.**

### Step 0c: D1 + Vectorize Cross-Reference
- D1 portfolio-state: `npx wrangler d1 execute portfolio-state --remote --command "SELECT type, COUNT(*) as count FROM resources GROUP BY type" -y`
- D1 living-paper: paper count vs KG Paper count
- Vectorize: `search_memories({query: "project state", limit: 5})`

**GATE:** If KG was NOT queried before "comprehensive" claim -> cherry-picking violation. Files on disk are an incomplete, stale subset.

---

## Edge Seeding Gate (MANDATORY)

### Trigger
Before executing work on ANY entity, check KG connectivity. Query `/neighbors/{entity}`. If neighbor count is 0 -> entity is orphaned. Seed taxonomy edges BEFORE proceeding.

### Minimum Viable Connection (HARD GATE)
Every entity must have at least ONE `BELONGS_TO` edge to a domain or program concept node.

### Seeding Protocol
1. Query `/nodes?label=Concept` for available domains (level=1) and programs (level=2)
2. Map entity to domain/program based on metadata (tags, domain field, name heuristics)
3. Seed edges via Python script posting to graph-api sync endpoint
4. Verify: re-query `/neighbors/{entity}` -> neighbor count must be > 0

### Why This Matters
Orphaned KG nodes produce fabricated impact analysis. "Nothing depends on this" is true only because no edges exist -- NOT because nothing depends on it.

---

## Memory Management

### Semantic Memory Search
```python
# Find past conversations, decisions, facts by MEANING (not keywords)
results = search_memories({
    "query": "What was the Cloudflare Full-Stack Mandate?",
    "limit": 5,
    "category": "project_fact"  # Optional filter
})
# categories: user_preference, project_fact, task_outcome, heuristic, anti_pattern
```

### Durable Fact Storage
```python
# Persist with vector embedding for future semantic recall
remember_fact({
    "content": "The Cloudflare Full-Stack Mandate requires all infrastructure decisions to evaluate Workers, D1, R2, KV, DO, AI, Vectorize, Queues, Pages, DNS, WAF, CDN as ONE integrated platform.",
    "category": "heuristic",
    "importance": 1.0,
    "summary": "Cloudflare Full-Stack Mandate",
    "session_id": "session-2026-07-17"
})
```

### Structured Recall
```python
# Recall by category or keyword from D1
facts = recall_facts({
    "category": "project_fact",
    "keyword": "CFPE",
    "limit": 10
})
```

### Paper Context & Search
```python
# Get full paper body from D1 living-paper
paper = get_paper_context({
    "slug": "cfpe-forecast-stages3-5-assumption-audit",
    "limit_chars": 10000
})
# Returns: {slug, title, doi, body (full markdown), published_at, ...}

# Semantic search across QWAV papers via Vectorize
papers = search_papers({
    "query": "room temperature quantum coherence biomolecules",
    "limit": 10
})
# Returns: [{slug, title, score, snippet}, ...] ranked by meaning similarity
```

---

## Cross-System Discovery Hierarchy

When discovering "what exists," query in this order:

| Priority | System | API | Returns |
|:---------|:-------|:----|:--------|
| **1. KG (canonical topology)** | graph-api Worker (`query_graph`) | `/stats`, `/nodes`, `/neighbors`, `/impact` | What exists AND how things connect |
| **2. D1 (structured records)** | `cloudflare/scripts/d1-query.py` | `portfolio-state`, `living-paper`, `qnfo-audit` | Row-level structured data |
| **3. Vectorize (semantic search)** | `search_memories`, `search_papers` | 768-dim cosine similarity | Meaning-based search across memories + papers |
| **4. MCP: AutoRAG (automated RAG)** | `cloudflare-autorag-mcp-server` | Workers AI + Vectorize pipeline | Full RAG pipeline — indexing, embedding, retrieval (PREFERRED over manual Vectorize) |
| **5. MCP: AI Gateway (query logging)** | `cloudflare-ai-gateway` | Gateway log search, prompt inspection | Trace AI queries, debug prompt/response patterns |
| **6. R2 (file artifacts)** | wrangler R2 object get/list | `qnfo/` bucket | Canonical file storage (last resort for discovery) |
| **7. Local filesystem** | `glob`, `grep`, `os.listdir` | CWD | Ephemeral cache -- verify against R2 before trusting |
| **8. Keyword Taxonomy** | `QNFO/qnfo-research:docs/QNFO-KEYWORD-TAXONOMY.md` (GitHub) + `memory_recall({query:"QNFO keyword taxonomy"})` | Program-keyword map for GitHub discovery | Canonical keyword taxonomy for discovering repos aligned with each QNFO research program (UMP/SLB/INM/CFE/RES/PLT/DEM) — use for GitHub star curation and repo discovery |

**Always query KG first.** Files on disk are an incomplete, stale subset. The KG is the single source of truth for ecosystem topology.

**Keyword Taxonomy (v1.0, 2026-08-05):** When discovering GitHub repos aligned with QNFO programs, consult `QNFO/qnfo-research:docs/QNFO-KEYWORD-TAXONOMY.md` (canonical doc, committed to git) or `memory_recall({query: "QNFO keyword taxonomy {program}"})` (per-program durable memories). The taxonomy maps each WBS program (UMP/SLB/INM/CFE/RES/PLT/DEM) to GitHub-searchable keywords organized by tier (core, geometry, algebra, etc.). It also covers cross-cutting themes: Agentic AI, 4-D Distribution Protocol, and Measurement Stratigraphy.

### AutoRAG Integration (v2.2)

When building or updating RAG pipelines for knowledge retrieval, prefer
`cloudflare-autorag-mcp-server` over manual Vectorize insert + Workers AI query patterns.
AutoRAG automates:
- Document ingestion and chunking
- Embedding generation via Workers AI
- Vectorize index population
- Query-time retrieval with reranking

Manual Vectorize operations (`search_memories`, `search_papers`, `remember_fact`) remain
available as fallbacks when AutoRAG is unreachable or for single-document operations.

### AI Gateway Logging (v2.2)

All AI-powered knowledge operations (semantic search, memory storage, paper retrieval) flow
through `qnfo-ai` Worker v4.1 → AI Gateway. Use `cloudflare-ai-gateway` MCP server to:
- Inspect prompt/response pairs for knowledge queries
- Debug embedding quality issues
- Audit AI usage patterns across the knowledge pipeline
- Verify no prompt injection or data leakage in stored memories

---

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| Claiming "comprehensive" without KG query | KG-First Discovery Gate -- query `/stats` first |
| Trusting stale memories without cross-reference | Verify against KG + D1 (two-system confirmation) |
| Orphaned KG nodes with 0 edges | Seed BELONGS_TO edges to taxonomy (min 1 edge) |
| Searching only files on disk for "what exists" | KG is canonical; disk is secondary confirmation |
| Skipping impact analysis before modifying entity | Query `/impact/{id}` to check downstream dependents |
| Storing memory without category | Always categorize: user_preference/project_fact/task_outcome/heuristic/anti_pattern |
| Ignoring search_memories for context | Semantic search finds decisions by meaning, not keywords |
| **ZENODO-KG-OWNERSHIP-1: Writing zenodo_doi to KG/D1 without verifying DOI ownership (2026-08-04)** | **HARD GATE (v2.3):** zenodo_doi/zenodo_url may only be written for DOIs verified QNFO-owned against the live API (creator search + person-name variant). `doi LIKE '%zenodo%'` matches external citations and placeholders. Case: blanket backfill created 1,245+ fake links (session dXXJ3TxRQ1VHzGdAyp-lo). Run `research/scripts/zenodo-ownership-check.py` after any backfill. Cross-ref: research v2.54 P5.OWNERSHIP. |
| **PHILPAPERS-DISCOVERABILITY-GAP: Zenodo records without keywords AND abstract are invisible to PhilPapers crawlers (2026-08-06)** | **HARD GATE (v2.8):** PhilPapers discovers papers via Zenodo → DataCite → CrossRef → PhilPapers crawler pipeline. Trigger: abstract (≥200 chars with philosophy-domain terms) + keywords (include at least 3 of: "philosophy of physics", "epistemology", "metaphysics", "ontology", "philosophy of mathematics", "foundations of quantum mechanics", "consilience"). Confirmed: QUNTUF/QUNSAI (2 of ~293) indexed because both have KW+ABS; papers without both are invisible. Fix: `zenodo_philpapers_optimizer.py` batch-adds ORCID 0009-0002-4317-5604 + philosophy keywords + community. Direct path: PhilArchive upload → guaranteed indexing in days. Scripts (git-tracked at `qnfo-skills/knowledge/scripts/`): `zenodo_philpapers_optimizer.py`, `zenodo_fix4.py`, `philpapers_submit.py`, `philpapers_monitor.py`. Cross-ref: author ORCID 0009-0002-4317-5604, PhilPapers IDs QUNTUF/QUNSAI. |

---

## PhilPapers Discoverability Pipeline (v2.8, 2026-08-06)

**Pipeline:** Zenodo DOI registration → DataCite metadata → CrossRef propagation → PhilPapers crawler → PhilPapers index.

**Confirmed indexed records:**

| PhilPapers ID | Title | Zenodo DOI | Keywords | Abstract |
|:---|---:|---|:---:|:---:|
| QUNTUF | The Ultrametric Foundation: A Unified Thesis on Number, Time, Knowledge, and Computation | 10.5281/zenodo.21208346 | 8 ✅ | ✅ |
| QUNSAI | Scaffolds and Invariants: An Epistemic Hygiene Audit of pi, Number Bases, and Geometric Centers | 10.5281/zenodo.21255344 | 9 ✅ | ✅ |

**Trigger mechanism:** PhilPapers crawls CrossRef metadata. Papers with both abstract AND philosophy-domain keywords get indexed. Papers missing either are invisible regardless of title/content quality.

**Discovery formula (validated):**
```
abstract_with_philosophy_terms + domain_keywords + ORCID + community + references
→ DataCite → CrossRef → PhilPapers indexing
```

**ORCID:** `0009-0002-4317-5604` (Rowan Brad Quni-Gudzinas). **Author name inconsistency:** "Quni-Gudzinas, Rowan" vs "Rowan Brad Quni-Gudzinas" across Zenodo records — canonicalize to "Rowan Brad Quni-Gudzinas".

**Automation scripts (Python, git-tracked at `qnfo-skills/knowledge/scripts/` — canonical thin-client location):**
- `zenodo_philpapers_optimizer.py` — batch metadata fix (ORCID, keywords, community, author name)
- `zenodo_fix4.py` — deposit-API-only fixer (paginated, targeted keywords, ORCID for person creators)
- `philpapers_submit.py` — strategy guide + CSV generator + PhilArchive manifest
- `philpapers_monitor.py` — autonomous PhilPapers index watchtower (daily check for new entries)
Local working copy: `C:\Users\LENOVO\AppData\Local\Temp\deepchat_work\` (volatile — always restore from git).

**Direct submission path:** Upload to https://philarchive.org for guaranteed indexing in days (bypasses crawl delay).

**Aggregator cascade:** ORCID → Google Scholar → Semantic Scholar → OSF Preprints → SSRN → PhilPapers. Each aggregator feeds downstream services.

**Scheduled monitoring:** Run `philpapers_monitor.py` daily. Checks PhilPapers for new QUN-prefixed records, compares against known indexed set, estimates coverage vs Zenodo corpus.

Current: **v2.8** (PhilPapers Discoverability Pipeline — Zenodo→DataCite→CrossRef→PhilPapers indexing confirmed via QUNTUF/QUNSAI; 2026-08-06)

