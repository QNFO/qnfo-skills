#!/usr/bin/env python3
"""Enforce DeepChat thin-client mandate (KIF-32 compliance).

Rules:
- No project files/archives in .deepchat
- No project files in AppData, Desktop, Documents, or system root
- Session offload files older than current session may be cleaned
- Staging files locally with intent to sync is hoarding
"""
import os, shutil, sys, subprocess
from datetime import datetime

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
    
    print("=== THIN-CLIENT COMPLIANCE AUDIT ===")
    
    # 1. Check .deepchat/projects
    projects_dir = os.path.join(deepchat, "projects")
    if os.path.exists(projects_dir):
        for d in os.listdir(projects_dir):
            dp = os.path.join(projects_dir, d)
            if os.path.isdir(dp):
                sz, fc = dir_size(dp)
                git = is_git_repo(dp)
                
                # Check if pushed to GitHub
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
    
    # 2. Check .deepchat/archive
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
    
    # 3. Check for project-like dirs in Desktop/Documents
    for label, path in [("Desktop", os.path.join(user, "Desktop")),
                        ("Documents", os.path.join(user, "Documents"))]:
        if not os.path.exists(path):
            continue
        for d in os.listdir(path):
            dp = os.path.join(path, d)
            if os.path.isdir(dp):
                git = is_git_repo(dp)
                if git or any(kw in d.lower() for kw in ['.git', 'node_modules', 'src', 'research', 'paper']):
                    sz, fc = dir_size(dp)
                    if sz > 0.5 * 1048576:  # >500 KB
                        print(f"  ⚡ {label}/{d}  {sz/1048576:.1f} MB  (potential project, git={git})")
    
    # 4. Session offload files (keep current session)
    sessions_dir = os.path.join(deepchat, "sessions")
    if os.path.exists(sessions_dir):
        try:
            # Determine current session ID (from env or guess latest)
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
                current = sessions[0][0]  # Most recently modified = current
            
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
    
    # 5. Clean if requested
    if clean and cleanable_sessions:
        print(f"\n=== CLEANING OLD SESSION DIRECTORIES ===")
        for s in cleanable_sessions:
            session_path = os.path.join(sessions_dir, s["id"])
            try:
                shutil.rmtree(session_path, ignore_errors=True)
                print(f"  DELETED: {s['id']} ({s['size_mb']} MB, {s['age_days']:.0f}d old)")
            except Exception as e:
                print(f"  ERROR: {s['id']} - {e}")
    
    # Summary
    print(f"\n=== THIN-CLIENT SUMMARY ===")
    critical = [v for v in violations if v["status"] in ("UNPUSHED", "ARCHIVE_VIOLATION", "NO_GIT")]
    if critical:
        print(f"  ⚡ {len(critical)} CRITICAL violation(s) — projects staged locally")
        for v in critical:
            print(f"    - {v['path']}: {v['size_mb']} MB ({v['status']})")
            print(f"      Fix: push to GitHub + upload to R2, then delete locally")
    else:
        print(f"  ✅ No thin-client violations")
    
    return violations, cleanable_sessions

if __name__ == "__main__":
    do_clean = "--clean" in sys.argv
    main(clean=do_clean)
