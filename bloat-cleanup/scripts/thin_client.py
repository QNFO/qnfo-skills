#!/usr/bin/env python3
"""Enforce DeepChat thin-client mandate (KIF-32 + KIF-48 compliance).

KIF-32: No local project files or archives in .deepchat, AppData, or anywhere
         in the local file system. Staging files locally with intent to sync
         is hoarding.
KIF-48: .deepchat root directory and file hygiene. Only operational directories
         and files permitted in .deepchat root. No orphan zip/archive files in
         AppData/Roaming. No project artifacts masquerading as operational files.

Rules:
- No project files/archives in .deepchat (KIF-32)
- No project files in AppData, Desktop, Documents, or system root (KIF-32)
- .deepchat root contains ONLY operational dirs/files (KIF-48)
- No orphan .zip/.7z/.rar/.tar archives in AppData/Roaming (KIF-48)
- Session offload files older than current session may be cleaned
- Staging files locally with intent to sync is hoarding
"""
import os, shutil, sys, subprocess
from datetime import datetime

# KIF-48: Operational directories allowed in .deepchat root
OPERATIONAL_DIRS = {
    ".git", ".wrangler", "skills", "sessions", "keys",
    "backups", "audit", "admin_queue", "scripts", "tmp"
}

# KIF-48: Operational files allowed in .deepchat root
OPERATIONAL_FILES = {
    ".gitignore", ".gitmodules", "keys.json",
    "verify_skills.ps1", "admin_watcher.ps1",
    "config.json", "package.json", "pnpm-lock.yaml",
    "CNAME", "README.md"
}

# KIF-48: Project file extensions that should NEVER be in .deepchat root
PROJECT_EXTENSIONS = {".js", ".ts", ".py", ".rs", ".go", ".java", ".c", ".cpp",
                      ".jsonc", ".yaml", ".yml", ".toml", ".reg", ".env",
                      ".worker.js", ".wrangler"}

# KIF-48: Orphan archive extensions to check in AppData
ORPHAN_ARCHIVE_EXTS = {".zip", ".7z", ".rar", ".tar", ".tar.gz", ".tgz"}


def dir_size(path):
    if not os.path.exists(path): return 0, 0
    total, fc = 0, 0
    try:
        for r, _, fs in os.walk(path):
            for f in fs:
                try: total += os.path.getsize(os.path.join(r, f)); fc += 1
                except: pass
    except: return 0, 0
    return total, fc

def is_git_repo(path):
    return os.path.exists(os.path.join(path, ".git"))

