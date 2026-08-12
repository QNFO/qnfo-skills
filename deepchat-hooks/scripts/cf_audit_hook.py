# -*- coding: utf-8 -*-
"""
DeepChat Hook: Cloudflare Infrastructure Audit (qnfo-audit integration)

Fires on DeepChat lifecycle events. Reads the full hook payload from stdin
(JSON; note: in production the app passes NO stdin — rely on argv placeholders
and DEEPCHAT_* env vars, which this script also reads), runs a lightweight
Cloudflare infrastructure audit against the qnfo-lifecycle worker (which
persists every audit run to D1 `audit_sessions`), and appends a local JSONL
audit trail under the skill's logs/ directory (skill git-tracked in the
qnfo-skills repo and synced to R2 via skill-sync).

Usage (registered in DeepChat Hooks settings):
  "<abs-python.exe>" "<abs-script>" --event {{event}} --conversationId {{conversationId}}

Event behavior:
  - SessionStart : health ping (lifecycle + gateway + archive, parallel) + status counts
  - SessionEnd   : health ping + status + full drift audit (/run/drift)
  - All events   : local JSONL record written; stdout summary printed

Timeout discipline (HARD): the app SIGKILLs hook commands after 30s
(COMMAND_TIMEOUT_MS = 30000). Worst-case budget here is ~13s: 0.8s stdin probe
+ 4s parallel health (max of 3) + 4s status + 4s drift. Never exceed 25s.

Stdlib only. Never raises. Always exits 0 so the hook never disrupts the app.
"""
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import urllib.request
import urllib.error

HOOK_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(HOOK_SKILL_DIR, "logs")

LIFECYCLE_BASE = "https://qnfo-lifecycle.q08.workers.dev"
GATEWAY_HEALTH = "https://qnfo-gateway.q08.workers.dev/health"
ARCHIVE_HEALTH = "https://qnfo-archive.q08.workers.dev/health"

HTTP_TIMEOUT = 4  # seconds per request (app kills hooks at 30s; budget < 25s)
STDIN_PROBE_TIMEOUT = 0.8  # seconds; production stdin is empty -> don't linger


def _ensure_log_dir():
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
    except Exception as e:
        print(f"[cf-audit-hook] WARN cannot create log dir: {e}", file=sys.stderr)


_ensure_log_dir()


def read_stdin_payload(timeout=STDIN_PROBE_TIMEOUT):
    """Read the full hook payload from stdin without hanging.

    NOTE: in production the app spawns the hook with NO stdin, so this probe
    times out quickly and returns {}. Event/conversationId are obtained from
    argv placeholders and DEEPCHAT_* env vars instead (see main()).
    """
    result = {}

    def _read():
        try:
            raw = sys.stdin.read()
            result["raw"] = raw
        except Exception as e:
            result["error"] = str(e)

    t = threading.Thread(target=_read, daemon=True)
    t.start()
    t.join(timeout)
    raw = result.get("raw", "")
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {"_raw_unparsed": raw[:2000]}


