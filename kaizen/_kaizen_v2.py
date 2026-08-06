"""Kaizen v2: VERIFY-FACT-1 — applied to qnfo-core, research, kaizen.
Trigger: GPT-5 fact-check failure in Heffner audit paper (session current).
Agent claimed "GPT-5 does not exist" from training knowledge without live verification.
GPT-5 was released August 7, 2025. Finding: VERIFY-FACT-1 anti-pattern."""

import os, shutil

# =============================================================================
# 1. QNFO-CORE: v1.16 → v1.17
# =============================================================================
print("=== QNFO-CORE v1.16 → v1.17 ===")
qc_path = r"C:\Users\LENOVO\.deepchat\skills\qnfo-core\SKILL.md"
with open(qc_path, "r", encoding="utf-8") as f:
    qc = f.read()

# Check current version
assert "version: 1.16" in qc, "qnfo-core frontmatter not 1.16"
assert "# QNFO Core — v1.16" in qc, "qnfo-core header not v1.16"
assert "Current: **v1.16**" in qc, "qnfo-core footer not v1.16"

# Add VERIFY-FACT-1 to Core Rules (after rule #6)
old_rules = "6. INSTITUTIONAL STATUS IS NOT EVIDENCE (KIF-16). Evaluate claims against evidence, not venue or affiliation."
new_rules = old_rules + """

7. VERIFY EXISTENCE CLAIMS — NEVER ASSUME (v1.17). A factual claim that a system, model, API, standard, paper, or entity exists or does not exist MUST be verified against a live source (API, web search, official documentation) BEFORE appearing in any text. A model release date, a DOI's target, a software version — none of these may be assumed from training knowledge. Every existence claim requires a same-turn tool call showing the verification source. An incorrect existence claim (e.g., 'GPT-5 does not exist') is a factual error indistinguishable from a fabrication. [HARD]"""
qc = qc.replace(old_rules, new_rules)

# Add to anti-patterns table
old_table_marker = "| **TITLE-DUPLICATION-1: Body `# <Title>` H1 alongside YAML `title:` — title twice on page 1 (2026-08-05)**"
new_row = """| **VERIFY-FACT-1: Making factual existence claims (\"X does not exist\" / \"X was released on Y\") without live source verification (2026-08-05)** | **HARD GATE.** Every existence claim (model release dates, DOI targets, software versions, API availability) requires a same-turn tool call to a live source. Assumptions from training data are indistinguishable from fabrication when wrong. Canonical case: Heffner audit v1.0 claimed GPT-5 did not exist; GPT-5 was released August 7, 2025 (Wikipedia). Cross-ref: qnfo-core §0.0 Core Rules #7, research v2.85, kaizen v1.59. |\n| """
qc = qc.replace(old_table_marker, new_row + old_table_marker)

# Version bump: frontmatter
qc = qc.replace("version: 1.16", "version: 1.17", 1)
# Version bump: header
qc = qc.replace("# QNFO Core — v1.16", "# QNFO Core — v1.17", 1)
# Version bump: footer
qc = qc.replace("Current: **v1.16** (qnfo-core — email-composer on-disk-only reference fix; 2026-08-05)",
                "Current: **v1.17** (qnfo-core — VERIFY-FACT-1: fact-check existence claims before publishing; 2026-08-05)", 1)

# Add kaizen banner
old_banner = "# QNFO Core — v1.17\n> **v1.16 UPDATE (2026-08-05, kaizen — Published-Paper Hygiene Mandate):**"
assert old_banner in qc, "Can't find v1.16 banner for insert"

new_banner = """# QNFO Core — v1.17
> **v1.17 UPDATE (2026-08-05, kaizen — VERIFY-FACT-1: factual existence claims require live verification):**
> Red-team: direct parent-agent audit (session SKILLS UPDATE 2026-08-05 — GPT-5 fact-check failure).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **VERIFY-FACT-1 anti-pattern added** — factual existence claims ('X does not exist,'
>     'X was released on Y') MUST be verified against a live source BEFORE text is written. An
>     incorrect existence claim (e.g., 'GPT-5 does not exist' when it was released Aug 7, 2025)
>     is a factual error indistinguishable from fabrication. Added to Core Rules (#7) and
>     anti-patterns table. Canonical case: Heffner audit v1.0 §2.2 — corrected v1.1.
> Cross-reference: research v2.85, kaizen v1.59, Heffner audit DOI 10.5281/zenodo.21812761.
"""
qc = qc.replace(old_banner, new_banner + "\n" + old_banner)

