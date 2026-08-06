import subprocess, shutil, json, os

# Copy live -> git
live = r"C:\Users\LENOVO\.deepchat\skills\kaizen\SKILL.md"
git = r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills\kaizen\SKILL.md"
shutil.copy2(live, git)

# Git add + commit + push
repo = r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills"
subprocess.run(["git", "-C", repo, "add", "kaizen/SKILL.md"], check=True)
subprocess.run(["git", "-C", repo, "commit", "-m", "feat(kaizen): v1.58 — SKILLS UPDATE ecosystem audit (0 HARD/0 SOFT/0 DESIGN)"], check=True)
subprocess.run(["git", "-C", repo, "push", "origin", "master"], check=True)
print("Git: committed + pushed")

# Update .kaizen_history
hist_path = r"C:\Users\LENOVO\.deepchat\skills\kaizen\.kaizen_history"
try:
    with open(hist_path, "r") as f:
        hist = json.load(f)
except:
    hist = {"skill": "kaizen", "entries": []}

hist["entries"].append({
    "version": "v1.58",
    "date": "2026-08-05",
    "type": "kaizen",
    "red_team_roles": 5,
    "hard_findings": 0,
    "soft_findings": 0,
    "design_findings": 0,
    "watchtower_triggered": False,
    "summary": "SKILLS UPDATE ecosystem audit: 18 QNFO skills N-2 CLEAN, 0 orphans, all cross-refs consistent."
})

with open(hist_path, "w") as f:
    json.dump(hist, f, indent=2)

# Git add dotfile
subprocess.run(["git", "-C", repo, "add", "kaizen/.kaizen_history"], check=True)
subprocess.run(["git", "-C", repo, "commit", "-m", "chore(kaizen): update .kaizen_history for v1.58"], check=True)
subprocess.run(["git", "-C", repo, "push", "origin", "master"], check=True)
print("Git: .kaizen_history committed + pushed")
print("DONE")
