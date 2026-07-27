#!/usr/bin/env python3
"""Dynamic runtime service analysis — discovers ALL services and classifies
them by heuristic rules (no fixed list). Read-only; no admin required.

Output: structured JSON-style report with per-service classification,
risk level, and rationale. Designed as the intelligence layer for
dynamic_disable.py.

v1.0 — 2026-07-27 KAIZEN: replaces hardcoded BLOAT_SERVICES list with
runtime heuristic classification. KIF-40 (dynamic service audit)."""

import json, os, subprocess, sys
from collections import OrderedDict

# ── CLASSIFICATION RULES ────────────────────────────────────────────────

# CRITICAL: Services that must NEVER be disabled — doing so risks
# unbootable system, network loss, or security compromise.
CRITICAL_OS_SERVICES = {
    "RpcSs", "RpcLocator", "RpcEptMapper", "DcomLaunch",
    "SamSs", "LSM", "EventLog", "EventSystem",
    "PlugPlay", "Power", "Schedule", "BFE", "MpsSvc",
    "WinDefend", "WdNisSvc", "SecurityHealthService",
    "wuauserv", "CryptSvc", "KeyIso", "VaultSvc",
    "LanmanWorkstation", "LanmanServer", "netprofm", "NlaSvc",
    "DHCP", "DNScache", "lmhosts", "W32Time",
    "TrustedInstaller", "msiserver", "gpsvc", "iphlpsvc",
    "Winmgmt", "spoolsv", "ShellHWDetection",
    "Dnscache", "Tcpip", "Netman", "Nsi", "NdisVirtualBus",
    "Wcmsvc", "WinHttpAutoProxySvc", "BrokerInfrastructure",
    "CoreMessagingRegistrar", "StateRepository", "TileDataModelSvc",
    "UserManager", "ProfSvc", "SENS", "Themes",
    "AudioSrv", "AudioEndpointBuilder", "DeviceInstall",
    "DisplayEnhancementService", "DPS", "WdiServiceHost", "WdiSystemHost",
    "StorSvc", "SysMain",
    "FontCache3.0.0.0",
    # KIF-40 kaizen additions -- core Windows services with non-obvious display names:
    "WlanSvc",                # WLAN AutoConfig
    "wscsvc",                 # Security Center
    "TrkWks",                 # Distributed Link Tracking Client
    "SystemEventsBroker",     # System Events Broker
    "DispBrokerDesktopSvc",   # Display Policy Service
    "camsvc",                 # Capability Access Manager
    "TextInputManagementService",  # Text Input Management
    "cbdhsvc",                # Clipboard User Service (prefix match)
    "UsoSvc",                 # Update Orchestrator Service
    "Dhcp",                   # DHCP Client (lowercase variant)
    "nsi",                    # Network Store Interface (lowercase variant)
}

# HIGH-CONFIDENCE BLOAT: Vendor bloatware, telemetry, ad-platform services
# that are safe to disable if the user doesn't need the feature.
BLOAT_PATTERNS = {
    # ── Vendor bloat ──
    "lenovo": "vendor:Lenovo",
    "dolby": "vendor:Dolby",
    "elevoc": "vendor:Elevoc",

    # ── Windows Search / Indexing (heavy I/O, rarely needed with SSD) ──
    "wsearch": "service:Windows Search indexing (heavy disk I/O)",
    "searchindexer": "service:Search indexer",
    "searchhost": "service:Search host",

    # ── Telemetry & Data Collection ──
    "diagtrack": "service:Telemetry (Connected User Experiences)",
    "dusmsvc": "service:Data Usage collection",
    "wpnservice": "service:Push notifications",
    "wpnuser": "service:Push notifications (user)",

    # ── Connected Devices / Phone Link ──
    "cdpsvc": "service:Connected Devices Platform (Phone Link)",
    "cdpuser": "service:CDP User Service",

    # ── Program Compatibility ──
    "pcasvc": "service:Program Compatibility Assistant",

    # ── Windows Image Acquisition (scanners, cameras) ──
    "stisvc": "service:Windows Image Acquisition (scanners/cameras)",

    # ── Font Cache (redundant with FontCache3.0.0.0) ──
    "fontcache": "service:Font cache (legacy)",

    # ── Office Click-to-Run ──
    "clicktorunsvc": "service:Office Click-to-Run",
    "clicktorun": "vendor:Office-ClickToRun",
    "sdxhelper": "vendor:Office-SDX",

    # ── Xbox / Game Bar ──
    "xbox": "service:Xbox/Game Bar",
    "xbl": "service:Xbox Live",

    # ── OneDrive (if user doesn't use) ──
    "onedrive": "service:OneDrive sync",

    # ── Adobe background updaters ──
    "adobeupdate": "vendor:Adobe auto-update",
    "adobearmservice": "vendor:Adobe ARM",
    "adobe_acrobat_update": "vendor:Adobe update",
    "agsservice": "vendor:Adobe Genuine Software",

    # ── Google updaters ──
    "googleupdate": "vendor:Google auto-update",
    "googleupdater": "vendor:Google updater",
    "gupdate": "vendor:Google updater",
    "gupdatem": "vendor:Google updater",

    # ── Other known bloat ──
    "pc manager": "vendor:Lenovo PC Manager",
    "mspcmanagerservice": "vendor:Lenovo PC Manager",
}