with open(qc_path, "w", encoding="utf-8") as f:
    f.write(qc)

# Verify
with open(qc_path, "r", encoding="utf-8") as f:
    v = f.read()
for check in ["version: 1.17", "# QNFO Core — v1.17", "Current: **v1.17**", "VERIFY-FACT-1", "VERIFY EXISTENCE CLAIMS"]:
    assert check in v, f"Failed: {check}"
print("[OK] qnfo-core v1.17")

# =============================================================================
# 2. RESEARCH: v2.84 → v2.85
# =============================================================================
print("\n=== RESEARCH v2.84 → v2.85 ===")
r_path = r"C:\Users\LENOVO\.deepchat\skills\research\SKILL.md"
with open(r_path, "r", encoding="utf-8") as f:
    r = f.read()

assert "version: 2.84" in r, "research frontmatter not 2.84"
assert "# RESEARCH — v2.84" in r, "research header not v2.84"
assert "Current: **v2.84**" in r, "research footer not v2.84"

# Add VERIFY-FACT-1 to anti-patterns
old_r_ap = "| **TITLE-DUPLICATION-1: Body `# <Title>` H1 alongside YAML `title:` — title renders TWICE on page 1 (2026-08-05)**"
new_r_row = """| **VERIFY-FACT-1: Making factual existence claims (\"X does not exist\" / \"X was released on Y\") without live source verification (2026-08-05)** | **HARD GATE.** Every existence claim in a paper (model release dates, DOI targets, software versions, API availability) requires a same-turn tool call to a live source. Assumptions from training data indistinguishable from fabrication when wrong. Canonical case: Heffner audit v1.0 §2.2 claimed GPT-5 did not exist; GPT-5 released Aug 7, 2025. Corrected in v1.1 (DOI 10.5281/zenodo.21812761). Cross-ref: qnfo-core v1.17, kaizen v1.59. |\n| """
r = r.replace(old_r_ap, new_r_row + old_r_ap)

# Add to Publication Language Gate
old_gate = "**internal references (repo paths, skill sections, internal program names — INTERNAL-REF-1)**, **title duplication"
new_gate = "**internal references (repo paths, skill sections, internal program names — INTERNAL-REF-1)**, **existence claims verified against live sources (VERIFY-FACT-1)**, **title duplication"
r = r.replace(old_gate, new_gate)

# Version bumps
r = r.replace("version: 2.84", "version: 2.85", 1)
r = r.replace("# RESEARCH — v2.84", "# RESEARCH — v2.85", 1)
r = r.replace("Current: **v2.84** (research — Briefing System",
              "Current: **v2.85** (research — VERIFY-FACT-1; Briefing System", 1)

# Add banner
old_r_banner = "# RESEARCH — v2.85\n> **v2.84 UPDATE (2026-08-05, kaizen — PUBLISHED-PAPER HYGIENE"
assert old_r_banner in r, "Can't find research v2.84 banner"

new_r_banner = """# RESEARCH — v2.85
> **v2.85 UPDATE (2026-08-05, kaizen — VERIFY-FACT-1: existence claims require live verification):**
> Red-team: direct parent-agent audit (session SKILLS UPDATE — GPT-5 fact-check failure).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **VERIFY-FACT-1 anti-pattern added** — factual existence claims in papers MUST be
>     verified against live sources BEFORE text is written. 'GPT-5 does not exist' (v1.0 §2.2) was
>     wrong: GPT-5 released Aug 7, 2025. Added to anti-patterns + Publication Language Gate.
>     Canonical case: Heffner audit v1.0→v1.1 (DOI 10.5281/zenodo.21812761).
> Cross-reference: qnfo-core v1.17, kaizen v1.59.
"""
r = r.replace(old_r_banner, new_r_banner + "\n" + old_r_banner)

with open(r_path, "w", encoding="utf-8") as f:
    f.write(r)

