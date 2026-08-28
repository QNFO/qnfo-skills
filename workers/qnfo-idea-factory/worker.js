// qnfo-idea-factory v1.3.0 — public read-only "Idea Factory" chat UI.
// RESEARCH THREADS ONLY (category='research' in qnfo-audit.chat_sessions).
// Infra/delegation/automation sessions are stored (category='infra') but NEVER served publicly.
// Full multi-message conversations are rendered as LLM-style chat bubbles.
// Routes: GET / (UI), /api/sessions, /api/session/:id, /api/feed, /health, /robots.txt
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors() });
    }
    try {
      if (path === "/health") return json({ status: "ok", worker: "qnfo-idea-factory", version: "1.3.0", bindings: { d1: !!env.QNFO_AUDIT } });
      if (path === "/robots.txt") return new Response("User-agent: *\nAllow: /\n", { headers: { "Content-Type": "text/plain", "Cache-Control": "public, max-age=86400" } });
      if (path === "/api/sessions") return handleSessions(url, env);
      if (path.startsWith("/api/session/")) return handleSession(path, env);
      if (path === "/api/feed") return handleFeed(url, env);
      if (path === "/api/ask" && request.method === "POST") return handleAsk(url, request, env);
      if (path === "/api/proposals" && request.method === "POST") return handleProposalPost(request, env);
      if (path === "/api/proposals" && request.method === "GET") return handleProposalList(request, env);
      if (path === "/") return serveUI();
      return json({ error: "Not found" }, 404);
    } catch (e) {
      return json({ error: "Server error: " + e.message }, 500);
    }
  }
};

function cors() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  };
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: Object.assign({ "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }, cors())
  });
}

// ---------------------------------------------------------------------------
// REDACTION LAYER — applied to every string before it leaves this worker
// ---------------------------------------------------------------------------
const REDACT = "[redacted]";