# SUSPICIOUS: Third-party services that auto-start but aren't obviously
# essential. These are flagged for user review before disabling.
SUSPICIOUS_PATTERNS = {
    "update": "auto-updater (third-party)",
    "updater": "auto-updater (third-party)",
    "helper": "helper service (third-party, auto-start)",
    "sync": "sync service (third-party)",
    "cloud": "cloud sync service",
    "telemetry": "telemetry (third-party)",
}

# USER-INSTALLED / KNOWN: Common services from legitimate user-installed
# software. Flagged but not auto-targeted — user decides.
USER_SOFTWARE_PATTERNS = {
    "mysql": "database",
    "mariadb": "database",
    "postgresql": "database",
    "mongodb": "database",
    "redis": "cache",
    "docker": "container",
    "nginx": "web server",
    "apache": "web server",
    "node.js": "runtime",
    "steam": "gaming platform",
    "discord": "chat",
    "slack": "chat",
    "teams": "collaboration",
    "zoom": "video conference",
    "tailscale": "VPN",
    "wireguard": "VPN",
    "openvpn": "VPN",
    "zerotier": "VPN",
    "virtualbox": "virtualization",
    "vmware": "virtualization",
    "dropbox": "cloud storage",
    "epicgames": "gaming platform",
    "battlenet": "gaming platform",
    "origin": "gaming platform",
    "ea": "gaming platform",
    "ubisoft": "gaming platform",
    "gog": "gaming platform",
}


