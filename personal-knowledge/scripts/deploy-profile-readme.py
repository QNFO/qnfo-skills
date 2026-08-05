#!/usr/bin/env python3
"""
deploy-profile-readme.py — Canonical GitHub profile README deployment script.

THIN-CLIENT CANONICAL ASSET (git-github v2.17 protocol):
  - PRIMARY canonical:  QNFO/qnfo-skills:personal-knowledge/scripts/deploy-profile-readme.py
  - SECONDARY durable:  R2 deepchat bucket via skill-sync.js
  - Runtime view:       .deepchat\\skills\\personal-knowledge\\scripts\\ (re-hydrated from git/R2)
  - NEVER save copies to Desktop/Documents/Program Files. Temp clones are deleted in finally.

Usage:
  python deploy-profile-readme.py --src <path-to-README.md> [--repo rwnq8/rwnq8] [--branch main] [--commit-msg "ACTION:..."]

What it does (all in ONE turn — TEMP volatility mandate, git-github v2.16):
  1. Clone {repo} to %TEMP% (volatile — one-turn only)
  2. Copy --src over README.md
  3. Set git identity (fresh-clone gate)
  4. Commit with -F (NEVER -m on cmd.exe — GIT-COMMIT-M-QUOTE-1)
  5. Push origin {branch}
  6. Verify via git ls-remote (Anti-Phantom Gate)
  7. Verify profile page serves the README (curl | grep profile-readme)
  8. If profile NOT serving: print SHARE-TO-PROFILE-REQUIRED instruction
     (CLI-created repos are NOT auto-promoted — personal-knowledge v1.2,
      GITHUB-CDN-PROPAGATION-1 revised 2026-08-05)
  9. Delete temp clone (finally block)

Dependencies: Python 3 stdlib only. Requires: git, curl (for --verify-profile).
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

GIT_IDENTITY_EMAIL = "rowan@qnfo.org"
GIT_IDENTITY_NAME = "Rowan Brad Quni-Gudzinas"
DEFAULT_REPO = "rwnq8/rwnq8"
DEFAULT_BRANCH = "main"
DEFAULT_SRC = r"C:\Users\LENOVO\AppData\Local\Temp\resume-build\rwnq8-README.md"


def run(cmd, cwd=None, check=True, timeout=120):
    """Run a subprocess; print stdout/stderr on failure; raise on non-zero."""
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout)
    if check and r.returncode != 0:
        print(f"  FAILED: {' '.join(cmd)}")
        print(f"  stdout: {r.stdout[-2000:]}")
        print(f"  stderr: {r.stderr[-2000:]}")
        sys.exit(r.returncode)
    return r


def main():
    ap = argparse.ArgumentParser(description="Deploy a GitHub profile README (canonical script)")
    ap.add_argument("--src", default=DEFAULT_SRC, help="Source README.md path")
    ap.add_argument("--repo", default=DEFAULT_REPO, help="Target repo owner/name (default rwnq8/rwnq8)")
    ap.add_argument("--branch", default=DEFAULT_BRANCH, help="Target branch (default main)")
    ap.add_argument("--commit-msg", default=None, help="Commit message (written to file, committed with -F)")
    ap.add_argument("--skip-profile-verify", action="store_true", help="Skip the curl profile check")
    args = ap.parse_args()

    src = os.path.abspath(args.src)
    if not os.path.exists(src):
        print(f"[FATAL] Source README not found: {src}")
        sys.exit(2)

    workdir = os.path.join(tempfile.gettempdir(), f"{args.repo.split('/')[-1]}-deploy-{uuid.uuid4().hex[:8]}")
    commit_msg_file = os.path.join(tempfile.gettempdir(), f"commit-msg-{uuid.uuid4().hex[:8]}.txt")
    repo_url = f"https://github.com/{args.repo}.git"
    profile_url = f"https://github.com/{args.repo.split('/')[0]}"

    try:
        # 0. Pre-clean any leftover (CLONE-LEFTOVER-1)
        shutil.rmtree(workdir, ignore_errors=True)

        # 1. Clone
        print(f"[1/8] Cloning {args.repo} -> {workdir}")
        run(["git", "clone", repo_url, workdir])

        # 2. Fresh-clone identity gate (git-github v2.14)
        print("[2/8] Setting git identity")
        run(["git", "config", "user.email", GIT_IDENTITY_EMAIL], cwd=workdir)
        run(["git", "config", "user.name", GIT_IDENTITY_NAME], cwd=workdir)

        # 3. Copy README
        print(f"[3/8] Copying {src} -> README.md")
        shutil.copy2(src, os.path.join(workdir, "README.md"))

        # 4. Commit message via file (GIT-COMMIT-M-QUOTE-1: never -m with special chars)
        msg = args.commit_msg or (
            "ACTION:EDIT FILE: README.md RATIONALE: Update GitHub profile landing page "
            f"({args.repo})"
        )
        with open(commit_msg_file, "w", encoding="utf-8") as f:
            f.write(msg)
        print("[4/8] Staging + committing (commit -F)")
        run(["git", "add", "README.md"], cwd=workdir)
        run(["git", "commit", "-F", commit_msg_file], cwd=workdir)

        # 5. Push
        print(f"[5/8] Pushing origin {args.branch}")
        run(["git", "push", "origin", args.branch], cwd=workdir)

        # 6. Verify remote (Anti-Phantom Gate)
        print("[6/8] Verifying remote ref")
        r = run(["git", "ls-remote", "origin", f"refs/heads/{args.branch}"], cwd=workdir)
        print(f"  REMOTE: {r.stdout.strip()}")

        # 7. Profile-page verification (curl raw HTML — server-side truth)
        if not args.skip_profile_verify:
            print("[7/8] Verifying profile page serves README (curl)")
            time.sleep(2)
            r = run(["curl", "-s", "-L", "-H",
                     "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                     profile_url], check=False, timeout=60)
            html = r.stdout
            if "profile-readme" in html and "markdown-body" in html:
                print(f"  PROFILE OK: README serving at {profile_url}")
            else:
                print("  " + "=" * 70)
                print("  SHARE-TO-PROFILE-REQUIRED: README pushed but NOT yet on profile page.")
                print(f"  Open {args.repo} in a logged-in browser and click 'Share to Profile'.")
                print("  (CLI-created profile repos are NOT auto-promoted — personal-knowledge v1.2,")
                print("   GITHUB-CDN-PROPAGATION-1 revised 2026-08-05; waiting/force-push do NOT help)")
                print("  " + "=" * 70)
        else:
            print("[7/8] Skipping profile verification (--skip-profile-verify)")

        print("[8/8] Deploy complete")
    finally:
        # 9. Cleanup (TEMP volatility — always delete, even on failure)
        os.chdir(tempfile.gettempdir())
        shutil.rmtree(workdir, ignore_errors=True)
        if os.path.exists(commit_msg_file):
            os.remove(commit_msg_file)
        print("[cleanup] Temp clone + commit-msg file removed")


if __name__ == "__main__":
    main()