function redact(s) {
  if (!s) return s;
  let t = String(s);
  // Protect DOIs and URLs (never mangle them)
  const protectedParts = [];
  t = t.replace(/(https?:\/\/[^\s"'<>()]+)/g, (m) => { protectedParts.push(m); return "\u0000P" + (protectedParts.length - 1) + "\u0000"; });
  t = t.replace(/(10\.\d{4,9}\/\S+)/g, (m) => { protectedParts.push(m); return "\u0000P" + (protectedParts.length - 1) + "\u0000"; });

  // Emails
  t = t.replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, REDACT);
  // Bearer tokens
  t = t.replace(/\bBearer\s+[A-Za-z0-9._~+/-]+=*/gi, "Bearer " + REDACT);
  // Key/value secrets: token=..., key=..., secret=..., password=..., authorization=...
  t = t.replace(/(\b(?:api[_-]?key|secret|password|passwd|authorization|auth[_-]?token|access[_-]?token|refresh[_-]?token|zenodo[_-]?token|cf[_-]?token|github[_-]?token)\b\s*[:=]\s*["']?)[A-Za-z0-9._~+/-]{8,}/gi, "$1" + REDACT);
  // Known token prefixes (wrangler OAuth, CF API tokens start with a long alnum)
  t = t.replace(/\b(?:wWbJ|AoG|cf-api|glpat|ghp_|xox[baprs]-)[A-Za-z0-9_-]{6,}/g, REDACT);
  // Long hex (32+) — usually a hash/secret
  t = t.replace(/\b[0-9a-fA-F]{32,}\b/g, REDACT);
  // Windows paths
  t = t.replace(/\b[A-Za-z]:\\[^\s"'<>|]*/g, REDACT);
  // MSYS paths / home
  t = t.replace(/\/(?:c|d|e|f|g)\/Users\/[^\s"'<>|]*/gi, REDACT);
  t = t.replace(/%[A-Za-z]+%/g, REDACT);
  // IP addresses
  t = t.replace(/\b\d{1,3}(?:\.\d{1,3}){3}\b/g, REDACT);
  // Phone numbers
  t = t.replace(/\+\d{1,3}[\d\s()-]{7,}\b/g, REDACT);
  // Long session/run IDs that look like internal handles
  t = t.replace(/\b(?:session|thread|run|task|delegation|bg_|th_)[A-Za-z0-9_-]{10,}\b/gi, (m) => m.split(/[:_-]/)[0] + ":" + REDACT);
  // Generic long alphanumeric runs (24+) that survived the above = suspicious
  t = t.replace(/\b[A-Za-z0-9_-]{24,}\b/g, REDACT);

  // Restore protected parts
  t = t.replace(/\u0000P(\d+)\u0000/g, (_, i) => protectedParts[Number(i)] || "");
  return t;
}

// ---------------------------------------------------------------------------
// API handlers — RESEARCH THREADS ONLY
// ---------------------------------------------------------------------------
async function handleSessions(url, env) {
  const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit") || "50", 10), 1), 100);
  const offset = Math.max(parseInt(url.searchParams.get("offset") || "0", 10), 0);
  const q = (url.searchParams.get("q") || "").trim().slice(0, 100);

  let sql = "SELECT thread_id, title, category, agent_id, model_id, messages, created_at, updated_at FROM chat_sessions WHERE category = 'research'";
  const params = [];
  if (q) {
    sql += " AND (title LIKE ? OR messages LIKE ?)";
    params.push("%" + q + "%", "%" + q + "%");
  }
  sql += " ORDER BY COALESCE(updated_at, created_at) DESC LIMIT ? OFFSET ?";
  params.push(limit, offset);

  const res = await env.QNFO_AUDIT.prepare(sql).bind(...params).all();
  const items = [];
  for (const t of res.results || []) {
    let messages = [];
    try { messages = JSON.parse(t.messages || "[]"); } catch (e) { messages = []; }
    if (!Array.isArray(messages)) messages = [];
    if (messages.length === 0) continue; // skip empty closeout stubs
    items.push({
      id: t.thread_id,
      kind: "thread",
      title: redact((t.title || (messages.find((m) => m && m.role === "user") || {}).content || "(untitled)").slice(0, 300)),
      created_at: normTs(t.updated_at || t.created_at),
      message_count: messages.length,
      model: t.model_id || null,
      tags: ["conversation"]
    });
  }

  return json({
    count: items.length,
    limit,
    offset,
    sessions: items.map((s) => ({ id: s.id, kind: s.kind, title: s.title, created_at: s.created_at, message_count: s.message_count, model: s.model, tags: s.tags }))
  });
}

async function handleSession(path, env) {
  const id = decodeURIComponent(path.split("/").slice(3).join("/"));
  if (!id) return json({ error: "Missing id" }, 400);
  const row = await env.QNFO_AUDIT.prepare(
    "SELECT thread_id, title, category, agent_id, model_id, messages, created_at, updated_at FROM chat_sessions WHERE thread_id = ? AND category = 'research'"
  ).bind(id).first();
  if (!row) return json({ error: "Session not found or not public" }, 404);
  let messages = [];
  try { messages = JSON.parse(row.messages || "[]"); } catch (e) { messages = []; }
  if (!Array.isArray(messages)) messages = [];
  const clean = messages.map((m) => ({
    role: m && m.role || "unknown",
    content: redact(String(m && m.content || "").slice(0, 20000)),
    timestamp: m && m.timestamp ? new Date(m.timestamp).toISOString() : null
  }));
  return json({
    id: row.thread_id,
    kind: "thread",
    title: redact((row.title || "").slice(0, 500)),
    category: row.category,
    model: row.model_id || null,
    created_at: normTs(row.created_at),
    updated_at: normTs(row.updated_at),
    message_count: clean.length,
    messages: clean
  });
}

async function handleFeed(url, env) {
  // Real-time feed: research threads newer than `after` (epoch ms). Polled by the UI.
  const afterParam = url.searchParams.get("after");
  const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit") || "30", 10), 1), 100);
  let afterMs = 0;
  if (afterParam) {
    const n = Number(afterParam);
    afterMs = Number.isFinite(n) && n > 1000000000000 ? n : Date.parse(afterParam) || 0;
  }
  const now = Date.now();
  const res = await env.QNFO_AUDIT.prepare(
    "SELECT thread_id, title, messages, created_at, updated_at FROM chat_sessions WHERE category = 'research'"
  ).all();
  const items = [];
  for (const t of res.results || []) {
    const ts = normTs(t.updated_at || t.created_at);
    const ms = Date.parse(ts);
    if (ms > afterMs) {
      let messages = [];
      try { messages = JSON.parse(t.messages || "[]"); } catch (e) { messages = []; }
      if (!Array.isArray(messages) || messages.length === 0) continue; // skip empty closeout stubs
      const userMsg = messages.find((m) => m && m.role === "user");
      items.push({
        id: t.thread_id,
        kind: "thread",
        title: redact((t.title || (userMsg && userMsg.content) || t.thread_id).slice(0, 300)),
        created_at: ts,
        message_count: messages.length
      });
    }
  }
  items.sort((a, b) => (b.created_at || "").localeCompare(a.created_at || "")).slice(0, limit);
  return json({ after: now, count: items.length, sessions: items });
}

function normTs(v) {
  if (!v) return null;
  if (typeof v === "number") return new Date(v).toISOString();
  let s = String(v).replace(" ", "T");
  if (!/Z$|[+-]\d\d:\d\d$/.test(s)) s += "Z";
  const d = new Date(s);
  return Number.isNaN(d.getTime()) ? String(v) : d.toISOString();
}

// ---------------------------------------------------------------------------
// ASK + PARTICIPATION — public, read-only for threads; questions answered from
// the corpus via qnfo-qwav /ai/ask; related research threads surfaced.
// ---------------------------------------------------------------------------
async function handleAsk(url, request, env) {
  let body;
  try { body = await request.json(); } catch (e) { body = {}; }
  const query = String(body.query || "").trim().slice(0, 500);
  if (!query) return json({ error: "Missing query" }, 400);
  try {
    const [qwavResp, threadRes] = await Promise.all([
      fetch("https://qnfo-qwav.q08.workers.dev/ai/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json", "User-Agent": "qnfo-idea-factory/1.2" },
        body: JSON.stringify({ query })
      }).then((r) => r.json()).catch(() => ({ error: "ask backend unreachable" })),
      relatedThreads(query, env)
    ]);
    const threads = [];
    for (const t of threadRes || []) {
      threads.push({
        id: t.id,
        title: t.title,
        created_at: t.created_at,
        message_count: t.message_count
      });
    }
    return json({
      query,
      answer: qwavResp.answer || null,
      sources: (qwavResp.sources || []).slice(0, 6).map((s) => ({ file: redact(s.file || ""), slug: s.slug, score: s.score })),
      model: qwavResp.model || null,
      backend_error: qwavResp.error || null,
      threads
    });
  } catch (e) {
    return json({ error: "Ask failed: " + e.message }, 502);
  }
}

// Find research threads related to a query: tokenize into meaningful terms and
// match ANY term against title or message content (phrase-LIKE misses multi-word
// queries). Sorted by newest; deduped by id.
async function relatedThreads(query, env, limit = 6) {
  const terms = String(query || "")
    .toLowerCase()
    .replace(/[^a-z0-9+\- ]+/g, " ")
    .split(/\s+/)
    .filter((t) => t.length >= 3)
    .slice(0, 8);
  if (!terms.length) return [];
  const res = await env.QNFO_AUDIT.prepare(
    "SELECT thread_id, title, messages, created_at, updated_at FROM chat_sessions WHERE category = 'research'"
  ).all();
  const scored = [];
  for (const t of res.results || []) {
    let messages = [];
    try { messages = JSON.parse(t.messages || "[]"); } catch (e) { messages = []; }
    if (!Array.isArray(messages) || messages.length === 0) continue;
    const hay = ((t.title || "") + " " + messages.map((m) => m && m.content || "").join(" ")).toLowerCase();
    let score = 0;
    for (const term of terms) {
      if (hay.includes(term)) score++;
    }
    if (terms.length <= 3 ? score >= 1 : score >= 2) {
      scored.push({
        id: t.thread_id,
        title: redact((t.title || (messages.find((m) => m && m.role === "user") || {}).content || t.thread_id).slice(0, 300)),
        created_at: normTs(t.updated_at || t.created_at),
        message_count: messages.length,
        score
      });
    }
  }
  scored.sort((a, b) => (b.score - a.score) || ((b.created_at || "").localeCompare(a.created_at || "")));
  return scored.slice(0, limit);
}

async function handleProposalPost(request, env) {
  let body;
  try { body = await request.json(); } catch (e) { body = {}; }
  // Honeypot: bots fill the website field; humans leave it empty
  if (String(body.website || "").trim()) return json({ ok: true, status: "submitted" }, 200);
  const idea = String(body.idea || "").trim().slice(0, 2000);
  if (idea.length < 20) return json({ error: "Please share a bit more (at least 20 characters)." }, 400);
  const name = String(body.name || "").trim().slice(0, 100);
  const contact = String(body.contact || "").trim().slice(0, 200);
  const cf = request.headers.get("CF-Connecting-IP") || "";
  const ipHash = await sha256(cf).catch(() => "");
  // Rate limit: max 3 proposals per IP per hour
  const hourAgo = new Date(Date.now() - 3600 * 1000).toISOString();
  const recent = await env.QNFO_AUDIT.prepare(
    "SELECT COUNT(*) AS n FROM idea_proposals WHERE ip_hash = ? AND created_at > ?"
  ).bind(ipHash, hourAgo).first();
  if ((recent?.n || 0) >= 3) return json({ error: "Please wait a bit before submitting again." }, 429);
  const res = await env.QNFO_AUDIT.prepare(
    "INSERT INTO idea_proposals (name, idea, contact, status, ip_hash, created_at) VALUES (?, ?, ?, 'new', ?, ?)"
  ).bind(name, idea, contact, ipHash, new Date().toISOString()).run();
  return json({ ok: true, status: "submitted", id: res.meta.last_row_id });
}

async function handleProposalList(request, env) {
  // Private review endpoint: requires X-Sync-Token (not exposed in the UI).
  const auth = request.headers.get("X-Sync-Token");
  if (!auth || auth !== (env.SYNC_TOKEN || "")) return json({ error: "Unauthorized" }, 401);
  const res = await env.QNFO_AUDIT.prepare(
    "SELECT id, name, idea, contact, status, created_at FROM idea_proposals ORDER BY created_at DESC LIMIT 100"
  ).all();
  return json({ count: res.results.length, proposals: res.results });
}

async function sha256(s) {
  const data = new TextEncoder().encode(String(s));
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

// ---------------------------------------------------------------------------
// UI
// ---------------------------------------------------------------------------
const UI_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QNFO Idea Factory</title>
<meta name="description" content="A public read-only window into the QNFO research conversations — ideas as they develop, live.">
<meta property="og:title" content="QNFO Idea Factory">
<meta property="og:description" content="Public read-only window into QNFO research conversations — ideas as they develop.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://ideas.qnfo.org">
<link rel="canonical" href="https://ideas.qnfo.org">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%231a56db'/><text x='16' y='23' text-anchor='middle' font-size='16' fill='white' font-family='system-ui'>Q</text></svg>">
<style>
:root{--blue:#1a56db;--blue-dark:#1040a8;--blue-light:#dbeafe;--blue-subtle:#eff6ff;--text:#1a1a2e;--muted:#6b7280;--bg:#ffffff;--surface:#f9fafb;--border:#e5e7eb;--radius:8px;--radius-lg:12px;--user-bubble:#1a56db;--asst-bubble:#f3f4f6}
*{box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,-apple-system,Roboto,sans-serif;margin:0;color:var(--text);background:var(--bg);line-height:1.6}
.top-nav{display:flex;align-items:center;gap:1rem;padding:.7rem 1.25rem;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:50;flex-wrap:wrap}
.top-nav .brand{font-weight:800;font-size:1.05rem;color:var(--text);text-decoration:none;display:flex;align-items:center;gap:.45rem}
.top-nav a.nav-link{color:var(--muted);text-decoration:none;font-weight:500;font-size:.85rem;padding:.35rem .7rem;border-radius:6px;transition:all .15s}
.top-nav a.nav-link:hover{color:var(--blue);background:var(--blue-subtle)}
.top-nav .live{display:inline-flex;align-items:center;gap:.4rem;margin-left:auto;font-size:.75rem;font-weight:600;color:#16a34a;background:#f0fdf4;border:1px solid #bbf7d0;padding:.25rem .6rem;border-radius:999px}
.top-nav .live .dot{width:8px;height:8px;border-radius:50%;background:#22c55e;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
.layout{display:grid;grid-template-columns:340px 1fr;min-height:calc(100vh - 56px)}
.sidebar{border-right:1px solid var(--border);background:var(--surface);overflow-y:auto;padding:1rem}
.sidebar h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 .6rem}
.search{width:100%;padding:.55rem .75rem;border:2px solid var(--border);border-radius:var(--radius);font-size:.85rem;margin-bottom:.8rem;outline:none}
.search:focus{border-color:var(--blue)}
.filter-row{display:flex;gap:.35rem;margin-bottom:.9rem;flex-wrap:wrap}
.filter-btn{padding:.3rem .7rem;border:1.5px solid var(--border);border-radius:999px;background:var(--bg);color:var(--text);cursor:pointer;font-size:.78rem;font-weight:500;transition:all .15s}
.filter-btn.active{background:var(--blue);color:#fff;border-color:var(--blue)}
.session-item{padding:.65rem .75rem;border-radius:var(--radius);cursor:pointer;margin-bottom:.35rem;border:1px solid transparent;transition:all .12s}
.session-item:hover{background:#fff;border-color:var(--border)}
.session-item.active{background:var(--blue-subtle);border-color:var(--blue-light)}
.session-item .t{font-size:.85rem;font-weight:600;color:var(--text);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.35}
.session-item .m{font-size:.72rem;color:var(--muted);margin-top:.25rem;display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}
.badge{display:inline-block;background:var(--blue-subtle);color:var(--blue);padding:.08rem .45rem;border-radius:999px;font-size:.68rem;font-weight:600}
.main{display:flex;flex-direction:column;height:calc(100vh - 56px);position:relative}
.hero{padding:1.6rem 2rem 1rem;border-bottom:1px solid var(--border);background:linear-gradient(135deg,#eff6ff 0%,#f0f9ff 50%,#faf5ff 100%)}
.hero h1{margin:0;font-size:1.45rem;font-weight:800;background:linear-gradient(135deg,#1a56db,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero p{margin:.4rem 0 0;color:var(--muted);font-size:.85rem;max-width:640px}
.conv{flex:1;overflow-y:auto;padding:1.5rem 2rem}
.msg{display:flex;margin-bottom:1.1rem;max-width:820px}
.msg.user{flex-direction:row-reverse;margin-left:auto}
.msg .avatar{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0;margin:0 .6rem}
.msg.user .avatar{background:var(--blue);color:#fff}
.msg.assistant .avatar{background:#e5e7eb;color:#374151}
.msg .body{max-width:82%;padding:.75rem 1rem;border-radius:14px;font-size:.9rem;white-space:pre-wrap;word-break:break-word}
.msg.user .body{background:var(--user-bubble);color:#fff;border-top-right-radius:4px}
.msg.assistant .body{background:var(--asst-bubble);border-top-left-radius:4px}
.msg .meta{font-size:.68rem;color:var(--muted);margin-top:.3rem;display:block}
.msg.user .meta{text-align:right;color:rgba(255,255,255,.75)}
.msg pre{background:#1f2937;color:#e5e7eb;padding:.6rem .8rem;border-radius:8px;overflow-x:auto;font-size:.78rem;white-space:pre-wrap}
.msg code{font-family:Consolas,monospace;font-size:.85em}
.empty{color:var(--muted);text-align:center;padding:3rem 1rem}
.empty .big{font-size:2.4rem;margin-bottom:.6rem}
.load-more{display:block;margin:1rem auto;padding:.5rem 1.2rem;border:1.5px solid var(--border);border-radius:999px;background:#fff;color:var(--blue);cursor:pointer;font-size:.8rem;font-weight:600}
.load-more:hover{border-color:var(--blue)}
.footer-note{position:sticky;bottom:0;background:rgba(255,255,255,.9);border-top:1px solid var(--border);padding:.6rem 1.5rem;font-size:.72rem;color:var(--muted);text-align:center}
a{color:var(--blue)}
/* Ask + participation */
.ask-box{margin:1rem 0 0;padding:1rem 1.1rem;background:rgba(255,255,255,.85);border:1px solid var(--blue-light);border-radius:var(--radius-lg)}
.ask-box .row{display:flex;gap:.5rem}
.ask-box input{flex:1;padding:.65rem .8rem;border:2px solid var(--border);border-radius:var(--radius);font-size:.9rem;outline:none}
.ask-box input:focus{border-color:var(--blue)}
.ask-box button{padding:.65rem 1.1rem;border-radius:var(--radius);border:none;cursor:pointer;background:var(--blue);color:#fff;font-weight:600;font-size:.88rem}
.ask-box button:disabled{opacity:.5;cursor:wait}
.chips{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.6rem}
.chips button{background:var(--surface);border:1px solid var(--border);color:var(--muted);border-radius:999px;padding:.3rem .7rem;font-size:.74rem;cursor:pointer;transition:all .15s;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chips button:hover{color:var(--blue);border-color:var(--blue);background:var(--blue-subtle)}
#ask-result{margin-top:.8rem;display:none}
#ask-result .ans{background:var(--asst-bubble);border-radius:12px;padding:.85rem 1rem;font-size:.88rem;white-space:pre-wrap;line-height:1.6}
#ask-result .srcs{margin-top:.5rem}
#ask-result .srcs .src{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:.4rem .7rem;margin-bottom:.3rem;font-size:.78rem;display:flex;justify-content:space-between;gap:.5rem}
#ask-result .srcs .src a{color:var(--blue);font-weight:500}
#ask-result .threads{margin-top:.6rem}
#ask-result .threads .th{background:var(--blue-subtle);border:1px solid var(--blue-light);border-radius:8px;padding:.45rem .7rem;margin-bottom:.3rem;font-size:.8rem;cursor:pointer}
#ask-result .threads .th:hover{border-color:var(--blue)}
.propose{margin:1rem 0 0;padding:1rem 1.1rem;background:rgba(255,255,255,.85);border:1px solid var(--border);border-radius:var(--radius-lg)}
.propose h3{margin:0 0 .4rem;font-size:.9rem;color:var(--text)}
.propose p{margin:0 0 .6rem;font-size:.78rem;color:var(--muted)}
.propose textarea{width:100%;padding:.6rem .8rem;border:2px solid var(--border);border-radius:var(--radius);font-size:.88rem;font-family:inherit;outline:none;resize:vertical;min-height:70px}
.propose textarea:focus{border-color:var(--blue)}
.propose .mini{display:flex;gap:.5rem;margin-top:.5rem}
.propose .mini input{flex:1;padding:.5rem .7rem;border:2px solid var(--border);border-radius:var(--radius);font-size:.82rem;outline:none}
.propose .mini input:focus{border-color:var(--blue)}
.propose .mini button{padding:.55rem 1rem;border-radius:var(--radius);border:none;cursor:pointer;background:var(--blue);color:#fff;font-weight:600;font-size:.84rem;white-space:nowrap}
.propose .mini button:disabled{opacity:.5;cursor:wait}
.propose .hp{position:absolute;left:-9999px;opacity:0}
#propose-status{font-size:.78rem;margin-top:.5rem;color:var(--muted)}
@media(max-width:820px){.layout{grid-template-columns:1fr}.sidebar{max-height:34vh;border-right:none;border-bottom:1px solid var(--border)}.main{height:auto;min-height:60vh}.conv{padding:1rem}.msg .body{max-width:88%}}
</style>
</head>
<body>
<nav class="top-nav">
  <a class="brand" href="/">💡 QNFO Idea Factory</a>
  <a class="nav-link" href="https://qnfo.org">QNFO</a>
  <a class="nav-link" href="https://papers.qnfo.org">Papers</a>
  <a class="nav-link" href="https://graph-api.qnfo.org/stats">Graph</a>
  <a class="nav-link" href="https://qwav.org">QWAV</a>
  <a class="nav-link" href="https://ask.qwav.tech">Ask</a>
  <span class="live"><span class="dot"></span>LIVE</span>
</nav>
<div class="layout">
  <aside class="sidebar">
    <input class="search" id="search" type="search" placeholder="Search research sessions...">
    <h2 id="count-label">Research conversations</h2>
    <div id="session-list"><div class="empty"><div class="big">⏳</div>Loading...</div></div>
  </aside>
  <main class="main">
    <div class="hero">
      <h1>Where the ideas form</h1>
      <p>A public, read-only window into the QNFO research conversations — the full thread of prompts, explorations, and open questions as they develop, in real time. Infrastructure and internal operations are never shown here. Sensitive details (tokens, emails, paths) are redacted automatically.</p>
      <div class="ask-box">
        <div class="row">
          <input id="ask-input" type="text" maxlength="500" placeholder="Ask the research corpus anything…" autocomplete="off">
          <button id="ask-go" onclick="doAsk()">Ask</button>
        </div>
        <div class="chips" id="ask-chips"></div>
        <div id="ask-result"></div>
      </div>
      <div class="propose">
        <h3>💡 Propose an idea</h3>
        <p>Have a question, experiment, or direction the QNFO research should explore? Share it — the proposals are reviewed by the research lead and the best ones enter the queue.</p>
        <textarea id="prop-idea" maxlength="2000" placeholder="Describe the idea, question, or experiment…"></textarea>
        <div class="mini">
          <input id="prop-name" maxlength="100" placeholder="Your name (optional)">
          <input id="prop-contact" maxlength="200" placeholder="Email / handle (optional)">
          <button id="prop-go" onclick="doPropose()">Submit</button>
        </div>
        <input class="hp" id="prop-website" tabindex="-1" autocomplete="off">
        <div id="propose-status"></div>
      </div>
    </div>
    <div class="conv" id="conv"><div class="empty"><div class="big">💬</div>Select a research session to read the full conversation.</div></div>
    <div class="footer-note">QNFO Idea Factory · read-only public archive · research threads only · ideas.qnfo.org · <a href="https://qnfo.org" target="_blank" rel="noopener">QNFO Research</a></div>
  </main>
</div>
<script>
var state={q:'',offset:0,limit:50,hasMore:false,lastAfter:Date.now(),sessions:[],selected:null,polling:true};
var $=function(s){return document.querySelector(s);};
function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function fmtTs(ts){if(!ts)return '';var d=new Date(ts);if(isNaN(d))return '';var now=new Date();var sameDay=d.toDateString()===now.toDateString();return sameDay?d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}):d.toLocaleDateString([],{month:'short',day:'numeric',year:d.getFullYear()===now.getFullYear()?undefined:'numeric'});}
function renderList(){
  var el=$('#session-list');var items=state.sessions;
  if(!items.length){el.innerHTML='<div class="empty"><div class="big">🔭</div>No research sessions found.</div>';return;}
  el.innerHTML=items.map(function(s){
    return '<div class="session-item'+(state.selected===s.id?' active':'')+'" data-id="'+esc(s.id)+'"><div class="t">'+esc(s.title||'(untitled)')+'</div><div class="m"><span>'+fmtTs(s.created_at)+'</span><span>'+s.message_count+' messages</span></div></div>';
  }).join('');
  if(state.hasMore)el.insertAdjacentHTML('beforeend','<button class="load-more" id="load-more">Load more</button>');
  $('#count-label').textContent=items.length+' research conversations'+(state.q?' matching "'+state.q+'"':'');
  Array.prototype.forEach.call(document.querySelectorAll('.session-item'),function(n){n.onclick=function(){openSession(n.getAttribute('data-id'));};});
  var lm=$('#load-more');if(lm)lm.onclick=loadMore;
}
function renderMsg(m){
  var html='<div class="msg '+esc(m.role)+'"><div class="avatar">'+(m.role==='user'?'R':'Q')+'</div><div class="body">'+esc(m.content)+'<span class="meta">'+fmtTs(m.timestamp)+(m.role==='user'?' · Rowan':' · QNFO agent')+'</span></div></div>';
  return html;
}
function openSession(id){
  state.selected=id;
  var conv=$('#conv');conv.innerHTML='<div class="empty"><div class="big">⏳</div>Loading conversation...</div>';
  Array.prototype.forEach.call(document.querySelectorAll('.session-item'),function(n){n.classList.toggle('active',n.getAttribute('data-id')===id);});
  fetch('/api/session/'+encodeURIComponent(id)).then(function(r){return r.json();}).then(function(d){
    if(d.error){conv.innerHTML='<div class="empty"><div class="big">⚠️</div>'+esc(d.error)+'</div>';return;}
    var head='<div class="hero" style="padding:.9rem 2rem"><h1 style="font-size:1.1rem">'+(d.title||'Research conversation')+'</h1><p style="font-size:.75rem">'+d.message_count+' messages · '+fmtTs(d.created_at)+(d.model?' · '+esc(d.model):'')+'</p></div>';
    var body='<div class="conv" id="conv-inner" style="padding:1.5rem 2rem">';
    if(d.messages&&d.messages.length){
      body+=d.messages.map(renderMsg).join('');
    }else{
      body+='<div class="empty"><div class="big">🤫</div>No messages in this record.</div>';
    }
    body+='</div>';
    conv.innerHTML=head+body;
    var ci=$('#conv-inner');if(ci)ci.scrollTop=0;
  }).catch(function(e){conv.innerHTML='<div class="empty">Failed to load: '+esc(String(e))+'</div>';});
}
function loadSessions(reset){
  if(reset){state.offset=0;state.sessions=[];}
  var params=new URLSearchParams({limit:String(state.limit),offset:String(state.offset)});
  if(state.q)params.set('q',state.q);
  fetch('/api/sessions?'+params.toString()).then(function(r){return r.json();}).then(function(d){
    if(d.error)return;
    state.sessions=d.sessions||[];
    state.hasMore=state.sessions.length>=state.limit;
    renderList();
    if(!state.selected&&state.sessions.length){openSession(state.sessions[0].id);}
  });
}
function loadMore(){
  state.offset+=state.limit;
  fetch('/api/sessions?limit='+state.limit+'&offset='+state.offset+(state.q?'&q='+encodeURIComponent(state.q):'')).then(function(r){return r.json();}).then(function(d){
    if(d.error)return;
    state.sessions=state.sessions.concat(d.sessions||[]);
    state.hasMore=(d.sessions||[]).length>=state.limit;
    renderList();
  });
}
function pollFeed(){
  if(!state.polling)return;
  fetch('/api/feed?after='+state.lastAfter).then(function(r){return r.json();}).then(function(d){
    if(d.error)return;
    state.lastAfter=d.after||Date.now();
    if(d.sessions&&d.sessions.length&&!state.q){
      var known={};state.sessions.forEach(function(s){known[s.id]=1;});
      var fresh=d.sessions.filter(function(s){return !known[s.id];});
      if(fresh.length){state.sessions=fresh.concat(state.sessions);state.hasMore=state.sessions.length>=state.limit;renderList();}
    }
  }).catch(function(){});
}
$('#search').addEventListener('input',function(){state.q=this.value.trim();loadSessions(true);});
$('#ask-input').addEventListener('keydown',function(e){if(e.key==='Enter')doAsk();});
function doAsk(){
  var q=$('#ask-input').value.trim();if(!q)return;
  var box=$('#ask-result');box.style.display='block';box.innerHTML='<div class="ans">⏳ Searching the research corpus…</div>';
  var btn=$('#ask-go');btn.disabled=true;
  fetch('/api/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query:q})}).then(function(r){return r.json();}).then(function(d){
    if(d.error){box.innerHTML='<div class="ans">⚠️ '+esc(d.error)+'</div>';return;}
    var html='';
    if(d.answer){html+='<div class="ans">'+esc(d.answer)+'</div>';}
    else if(d.backend_error){html+='<div class="ans">⚠️ '+esc(d.backend_error)+'</div>';}
    if(d.sources&&d.sources.length){
      html+='<div class="srcs"><h3 style="font-size:.8rem;color:var(--muted);text-transform:uppercase;margin:.6rem 0 .3rem">Sources ('+d.sources.length+')</h3>';
      d.sources.forEach(function(s){
        var label=esc(s.file||s.slug||'source');
        html+='<div class="src">'+(s.slug?'<a href="https://papers.qnfo.org/papers/'+encodeURIComponent(s.slug)+'" target="_blank" rel="noopener">'+label+'</a>':'<span>'+label+'</span>')+(s.score!=null?'<span style="color:var(--muted)">'+Number(s.score).toFixed(3)+'</span>':'')+'</div>';
      });
      html+='</div>';
    }
    if(d.threads&&d.threads.length){
      html+='<div class="threads"><h3 style="font-size:.8rem;color:var(--muted);text-transform:uppercase;margin:.6rem 0 .3rem">Related idea threads ('+d.threads.length+')</h3>';
      d.threads.forEach(function(t){
        html+='<div class="th" data-id="'+esc(t.id)+'" onclick="openSession(this.dataset.id)">'+esc(t.title||'(untitled)')+'<span style="color:var(--muted);font-size:.72rem"> · '+t.message_count+' messages</span></div>';
      });
      html+='</div>';
    }
    if(!d.answer&&!d.backend_error&&(!d.threads||!d.threads.length)){html='<div class="ans">No research found for that yet — try a different phrasing.</div>';}
    box.innerHTML=html;
  }).catch(function(e){box.innerHTML='<div class="ans">Failed: '+esc(String(e))+'</div>';}).finally(function(){btn.disabled=false;});
}
function loadAskChips(){
  fetch('/api/sessions?limit=8').then(function(r){return r.json();}).then(function(d){
    if(!d.sessions||!d.sessions.length)return;
    var el=$('#ask-chips');el.innerHTML='';
    d.sessions.slice(0,6).forEach(function(s){
      var b=document.createElement('button');b.textContent=s.title&&s.title.length>60?s.title.slice(0,60)+'…':(s.title||'ask');
      b.title=s.title||'';b.onclick=function(){$('#ask-input').value=s.title||'';doAsk();};el.appendChild(b);
    });
  }).catch(function(){});
}
function doPropose(){
  var idea=$('#prop-idea').value.trim();
  var st=$('#propose-status');
  if(idea.length<20){st.textContent='Please share a bit more (at least 20 characters).';return;}
  var btn=$('#prop-go');btn.disabled=true;st.textContent='Submitting…';
  fetch('/api/proposals',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({idea:idea,name:$('#prop-name').value.trim(),contact:$('#prop-contact').value.trim(),website:$('#prop-website').value})}).then(function(r){return r.json();}).then(function(d){
    if(d.error){st.textContent=esc(d.error);}
    else{st.innerHTML='✅ Submitted. Thank you — it will be reviewed for the research queue.';$('#prop-idea').value='';$('#prop-name').value='';$('#prop-contact').value='';}
  }).catch(function(e){st.textContent='Failed: '+esc(String(e));}).finally(function(){btn.disabled=false;});
}
loadSessions(true);
loadAskChips();
setInterval(pollFeed,30000);
</script>
</body>
</html>`;

function serveUI() {
  return new Response(UI_HTML, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "public, max-age=60"
    }
  });
}