def query_all_services():
    """Query all services via Get-CimInstance Win32_Service.
    Returns list of dicts with Name, DisplayName, State, StartMode, ProcessId."""
    ps_cmd = (
        "Get-CimInstance Win32_Service | "
        "Select-Object Name, DisplayName, State, StartMode, ProcessId | "
        "ConvertTo-Json -Compress"
    )
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True, encoding="utf-8", errors="replace",
            timeout=30
        )
        if r.returncode != 0:
            print(f"ERROR: PowerShell failed: {r.stderr}", file=sys.stderr)
            return []
        raw = r.stdout.strip()
        if not raw:
            return []
        data = json.loads(raw)
        # Handle single service (dict) vs list
        if isinstance(data, dict):
            data = [data]
        return data
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON parse failed: {e}", file=sys.stderr)
        print(f"Raw output (first 500 chars): {r.stdout[:500]}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return []


def _match_pattern(pattern, combined, name_lower):
    """Match a pattern against service name + display name.
    Short patterns (<=3 chars) require word boundary to avoid false positives
    (e.g., 'ea' matching inside 'deviceassociation', 'webthreatdef')."""
    if len(pattern) > 3:
        return pattern in combined
    # Short pattern: require word boundary (space, underscore, or start/end)
    import re
    # Check if pattern appears at start of name, or with word boundary
    if name_lower.startswith(pattern):
        return True
    if re.search(rf'\b{re.escape(pattern)}', combined):
        return True
    return False


def classify_service(svc):
    """Classify a service as essential/bloat/suspicious/user_installed/unknown.
    Returns (classification, reason_string)."""
    name = (svc.get("Name") or "").strip()
    display = (svc.get("DisplayName") or "").strip()
    start_mode = (svc.get("StartMode") or "").strip()
    state = (svc.get("State") or "").strip()

    name_lower = name.lower()
    display_lower = display.lower()
    combined = f"{name_lower} {display_lower}"

    # ── Rule 0: CRITICAL OS — never touch ──
    # Check exact name + prefix match (handles suffixed services like cbdhsvc_6dc3e)
    if name in CRITICAL_OS_SERVICES:
        return "essential", "critical OS service (hardcoded safelist)"
    for critical in CRITICAL_OS_SERVICES:
        if name_lower.startswith(critical.lower()) and len(critical) >= 5:
            return "essential", "critical OS service (prefix match in safelist)"

    # ── Rule 1: Disabled / Stopped + Manual — low priority ──
    if state == "Stopped" and start_mode in ("Manual", "Disabled"):
        # Still check for vendor bloat — even stopped, may be worth flagging
        for pattern, reason in BLOAT_PATTERNS.items():
            if _match_pattern(pattern, combined, name_lower):
                return "bloat_stopped", f"{reason} (currently stopped/{start_mode})"
        return "inactive", f"stopped + {start_mode} (dormant)"

    # ── Rule 2: Vendor bloat (Lenovo, Dolby, Elevoc) — high confidence ──
    for pattern, reason in BLOAT_PATTERNS.items():
        if _match_pattern(pattern, combined, name_lower):
            return "bloat", reason

    # ── Rule 3: Windows core patterns that are essential ──
    # Most Windows-owned services with "Windows" in display name and Auto start
    # are essential — but only if they don't match bloat patterns above
    if "windows " in display_lower or display_lower.startswith("windows"):
        if start_mode == "Auto" and state == "Running":
            return "essential", "Windows core service (auto-start, running)"

    # ── Rule 4: Suspicious patterns (auto-updaters, helpers, sync) ──
    if start_mode == "Auto" and state == "Running":
        for pattern, reason in SUSPICIOUS_PATTERNS.items():
            if _match_pattern(pattern, combined, name_lower):
                return "suspicious", f"{reason} — auto-start, running"

    # ── Rule 5: User-installed software ──
    for pattern, reason in USER_SOFTWARE_PATTERNS.items():
        if _match_pattern(pattern, combined, name_lower):
            return "user_installed", f"{reason} (user-installed software)"

    # ── Rule 6: Auto-start but not in safelist ──
    if start_mode == "Auto" and state == "Running":
        # If display name looks third-party (no "Microsoft" or "Windows")
        if "microsoft" not in display_lower and "windows" not in display_lower:
            return "suspicious", f"third-party auto-start service — review"

    # ── Rule 7: Manual start but running (was triggered) —─
    if state == "Running" and start_mode == "Manual":
        return "unknown", f"running but manual start — investigate"

    # ── Default ──
    return "unknown", "no heuristic match"


def audit():
    """Main audit: query, classify, report."""
    print("=" * 72)
    print("  DYNAMIC SERVICE AUDIT — Runtime Heuristic Classification")
    print("=" * 72)
    print()

    services = query_all_services()
    if not services:
        print("FATAL: Could not query services.", file=sys.stderr)
        return None

    print(f"Discovered {len(services)} services. Classifying...\n")

    results = []
    counts = {}

    for svc in services:
        classification, reason = classify_service(svc)
        entry = OrderedDict([
            ("name", svc.get("Name", "")),
            ("display", svc.get("DisplayName", "")),
            ("state", svc.get("State", "")),
            ("start_mode", svc.get("StartMode", "")),
            ("pid", svc.get("ProcessId", 0)),
            ("classification", classification),
            ("reason", reason),
        ])
        results.append(entry)
        counts[classification] = counts.get(classification, 0) + 1

    # ── Report ──
    print("── Classification Summary ──")
    summary_order = ["essential", "bloat", "bloat_stopped", "suspicious",
                     "user_installed", "inactive", "unknown"]
    for cls in summary_order:
        if cls in counts:
            print(f"  {cls:<22}: {counts[cls]:>4}")

    total_non_essential = sum(v for k, v in counts.items() if k != "essential")
    print(f"  {'───':<22}  {'────'}")
    print(f"  {'total (non-essential)':<22}: {total_non_essential:>4}")
    print()

    # Bloat detail
    bloat_services = [s for s in results if s["classification"] in ("bloat", "bloat_stopped")]
    suspicious_services = [s for s in results if s["classification"] == "suspicious"]
    user_services = [s for s in results if s["classification"] == "user_installed"]

    if bloat_services:
        print("── HIGH-CONFIDENCE BLOAT (safe to disable) ──")
        for s in bloat_services:
            running = "RUNNING" if s["state"] == "Running" else "stopped"
            print(f"  [{running:>7}] {s['name']:<40} {s['reason']}")
        print()

    if suspicious_services:
        print("── SUSPICIOUS (review before disabling) ──")
        for s in suspicious_services:
            running = "RUNNING" if s["state"] == "Running" else "stopped"
            print(f"  [{running:>7}] {s['name']:<40} {s['reason']}")
        print()

    if user_services:
        print("── USER-INSTALLED SOFTWARE (your call) ──")
        for s in user_services:
            running = "RUNNING" if s["state"] == "Running" else "stopped"
            print(f"  [{running:>7}] {s['name']:<40} {s['reason']}")
        print()

    print(f"── ACTIONABLE TARGETS ──")
    actionable_bloat = sum(1 for s in bloat_services if s["state"] == "Running")
    actionable_suspicious = sum(1 for s in suspicious_services if s["state"] == "Running")
    print(f"  Bloat (running, can disable):   {actionable_bloat}")
    print(f"  Suspicious (running, review):    {actionable_suspicious}")
    print(f"  Total actionable (bloat):        {actionable_bloat + actionable_suspicious}")
    print()
    print("To disable bloat-classified services (admin required):")
    print("  skill_run bloat-cleanup scripts/dynamic_disable.py --apply --confirm")
    print()

    return {
        "summary": counts,
        "bloat": bloat_services,
        "suspicious": suspicious_services,
        "user_installed": user_services,
        "all": results,
    }


if __name__ == "__main__":
    audit()