def http_get(url, timeout=HTTP_TIMEOUT):
    """GET with a UA header; returns (ok, status, body_dict_or_text)."""
    req = urllib.request.Request(url, headers={"User-Agent": "deepchat-hook-audit/1.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            try:
                return True, resp.status, json.loads(body)
            except Exception:
                return True, resp.status, body
    except urllib.error.HTTPError as e:
        try:
            return False, e.code, json.loads(e.read().decode("utf-8", errors="replace"))
        except Exception:
            return False, e.code, {"error": str(e)}
    except Exception as e:
        return False, 0, {"error": str(e)}


def log_record(record):
    """Append one JSONL record to the monthly audit log (bounded, pruned)."""
    month = time.strftime("%Y-%m")
    log_path = os.path.join(LOG_DIR, f"audit-{month}.jsonl")
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[cf-audit-hook] WARN log write failed: {e}", file=sys.stderr)
    # prune logs older than 90 days
    try:
        cutoff = time.time() - 90 * 86400
        for fn in os.listdir(LOG_DIR):
            if not fn.startswith("audit-") or not fn.endswith(".jsonl"):
                continue
            p = os.path.join(LOG_DIR, fn)
            try:
                if os.path.getmtime(p) < cutoff:
                    os.remove(p)
            except Exception:
                pass
    except Exception:
        pass


def run_health_ping():
    """Health-check lifecycle/gateway/archive in PARALLEL (worst case = 4s)."""
    targets = [
        ("lifecycle", LIFECYCLE_BASE + "/health"),
        ("gateway", GATEWAY_HEALTH),
        ("archive", ARCHIVE_HEALTH),
    ]

    def _check(item):
        name, url = item
        ok, status, body = http_get(url)
        return name, {
            "ok": ok and status == 200,
            "http": status,
            "detail": (body.get("status") if isinstance(body, dict) else None),
        }

    checks = {}
    with ThreadPoolExecutor(max_workers=3) as ex:
        for name, check in ex.map(_check, targets):
            checks[name] = check
    return checks


def run_status():
    ok, status, body = http_get(LIFECYCLE_BASE + "/status")
    return {
        "ok": ok and status == 200,
        "http": status,
        "projects": body.get("projects") if isinstance(body, dict) else None,
        "auditSessions": body.get("auditSessions") if isinstance(body, dict) else None,
    }


def run_drift_audit():
    ok, status, body = http_get(LIFECYCLE_BASE + "/run/drift")
    if isinstance(body, dict):
        return {
            "ok": ok and status == 200,
            "http": status,
            "verdict": body.get("verdict"),
            "driftCount": body.get("driftCount"),
            "drift": body.get("drift", []),
            "warnings": body.get("warnings", []),
        }
    return {"ok": False, "http": status, "detail": str(body)[:300]}


def main():
    payload = read_stdin_payload()
    argv = dict(zip(sys.argv[1::2], sys.argv[2::2]))

    # Precedence: argv placeholders > DEEPCHAT_* env > stdin payload
    event = (argv.get("--event")
             or os.environ.get("DEEPCHAT_HOOK_EVENT")
             or payload.get("event", ""))
    conv_id = (argv.get("--conversationId")
               or os.environ.get("DEEPCHAT_CONVERSATION_ID")
               or (payload.get("session") or {}).get("conversationId", ""))
    is_test_raw = (argv.get("--isTest")
                   or os.environ.get("DEEPCHAT_HOOK_IS_TEST")
                   or ("" if payload.get("isTest") is None else str(payload.get("isTest"))))
    if isinstance(is_test_raw, bool):
        is_test = is_test_raw
    elif isinstance(is_test_raw, str):
        is_test = is_test_raw.lower() in ("1", "true", "yes")
    else:
        is_test = False

    session = payload.get("session") or {}
    agent_id = os.environ.get("DEEPCHAT_AGENT_ID") or session.get("agentId")
    workdir = os.environ.get("DEEPCHAT_WORKDIR") or session.get("workdir")

    started = time.time()
    record = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "event": event,
        "isTest": bool(is_test),
        "conversationId": conv_id,
        "agentId": agent_id,
        "workdir": workdir,
        "source": "deepchat-hook",
        "checks": {},
        "drift": None,
        "ok": True,
    }

    checks = run_health_ping()
    record["checks"] = checks
    record["ok"] = record["ok"] and all(c["ok"] for c in checks.values())

    if event == "SessionEnd":
        record["status"] = run_status()
        drift = run_drift_audit()
        record["drift"] = drift
        record["ok"] = record["ok"] and drift.get("ok", False)

    record["elapsedMs"] = int((time.time() - started) * 1000)
    log_record(record)

    status_line = " | ".join(f"{k}={v['http']}" for k, v in checks.items())
    print(f"[cf-audit-hook] event={event} health:{status_line} ok={record['ok']}")
    if record.get("drift") is not None:
        d = record["drift"]
        print(f"[cf-audit-hook] drift verdict={d.get('verdict')} count={d.get('driftCount')}")
    if record.get("status"):
        s = record["status"]
        print(f"[cf-audit-hook] status projects={s.get('projects')} auditSessions={s.get('auditSessions')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[cf-audit-hook] FATAL {e}", file=sys.stderr)
        sys.exit(0)
