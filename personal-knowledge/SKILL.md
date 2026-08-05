---
name: personal-knowledge
description: Query the PERSONAL semantic layer (personal-life Vectorize/D1/Workers) from DeepChat. Use when the user asks about their own files, documents, life admin, Obsidian vault, personal archives, or anything NOT QNFO/QWAV research. Bridges personal-search endpoint + durable memories + conversation history + Obsidian vault. STRICTLY personal domain — never mixes with qnfo-* (user mandate 2026-08-04).
version: 1.0
kif_tags: [PERSONAL]
---

# PERSONAL KNOWLEDGE — v1.0 (2026-08-04)

> **PURPOSE:** The user uses DeepChat as the single interface for ALL information
> needs. This skill is the integration path for their PERSONAL files — everything
> that is NOT QNFO/QWAV research (which stays in `search_papers` / `query_graph` /
> `qnfo-projects`). Do NOT cross-contaminate.

## Separation Mandate (HARD — user directive 2026-08-04)

- Personal layer: `d-drive` bucket, `personal-life` Vectorize, `personal-life` D1,
  `personal-life-indexer` + `personal-life-search` Workers
- QNFO layer: `qnfo-*` buckets/indexes/Workers, `search_papers`, `query_graph`
- **These NEVER mix.** Personal files in qnfo-projects = BUCKET-COMMINGLE-1 (HARD).

## Architecture

```
D:\Archive, D:\Obsidian, D:\Downloads, D:\Google⁠ Download Your Data ...
   │  rclone sync (detached, resumable)
   ▼
d-drive bucket (R2)
   │  personal-life-indexer Worker (cron 0 */12 + /index?cursor=)
   ▼
personal-life Vectorize (768d cosine)  +  personal-life D1 (files registry)
   │
   ▼
personal-life-search Worker:  GET /search?q=<query>&topK=N
   ▼
DeepChat UI (the user's interface)
```

## Query Endpoints

| Endpoint | Method | Purpose |
|:---------|:-------|:--------|
| `https://personal-life-search.q08.workers.dev/search?q=<query>&topK=20` | GET/POST | Semantic search over personal files |
| `https://personal-life-search.q08.workers.dev/stats` | GET | Count of indexed files |
| `https://personal-life-indexer.q08.workers.dev/index?limit=N&scanCap=N&prefix=...&cursor=...` | GET/POST | Trigger/resume indexing |
| `https://personal-life-indexer.q08.workers.dev/files?prefix=...&limit=N` | GET | List indexed file registry |

## DeepChat Integration Path (when user asks about personal content)

```
1. personal-life-search  →  /search?q=<user question>     (semantic hits on their files)
2. search_memories       →  durable memories (preferences, facts, outcomes)
3. search_conversations  →  past DeepChat conversations about this topic
4. Synthesize ONE answer across all three sources (user hates checking multiple places)
```

**Cross-reference rule:** personal results are surfaced with their R2 path
(e.g., `obsidian/notes/v1/2025/07/02/_25183003234.md`) so the user can open them
via the mounted drive or rclone cat.

## Handling Different File Types

The indexer covers text formats automatically (md, txt, csv, json, html, tex, bib,
yaml, log, ini, ...). **PDFs and .docx are NOT auto-indexed** — they need the
extraction helper:

```python
# extract_pdf_text.py — run manually, upload result to d-drive/_extracted/
# Requires: pip install pypdf python-docx (or PyMuPDF)
import os, sys, glob
from pathlib import Path

def extract_pdf(p):
    try:
        from pypdf import PdfReader
        return "\n".join((pg.extract_text() or "") for pg in PdfReader(p).pages)
    except Exception:
        try:
            import fitz  # PyMuPDF
            return "".join(pg.get_text() for pg in fitz.open(p))
        except Exception as e:
            return f"[extract failed: {e}]"

def extract_docx(p):
    from docx import Document
    return "\n".join(par.text for par in Document(p).paragraphs)

# For each PDF/DOCX in a folder, write <name>.txt into D:\_extracted\, then:
# rclone copy D:\_extracted primary-r2:d-drive/_extracted --transfers 8
# (indexer TEXT_EXTS includes 'txt' — next cron/slice picks them up)
```

## Indexer Operations (for the agent)

```bash
# Resume interrupted indexing from saved cursor
python C:\Users\LENOVO\AppData\Local\Temp\per_driver.py   # or replicate the loop:
#   GET /index?limit=300&scanCap=400&prefix=obsidian/&cursor=<last cursor>
#   save returned cursor; repeat until "done": true

# Full re-index of a prefix (registry sig skips unchanged files)
#   GET /index?limit=200&scanCap=400&prefix=downloads/

# Clean a bad file (40023 vector): delete its D1 row + vectorize vectors, re-run
```

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| **PERSONAL-QNFO-MIX-1:** answering a personal question from search_papers (QNFO corpus) or answering a research question from personal-life | Route by domain: personal → /search?q= (this skill); research → search_papers/query_graph (research skill). Verify the source layer in the answer. |
| **PERSONAL-STATS-ONLY-1:** reporting "filesIndexed: N" without actually searching | The user wants ANSWERS, not index stats. Always run /search?q= for their actual question. |
| **PDF-SKIP-1:** telling the user "PDFs aren't indexed" instead of extracting them | Run the extraction helper + rclone to _extracted/ so the indexer picks them up. |
| **SINGLE-SOURCE-1:** answering from only the search endpoint | Bridge memories + conversations too — DeepChat is the single interface; the answer should be too. |

## Related
- cloudflare v3.32 §Vectorize Indexing Gotchas (indexer anti-patterns)
- knowledge skill (QNFO memory/KG — different layer, never merged)
- system v2.13 (skill-sync, desktop boundary)
