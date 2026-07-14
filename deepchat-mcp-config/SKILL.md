---
name: deepchat-mcp-config
description: DeepChat MCP server configurations for QNFO RAG bridge — auto-loads at session start to restore MCP settings after disaster recovery/reinstall/app data loss. Includes exact settings for qnfo-memory-mcp (6 tools, Vectorize + D1 bindings) and qnfo-ai-search (Cloudflare managed fallback). Priority 1 — auto-loads when MCP settings are missing or user asks about RAG/search/memory configuration. Use this skill for disaster recovery: reinstall DeepChat, then read this skill to restore all MCP connections.
version: "1.0"
category: infrastructure
tags: [mcp, rag, disaster-recovery, vectorize, settings]
---

> **Related:** deepchat-settings, mcp-builder, qnfo-agent

## execute_plan (MANDATORY — Before Any Execution)

update_plan([
  {"step": "Verify DeepChat MCP settings are configured", "status": "pending"},
  {"step": "If settings missing: instruct user to re-add MCP servers using exact values below", "status": "pending"},
  {"step": "Verify MCP Worker health at /health endpoint", "status": "pending"},
  {"step": "Test tool discovery: initialize + tools/list", "status": "pending"},
  {"step": "If AI Search instance missing: guide user through Cloudflare dashboard setup", "status": "pending"}
])

# DeepChat MCP Configuration — Disaster Recovery Skill v1.0

> **Purpose:** Survives DeepChat reinstall, app data loss, OS migration, hardware failure.
> **Auto-load trigger:** Auto-loads when MCP settings are missing or user mentions RAG/search/memory/vector configuration.

---

## Server 1: qnfo-memory-mcp (PRIMARY — 6 Tools, Direct Bindings)

### DeepChat Settings → MCP → Add Server

| Field | Exact Value |
|-------|-------------|
| **Server Name** | `qnfo-memory-mcp` |
| **URL / Endpoint** | `https://qnfo-memory-mcp.q08.workers.dev/mcp` |
| **Transport Type** | `Streamable HTTP` (POST /mcp) |
| **API Key / Token** | *(leave blank — no authentication required)* |
| **Protocol Version** | `2024-11-05` (auto-negotiated) |

### Tools Auto-Discovered (6 tools)

| Tool | Required Args | Optional Args | Description |
|------|--------------|---------------|-------------|
| `search_papers` | `query` (string) | `limit` (number, 1-20, default 10) | Semantic search across QWAV research papers |
| `search_memories` | `query` (string) | `limit` (number, 1-20, default 5), `category` (string: user_preference/project_fact/task_outcome/heuristic/anti_pattern) | Semantic search across persistent agent memories |
| `remember_fact` | `content` (string), `category` (string, enum) | `importance` (number, 0-1, default 0.7), `summary` (string), `session_id` (string) | Store durable fact with D1 + Vectorize dual storage |
| `recall_facts` | *(none — all optional)* | `category` (string), `keyword` (string), `limit` (number, default 10) | Structured recall by category or keyword |
| `query_graph` | `endpoint` (string: stats/nodes/neighbors/impact/query) | `params` (object: label, search, id, query) | Query QNFO Knowledge Graph (2,064+ nodes) |
| `get_paper_context` | `slug` (string) | `limit_chars` (number, default 5000) | Retrieve full paper body from D1 living-paper |

### Architecture (What It Connects To)
```
Worker Bindings (v1.4):
├── AI           → @cf/baai/bge-base-en-v1.5 (768-dim)
├── MEMORY_DB    → D1 qnfo-graph (agent_memories table)
├── PAPER_DB     → D1 living-paper (616 papers)
├── MEMORY_VZ    → Vectorize qnfo-handoffs (768-dim, cosine)
├── PAPER_VZ     → Vectorize qwav-research-v2 (768-dim, cosine)
└── GRAPH        → Service binding: graph-api
```

### Health Check (before registration)
```
GET https://qnfo-memory-mcp.q08.workers.dev/health
Expected: {"status":"ok","server":"qnfo-memory-mcp","version":"1.0.0","protocol":"2024-11-05",...}
```

---

## Server 2: qnfo-ai-search (MANAGED REDUNDANCY — Cloudflare AI Search)

### Prerequisite: Create Instance in Cloudflare Dashboard

1. Go to: https://dash.cloudflare.com/?to=/:account/ai/ai-search
2. Click **Create Instance**
3. Configure:
   - **Name:** `qnfo-research`
   - **Data Source:** R2 bucket `qnfo`, prefix `qnfo/papers/`
   - **Embedding Model:** `@cf/baai/bge-base-en-v1.5` (768-dim)
   - **Chunking:** Default (512 tokens)
