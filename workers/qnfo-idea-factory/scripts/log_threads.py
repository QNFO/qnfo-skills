#!/usr/bin/env python3
"""
log_threads.py - Push FULL DeepChat conversation threads to Cloudflare chat_sessions.

The metadata-only log_chat.py pipeline ships title/summary (first user message) to
chat_logs; this script reconstructs the COMPLETE user/assistant conversation from the
local agent.db (deepchat_messages + deepchat_user_messages + deepchat_assistant_blocks)
and pushes it to qnfo-thread-ingest /threads for the public Idea Factory.

Classification (research vs infra) - the public feed serves ONLY research:
  research = agent_id 'deepchat' AND session_kind 'regular'   (the user's research agent)
  infra    = everything else (automation, personal, subagent audits)

Usage:
  python C:/Users/LENOVO/.deepchat/scripts/log_threads.py [--all] [--dry-run] [--limit N]
    --all      backfill ALL sessions (ignore incremental state)
    --dry-run  print what would be pushed without sending
    --limit N  max sessions to process (default 200)
"""

import sqlite3, json, os, sys, time, argparse, urllib.request

AGENT_DB = os.path.expandvars(r"%APPDATA%\DeepChat\app_db\agent.db")
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".log_threads_state.json")
API = "https://qnfo-thread-ingest.q08.workers.dev/threads"
MAX_CONTENT = 20000
MAX_MESSAGES = 500


def _token():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".sync_token")
    try:
        with open(p) as f:
            return f.read().strip()
    except Exception:
        return ""


UA = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json", "X-Sync-Token": _token()}


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"last_updated": 0, "last_run": None}


def save_state(state):
    state["last_run"] = time.time()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def unwrap_user_text(raw):
    """User message content is a JSON wrapper {'text': '...', 'files': [], ...} or plain string."""
    raw = str(raw or "")
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict) and "text" in parsed:
            return str(parsed["text"])
        return raw
    except Exception:
        return raw


def classify(agent_id, session_kind):
    if agent_id == "deepchat" and session_kind == "regular":
        return "research"
    return "infra"


def fetch_threads(last_updated, all_sessions, limit):
    conn = sqlite3.connect(f"file:{AGENT_DB}?mode=ro", uri=True, timeout=10)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. Session metadata: new_sessions (title/agent/kind) + deepchat_sessions (model)
    sql = """SELECT ns.id AS session_id, ns.agent_id, ns.session_kind, ns.title,
                    ns.created_at AS ns_created, ns.updated_at AS ns_updated,
                    ds.model_id, ds.provider_id, ds.summary_text
             FROM new_sessions ns
             LEFT JOIN deepchat_sessions ds ON ds.id = ns.id"""
    if not all_sessions:
        sql += " WHERE ns.updated_at > ?"
    sql += " ORDER BY ns.updated_at DESC LIMIT ?"
    params = [last_updated] if not all_sessions else []
    params.append(int(limit))

    cur.execute(sql, params)
    sessions = [dict(r) for r in cur.fetchall()]

    out = []
    for s in sessions:
        sid = s["session_id"]
        category = classify(s.get("agent_id"), s.get("session_kind"))
        title = (s.get("title") or "").strip()[:300]
        model = (s.get("model_id") or "").strip()[:100]

        # 2. Messages in order
        cur.execute(
            "SELECT id, order_seq, role, content, created_at FROM deepchat_messages "
            "WHERE session_id = ? ORDER BY order_seq LIMIT ?",
            (sid, MAX_MESSAGES),
        )
        msgs = [dict(r) for r in cur.fetchall()]

        clean = []
        prev_sig = None
        for m in msgs:
            role = m["role"]
            content = ""
            if role == "user":
                # Prefer the plain-text table; fall back to unwrapping the JSON wrapper
                cur.execute("SELECT text FROM deepchat_user_messages WHERE message_id = ?", (m["id"],))
                ur = cur.fetchone()
                content = ur["text"] if ur and ur["text"] else unwrap_user_text(m["content"])
            elif role == "assistant":
                # Assistant text = concatenated 'content' blocks (NOT reasoning/tool_call/action)
                cur.execute(
                    "SELECT text_content FROM deepchat_assistant_blocks "
                    "WHERE message_id = ? AND block_type = 'content' ORDER BY block_index",
                    (m["id"],),
                )
                blocks = [r["text_content"] for r in cur.fetchall() if r["text_content"]]
                if not blocks:
                    continue  # tool-call-only or reasoning-only turn: not part of the visible thread
                content = "\n\n".join(blocks)
            else:
                continue

            content = content.strip()
            if not content:
                continue
            if len(content) > MAX_CONTENT:
                content = content[:MAX_CONTENT] + "\n…[truncated]"

            ts = m.get("created_at")
            ts_iso = None
            if ts:
                try:
                    ts_iso = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(int(ts) / 1000))
                except Exception:
                    ts_iso = None

            # Dedupe consecutive identical messages (CMD prompts repeat)
            sig = role + "|" + content[:80]
            if sig == prev_sig:
                continue
            prev_sig = sig

            clean.append({"role": role, "content": content, "timestamp": ts_iso})

        if len(clean) < 1:
            continue

        out.append({
            "session_id": str(sid)[:200],
            "title": title,
            "category": category,
            "agent_id": s.get("agent_id") or "",
            "model_id": model,
            "provider_id": s.get("provider_id") or "",
            "messages": clean,
            "created_at": s.get("ns_created"),
            "updated_at": s.get("ns_updated"),
            "summary": (s.get("summary_text") or "")[:2000],
        })
    conn.close()
    return out


def _post(url, body, timeout=40):
    req = urllib.request.Request(url, data=body, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout)


def push(threads, dry_run=False):
    pushed = 0
    failed = 0
    max_updated = 0
    for t in threads:
        body = json.dumps(t).encode()
        if dry_run:
            print(f"[DRY] {t['session_id']} [{t['category']}] {t['title'][:60]!r} "
                  f"msgs={len(t['messages'])}")
            pushed += 1
            continue
        ok = False
        last_err = "unknown"
        for attempt in (1, 2):
            try:
                resp = _post(API, body)
                result = json.loads(resp.read())
                if result.get("success"):
                    ok = True
                    break
                last_err = f"api: {result}"
            except Exception as e:
                last_err = f"net: {e}"
            if attempt == 1:
                time.sleep(2)
        if ok:
            print(f"  pushed {t['session_id']} [{t['category']}] "
                  f"{t['title'][:50]!r} msgs={len(t['messages'])}")
            pushed += 1
        else:
            failed += 1
            print(f"  FAILED {t['session_id']}: {last_err}", file=sys.stderr)
        if t.get("updated_at"):
            try:
                max_updated = max(max_updated, int(t["updated_at"]))
            except Exception:
                pass
    return pushed, failed, max_updated


def main():
    ap = argparse.ArgumentParser(description="Push full DeepChat threads to Cloudflare")
    ap.add_argument("--all", action="store_true", help="Backfill ALL sessions (ignore state)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=200)
    args = ap.parse_args()

    state = load_state()
    last_updated = 0 if args.all else state.get("last_updated", 0)
    threads = fetch_threads(last_updated, args.all, args.limit)

    research = [t for t in threads if t["category"] == "research"]
    infra = [t for t in threads if t["category"] == "infra"]
    print(f"found {len(threads)} sessions ({len(research)} research, {len(infra)} infra)")

    pushed, failed, max_updated = push(threads, args.dry_run)
    if max_updated:
        state["last_updated"] = max_updated
        save_state(state)
    print(f"pushed={pushed} failed={failed}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
