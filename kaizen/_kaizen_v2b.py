"""Kaizen v2 FIXED: VERIFY-FACT-1 — applied to qnfo-core, research, kaizen.
Uses short, unique substrings for banner insertion instead of full header+banner match."""

import os, shutil, subprocess

# =============================================================================
# 1. QNFO-CORE: v1.16 → v1.17
# =============================================================================
print("=== QNFO-CORE v1.16 → v1.17 ===")
qc_path = r"C:\Users\LENOVO\.deepchat\skills\qnfo-core\SKILL.md"

# Re-read fresh (script was partially applied, need to restore)
# First, copy back from git
subprocess.run(["git", "-C", r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills", "checkout", "qnfo-core/SKILL.md"], check=True)
shutil.copy2(r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills\qnfo-core\SKILL.md", qc_path)

with open(qc_path, "r", encoding="utf-8") as f:
    qc = f.read()

assert "version: 1.16" in qc and "# QNFO Core — v1.16" in qc and "Current: **v1.16**" in qc, "qnfo-core version mismatch"

# Rule 6 + VERIFY-FACT-1
qc = qc.replace(
    "6. INSTITUTIONAL STATUS IS NOT EVIDENCE (KIF-16). Evaluate claims against evidence, not venue or affiliation.",
    "6. INSTITUTIONAL STATUS IS NOT EVIDENCE (KIF-16). Evaluate claims against evidence, not venue or affiliation.\n\n7. VERIFY EXISTENCE CLAIMS — NEVER ASSUME (v1.17). A factual claim that a system, model, API, standard, paper, or entity exists or does not exist MUST be verified against a live source (API, web search, official documentation) BEFORE appearing in any text. A model release date, a DOI's target, a software version — none of these may be assumed from training knowledge. Every existence claim requires a same-turn tool call showing the verification source. An incorrect existence claim (e.g., 'GPT-5 does not exist') is a factual error indistinguishable from a fabrication. [HARD]"
)

# Add anti-pattern row
qc = qc.replace(
    "| **TITLE-DUPLICATION-1: Body `# <Title>` H1 alongside YAML `title:` — title twice on page 1 (2026-08-05)**",
    "| **VERIFY-FACT-1: Making factual existence claims (\"X does not exist\" / \"X was released on Y\") without live source verification (2026-08-05)** | **HARD GATE.** Every existence claim requires a same-turn tool call to a live source. Assumptions from training data are indistinguishable from fabrication when wrong. Canonical case: Heffner audit v1.0 claimed GPT-5 didn't exist; GPT-5 released Aug 7, 2025 (Wikipedia). Cross-ref: research v2.85, kaizen v1.59. |\n| **TITLE-DUPLICATION-1: Body `# <Title>` H1 alongside YAML `title:` — title twice on page 1 (2026-08-05)**"
)

# Version bumps
qc = qc.replace("version: 1.16", "version: 1.17", 1)
qc = qc.replace("# QNFO Core — v1.16", "# QNFO Core — v1.17", 1)
qc = qc.replace("Current: **v1.16** (qnfo-core — email-composer on-disk-only reference fix; 2026-08-05)",
                "Current: **v1.17** (qnfo-core — VERIFY-FACT-1: fact-check existence claims before publishing; 2026-08-05)", 1)

# Insert banner using a unique anchor that survives the header bump
anchor = "> **v1.16 UPDATE (2026-08-05, kaizen — Published-Paper Hygiene Mandate):**"
assert anchor in qc, "v1.16 banner not found"

banner = """# QNFO Core — v1.17
> **v1.17 UPDATE (2026-08-05, kaizen — VERIFY-FACT-1: factual existence claims require live verification):**
> Red-team: direct parent-agent audit (session SKILLS UPDATE — GPT-5 fact-check failure).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **VERIFY-FACT-1 anti-pattern added** — factual existence claims require live
>     source verification. 'GPT-5 does not exist' was false (released Aug 7, 2025).
>     Added to Core Rules (#7) + anti-patterns table. Canonical case: Heffner audit
>     v1.0→v1.1 (DOI 10.5281/zenodo.21812761).
> Cross-reference: research v2.85, kaizen v1.59."""
qc = qc.replace(f"# QNFO Core — v1.17\n{anchor}", f"{banner}\n{anchor}", 1)

with open(qc_path, "w", encoding="utf-8") as f:
    f.write(qc)

with open(qc_path, "r", encoding="utf-8") as f:
    v = f.read()
for check in ["version: 1.17", "v1.17 UPDATE", "Current: **v1.17**", "VERIFY-FACT-1", "VERIFY EXISTENCE CLAIMS"]:
    assert check in v, f"Failed qnfo-core: {check}"
print("[OK] qnfo-core v1.17")

# =============================================================================
# 2. RESEARCH: v2.84 → v2.85
# =============================================================================
print("\n=== RESEARCH v2.84 → v2.85 ===")
r_path = r"C:\Users\LENOVO\.deepchat\skills\research\SKILL.md"
subprocess.run(["git", "-C", r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills", "checkout", "research/SKILL.md"], check=True)
shutil.copy2(r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills\research\SKILL.md", r_path)

with open(r_path, "r", encoding="utf-8") as f:
    r = f.read()

assert "version: 2.84" in r and "# RESEARCH — v2.84" in r and "Current: **v2.84**" in r, "research version mismatch"

# Add anti-pattern
r = r.replace(
    "| **TITLE-DUPLICATION-1: Body `# <Title>` H1 alongside YAML `title:` — title renders TWICE on page 1 (2026-08-05)**",
    "| **VERIFY-FACT-1: Making factual existence claims without live source verification (2026-08-05)** | **HARD GATE.** Every existence claim requires a same-turn tool call. Assumptions from training data = fabrication when wrong. Canonical case: Heffner audit v1.0 → v1.1 (DOI 10.5281/zenodo.21812761). Cross-ref: qnfo-core v1.17, kaizen v1.59. |\n| **TITLE-DUPLICATION-1: Body `# <Title>` H1 alongside YAML `title:` — title renders TWICE on page 1 (2026-08-05)**"
)

# Add to Publication Language Gate
r = r.replace(
    "**internal references (repo paths, skill sections, internal program names — INTERNAL-REF-1)**, **title duplication",
    "**internal references (repo paths, skill sections, internal program names — INTERNAL-REF-1)**, **existence claims verified against live sources (VERIFY-FACT-1)**, **title duplication"
)

# Version bumps
r = r.replace("version: 2.84", "version: 2.85", 1)
r = r.replace("# RESEARCH — v2.84", "# RESEARCH — v2.85", 1)
r = r.replace("Current: **v2.84** (research — Briefing System",
              "Current: **v2.85** (research — VERIFY-FACT-1; Briefing System", 1)

# Banner
r_anchor = "> **v2.84 UPDATE (2026-08-05, kaizen — PUBLISHED-PAPER HYGIENE"
assert r_anchor in r, "v2.84 banner not found"

r_banner = """# RESEARCH — v2.85
> **v2.85 UPDATE (2026-08-05, kaizen — VERIFY-FACT-1: existence claims require live verification):**
> Red-team: direct parent-agent audit (session SKILLS UPDATE — GPT-5 fact-check failure).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **VERIFY-FACT-1 anti-pattern added** — factual existence claims in papers MUST be
>     verified against live sources. 'GPT-5 does not exist' (v1.0 §2.2) was wrong. Added to
>     anti-patterns + Publication Language Gate. Canonical case: DOI 10.5281/zenodo.21812761.
> Cross-reference: qnfo-core v1.17, kaizen v1.59."""
r = r.replace(f"# RESEARCH — v2.85\n{r_anchor}", f"{r_banner}\n{r_anchor}", 1)

with open(r_path, "w", encoding="utf-8") as f:
    f.write(r)

with open(r_path, "r", encoding="utf-8") as f:
    v = f.read()
for check in ["version: 2.85", "v2.85 UPDATE", "Current: **v2.85**", "VERIFY-FACT-1"]:
    assert check in v, f"Failed research: {check}"
print("[OK] research v2.85")

# =============================================================================
# 3. KAIZEN: v1.58 → v1.59
# =============================================================================
print("\n=== KAIZEN v1.58 → v1.59 ===")
k_path = r"C:\Users\LENOVO\.deepchat\skills\kaizen\SKILL.md"
subprocess.run(["git", "-C", r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills", "checkout", "kaizen/SKILL.md"], check=True)
shutil.copy2(r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills\kaizen\SKILL.md", k_path)

with open(k_path, "r", encoding="utf-8") as f:
    k = f.read()

assert "version: 1.58" in k and "# KAIZEN — v1.58" in k and "Current: **v1.58**" in k, "kaizen version mismatch"

# Add anti-pattern
k = k.replace(
    "| **TITLE-DUPLICATION-1: Published paper renders the title TWICE on page 1",
    "| **VERIFY-FACT-1: Factual existence claims without live source verification (2026-08-05)** | **HARD GATE.** 'GPT-5 does not exist' was wrong — released Aug 7, 2025. Every existence claim requires a same-turn tool call. Owner: qnfo-core v1.17. Canonical case: Heffner audit v1.0 → v1.1 (DOI 10.5281/zenodo.21812761). |\n| **TITLE-DUPLICATION-1: Published paper renders the title TWICE on page 1"
)

# Version bumps
k = k.replace("version: 1.58", "version: 1.59", 1)
k = k.replace("# KAIZEN — v1.58", "# KAIZEN — v1.59", 1)
k = k.replace("Current: **v1.58** (kaizen — SKILLS UPDATE ecosystem audit + cross-ref verification; 2026-08-05)",
              "Current: **v1.59** (kaizen — VERIFY-FACT-1: factual existence claims require live verification; 2026-08-05)", 1)

# Banner
k_anchor = "> **v1.58 UPDATE (2026-08-05, kaizen — SKILLS UPDATE ecosystem audit + cross-ref verification):**"
assert k_anchor in k, "v1.58 banner not found"

k_banner = """# KAIZEN — v1.59
> **v1.59 UPDATE (2026-08-05, kaizen — VERIFY-FACT-1: factual existence claims require live verification):**
> Red-team: direct parent-agent audit (session SKILLS UPDATE — GPT-5 fact-check failure).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **VERIFY-FACT-1 anti-pattern added** — factual existence claims made from
>     training data without live verification are indistinguishable from fabrication when
>     wrong. Canonical case: Heffner audit v1.0 §2.2 (DOI 10.5281/zenodo.21812761).
> Cross-reference: qnfo-core v1.17, research v2.85."""
k = k.replace(f"# KAIZEN — v1.59\n{k_anchor}", f"{k_banner}\n{k_anchor}", 1)

with open(k_path, "w", encoding="utf-8") as f:
    f.write(k)

with open(k_path, "r", encoding="utf-8") as f:
    v = f.read()
for check in ["version: 1.59", "v1.59 UPDATE", "Current: **v1.59**", "VERIFY-FACT-1"]:
    assert check in v, f"Failed kaizen: {check}"
print("[OK] kaizen v1.59")

# =============================================================================
# 4. GIT SYNC
# =============================================================================
print("\n=== GIT SYNC ===")
git_repo = r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills"
for skill_name, skill_file in [
    ("qnfo-core", "qnfo-core/SKILL.md"),
    ("research", "research/SKILL.md"),
    ("kaizen", "kaizen/SKILL.md"),
]:
    src = rf"C:\Users\LENOVO\.deepchat\skills\{skill_name}\SKILL.md"
    dst = os.path.join(git_repo, skill_file)
    shutil.copy2(src, dst)
    print(f"  Copied: {skill_name}")

subprocess.run(["git", "-C", git_repo, "add",
    "qnfo-core/SKILL.md", "research/SKILL.md", "kaizen/SKILL.md"], check=True)

subprocess.run(["git", "-C", git_repo, "commit", "-m",
    "feat(skills): VERIFY-FACT-1 — qnfo-core v1.17, research v2.85, kaizen v1.59"], check=True)

subprocess.run(["git", "-C", git_repo, "push", "origin", "master"], check=True)
print("[OK] git synced")

# Update .kaizen_history for kaizen skill
import json
hist_path = r"C:\Users\LENOVO\.deepchat\skills\kaizen\.kaizen_history"
try:
    with open(hist_path, "r") as f:
        hist = json.load(f)
except:
    hist = {"skill": "kaizen", "entries": []}

hist["entries"].append({
    "version": "v1.59",
    "date": "2026-08-05",
    "type": "kaizen",
    "red_team_roles": 5,
    "hard_findings": 1,
    "soft_findings": 0,
    "design_findings": 0,
    "watchtower_triggered": False,
    "summary": "VERIFY-FACT-1: factual existence claims require live source verification. GPT-5 fact-check failure in Heffner audit v1.0."
})

with open(hist_path, "w") as f:
    json.dump(hist, f, indent=2)

# Also copy to git repo and commit the dotfile
import shutil as sh
sh.copy2(hist_path, os.path.join(git_repo, "kaizen", ".kaizen_history"))
subprocess.run(["git", "-C", git_repo, "add", "kaizen/.kaizen_history"], check=True)
subprocess.run(["git", "-C", git_repo, "commit", "-m", "chore(kaizen): update .kaizen_history for v1.59"], check=True)
subprocess.run(["git", "-C", git_repo, "push", "origin", "master"], check=True)

print("\n=== ALL DONE ===")
print("qnfo-core: v1.16 → v1.17")
print("research: v2.84 → v2.85")
print("kaizen: v1.58 → v1.59")
