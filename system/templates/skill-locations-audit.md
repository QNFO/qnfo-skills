# Skill Locations Audit Checklist

**Purpose:** Verify skill ecosystem integrity — no duplicates, no conflicts, all layers synced.
**Run:** Before any skill deployment, after DeepChat updates, monthly maintenance.

---

## 1. Canonical Location Verification

**Canonical Path:** `%USERPROFILE%\.deepchat\skills\` (e.g., `C:\Users\LENOVO\.deepchat\skills\`)

- [ ] Directory exists
- [ ] Is a git repository (`.git` present)
- [ ] Remote `origin` = `https://github.com/QNFO/qnfo-skills.git`
- [ ] Remote `rwnq8` = `https://github.com/rwnq8/qnfo-skills.git`
- [ ] Working tree clean (`git status --short` returns empty)
- [ ] Local HEAD matches `origin/master`
- [ ] Local HEAD matches `rwnq8/master`

**Commands:**
```bash
cd %USERPROFILE%\.deepchat\skills
git status --short                      # Should be empty
git remote -v                           # Should show origin + rwnq8
git fetch --all
git log -1 --oneline                    # Note HEAD commit
git log -1 --oneline origin/master      # Should match
git log -1 --oneline rwnq8/master       # Should match
```

Or verify with Python:
```python
import os, subprocess, pathlib

skills_dir = os.path.expandvars(r"%USERPROFILE%\.deepchat\skills")
git_dir = os.path.join(skills_dir, ".git")
print(f".git present: {os.path.isdir(git_dir)}")

result = subprocess.run(["git", "-C", skills_dir, "status", "--short"], capture_output=True, text=True)
print(f"Working tree clean: {result.stdout.strip() == ''}")

result = subprocess.run(["git", "-C", skills_dir, "remote", "-v"], capture_output=True, text=True)
print(result.stdout)
```

---

## 2. Stale Location Detection

**Known stale paths to check:**

| Path | Expected State |
|:-----|:---------------|
| `%APPDATA%\.deepchat\skills\` | **MUST NOT EXIST** |
| `%APPDATA%\DeepChat\skills\` | **MUST BE EMPTY** |
| `%LOCALAPPDATA%\DeepChat\skills\` | **MUST NOT EXIST** |

**Commands (Python):**
```python
import os

for path_var in [r"%APPDATA%\.deepchat\skills", r"%APPDATA%\DeepChat\skills", r"%LOCALAPPDATA%\DeepChat\skills"]:
    full = os.path.expandvars(path_var)
    exists = os.path.exists(full)
    is_empty = exists and len(os.listdir(full)) == 0 if exists else True
    print(f"{path_var}: exists={exists}, empty={is_empty}")
    assert not exists or is_empty, f"STALE: {path_var}"
```

**If stale locations exist:**
1. Check for version conflicts (compare SKILL.md versions)
2. Merge any valuable changes to canonical location
3. Delete stale directory:
```python
import shutil
shutil.rmtree(path)  # Replace `path` with the stale directory
```

---

## 3. Skill Count Verification

| Layer | Expected Count | Command |
|:------|:---------------|:--------|
| Local disk | 24+ | Python: count dirs with SKILL.md in skills root |
| GitHub (origin) | Same as local | `git ls-tree --name-only origin/master` |
| GitHub (rwnq8) | Same as local | `git ls-tree --name-only rwnq8/master` |
| R2 backup | Same as local | `npx wrangler r2 object list ...` |

**Python verification:**
```python
import os

skills_dir = os.path.expandvars(r"%USERPROFILE%\.deepchat\skills")
count = sum(1 for d in os.listdir(skills_dir)
            if os.path.isdir(os.path.join(skills_dir, d))
            and os.path.exists(os.path.join(skills_dir, d, "SKILL.md")))
print(f"Skills on disk: {count}")
assert count >= 24, f"Expected >=24 skills, found {count}"
```

---

## 4. Supplemental Files Audit

Skills are NOT just SKILL.md — they include scripts, references, templates, and assets.

**Check supplemental file counts (Python):**
```python
import os

skills_dir = os.path.expandvars(r"%USERPROFILE%\.deepchat\skills")
count = 0
for root, dirs, files in os.walk(skills_dir):
    if ".git" in root:
        continue
    for f in files:
        if f != "SKILL.md":
            count += 1
print(f"Supplemental files: {count}")
```

**Expected supplemental files by skill:**

| Skill | scripts/ | references/ | templates/ | assets/ |
|:------|:---------|:------------|:-----------|:--------|
| cloudflare | 8 | 2 | 0 | 0 |
| research | 10 | 2 | 15+ | 0 |
| docx | 10+ | 0 | 5+ | 0 |
| pptx | 10+ | 0 | 0 | 0 |
| pdf | 8 | 2 | 0 | 0 |
| system | 4 | 0 | 1 | 0 |

**Sync verification:** All supplemental files must exist on R2 backup, not just SKILL.md.

---

## 5. Version Conflict Resolution

If the same skill exists in multiple locations with different versions:

1. **Compare versions (Python):**
   ```python
   import re

   def get_version(path):
       with open(path, encoding='utf-8') as f:
           for line in f:
               m = re.match(r'version:\s*(.+)', line)
               if m:
                   return m.group(1).strip()
       return None

   v1 = get_version(r"<canonical>\<skill>\SKILL.md")
   v2 = get_version(r"<stale>\<skill>\SKILL.md")
   print(f"Canonical: {v1}, Stale: {v2}")
   ```

2. **Compare content (Python):**
   ```python
   import difflib

   with open("<canonical>\\<skill>\\SKILL.md", encoding='utf-8') as f:
       canonical_lines = f.readlines()
   with open("<stale>\\<skill>\\SKILL.md", encoding='utf-8') as f:
       stale_lines = f.readlines()

   diff = difflib.unified_diff(canonical_lines, stale_lines)
   for line in diff:
       print(line, end='')
   ```

3. **Resolution rules:**
   - Higher version number wins
   - If versions equal, canonical location wins
   - If stale has valuable changes, merge to canonical first, then delete stale

---

## 6. R2 Backup Verification

**Full sync command:**
```bash
node %USERPROFILE%\.deepchat\skills\system\scripts\skill-sync.js
```

**Manual verification (Python):**
```python
import subprocess

# List all R2 skill objects
subprocess.run(["npx", "wrangler", "r2", "object", "list", "qnfo-skills",
                "--prefix=prompts/skills/", "--remote"])

# Verify specific skill content
subprocess.run(["npx", "wrangler", "r2", "object", "get", "qnfo-skills",
                "prompts/skills/qnfo-agent/SKILL.md", "--remote", "--file=-"])
```

---

## 7. Automated Health Check

**Run the full audit in one command:**
```bash
python %USERPROFILE%\.deepchat\skills\system\scripts\skill-audit.py
```

Expected output:
- All directories exist
- No stale locations
- Skill count >= 24 and matches across all layers
- No version conflicts
- R2 backup sync verified
- All checks passed ✓
