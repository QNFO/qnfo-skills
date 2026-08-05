r"""
write-to-obsidian.py -- canonical Obsidian daily-note appender (stdlib only, zero deps).

Usage:
  echo "content" | python write-to-obsidian.py --slug "daily-briefing" --section "Daily Research Briefing"
  python write-to-obsidian.py --slug "job-market-watch" --section "Job Market Watch" --file report.txt
  python write-to-obsidian.py --slug "conference-radar" --section "Conference Radar" --text "raw text"

Each --slug produces a DESCRIPTIVE, recognizable filename:
  D:/Obsidian/notes/v1/YYYY/MM/DD/_<slug>-YYYY-MM-DD.md
Examples:
  _daily-briefing-2026-08-05.md
  _job-market-watch-2026-08-05.md
  _conference-radar-2026-08-05.md

Same slug on the same day = APPENDS sections to the same file (multiple runs accumulate).
Different slugs = separate files (each report type is independently identifiable).

GitHub canonical: QNFO/qnfo-skills -> research/scripts/write-to-obsidian.py
Local execution: C:/Users/LENOVO/.deepchat/skills/research/scripts/write-to-obsidian.py
"""

import argparse, datetime, os, sys, subprocess


# ── Filename: _<slug>-YYYY-MM-DD.md ──────────────────────────────────

def note_filename(slug):
    """Generate descriptive filename: _<slug>-YYYY-MM-DD.md"""
    now = datetime.datetime.now()
    return f'_{slug}-{now.year:04d}-{now.month:02d}-{now.day:02d}.md'

def obsidian_dir(now=None):
    now = now or datetime.datetime.now()
    return rf'D:\Obsidian\notes\v1\{now.year:04d}\{now.month:02d}\{now.day:02d}'

def find_or_create_note(slug):
    """Find existing note for this slug in today's dir, or create one. Returns (path, is_new)."""
    d = obsidian_dir()
    os.makedirs(d, exist_ok=True)

    fname = note_filename(slug)
    path = os.path.join(d, fname)

    if os.path.exists(path):
        return path, False

    # Create new note with header
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    header = f'# {slug.replace("-", " ").title()}\n\n> {now}\n\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(header)
    return path, True


# ── Section appender ─────────────────────────────────────────────────

def append_section(path, section_title, body):
    """Append a timestamped section to the note."""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f'\n---\n\n## {section_title}\n\n')
        f.write(f'*{now}*\n\n')
        f.write(body.strip() + '\n')


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Append content to an Obsidian daily note.')
    parser.add_argument('--slug', required=True,
                        help='Report slug (e.g. "daily-briefing", "job-market-watch") -- determines filename: _<slug>-YYYY-MM-DD.md')
    parser.add_argument('--section', required=True,
                        help='Section heading (e.g. "Daily Research Briefing")')
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

    # Find or create today's note for this slug
    note_path, is_new = find_or_create_note(args.slug)

    # Append the section
    append_section(note_path, args.section, body)

    action = 'Created' if is_new else 'Updated'
    print(f'{action} note: {note_path}')
    print(f'  Slug: {args.slug}')
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
                pass


if __name__ == '__main__':
    main()
