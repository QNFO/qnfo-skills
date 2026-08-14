---
name: knowledge
description: QNFO Knowledge Graph and durable memory management -- graph querying for due diligence and impact analysis (stats, nodes, neighbors, impact, query endpoints), ultrametric clustering and taxonomy edge seeding, semantic memory search via Vectorize, persistent fact storage in D1/Vectorize, cross-system discovery, and paper context retrieval. Use for remembering, recalling, and discovering knowledge across the QNFO ecosystem.
version: 2.11
triggers: ["knowledge graph", "KG", "graph", "graph-api", "dependencies", "impact", "neighbors", "nodes", "edges", "due diligence", "memory", "remember", "recall", "durable learning", "semantic search", "Vectorize", "D1 memory", "fact storage", "discovery", "cross-system", "ultrametric", "p-adic", "taxonomy", "impact analysis", "what exists", "who depends", "ecosystem", "paper search", "memory search", "fact", "knowledge base"]
related: ["qnfo-core"]
priority: 1
platform: cloudflare
autonomous: true
self_sufficient: true
---
> **v2.11 UPDATE (2026-08-14, kaizen — Zenodo Dissemination Playbook D1-D7 implemented):**
> Red-team: subagent reviewer stalled -> direct parent-agent adversarial audit (session waFvkOWgtaYZqNMLWOqdW continuation).
> HARD: 0. SOFT: 0. DESIGN: 0 (post-fix).
> Changes:
> (1) [HARD] **Zenodo Dissemination Playbook section added** — implements playbook
>     D1-D7 (from AI Mode export `_26226160010.md`, playbook note
>     `D:\Obsidian\notes\v1\2026\08\14\Zenodo-dissemination-playbook-2026-08-14.md`):
>     D1 EuroSciVoc scheme/identifier subjects, D2 alternate_identifiers,
>     D3 3+ communities, D4 Semantic Scholar gap monitoring, D5 OpenCitations COCI
>     + doi.org meta verification, D6 bucket machine-readable files, D7 fediverse
>     broadcast. Live-verified 2026-08-14: OpenAIRE indexes QNFO (QUNTUF+UCS both
>     total=1); Semantic Scholar does NOT index 5/5 sampled QNFO records (404);
>     QUNTUF subjects are plain arXiv strings WITHOUT scheme/URI; alternate_identifiers
>     EMPTY; 1 community only; COCI baseline 0.
> (2) [HARD] **New scripts (git-tracked qnfo-skills/knowledge/scripts/)** —
>     `zenodo_dissemination_enhancer.py` (D1-D3, dry-run default), 
>     `zenodo_dissemination_health.py` (D4-D5, cron-ready JSON, exit codes),
>     `zenodo_bucket_assets.py` (D6, generate-only default). D7 script lives in
>     social-media-management skill (`zenodo_broadcast.py`, compose-only default).
> (3) [DESIGN] **execute_plan literal example added** — `[QNFO.OUTREACH.2026-08-14-CONTINUE.P7]`.
> Cross-reference: playbook note 2026-08-14, social-media-management v1.7.0, kaizen v1.9x.
> **v2.10 UPDATE (2026-08-10, kaizen — PAPER-CONTEXT-TOOL-EMPTY-1: direct D1 query is the canonical paper-body path):**
> Red-team: direct parent-agent 5-adversary audit follow-up (session 0SnaUK-QccIJkohojGMQS). Watchtower: 20/20 QNFO skills N-2 CLEAN pre-edit. HARD: 1. SOFT: 0. DESIGN: 1. Changes:
> (1) [HARD] **PAPER-CONTEXT-TOOL-EMPTY-1 anti-pattern added** — `get_paper_context` and `search_papers_enriched` return EMPTY in this environment (verified repeatedly 2026-08-10) even when the paper body exists in D1 living-paper. An empty tool result does NOT mean the paper is missing (VECTORIZE-SILO-1 class). Canonical case: JPCUB verification — all get_paper_context probes returned empty; the same bodies were retrieved by direct Cloudflare D1 HTTP API query (papers table, body_md column). Working path: token `C:\Users\LENOVO\tokens\cloudflare`; POST https://api.cloudflare.com/client/v4/accounts/{acct}/d1/database/{db}/query with acct=edb167b78c9fb901ea5bca3ce58ccc4b, db=70a58cb3-b2cd-498d-877f-ecca86859a22 (living-paper), SQL `SELECT slug, doi, body_md FROM papers WHERE lower(doi) LIKE ?`.
> (2) [DESIGN] **Paper Context & Search section updated** — get_paper_context remains the documented tool, but a direct-D1 fallback block now precedes it when the tool returns empty.
> Cross-reference: kaizen v1.94, VECTORIZE-SILO-1, D1 living-paper > **v2.9 UPDATE (2026-08-10, user directive — judicious labeling + monthly cadence):**
> Red-team: 5-adversary audit of the PhilPapers monitor scheduled task (session _YeVIWmYVfkpQao_Ujkh0).
> Changes:
> (1) [HARD] **Judicious labeling policy (user directive 2026-08-10):** only papers that ARE
>     philosophy papers may carry philosophy-class labels (philosophy of physics/mathematics/
>     science/information, epistemology, metaphysics, ontology, structural realism, paradigm
>     theory). The 2026-08-06 batch injected these into ~99% of the corpus (675/680) including
>     license agreements, patent filings, physics-only and finance records — an over-tagging
>     incident. **EXISTING RECORDS LEFT AS-IS per user directive — no retroactive edits.**
>     `zenodo_philpapers_optimizer.py` now gates keyword injection behind
>     `is_philosophy_core_record()`; `philpapers_monitor.py` v2 shares the PHIL_LABELS list.
> (2) [HARD] **Scheduled task runs MONTHLY, not daily** (1st of month 06:00 UTC — scheduled
>     task "PhilPapers Index Monitor (Monthly)", id 48240e95). The documented "daily cron
>     ffc8f08f" NEVER existed in the scheduler (verified live 2026-08-10); daily polling is
>     waste because the Zenodo→DataCite→CrossRef→PhilPapers crawl cycle is days-to-weeks.
>     `philpapers_monitor.py` v2: ORCID-identifier query (fuzzy name queries return 0 hits),
>     size≤25 pagination (unauthenticated API cap), coverage math ZeroDivision guard,
>     total_checks increments on 403 cycles, domain-scoped coverage denominator.
> (3) [SOFT] PhilPapers live index is Cloudflare-blocked (403 on every path as of 2026-08-10)
>     — monitor falls back to search-engine cross-checks; K=0 new.
> Cross-reference: kaizen v1.80, philpapers_monitor.py v2, zenodo_philpapers_optimizer.py v2.9.

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

