"""
write-to-obsidian.py — canonical Obsidian daily-note appender (stdlib only, zero deps).

Usage:
  echo "content" | python write-to-obsidian.py --section "Daily Briefing"
  python write-to-obsidian.py --section "Job Market Watch" --file report.txt
  python write-to-obsidian.py --section "QNFO Status" --text "All systems operational."

Writes/appends a timestamped section into today's Obsidian daily note:
  D:\\Obsidian\\notes\\v1\\YYYY\\MM\\DD\\_YYDDDDHHmmss.md

Naming convention (user-confirmed 2026-08-05):
  _YYDDDDHHmmss.md  where YY=year, DDD=day-of-year, HHmmss=local time.

If a note already exists in today's directory (any file starting with _), it APPENDS to
that file (so multiple reports accumulate in one daily note). If no note exists yet,
creates one with a header.

GitHub canonical: QNFO/qnfo-skills → research/scripts/write-to-obsidian.py
Local execution: C:\\Users\\LENOVO\\.deepchat\\skills\\research\\scripts\\write-to-obsidian.py
"""

import argparse, datetime, os, sys, subprocess


# ── Naming convention ────────────────────────────────────────────────

def note_name():
    now = datetime.datetime.now()
    yy = str(now.year)[2:]
    ddd = f'{now.timetuple().tm_yday:03d}'
    hhmmss = now.strftime('%H%M%S')
    return f'_{yy}{ddd}{hhmmss}.md'

def obsidian_dir(now=None):
    now = now or datetime.datetime.now()
    return rf'D:\Obsidian\notes\v1\{now.year:04d}\{now.month:02d}\{now.day:02d}'

def find_or_create_note(content=''):
    """Find existing note in today's dir, or create one. Returns (path, is_new)."""
    d = obsidian_dir()
    os.makedirs(d, exist_ok=True)

    # Look for existing notes in today's directory
    existing = sorted([
        f for f in os.listdir(d)
        if f.startswith('_') and f.endswith('.md')
    ])

    if existing:
        path = os.path.join(d, existing[-1])
        return path, False

    # Create new note
    path = os.path.join(d, note_name())
    header = f'# QNFO Research Intelligence\n\n> Generated {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(header)
    return path, True


# ── Section appender ─────────────────────────────────────────────────

def append_section(path, section_title, body):
    """Append a timestamped section to the note."""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f'\n---\n\n## {section_title}\n\n')
        f.write(f'*Generated {now}*\n\n')
        f.write(body.strip() + '\n')


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Append content to Obsidian daily note.')
    parser.add_argument('--section', required=True, help='Section title (e.g. "Daily Briefing")')
    parser.add_argument('--file', help='Read content from file (default: stdin)')
    parser.add_argument('--text', help='Content as command-line string')
    parser.add_argument('--no-git', action='store_true', help='Skip git stage (for cron agents)')
    args = parser.parse_args()

    # Resolve content
    if args.text:
        body = args.text
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            body = f.read()
    else:
        body = sys.stdin.read()

    if not body.strip():
        print('ERROR: no content provided', file=sys.stderr)
        sys.exit(1)

    # Find or create today's note
    note_path, is_new = find_or_create_note(body)

    # Append the section
    append_section(note_path, args.section, body)

    action = 'Created' if is_new else 'Updated'
    print(f'{action} note: {note_path}')
    print(f'  Section: {args.section}')
    print(f'  Size: {len(body)} chars')

    # Git stage if Obsidian is a git repo
    if not args.no_git:
        obs_root = os.path.dirname(obsidian_dir())
        if os.path.isdir(os.path.join(obs_root, '.git')):
            try:
                subprocess.run(['git', '-C', obs_root, 'add', note_path],
                               capture_output=True, text=True, timeout=10)
                print(f'  Git: staged {os.path.basename(note_path)}')
            except Exception:
                pass  # git stage is best-effort for cron agents


if __name__ == '__main__':
    main()
