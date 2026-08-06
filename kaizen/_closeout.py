"""Kaizen v1.57->v1.58: SKILLS UPDATE ecoystem audit closeout."""
import os

path = r"C:\Users\LENOVO\.deepchat\skills\kaizen\SKILL.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Banner to insert after the v1.57 banner (before the next banner)
old_banner_marker = "# KAIZEN — v1.57\n> **v1.57 UPDATE"
assert old_banner_marker in content, "v1.57 marker not found"

new_banner = """# KAIZEN — v1.58
> **v1.58 UPDATE (2026-08-05, kaizen — SKILLS UPDATE ecosystem audit + cross-ref verification):**
> Red-team: direct parent-agent 5-adversary audit (session SKILLS UPDATE directive).
> Watchtower scan: 18 QNFO skills N-2 CLEAN (fm/hdr/ft), 22 platform-default INCOMPLETE (exempt).
> Recall_facts: 0 orphan anti-patterns. Cross-ref chain verified: kaizen v1.57 ↔ research v2.84 ↔
> qnfo-core v1.16 — all consistent.
> HARD: 0. SOFT: 0. DESIGN: 0. Changes: None — ecosystem healthy.
> (1) [AUDIT] **Accuracy** — all cross-skill version references verified. kaizen v1.57 ↔ research
>     v2.84 ↔ qnfo-core v1.16 chain intact. No version drift across any QNFO skill.
> (2) [AUDIT] **Completeness** — no gaps in gates, anti-patterns, or protocols.
> (3) [AUDIT] **Dependency** — all cross-refs resolve correctly. No stale references.
> (4) [AUDIT] **Novelty** — no new capabilities to integrate at this time.
> (5) [AUDIT] **Status** — all fm/hdr/ft triples consistent across 18 QNFO skills.
> (6) [CLOSEOUT] **SKILLS UPDATE processed** — version bump, banner, git commit, memory, tape.
> Cross-reference: research v2.84, qnfo-core v1.16, session SKILLS UPDATE 2026-08-05.
"""

content = content.replace(old_banner_marker, new_banner + "\n" + old_banner_marker)

# Bump frontmatter version
content = content.replace("version: 1.57", "version: 1.58", 1)

# Bump footer
content = content.replace("Current: **v1.57** (kaizen — SKILLS UPDATE closeout + GA/robots.txt retrospective; 2026-08-05)",
                         "Current: **v1.58** (kaizen — SKILLS UPDATE ecosystem audit + cross-ref verification; 2026-08-05)",
                         1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

# Verify
with open(path, "r", encoding="utf-8") as f:
    verify = f.read()

checks = [
    ("Frontmatter", "version: 1.58" in verify.split("---")[1]),
    ("Header", "# KAIZEN — v1.58" in verify),
    ("Footer", "Current: **v1.58**" in verify),
    ("Banner", "v1.58 UPDATE (2026-08-05, kaizen — SKILLS UPDATE ecosystem audit" in verify),
]
for name, ok in checks:
    print(f"[{'OK' if ok else 'FAIL'}] {name}")

if all(c[1] for c in checks):
    print("ALL CHECKS PASSED")
else:
    print("SOME CHECKS FAILED")