# KNOWLEDGE — v2.10
(70a58cb3-b2cd-498d-877f-ecca86859a22), session 0SnaUK-QccIJkohojGMQS.
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
Cross-ref: research v2.97 P5.OWNERSHIP, kaizen v2.08.

**KG dual-schema note (2026-08-07):** the KG stores Zenodo linkage two ways —
`properties.zenodo_doi` (legacy 4-D seed, was 11 nodes) and `properties.doi` + `type: "zenodo"`
(bulk seed, 1,113 nodes). Querying `zenodo_doi` alone returns a false "not indexed" verdict.
Reconciled 2026-08-07: backfilled `properties.zenodo_doi` onto all 726 distinct DOI-bearing nodes
(now 1,113 nodes carry both keys), ownership-verified against the live Zenodo API (10/10 sampled).
Future audits MUST query BOTH `properties.doi` and `properties.zenodo_doi`, or match node `name` = DOI.
D1 living-paper likewise: `zenodo_doi` backfilled from the canonical `doi` column (209 -> 412 distinct).

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
   **SYNC CONTRACT (verified live 2026-08-11, session FMQelHEBu67pv0QrOWU6h):**
   - `POST https://graph-api.qnfo.org/sync` with header `X-Sync-Token` (token at `C:\Users\LENOVO\tokens\qnfo-sync-token`)
   - Body: `{"action":"bulk","edges":[{ "id": "<stable-edge-id>", "source_id": "<src>", "target_id": "<tgt>", "relationship_type": "<TYPE>" }]}` — `id`, `source_id`, `target_id`, `relationship_type` are ALL REQUIRED. Other key names (`type`, `relationship`, `source`/`target`, `from`/`to`, `rel`) return `Edge undefined: D1_TYPE_ERROR: Type 'undefined' not supported for value 'undefined'` (5 shapes tested and failed).
   - Nodes: `{"action":"bulk","nodes":[{ "id": "<node-id>", "label": "<Label>", "name": "<Name>", "properties": { ... } }]}` — full-replace semantics for properties (verified: vault node note_count reconciled 5588→5616 same-turn).
   - READ: `POST https://graph-api.qnfo.org/query` body `{"query": "<SQL>"}` — param MUST be `query` (NOT `sql`; `{"sql":...}` returns 400 "Missing query"). Response `{results: [...]}`.
   - THROTTLE + RESUME (verified): endpoint throttles sustained bulk writes (~0.5-1 edge/sec); background exec sessions die ~15-20 min. Bulk seeding MUST be idempotent-resumable: query existing edges first (`SELECT target_id FROM edges WHERE source_id=? AND relationship_type=?`), seed only missing, log progress-to-file, run `python -u` unbuffered. Canonical: vault:obsidian-v1 → 5,616 CONTAINS edges seeded across 3 process lifetimes, `edgesInserted` counts only new rows.
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
# FALLBACK (PAPER-CONTEXT-TOOL-EMPTY-1): if get_paper_context returns empty, the body exists in D1 living-paper. Query directly via Cloudflare D1 HTTP API:
#   POST https://api.cloudflare.com/client/v4/accounts/{acct}/d1/database/{db}/query
#   acct=edb167b78c9fb901ea5bca3ce58ccc4b, db=70a58cb3-b2cd-498d-877f-ecca86859a22 (living-paper)
#   SELECT slug, doi, body_md FROM papers WHERE lower(doi) LIKE '%<fragment>%'
# token: C:\Users\LENOVO\tokens\cloudflare

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
| **PAPER-CONTEXT-TOOL-EMPTY-1: Treating an empty get_paper_context / search_papers_enriched result as 'paper not in D1' (2026-08-10)** | **HARD GATE (v2.10):** these tools return EMPTY in this environment even when the paper body exists (VECTORIZE-SILO-1 class; canonical case: JPCUB verification 2026-08-10). An empty result is a TOOL gap, not a DATA gap. Fallback: direct Cloudflare D1 HTTP API query against living-paper DB 70a58cb3-b2cd-498d-877f-ecca86859a22 (papers table, body_md) using token C:\Users\LENOVO\tokens\cloudflare. Verify presence with SELECT slug,doi,body_md before concluding missing. Cross-ref: VECTORIZE-SILO-1, kaizen v1.94. |
| **ZENODO-KG-OWNERSHIP-1: Writing zenodo_doi to KG/D1 without verifying DOI ownership (2026-08-04)** | **HARD GATE (v2.3):** zenodo_doi/zenodo_url may only be written for DOIs verified QNFO-owned against the live API (creator search + person-name variant). `doi LIKE '%zenodo%'` matches external citations and placeholders. Case: blanket backfill created 1,245+ fake links (session dXXJ3TxRQ1VHzGdAyp-lo). Run `research/scripts/zenodo-ownership-check.py` after any backfill. Cross-ref: research v2.54 P5.OWNERSHIP. |
| **PHILPAPERS-DISCOVERABILITY-GAP: Zenodo records without keywords AND abstract are invisible to PhilPapers crawlers (2026-08-06)** | **HARD GATE (v2.9):** PhilPapers discovers papers via Zenodo → DataCite → CrossRef → PhilPapers crawler pipeline. Trigger: abstract (≥200 chars with philosophy-domain terms) + keywords. **JUDICIOUS LABELING (user directive 2026-08-10):** only papers that ARE philosophy papers may carry philosophy-class labels — non-philosophy QNFO records (physics, engineering, licensing, patents, finance) must NOT be tagged as philosophy. Existing records left AS-IS (over-tagging incident: 675/680 from the 2026-08-06 batch — no retroactive edits). Confirmed indexed: QUNTUF/QUNSAI (2 of ~293). Future optimizer runs gate injection behind `is_philosophy_core_record()`; monitor runs MONTHLY (not daily). Direct path: PhilArchive upload → guaranteed indexing in days. Scripts (git-tracked at `qnfo-skills/knowledge/scripts/`): `zenodo_philpapers_optimizer.py`, `zenodo_fix4.py`, `philpapers_submit.py`, `philpapers_monitor.py` (v2). Cross-ref: author ORCID 0009-0002-4317-5604, PhilPapers IDs QUNTUF/QUNSAI. |
| **S2-ZENODO-GAP-1: Assuming Semantic Scholar ingests QNFO Zenodo records (2026-08-14)** | **HARD GATE (v2.11):** live probe of 5/5 flagship QNFO DOIs (21208346, 21255344, 21824396, 21827737, 21547793) returned 404 — Semantic Scholar does NOT index the QNFO corpus today, despite the generic claim in `_26226160010.md` session 1. OpenAIRE EXPLORE is the confirmed active indexer (total=1 for QUNTUF + Ultrametric Code Spaces). Do not claim S2 coverage in outreach or metrics; monitor via `zenodo_dissemination_health.py` (D4) and treat S2 absence as a discovery gap to close via metadata levers (D1 subjects scheme/URI, D2 alternate_identifiers, D6 bucket schema files). |
| **SUBJECT-SCHEME-GAP-1: Subjects as plain arXiv strings without scheme/identifier (2026-08-14)** | **HARD GATE (v2.11):** QUNTUF subjects are `{"term": "Physics - High Energy Physics - Phenomenology (hep-ph)"}` with NO `scheme`/`identifier` — aggregators parse Term IDs/URIs, not bare strings (playbook §2). Do not claim "vocabulary-optimized" metadata for records lacking `scheme`/`identifier` on subjects. Enrichment path: `zenodo_dissemination_enhancer.py --subjects-json <map> --record <id> --apply` (D1). Never fabricate URIs — pass real EuroSciVoc term identifiers only. |
| **ALTERNATE-IDENTIFIER-GAP-1: Empty alternate_identifiers (2026-08-14)** | **HARD GATE (v2.11):** `alternate_identifiers` is EMPTY on QUNTUF — duplicate-merge levers (SWH etc.) are unapplied (playbook §4, D2). Path: `zenodo_dissemination_enhancer.py --alternate-json <map> --record <id> --apply`. |
| **COMMUNITY-COUNT-GAP-1: Single community per record (2026-08-14)** | **HARD GATE (v2.11):** QUNTUF carries only `qnfo`; playbook recommends 3+ high-traffic communities per record (D3). Membership is via deposit-metadata `communities` field. Only add EXISTING communities (verify via `/api/communities/{slug}`; the enhancer skips non-existent slugs). NOTE: `ecfunded`/grant-linked communities apply to EU-funded records — QNFO is self-funded, so grant-linked slugs are NOT applicable; do not fabricate grant linkage. |

