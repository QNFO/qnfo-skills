#!/usr/bin/env python3
"""email-send-guard.py — SCRIPTED ENFORCEMENT of TEST-SEND-EXTERNAL-1 (email-composer v2.17).

HARD GATE (PROSE-GATE-ADVISORY-1): test/diagnostic emails must NEVER go to real external
recipients. This script machine-checks the recipient allowlist for `--mode test` sends.

Usage:
  python email-send-guard.py --to <recipient> --mode test      # exit 1 on violation
  python email-send-guard.py --to <recipient> --mode send      # real outreach; warning if external
  python email-send-guard.py --check-recipient <addr>          # allowlist lookup only

Exit codes:
  0 = allowed (test recipient is user-owned or internal domain)
  1 = TEST-SEND-EXTERNAL-1 violation (test send to a real external recipient)
  2 = usage error

Canonical case: 2026-08-10 MATRIX E -> tp53@rice.edu (D1 id=66) — a test email to a real
researcher; this guard makes that impossible for --mode test.
"""
import argparse
import sys

# User-owned mailbox — the ONLY external-address allowed for test sends
USER_OWNED_MAILBOXES = {"rwnquni@outlook.com"}

# Internal QNFO/QWAV domains (Email Sending onboarded + owned by the project)
INTERNAL_DOMAINS = {
    "qnfo.org", "qwav.org", "qwav.tech", "qwav.net", "qwav.uk",
    "q-wave.tech", "qwave.tech", "q08.org", "qnfo.net", "qnfo.uk",
    "empoweringchange.today",
}

VIOLATION_MSG = (
    "TEST-SEND-EXTERNAL-1 VIOLATION: test/diagnostic emails may ONLY go to the user's own "
    "mailbox (rwnquni@outlook.com) or internal QNFO/QWAV domains. NEVER to a real external "
    "recipient - even with a \"test\"/\"matrix\" subject it is still a contact, burns the "
    "recipient, and violates the no-repeat-contact mandate. See email-composer v2.17 "
    "TEST-SEND-EXTERNAL-1 + Repair-Send Protocol."
)


def classify(recipient):
    """Return (allowed_for_test: bool, classification: str)."""
    r = recipient.strip().lower()
    if r in USER_OWNED_MAILBOXES:
        return True, "USER-OWNED MAILBOX (test-allowed)"
    if "@" in r and r.split("@")[1] in INTERNAL_DOMAINS:
        return True, "INTERNAL DOMAIN (test-allowed)"
    return False, "EXTERNAL RECIPIENT (test-FORBIDDEN)"


def main():
    ap = argparse.ArgumentParser(description="TEST-SEND-EXTERNAL-1 scripted send-guard")
    ap.add_argument("--to", help="recipient email address")
    ap.add_argument("--mode", choices=["test", "send"], default="test",
                    help="test = enforce allowlist (default); send = real outreach (warning only)")
    ap.add_argument("--check-recipient", dest="check", help="allowlist lookup only")
    args = ap.parse_args()

    target = args.check or args.to
    if not target:
        ap.print_usage()
        return 2

    allowed, classification = classify(target)

    if args.check:
        print("{0}: {1} | test_allowed={2}".format(target, classification, allowed))
        return 0 if allowed else 1

    if args.mode == "test":
        if not allowed:
            print(VIOLATION_MSG, file=sys.stderr)
            print("BLOCKED: {0} ({1})".format(target, classification), file=sys.stderr)
            return 1
        print("ALLOWED (test): {0} ({1})".format(target, classification))
        return 0

    # mode == 'send' (real outreach)
    if not allowed:
        print("WARNING: {0} is an external recipient ({1}). "
              "Verify identity from the arXiv SOURCE tarball (CONNECTION-POINT-UNVERIFIED-1) "
              "and no-repeat-contact count BEFORE sending.".format(target, classification))
        return 0
    print("NOTICE: {0} is internal/user-owned ({1}); send proceeds.".format(target, classification))
    return 0


if __name__ == "__main__":
    sys.exit(main())