def main(clean=False):
    user = os.environ["USERPROFILE"]
    deepchat = os.path.join(user, ".deepchat")
    violations = []
    cleanable_sessions = []
    
    print("=== THIN-CLIENT COMPLIANCE AUDIT (KIF-32 + KIF-48) ===")
    
    # ============================================================
    # KIF-48: .deepchat ROOT HYGIENE — directories
    # ============================================================
    print("\n--- KIF-48: .deepchat Root Directory Hygiene ---")
    root_dirs = [d for d in os.listdir(deepchat)
                 if os.path.isdir(os.path.join(deepchat, d))]
    rogue_dirs = []
    for d in sorted(root_dirs):
        if d.startswith("tmp-") and not d == "tmp":
            rogue_dirs.append(d)
            sz, fc = dir_size(os.path.join(deepchat, d))
            print(f"  ⚡ TEMP DIR: {d:<30} {sz/1048576:>6.1f} MB  {fc} files")
            violations.append({
                "path": d + "/", "full_path": os.path.join(deepchat, d),
                "size_mb": round(sz/1048576, 1), "status": "KIF-48_TEMP_DIR"
            })
        elif d not in OPERATIONAL_DIRS:
            rogue_dirs.append(d)
            sz, fc = dir_size(os.path.join(deepchat, d))
            git = is_git_repo(os.path.join(deepchat, d))
            print(f"  ⚡ ROGUE DIR: {d:<28} {sz/1048576:>6.1f} MB  git={git}  {fc} files")
            violations.append({
                "path": d + "/", "full_path": os.path.join(deepchat, d),
                "size_mb": round(sz/1048576, 1), "has_git": git,
                "status": "KIF-48_ROGUE_DIR"
            })
        else:
            sz, _ = dir_size(os.path.join(deepchat, d))
            print(f"  ✓  {d:<30} operational  ({sz/1048576:.1f} MB)")
    
    # ============================================================
    # KIF-48: .deepchat ROOT HYGIENE — files
    # ============================================================
    print("\n--- KIF-48: .deepchat Root File Hygiene ---")
    root_files = [f for f in os.listdir(deepchat)
                  if os.path.isfile(os.path.join(deepchat, f))]
    rogue_files = []
    for f in sorted(root_files):
        fp = os.path.join(deepchat, f)
        sz = os.path.getsize(fp)
        
        # Allow operational files
        if f in OPERATIONAL_FILES:
            print(f"  ✓  {f:<35} operational  ({sz/1024:.1f} KB)")
            continue
        
        # Allow temp script files (tmp-*.ps1) — flagged but not violations
        if f.startswith("tmp-") and f.endswith(".ps1"):
            print(f"  ⚠  {f:<35} temp script  ({sz/1024:.1f} KB) — clean after use")
            continue
        
        # Check for project file extensions
        ext = os.path.splitext(f)[1].lower()
        if ext in PROJECT_EXTENSIONS or any(f.endswith(pe) for pe in PROJECT_EXTENSIONS):
            rogue_files.append(f)
            print(f"  ⚡ PROJECT FILE: {f:<28} {sz/1024:.1f} KB  (ext={ext})")
            violations.append({
                "path": f, "full_path": fp,
                "size_mb": round(sz/1048576, 1),
                "status": "KIF-48_PROJECT_FILE"
            })
        else:
            # Unknown file type — flag for review
            rogue_files.append(f)
            print(f"  ⚡ UNKNOWN FILE: {f:<27} {sz/1024:.1f} KB")
            violations.append({
                "path": f, "full_path": fp,
                "size_mb": round(sz/1048576, 1),
                "status": "KIF-48_UNKNOWN_FILE"
            })
    
    # ============================================================
    # KIF-48: Orphan archives in AppData\Roaming
    # ============================================================
    print("\n--- KIF-48: Orphan Archive Scan (AppData\\Roaming) ---")
    roaming = os.path.join(user, "AppData", "Roaming")
    local_appdata = os.path.join(user, "AppData", "Local")
    for label, scan_path in [("Roaming", roaming), ("Local", local_appdata)]:
        if not os.path.exists(scan_path):
            continue
        try:
            for f in os.listdir(scan_path):
                fp = os.path.join(scan_path, f)
                if not os.path.isfile(fp):
                    continue
                ext_lower = f.lower()
                if any(ext_lower.endswith(ext) for ext in ORPHAN_ARCHIVE_EXTS):
                    sz = os.path.getsize(fp)
                    if sz > 10 * 1048576:  # Only flag archives > 10 MB
                        age = (datetime.now().timestamp() - os.path.getmtime(fp)) / 86400
                        print(f"  ⚡ ORPHAN ARCHIVE: {label}\\{f:<40} {sz/1048576:>7.1f} MB  ({age:.0f}d old)")
                        violations.append({
                            "path": f"{label}\\{f}", "full_path": fp,
                            "size_mb": round(sz/1048576, 1),
                            "age_days": round(age, 0),
                            "status": "KIF-48_ORPHAN_ARCHIVE"
                        })
        except Exception as e:
            print(f"  (scan error for {label}: {e})")
    
    # ============================================================
    # KIF-32: .deepchat/projects
    # ============================================================
    print("\n--- KIF-32: .deepchat/projects/ ---")
    projects_dir = os.path.join(deepchat, "projects")
    if os.path.exists(projects_dir):
        for d in os.listdir(projects_dir):
            dp = os.path.join(projects_dir, d)
            if os.path.isdir(dp):
                sz, fc = dir_size(dp)
                git = is_git_repo(dp)
                
                pushed = False
                if git:
                    try:
                        r = subprocess.run(["git", "-C", dp, "log", "--branches", "--not", "--remotes", "--oneline"],
                                          capture_output=True, text=True, timeout=10, cwd=dp)
                        pushed = not r.stdout.strip()
                    except:
                        pushed = "unknown"
                
                status = "UNPUSHED" if git and not pushed else ("PUSHED" if pushed else "NO_GIT")
                
                violations.append({
                    "path": d,
                    "full_path": dp,
                    "size_mb": round(sz/1048576, 1),
                    "has_git": git,
                    "pushed": pushed,
                    "status": status
                })
                
                icon = "⚡" if not pushed else "  "
                print(f"  {icon} .deepchat/projects/{d:<35} {sz/1048576:>6.1f} MB  git={git}  {status}")
    else:
        print(f"  ✓  projects/ directory not present — clean")
    
    # ============================================================
    # KIF-32: .deepchat/archive
    # ============================================================
    print("\n--- KIF-32: .deepchat/archive/ ---")
    archive_dir = os.path.join(deepchat, "archive")
    if os.path.exists(archive_dir):
        sz, fc = dir_size(archive_dir)
        if sz > 0:
            violations.append({
                "path": "archive/",
                "full_path": archive_dir,
                "size_mb": round(sz/1048576, 1),
                "has_git": False,
                "pushed": False,
                "status": "ARCHIVE_VIOLATION"
            })
            print(f"  ⚡ .deepchat/archive/  {sz/1048576:.1f} MB  (VIOLATION)")
        else:
            print(f"  ✓  archive/ is empty")
    else:
        print(f"  ✓  archive/ directory not present")
    
    # ============================================================
    # KIF-32: Desktop/Documents project detection
    # ============================================================
    print("\n--- KIF-32: Desktop/Documents Project Scan ---")
    for label, path in [("Desktop", os.path.join(user, "Desktop")),
                        ("Documents", os.path.join(user, "Documents"))]:
        if not os.path.exists(path):
            continue
        found = 0
        for d in os.listdir(path):
            dp = os.path.join(path, d)
            if os.path.isdir(dp):
                git = is_git_repo(dp)
                if git or any(kw in d.lower() for kw in ['.git', 'node_modules', 'src', 'research', 'paper']):
                    sz, fc = dir_size(dp)
                    if sz > 0.5 * 1048576:
                        print(f"  ⚡ {label}/{d}  {sz/1048576:.1f} MB  (potential project, git={git})")
                        found += 1
        if found == 0:
            print(f"  ✓  {label}: clean")
    
    # ============================================================
    # Session offload files
    # ============================================================
    sessions_dir = os.path.join(deepchat, "sessions")
    if os.path.exists(sessions_dir):
        try:
            current = None
            sessions = []
            for d in os.listdir(sessions_dir):
                dp = os.path.join(sessions_dir, d)
                if os.path.isdir(dp):
                    sz, fc = dir_size(dp)
                    mtime = os.path.getmtime(dp)
                    sessions.append((d, sz, fc, mtime, dp))
            
            sessions.sort(key=lambda x: x[3], reverse=True)
            if sessions:
                current = sessions[0][0]
            
            old_count = 0
            old_size = 0
            for sid, sz, fc, mtime, dp in sessions:
                if sid != current:
                    age_days = (datetime.now().timestamp() - mtime) / 86400
                    old_count += 1
                    old_size += sz
                    cleanable_sessions.append({"id": sid, "size_mb": round(sz/1048576, 1), "age_days": round(age_days, 1)})
            
            if old_count > 0:
                print(f"\n  Session offload files: {old_count} old sessions, {old_size/1048576:.1f} MB (current: {current})")
        except Exception as e:
            print(f"  Session audit error: {e}")
    
    # ============================================================
    # Clean if requested
    # ============================================================
    if clean and cleanable_sessions:
        print(f"\n=== CLEANING OLD SESSION DIRECTORIES ===")
        for s in cleanable_sessions:
            session_path = os.path.join(sessions_dir, s["id"])
            try:
                shutil.rmtree(session_path, ignore_errors=True)
                print(f"  DELETED: {s['id']} ({s['size_mb']} MB, {s['age_days']:.0f}d old)")
            except Exception as e:
                print(f"  ERROR: {s['id']} - {e}")
    
    # ============================================================
    # Summary
    # ============================================================
    print(f"\n=== THIN-CLIENT SUMMARY (KIF-32 + KIF-48) ===")
    critical = [v for v in violations if v["status"] in (
        "UNPUSHED", "ARCHIVE_VIOLATION", "NO_GIT",
        "KIF-48_ROGUE_DIR", "KIF-48_PROJECT_FILE", "KIF-48_ORPHAN_ARCHIVE"
    )]
    if critical:
        print(f"  ⚡ {len(critical)} CRITICAL violation(s):")
        for v in critical:
            print(f"    - {v['path']}: {v['size_mb']} MB ({v['status']})")
    else:
        print(f"  ✓  No thin-client violations (KIF-32 + KIF-48 clean)")
    
    if rogue_dirs:
        print(f"\n  KIF-48 rogue dirs present: {len(rogue_dirs)}")
        print(f"  Fix: verify they are project artifacts, push to GitHub, delete locally")
    if rogue_files:
        print(f"\n  KIF-48 rogue files present: {len(rogue_files)}")
        print(f"  Fix: remove project files from .deepchat root")
    
    return violations, cleanable_sessions

if __name__ == "__main__":
    do_clean = "--clean" in sys.argv
    main(clean=do_clean)