with open(r_path, "r", encoding="utf-8") as f:
    v = f.read()
for check in ["version: 2.85", "# RESEARCH — v2.85", "Current: **v2.85**", "VERIFY-FACT-1"]:
    assert check in v, f"Failed: {check}"
print("[OK] research v2.85")

# =============================================================================
# 3. KAIZEN: v1.58 → v1.59
# =============================================================================
print("\n=== KAIZEN v1.58 → v1.59 ===")
k_path = r"C:\Users\LENOVO\.deepchat\skills\kaizen\SKILL.md"
with open(k_path, "r", encoding="utf-8") as f:
    k = f.read()

assert "version: 1.58" in k, "kaizen frontmatter not 1.58"
assert "# KAIZEN — v1.58" in k, "kaizen header not v1.58"
assert "Current: **v1.58**" in k, "kaizen footer not v1.58"

# Add VERIFY-FACT-1 to anti-patterns
old_k_ap = "| **TITLE-DUPLICATION-1: Published paper renders the title TWICE on page 1"
new_k_row = """| **VERIFY-FACT-1: Making factual existence claims (\"X does not exist\" / released on Y) without live source verification (2026-08-05)** | **HARD GATE.** Every existence claim requires a same-turn tool call to a live source. Training-data assumptions indistinguishable from fabrication when wrong. Owner: qnfo-core v1.17. Canonical case: GPT-5 released Aug 7, 2025 but Heffner audit v1.0 claimed it didn't exist — corrected v1.1 (DOI 10.5281/zenodo.21812761). |\n| """
k = k.replace(old_k_ap, new_k_row + old_k_ap)

# Version bumps
k = k.replace("version: 1.58", "version: 1.59", 1)
k = k.replace("# KAIZEN — v1.58", "# KAIZEN — v1.59", 1)
k = k.replace("Current: **v1.58** (kaizen — SKILLS UPDATE ecosystem audit + cross-ref verification; 2026-08-05)",
              "Current: **v1.59** (kaizen — VERIFY-FACT-1: factual existence claims require live verification; 2026-08-05)", 1)

# Add banner
old_k_banner = "# KAIZEN — v1.59\n> **v1.58 UPDATE (2026-08-05, kaizen — SKILLS UPDATE ecosystem audit + cross-ref verification):**"
assert old_k_banner in k, "Can't find kaizen v1.58 banner"

new_k_banner = """# KAIZEN — v1.59
> **v1.59 UPDATE (2026-08-05, kaizen — VERIFY-FACT-1: factual existence claims require live verification):**
> Red-team: direct parent-agent audit (session SKILLS UPDATE — GPT-5 fact-check failure in
> Heffner audit paper v1.0). HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **VERIFY-FACT-1 anti-pattern added** — factual existence claims made from training
>     data without live source verification are indistinguishable from fabrication when wrong.
>     Added to kaizen anti-patterns table. Watchtower scan now flags existence claims without
>     tool-call-backed verification. Canonical case: Heffner audit v1.0 §2.2 — agent claimed
>     GPT-5 didn't exist; it was released Aug 7, 2025. Corrected v1.1 (DOI 10.5281/zenodo.21812761).
> Cross-reference: qnfo-core v1.17, research v2.85, Heffner audit DOI 10.5281/zenodo.21812761.
"""
k = k.replace(old_k_banner, new_k_banner + "\n" + old_k_banner)

with open(k_path, "w", encoding="utf-8") as f:
    f.write(k)

with open(k_path, "r", encoding="utf-8") as f:
    v = f.read()
for check in ["version: 1.59", "# KAIZEN — v1.59", "Current: **v1.59**", "VERIFY-FACT-1"]:
    assert check in v, f"Failed: {check}"
print("[OK] kaizen v1.59")

# =============================================================================
# 4. SYNC TO GIT
# =============================================================================
print("\n=== GIT SYNC ===")
import subprocess

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

print("\n=== ALL DONE ===")
print("qnfo-core: v1.16 → v1.17 — VERIFY-FACT-1")
print("research: v2.84 → v2.85 — VERIFY-FACT-1")
print("kaizen: v1.58 → v1.59 — VERIFY-FACT-1")