---

## Zenodo Dissemination Playbook (v2.11, 2026-08-14) — D1-D7 IMPLEMENTED

**Source:** AI Mode export `_26226160010.md` (5 concatenated sessions) distilled into
`D:\Obsidian\notes\v1\2026\08\14\Zenodo-dissemination-playbook-2026-08-14.md`.
**Live-verified 2026-08-14:** OpenAIRE indexes QNFO (QUNTUF + Ultrametric Code Spaces,
total=1 each); Semantic Scholar does NOT index 5/5 sampled QNFO DOIs (S2-ZENODO-GAP-1);
CORE API probe 429 (unverified); BASE not probed.

### Levers and tooling (all scripts git-tracked `qnfo-skills/knowledge/scripts/`)

| Lever | What | Script / path | Status |
|:------|:-----|:--------------|:-------|
| **D1** | EuroSciVoc `scheme`/`identifier` on subjects | `zenodo_dissemination_enhancer.py --subjects-json <map> --record <id> [--apply]` | Scripted; apply per-record |
| **D2** | `alternate_identifiers` (SWH etc.) | `zenodo_dissemination_enhancer.py --alternate-json <map> --record <id> [--apply]` | Scripted; apply per-record |
| **D3** | 3+ communities per record | `zenodo_dissemination_enhancer.py --community <slug> ...` (existence-verified) | Scripted; NOT grant-linked (self-funded) |
| **D4** | Semantic Scholar gap monitoring | `zenodo_dissemination_health.py --doi <doi>` (reports INDEXED/MISSING) | Scripted; baseline = 5/5 MISSING |
| **D5** | OpenCitations COCI + doi.org meta verification | `zenodo_dissemination_health.py` (exit 1 = NEW citations; state file `zenodo_dissemination_state.json`) | Scripted; baseline 0 citations |
| **D6** | Bucket machine-readable files (datacite.json / README.md / metadata.jsonld) | `zenodo_bucket_assets.py --record <id> [--upload]` | Scripted; generate-only default |
| **D7** | Fediverse broadcast on publish (<280-char impact copy) | `zenodo_broadcast.py` in **social-media-management** skill (compose-only default; `--post` explicit) | Scripted; plumbing exists (52 BS / 7 MA) |