4. Go to instance **Settings** → enable **Public Endpoint** ✅
5. Go to instance **Settings** → enable **MCP** ✅
6. Copy the MCP URL from the settings page

### DeepChat Settings → MCP → Add Server

| Field | Exact Value |
|-------|-------------|
| **Server Name** | `qnfo-ai-search` |
| **URL / Endpoint** | `https://<INSTANCE_ID>.search.ai.cloudflare.com/mcp` |
| **Transport Type** | `Streamable HTTP` |
| **API Key / Token** | *(leave blank if Public Endpoint enabled)* |

> **The INSTANCE_ID** is displayed in the Cloudflare dashboard after creating the instance. Fill it in once you have it.

---

## REST API Fallback (No MCP Registration Needed)

These are direct HTTP endpoints — usable without any DeepChat configuration:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://search-worker.q08.workers.dev/api/search/papers?q=X&limit=10` | GET | Semantic paper search |
| `https://search-worker.q08.workers.dev/api/search/semantic?q=X&limit=5` | GET | Raw Vectorize query |
| `https://search-worker.q08.workers.dev/api/search?q=X&type=all&limit=10` | GET | FTS5 keyword search |
| `https://search-worker.q08.workers.dev/health` | GET | Health check |
| `https://graph-api.q08.workers.dev/stats` | GET | Knowledge graph stats |
| `https://qnfo-ai-worker.q08.workers.dev/health` | GET | AI worker health |

---

## Disaster Recovery Protocol

### Scenario: DeepChat Reinstall / App Data Loss / New Machine

1. **Verify the skill exists:**
   - File: `%USERPROFILE%\.deepchat\skills\deepchat-mcp-config\SKILL.md`
   - Backup: R2 `qnfo/prompts/skills/deepchat-mcp-config/SKILL.md`

2. **Restore from R2 if local file missing:**
   ```bash
   npx wrangler r2 object get qnfo/prompts/skills/deepchat-mcp-config/SKILL.md --remote --file=SKILL.md
   ```

3. **Verify MCP Worker is healthy:**
   ```bash
   curl https://qnfo-memory-mcp.q08.workers.dev/health
   ```

4. **Re-add servers in DeepChat Settings → MCP** using the exact values in this document

5. **Verify tool discovery:**
   - DeepChat should auto-detect 6 tools from qnfo-memory-mcp
   - Test: "search for papers about ultrametric quantum computation"

### Scenario: MCP Worker Down

1. Check Cloudflare Dashboard → Workers & Pages → `qnfo-memory-mcp`
2. Redeploy if needed: `cd <project-dir> && npx wrangler deploy`
3. Source code at: `C:\Users\LENOVO\AppData\Local\Programs\DeepChat\memory-infra\qnfo-memory-mcp\`

### Scenario: Vectorize Index Corrupted

```bash
# Verify dimensions
npx wrangler vectorize get qnfo-handoffs --json
npx wrangler vectorize get qwav-research-v2 --json
# Both should show: {"config": {"dimensions": 768, "metric": "cosine"}}
```

---

## Verification Checklist

After MCP registration, verify all 6 tools are discoverable:

```python
import json, ssl, urllib.request
ctx = ssl.create_default_context()
body = json.dumps({"jsonrpc":"2.0","method":"tools/list","id":1}).encode()
r = urllib.request.Request("https://qnfo-memory-mcp.q08.workers.dev/mcp",
    data=body, method="POST",
    headers={"Content-Type":"application/json","User-Agent":"Verify/1.0"})
d = json.loads(urllib.request.urlopen(r, timeout=10, context=ctx).read())
tools = [t["name"] for t in d["result"]["tools"]]
print(f"Tools: {tools}")  # Should show 6 tools
assert len(tools) == 6, "MISSING TOOLS"
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-07-14 | Initial: MCP configurations for qnfo-memory-mcp + AI Search, disaster recovery protocol, REST API fallback URLs, verification checklist |

---

## RT: RED-TEAM SELF-AUDIT

Before claiming configuration valid:
1. **Health check:** Verify both MCP servers respond to /health
2. **Tool discovery:** Verify tools/list returns 6 tools
3. **Tool execution:** Test search_papers with a known query
4. **Persistence:** Verify D1 agent_memories has records
5. **Failover:** Verify REST API fallback /api/search/papers works

> **deepchat-mcp-config v1.0 — Disaster-recovery MCP configuration for DeepChat↔Vectorize RAG bridge**
