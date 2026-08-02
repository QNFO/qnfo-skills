# ============================================================
# DEPRECATED (2026-08-02) — PowerShell is RETIRED from QNFO operations
# ============================================================
# PowerShell has been deprecated across all skills and removed from the
# toolchain. Agent operations are PYTHON-FIRST only (windows-command-patterns
# v2.4+ mandates Python/Node; PowerShell is a HARD BLOCK for Cloudflare ops
# per cloudflare skill KIF-59).
#
# Windows PowerShell 5.1 (powershell.exe) remains only because it is a
# Windows system component and the DeepChat agent exec runtime — it cannot
# be uninstalled. PowerShell 7 (pwsh) HAS been uninstalled.
#
# DO NOT use this file in new workflows. Prefer the Python equivalent
# (see the parent skill's scripts/*.py).
# ============================================================