### Enhance flow (per record)
1. `python scripts\zenodo_dissemination_health.py --doi 10.5281/zenodo.XXXXXXX` — baseline S2/COCI/meta.
2. `python scripts\zenodo_dissemination_enhancer.py --record XXXXX --subjects-json subjects.json` — DRY-RUN first; `--apply` writes a draft; publish the draft for a new version.
3. `python scripts\zenodo_bucket_assets.py --record XXXXX` — generate D6 files; `--upload` streams to the draft bucket.
4. Broadcast: `python <social skill>\scripts\zenodo_broadcast.py --doi ... --title "..."` then `--post` when the record is live.

### Guardrails (playbook §7, unchanged hard gates)
- **ZENODO-KG-OWNERSHIP-1** — no DOI writes without live ownership verification.
- **No fabricated URIs** — EuroSciVoc identifiers must be real (the note's `http://europa.eu` example is a generic domain, NOT a term URI).
- **Judicious labeling** stays; grant-linked communities N/A (self-funded).
- **TEST-SEND-EXTERNAL-1 / BSKY-300-GRAPHEME-1** apply to D7 broadcasts.

---

## PhilPapers Discoverability Pipeline (v2.8, 2026-08-06)

**Pipeline:** Zenodo DOI registration → DataCite metadata → CrossRef propagation → PhilPapers crawler → PhilPapers index.

**Confirmed indexed records:**

| PhilPapers ID | Title | Zenodo DOI | Keywords | Abstract |
|:---|---:|---|:---:|:---:|
| QUNTUF | The Ultrametric Foundation: A Unified Thesis on Number, Time, Knowledge, and Computation | 10.5281/zenodo.21208346 | 8 ✅ | ✅ |
| QUNSAI | Scaffolds and Invariants: An Epistemic Hygiene Audit of pi, Number Bases, and Geometric Centers | 10.5281/zenodo.21255344 | 9 ✅ | ✅ |

**Corpus optimization status (2026-08-06, complete):** `zenodo_fix4.py` main pass fixed **773/900 deposits** (targeted philosophy keywords per title domain + ORCID `0009-0002-4317-5604` on person creators) with 39 already-optimized skips; retry pass (`zenodo_fix4_retry.py`, 60s timeouts + 4 retries + backoff) cleaned up ~74 transient failures (DNS burst, IncompleteRead, 5xx) adding ~264 more touches (618 records confirmed already optimized). Final retry pass (2nd run, low-traffic window) reduced errors to 18: 902 deposits, 680 skipped (already optimized), 204 fixed — remaining 18 are 14 titleless draft deposits (400 by design, cannot be edited) + ~4 persistent rate-limit/DNS failures. Previously-504 record Ultrametric Code Spaces (10.5281/zenodo.21824396) fixed + verified. Fixes verified persisted: sampled records return state=done + HTTP 200 on the public API with philosophy keywords present. All person-creator records now carry the ORCID; org-creator chapter-fragment stubs (STUB-RECORD-1 class) carry keywords only. QUNTUF/QUNSAI both verified with ORCID attached post-run.

**Corpus optimization v5 (2026-08-06, complete):** `zenodo_corpus_optimizer.py`
targeted the remaining discoverability levers — **823/902 deposits fixed** (66 already-optimized skips, 13 errors = drafts/transients):
- **Subjects (arXiv categories)**: ~900 records gained domain-matched subjects (`Physics - History and Philosophy of Physics (physics.hist-ph)`, `hep-ph`, `quant-ph`, `math.NT`, `cs.CC`) — the single biggest untapped lever (was 2/902)
- **Author canonicalization**: 8 name variants → `Quni-Gudzinas, Rowan Brad` (was 258 non-canonical, incl. QUNTUF itself `Quni-Gudzinas, Rowan`)
- **Language**: `eng` set on ~874 records (was 28/902)
- **Affiliation**: `QNFO` added (flat legacy schema — verified live, NOT v3 nested)
- **License**: normalized to cc-by-4.0
- **ORCID**: on remaining person-creators (orgs correctly excluded)
- **Abstracts**: `!desc<200(no-auto-backfill)` flags only — abstracts NEVER fabricated (real-source backfill from papers.qnfo.org is the deferred follow-up)
**Community membership**: QNFO + QWAV Zenodo communities confirmed `record_submission_policy: open`; the modern API removed dedicated membership routes (404/405), so membership goes via the deposit-metadata `communities` field (edit→set→PUT→publish, verified on 21354771 → records API shows `communities: [{'id': 'qnfo'}]`). Community pass (community_pass2.py) adds `qnfo` to all titled records.
Verified persisted: subjects + language + canonical name + affiliation on sampled records (state=done, public API 200). Scripts: `zenodo_corpus_optimizer.py`, `corpus_gap_audit.py`, `community_pass2.py` (git-tracked `qnfo-skills/knowledge/scripts/`).

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

**Scheduled monitoring:** Run `philpapers_monitor.py` **monthly** (1st of month 06:00 UTC — scheduled task "PhilPapers Index Monitor (Monthly)"; the old "daily cron ffc8f08f" never existed). The crawl cycle is days-to-weeks, so daily polling is waste. Checks PhilPapers for new QUN-prefixed records, compares against known indexed set, estimates coverage vs the philosophy-eligible Zenodo subset (judicious-labeling denominator).

Current: **v2.11** (Zenodo Dissemination Playbook D1-D7 implemented 2026-08-14 — enhancer/health/bucket-assets scripts + S2-ZENODO-GAP-1/SUBJECT-SCHEME-GAP-1/ALTERNATE-IDENTIFIER-GAP-1/COMMUNITY-COUNT-GAP-1; PhilPapers Discoverability Pipeline — judicious labeling + monthly cadence; QUNTUF/QUNSAI indexed, 2 of ~293)

