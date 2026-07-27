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
```powershell
cd $env:USERPROFILE\.deepchat\skills
Test-Path .git                          # Should be True
git remote -v                           # Should show origin + rwnq8
git status --short                      # Should be empty
git fetch --all
git log -1 --oneline                    # Note HEAD commit
git log -1 --oneline origin/master      # Should match
git log -1 --oneline rwnq8/master       # Should match
```

---

## 2. Stale Location Detection

**Known stale paths to check:**

| Path | Expected State |
|:-----|:---------------|
| `%APPDATA%\.deepchat\skills\` | **MUST NOT EXIST** |
| `%APPDATA%\DeepChat\skills\` | **MUST BE EMPTY** |
| `%LOCALAPPDATA%\DeepChat\skills\` | **MUST NOT EXIST** |

**Commands:**
```powershell
Test-Path "$env:APPDATA\.deepchat\skills"        # Should be False
Test-Path "$env:APPDATA\DeepChat\skills"         # Should be False or empty
Test-Path "$env:LOCALAPPDATA\DeepChat\skills"    # Should be False
```

**If stale locations exist:**
1. Check for version conflicts (compare SKILL.md versions)
2. Merge any valuable changes to canonical location
3. Delete stale directory: `Remove-Item -Recurse -Force <path>`

---

## 3. Skill Count Verification

| Layer | Expected Count | Command |
|:------|:---------------|:--------|
| Local disk | 24+ | `(Get-ChildItem $env:USERPROFILE\.deepchat\skills -Directory \| Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") }).Count` |
| GitHub (origin) | Same as local | `git ls-tree --name-only origin/master \| Measure-Object` |
| GitHub (rwnq8) | Same as local | `git ls-tree --name-only rwnq8/master \| Measure-Object` |
| R2 backup | Same as local | `npx wrangler r2 object list qnfo-skills --prefix=prompts/skills/ --remote \| Select-String "SKILL.md" \| Measure-Object` |

---

## 4. Supplemental Files Audit

Skills are NOT just SKILL.md — they include scripts, references, templates, and assets.

**Check supplemental file counts:**
```powershell
Get-ChildItem -Path "$env:USERPROFILE\.deepchat\skills" -Recurse -File |
  Where-Object { $_.Name -ne "SKILL.md" -and $_.FullName -notmatch "\\.git\\" } |
  Measure-Object
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

1. **Compare versions:**
   ```powershell
   Get-Content "<canonical>\<skill>\SKILL.md" | Select-String "version:"
   Get-Content "<stale>\<skill>\SKILL.md" | Select-String "version:"
   ```

2. **Compare content:**
   ```powershell
   Compare-Object (Get-Content "<canonical>\<skill>\SKILL.md") (Get-Content "<stale>\<skill>\SKILL.md")
   ```

3. **Resolution rules:**
   - Higher version number wins
   - If versions equal, canonical location wins
   - If stale has valuable changes, merge to canonical first, then delete stale

---

## 6. R2 Backup Verification

**Full sync command:**
```powershell
node "$env:USERPROFILE\.deepchat\skills\system\scripts\skill-sync.js"
```

**Manual verification:**
```powershell
# List all R2 skill objects
npx wrangler r2 object list qnfo-skills --prefix=prompts/skills/ --remote

# Verify specific skill content
npx wrangler r2 object get qnfo-skills prompts/skills/qnfo-agent/SKILL.md --remote --file=- | Select-String "version:"
```

---

## 7. Automated Audit Script

**Run the hygiene audit:**
```powershell
node "$env:USERPROFILE\.deepchat\skills\system\scripts\skill-hygiene.js"
```

**Exit codes:**
- `0` = All clean
- `1` = Stale locations found (cleanup needed)
- `2` = Version conflicts (manual resolution needed)
- `3` = Script error

**JSON report:** `%USERPROFILE%\.deepchat\audit\skill-hygiene-latest.json`

---

## 8. DeepChat Startup Integration

**Option A: Windows Task Scheduler (Recommended)**

Create a scheduled task that runs on user logon:
```powershell
$action = New-ScheduledTaskAction -Execute "node" -Argument "$env:USERPROFILE\.deepchat\skills\system\scripts\skill-hygiene.js"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
Register-ScheduledTask -TaskName "DeepChat-SkillHygiene" -Action $action -Trigger $trigger -Principal $principal -Description "Audit skill locations on startup"
```

**Option B: DeepChat Plugin (Future)**

If DeepChat adds plugin lifecycle hooks, register `skill-hygiene.js` as an `onStartup` handler.

**Option C: Manual Pre-Session Check**

At the start of any session involving skill modifications:
```
node $env:USERPROFILE\.deepchat\skills\system\scripts\skill-hygiene.js
```

---

## 9. Enforcement Gates

### Gate 1: Pre-Sync Gate
Before any `git push` or R2 upload:
- [ ] `skill-hygiene.js` exits with code 0
- [ ] No uncommitted changes in canonical directory
- [ ] All remotes fetched and in sync

### Gate 2: Post-Sync Verification
After any skill deployment:
- [ ] Local file exists
- [ ] GitHub commit visible
- [ ] R2 object readable with matching content

### Gate 3: Session Start Gate
At the start of any skill-related session:
- [ ] No stale locations exist
- [ ] Canonical location is git-clean
- [ ] Last audit < 24 hours old

---

## 10. Anti-Patterns

| Anti-Pattern | Detection | Fix |
|:-------------|:----------|:----|
| Duplicate skill directories | `skill-hygiene.js` exit code 1 | Delete stale locations |
| SKILL.md-only sync | R2 missing scripts/templates | Use `skill-sync.js` which syncs ALL files |
| Manual token copy | Truncated tokens cause auth failures | Always use `$env:TOKEN_NAME` directly |
| Editing skills in stale location | Changes lost on next sync | Only edit in canonical location |
| Forgetting rwnq8 remote | Mirror out of sync | `git push rwnq8 master` after every push |

---

*skill-locations-audit.md v1.0 — 2026-07-26*
