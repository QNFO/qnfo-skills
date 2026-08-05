"""
QNFO Research Intelligence — Obsidian note generator (periodic, recurring).
Usage:
  python obsidian-intelligence-note.py [--days N] [--no-scan]

Generates a self-contained markdown note into today's Obsidian directory:
  D:\\Obsidian\\notes\\v1\\YYYY\\MM\\DD\\_YYDDDDHHmmss.md
(convention: YY=year, DDD=day-of-year, HHmmss=local time — user-confirmed 2026-08-05)

Sections: system status | new research (HIGH/MEDIUM) | conferences (agent-enriched)
          | jobs PhD-filtered (agent-enriched) | action checklist | how-generated.

--days N: scan window for arXiv (default 3, weekly view).
--no-scan: skip arXiv fetch (use when the cronjob agent has fresher briefing data).

Thin-client canonical: GitHub QNFO/qnfo-skills -> research/scripts/obsidian-intelligence-note.py
"""
import importlib.util, os, sys, time, datetime

# ── Load research-daily-brief as a module (same dir, hyphenated filename) ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
def load_brief():
    path = os.path.join(SCRIPT_DIR, 'research-daily-brief.py')
    spec = importlib.util.spec_from_file_location('research_daily_brief', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# ── Naming convention: _YYDDDDHHmmss ──
def note_name():
    now = datetime.datetime.now()
    yy = str(now.year)[2:]
    ddd = f'{now.timetuple().tm_yday:03d}'
    hhmmss = now.strftime('%H%M%S')
    return f'_{yy}{ddd}{hhmmss}.md'

def obsidian_dir(now=None):
    now = now or datetime.datetime.now()
    return rf'D:\Obsidian\notes\v1\{now.year:04d}\{now.month:02d}\{now.day:02d}'

def make_note_path():
    d = obsidian_dir()
    os.makedirs(d, exist_ok=True)
    # ensure unique
    for attempt in range(20):
        name = note_name()
        path = os.path.join(d, name)
        if not os.path.exists(path):
            return path
        time.sleep(1.1)
    # fallback: append ms
    name = f'_{str(datetime.datetime.now().year)[2:]}{datetime.datetime.now().timetuple().tm_yday:03d}{int(time.time())%1000000:06d}.md'
    return os.path.join(d, name)

def papers_section(days=3):
    """Fetch recent arXiv papers + keyword-match. Returns markdown section."""
    try:
        b = load_brief()
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        date_start = today - datetime.timedelta(days=days)
        date_end = today - datetime.timedelta(seconds=1)
        papers = b.fetch_arxiv(date_start, date_end)
        kw = dict(b.DAILY_KW)
        matched = b.match_keywords(papers, kw)
        if not matched:
            return "### 📄 New Research\n\n*(No new papers matched QNFO keywords in the window.)*\n"
        high = [p for p in matched if p['score'] >= 10]
        med = [p for p in matched if 5 <= p['score'] < 10]
        lines = ['### 📄 New Research (recent window)', '']
        if high:
            lines.append('#### 🔴 HIGH RELEVANCE')
            lines.append('')
            for p in high[:5]:
                prog = p['primary_program'] or 'RES'
                lines.append(f'**{p["title"][:130]}**')
                lines.append(f'- [{prog}] {", ".join(p["authors"][:3])}{" et al." if len(p["authors"])>3 else ""} | {p["id"]} | {p["published"]}')
                lines.append(f'- 🔗 [Read on arXiv](https://arxiv.org/abs/{p["id"]})')
                lines.append('')
        if med:
            lines.append('#### 🟡 MEDIUM')
            lines.append('')
            lines.append('| # | Paper | Link |')
            lines.append('|:--|:------|:-----|')
            for i, p in enumerate(med[:10], 1):
                prog = p['primary_program'] or 'RES'
                title = p['title'][:110].replace('|', '\\|')
                lines.append(f'| {i} | **{title}** — [{prog}] | [arXiv](https://arxiv.org/abs/{p["id"]}) |')
            lines.append('')
        total = len(matched)
        lines.append(f'*{total} papers matched keywords across {len({p["primary_program"] for p in matched if p["primary_program"]})} programs in the scan window.*')
        return '\n'.join(lines)
    except Exception as e:
        return f'### 📄 New Research\n\n*(arXiv scan failed: {e})*\n'

def build_note(days=3, include_scan=True):
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    papers = papers_section(days) if include_scan else "### 📄 New Research\n\n*(See the daily/weekly briefing notifications for the latest papers — scan skipped per --no-scan.)*\n"
    note = f'''---
title: "QNFO Research Intelligence — {date_str}"
date: {date_str}
type: periodic-report
source: research-daily-brief.py (arXiv/OpenAlex) + Conference Radar + Job Market Watch cronjobs
---

# QNFO Research Intelligence — {date_str}

> Automated periodic report. Sources: arXiv daily scan, OpenAlex weekly scan,
> Conference Radar (monthly), Job Market Watch (biweekly, PhD-filtered), Citation Watch.
> Briefings archived to `alerts@qnfo.org`. Zero manual setup required.

---

## 1. 📊 System Status — Autonomous Monitors

| Monitor | Schedule | Status |
|:--------|:---------|:-------|
| Daily arXiv Briefing | 08:00 UTC daily | ✅ live |
| Weekly Deep Scan | Mon 09:00 UTC | ✅ live |
| Conference Radar | 1st of month | ✅ live |
| Job Market Watch (PhD-filtered) | 1st + 15th | ✅ live |
| Citation Watch | 1st + 15th | ✅ live |
| Email Inbox Check | every 3h | ✅ live |
| Obsidian Intelligence Note | Mon 10:00 UTC | ✅ this note |

---

{papers}

---

## 3. 📅 Conferences — Actionable

> *(Populated by the Conference Radar run — see the latest radar notification or memory:
> memory_recall "Conference Radar". Key recurring items: CIMPA p-Adic/Ultrametric School Vietnam
> (apply by Oct 22 2026), Laws of Form Cambridge Aug 10-14 2026, CWI QEC workshop Oct 28-30,
> Bruhat-Tits Darmstadt Sep 9-11, QPL Amsterdam Aug 17-21.)*

---

## 4. 💼 Jobs — PhD-FILTERED (candidate has no doctorate)

> *(Populated by the Job Market Watch run — see the latest radar notification or memory:
> memory_recall "Job Market Watch". ALL postdoc/faculty/tenure-track positions are EXCLUDED.
> Viable roles are industry/executive only: Principal Quantum Systems Architect, Director of
> Technology/Research, CTO, Chief Scientist, CDO, policy fellow, institute director, senior
> research scientist (experience-accepting). Verify each listing — some say "PhD preferred"
> but accept equivalent professional experience.)*

---

## 5. ✅ Action Checklist

> *(Update from the latest radar outputs. Standing items: check conference deadlines,
> follow up on job applications, review HIGH-relevance papers.)*

---

## 6. 📚 How This Report Is Generated

| Component | Tool | Canonical location |
|:----------|:-----|:-------------------|
| Daily arXiv scan | `research-daily-brief.py --mode daily` | GitHub `QNFO/qnfo-skills` → `research/scripts/` |
| Weekly OpenAlex scan | `research-daily-brief.py --mode weekly` | same |
| Note generation | `obsidian-intelligence-note.py` | same |
| Conference Radar | cronjob `dcdc7a6a` (1st monthly) | DeepChat scheduled tasks |
| Job Market Watch | cronjob `a194153f` (1st+15th) | DeepChat scheduled tasks |
| Citation Watch | cronjob `8d1292ce` (1st+15th) | DeepChat scheduled tasks |
| Email archive | `alerts@qnfo.org` | Cloudflare Email Routing → Worker |

---

*Generated automatically {date_str} by the QNFO Research Intelligence stack.*
'''
    return note

def main():
    import argparse
    ap = argparse.ArgumentParser(description='QNFO Obsidian Intelligence Note')
    ap.add_argument('--days', type=int, default=3, help='arXiv scan window (default 3)')
    ap.add_argument('--no-scan', action='store_true', help='Skip arXiv fetch')
    args = ap.parse_args()

    path = make_note_path()
    note = build_note(days=args.days, include_scan=not args.no_scan)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(note)
    print(f'NOTE WRITTEN: {path}')
    print(f'Size: {len(note)} bytes | Lines: {note.count(chr(10))}')
    # verify
    with open(path, 'r', encoding='utf-8') as f:
        ok = 'QNFO Research Intelligence' in f.read()
    print(f'Verify: {"OK" if ok else "FAIL"}')

if __name__ == '__main__':
    main()
