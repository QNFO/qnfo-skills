#!/usr/bin/env python3
"""
outlook-gtd-triage.py — GTD inbox-zero triage for personal Outlook accounts
(USER MANDATE 2026-08-20: "clean up/clear out my Outlook inboxes; I only want to
see what I must respond to or act upon; everything else dispatched autonomously
(GTD/Inbox Zero); keep all inboxes clean").

Modes (mutually exclusive):
  --dry-run   classify + print plan, move NOTHING
  --apply     classify + move (idempotent; NOISE -> per-account Deleted Items)
  --report    print current inbox/GTD-folder state (non-mutating; enumerates
              GTD-Waiting For items with dates for the Friday weekly review)

GTD routing (permanent folders under each Inbox):
  ACTION    stays in Inbox, red-flagged + unread  -> user must respond/act
  WAITING   -> Inbox/GTD-Waiting For              -> ball in someone else's court
  SOMEDAY   -> Inbox/GTD-Someday Maybe            -> read later / maybe
  REFERENCE -> Inbox/GTD-Reference                -> receipts, confirmations, records
  NOISE     -> THIS ACCOUNT's Deleted Items       -> marketing, notifications, codes

HARD CONSTRAINTS (mem-J8X6yO9zBjfn, user directive 2026-08-05/08-12):
  - COM ONLY, INVISIBLE: never opens Outlook UI; no visible OUTLOOK.EXE.
  - Outlook is quit ONLY if this script started it (GetObject fallback).
  - Never permanently deletes mail (Deleted Items is recoverable).
  - Idempotent: safe to run every day; items already in GTD folders are skipped.

Red-team remediation 2026-08-20 (completeness audit H-1/S-1..S-5 + D-1..D-4/D-6):
  H-1: Deleted Items resolved PER STORE (inbox.Store.GetDefaultFolder(3)) — the
       namespace-level default store previously swallowed the other account's NOISE.
  S-1: moved items marked read (UnRead=False) before Move.
  S-2: ACTION items marked unread + red-flagged (attention surface).
  S-3: per-account fault isolation (one failing account no longer aborts the other).
  S-4: meeting cancellations/responses -> REFERENCE; only live requests -> ACTION.
  S-5: empty sender falls through to conservative unknown-domain rules (not bulk NOISE).
  D-1: --report enumerates GTD-Waiting For items with received dates (weekly review).
  D-2: --report never creates folders (non-mutating lookup).
  D-3: --dry-run/--apply/--report are mutually exclusive.
  D-4: triage log rotated to last 500 lines.
  D-6: state actions[] carry a 160-char body snippet.

State: writes logs/email-gtd-state.json (last run) + appends logs/email-triage-log.md
for the Friday weekly review + PDB to consume (waiting-for overdue surfacing).
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

import win32com.client

ACCOUNTS = ["rowan.quni@outlook.com", "rwnquni@outlook.com"]
F_WAITING = "GTD-Waiting For"
F_SOMEDAY = "GTD-Someday Maybe"
F_REF = "GTD-Reference"
GTD_FOLDERS = {F_WAITING, F_SOMEDAY, F_REF}
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs"))
STATE_FILE = os.path.join(LOG_DIR, "email-gtd-state.json")
TRIAGE_LOG = os.path.join(LOG_DIR, "email-triage-log.md")
LOG_ROTATION = 500

# Machine/bulk senders: notification noise by default (subject may upgrade)
BULK_DOMAINS = {
    "github.com", "gitlab.com", "bitbucket.org", "cloudflare.com", "vercel.com",
    "netlify.com", "twitter.com", "x.com", "linkedin.com", "facebook.com",
    "instagram.com", "youtube.com", "reddit.com", "quora.com", "medium.com",
    "substack.com", "wordpress.com", "tumblr.com", "spotify.com", "netflix.com",
    "disneyplus.com", "hulu.com", "twitch.tv", "discord.com", "telegram.org",
    "whatsapp.com", "tiktok.com", "pinterest.com", "snapchat.com", "booking.com",
    "airbnb.com", "expedia.com", "tripadvisor.com", "skyscanner.net", "ebay.com",
    "etsy.com", "aliexpress.com", "temu.com", "shein.com", "wish.com", "shopify.com",
    "mailchimp.com", "sendinblue.com", "brevo.com", "hubspot.com", "salesforce.com",
    "klaviyo.com", "constantcontact.com", "campaignmonitor.com", "mailerlite.com",
    "convertkit.com", "beehiiv.com", "adobe.com", "dropbox.com", "notion.so",
    "slack.com", "zoom.us", "godaddy.com", "namecheap.com", "wix.com",
    "squarespace.com", "hostinger.com", "google.com", "googlemail.com",
    "microsoft.com", "apple.com", "amazon.com", "amazonaws.com", "npmjs.com",
    "pypi.org", "crates.io", "docker.com", "stackoverflow.com", "arxiv.org",
    "researchgate.net", "academia.edu", "orcid.org", "paypal.com", "stripe.com",
    "klarna.com", "afterpay.com", "revolut.com",
}
# Financial institutions: NEVER noise; alerts/statements are ACTION/REFERENCE
FINANCIAL_DOMAINS = {
    "chase.com", "bankofamerica.com", "wellsfargo.com", "citibank.com", "citi.com",
    "capitalone.com", "americanexpress.com", "amex.com", "discover.com", "usbank.com",
    "ally.com", "sofi.com", "chime.com", "ing.com", "rabobank.nl", "abnamro.nl",
    "ing.nl", "bunq.com", "n26.com", "wise.com", "transferwise.com", "payoneer.com",
    "vanguard.com", "fidelity.com", "schwab.com", "etrade.com", "traderepublic.com",
    "degiro.nl", "ibkr.com", "interactivebrokers.com",
}
HUMAN_DOMAINS = {
    "outlook.com", "hotmail.com", "live.com", "msn.com", "gmail.com", "yahoo.com",
    "ymail.com", "icloud.com", "me.com", "mac.com", "protonmail.com", "proton.me",
    "zoho.com", "aol.com", "gmx.com", "tutanota.com",
}
QNFO_DOMAINS = {"qnfo.org", "qwav.org", "qwav.tech", "qnfo.io"}

# USER-WITHDRAWN CONTEXTS (2026-08-25, user directive): contexts the user has
# explicitly withdrawn from. Sender domain + subject keyword match -> NOISE
# (Deleted Items, recoverable), never ACTION. Receipts are still protected:
# a receipt subject from a withdrawn domain does NOT match the context
# keywords (e.g., "Confirmation of order 101825" vs CWI keywords), so it falls
# through to the unknown-domain RX_RECEIPT rule -> REFERENCE (canonical: CWI
# order #101825 kept). Canonical context: CWI Summer School 2026 — poster
# withdrawn (NO-GO, mem-1PfbIHhO_YRj), user not participating/attending
# (mem-POIBBCi_hVEA); CWI summer-school mail is clutter.
WITHDRAWN_CONTEXTS = {
    "cwi.nl": ("CWI Summer School 2026", ("summer school", "poster", "slides", "practical information")),
}


def _withdrawn_context(dom, subject):
    """Return True if sender+subject match a context the user withdrew from."""
    if not dom:
        return False
    base = next((b for b in WITHDRAWN_CONTEXTS if dom == b or dom.endswith("." + b)), None)
    if base is None:
        return False
    _label, keywords = WITHDRAWN_CONTEXTS[base]
    sl = (subject or "").lower()
    return any(k in sl for k in keywords)

RX_RECEIPT = re.compile(
    r"receipt|invoice|statement|payment (received|confirmed)|order confirmation|"
    r"confirmation of order|your order|shipping confirmation|tracking (number|#)|"
    r"delivery (update|confirm)|tax (receipt|statement)|transaction (receipt|confirm)|"
    r"payment method|practical information|purchase (confirmed|confirmation)", re.I)
RX_WAITING = re.compile(
    r"application (received|submitted|is under)|received your (submission|paper)|"
    r"we (received|got) your|ticket[ #]?\d|"
    r"case[ #]?\d|support (request|ticket)|under review|in review|we'll (get back|follow)|"
    r"will (get back|follow up)|status update|awaiting", re.I)
RX_SYSTEM_NOTICE = re.compile(
    r"profile activat|account activat|welcome to|your (account|profile) is (now )?(active|ready)|"
    r"getting started", re.I)
RX_SOMEDAY = re.compile(
    r"invitation|you're invited|save the date|call for (papers|proposals)|cfp|"
    r"register now|webinar|meetup|event announcement|opportunity|nominations? (open|now)", re.I)
RX_ACTION = re.compile(
    r"^re:|^aw:|^sv:|deadline|action required|response required|please respond|"
    r"rsvp|decision needed|approval needed|urgent|reminder", re.I)
RX_CODE = re.compile(
    r"verification code|login code|security code|one-time (password|code)|otp|"
    r"confirm your email|email verification", re.I)
RX_NEWSLETTER = re.compile(
    r"newsletter|weekly (digest|roundup)|daily digest|top stories|this week|"
    r"unsubscribe", re.I)
RX_MARKETING = re.compile(
    r"sale|discount|promo|offer|limited time|deal of|% off|free shipping|"
    r"don't miss|act now|final hours", re.I)
RX_SECURITY = re.compile(
    r"security alert|fraud alert|unusual activity|sign-in (alert|attempt)|"
    r"new device|password (reset|changed)|2fa|two-factor", re.I)


def domain_of(sender):
    s = (sender or "").strip().lower()
    if "@" in s:
        return s.rsplit("@", 1)[1]
    return ""


def _dom_in(dom, domset):
    """Match a sender domain against a set of BASE domains, allowing
    subdomains (notify.cloudflare.com -> cloudflare.com). Exact match first,
    then suffix match on '.'. A non-subdomain lookalike (evilcloudflare.com)
    does NOT match (no leading dot)."""
    if not dom:
        return False
    if dom in domset:
        return True
    return any(dom.endswith("." + b) for b in domset)


def classify(item):
    """Return one of: ACTION, WAITING, SOMEDAY, REFERENCE, NOISE."""
    try:
        sender = (item.SenderEmailAddress or "").strip()
    except Exception:
        sender = ""
    try:
        subject = (item.Subject or "").strip()
    except Exception:
        subject = ""
    try:
        msgclass = (item.MessageClass or "")
    except Exception:
        msgclass = ""
    try:
        body = (item.Body or "")[:600]
    except Exception:
        body = ""
    try:
        received = item.ReceivedTime
        if hasattr(received, "tzinfo") and received.tzinfo is not None:
            received = received.astimezone().replace(tzinfo=None)
        age_days = (dt.datetime.now() - received).days if received else 0
    except Exception:
        age_days = 0

    # 1. Meeting items (S-4 refinement): only LIVE requests need ACTION;
    #    cancellations auto-update the calendar, responses are informational.
    mc = msgclass or ""
    if mc.startswith("IPM.Schedule.Meeting.Canceled"):
        return "REFERENCE"
    if mc.startswith("IPM.Schedule.Meeting.Resp"):
        return "REFERENCE"
    if "IPM.Schedule.Meeting" in mc:
        return "ACTION"

    # 2. Delivery/read reports -> NOISE
    if mc.startswith("IPM.Report") or mc.startswith("REPORT."):
        return "NOISE"

    dom = domain_of(sender)

    # 3. Financial institutions: alerts ACTION, statements/receipts REFERENCE, rest ACTION
    if _dom_in(dom, FINANCIAL_DOMAINS):
        if RX_RECEIPT.search(subject):
            return "REFERENCE"
        if RX_SECURITY.search(subject):
            return "ACTION"
        return "ACTION"  # conservative: bank mail is never noise

    # 3b. USER-WITHDRAWN CONTEXTS (2026-08-25): contexts the user explicitly
    #      withdrew from are NOISE, never ACTION (canonical: CWI Summer School).
    if _withdrawn_context(dom, subject):
        return "NOISE"

    # 4. QNFO system mail -> NOISE in a PERSONAL inbox (2026-08-28 root-cause):
    #    every qnfo.org/qwav.org-origin message reaching a personal Outlook/Gmail
    #    inbox is the agent's OWN outbound copy (outreach "Re:" copies, [PREVIEW],
    #    outreach-check / pre-publish notes). Inbound qnfo.org correspondence is
    #    captured by the qnfo-email Worker in D1 and is never forwarded here, so
    #    nothing in this branch needs the user's action. The real correspondence
    #    lives in the qnfo-email D1 (qnfo-audit.emails).
    if _dom_in(dom, QNFO_DOMAINS):
        return "NOISE"

    # 5. Human senders (personal domains) -> default ACTION, refined by subject
    if _dom_in(dom, HUMAN_DOMAINS):
        if RX_RECEIPT.search(subject):
            return "REFERENCE"
        if RX_WAITING.search(subject):
            return "WAITING"
        if RX_NEWSLETTER.search(subject):
            return "SOMEDAY"
        return "ACTION"

    # 6. Bulk/machine senders -> refine by subject, else NOISE.
    #    (S-5: empty/unknown sender falls through to the conservative
    #    unknown-domain rules below — never forced through the bulk branch.)
    if _dom_in(dom, BULK_DOMAINS):
        if RX_SECURITY.search(subject):
            return "ACTION" if _dom_in(dom, {"cloudflare.com", "microsoft.com", "google.com"}) else "WAITING"
        if RX_RECEIPT.search(subject):
            return "REFERENCE"
        if RX_WAITING.search(subject):
            return "WAITING"
        if RX_SYSTEM_NOTICE.search(subject):
            return "NOISE"
        if RX_ACTION.search(subject):
            return "ACTION"
        if RX_SOMEDAY.search(subject):
            return "SOMEDAY"
        if RX_CODE.search(subject):
            return "REFERENCE" if age_days < 1 else "NOISE"
        if RX_NEWSLETTER.search(subject) or RX_MARKETING.search(subject):
            return "NOISE"
        if age_days > 180:
            return "NOISE"
        return "NOISE"

    # 7. Unknown domains (businesses, universities, orgs) -> conservative
    if RX_RECEIPT.search(subject):
        return "REFERENCE"
    if RX_WAITING.search(subject):
        return "WAITING"
    if RX_SYSTEM_NOTICE.search(subject):
        return "NOISE"
    if RX_SOMEDAY.search(subject):
        return "SOMEDAY"
    if RX_NEWSLETTER.search(subject) or RX_MARKETING.search(subject):
        return "SOMEDAY" if RX_NEWSLETTER.search(subject) else "NOISE"
    return "ACTION"  # unknown sender: keep visible (conservative)


def get_outlook():
    """Attach to running Outlook or start hidden; return (app, was_started)."""
    try:
        app = win32com.client.GetObject(Class="Outlook.Application")
        return app, False
    except Exception:
        app = win32com.client.Dispatch("Outlook.Application")
        return app, True


def get_inbox(ns, email):
    """ns.Folders yields store-ROOT MAPIFolders (not Store objects); the root
    MAPIFolder exposes .Store, whose GetDefaultFolder(6) resolves the Inbox
    for that account (verified 2026-08-20 on both Outlook.com stores).

    Fix 2026-08-27 (daily-sweep guardrail): the gen_py _Store wrapper may not
    expose SmtpAddress under early binding; that AttributeError must NOT discard
    the valid Store (the combined try/except previously set store=None, skipping
    the working GetDefaultFolder(6) path -> INBOX NOT FOUND for every account).
    SmtpAddress is now read in its own try; Store survives. The fallback also
    uses Folders.Item("Inbox") instead of Folders("Inbox") (the _Folders wrapper
    is not callable under early binding)."""
    for root in ns.Folders:
        name = (root.Name or "").lower()
        try:
            store = root.Store
        except Exception:
            store = None
        smtp = ""
        if store is not None:
            try:
                smtp = (store.SmtpAddress or "").lower()
            except Exception:
                smtp = ""
        if email.lower() in name or email.lower() in smtp:
            if store is not None:
                try:
                    return store.GetDefaultFolder(6)  # olFolderInbox
                except Exception:
                    pass
            try:
                return root.Folders.Item("Inbox")
            except Exception:
                continue
    return None


def ensure_folder(inbox, name):
    for f in inbox.Folders:
        if f.Name == name:
            return f
    return inbox.Folders.Add(name)


def find_folder(inbox, name):
    """Non-mutating folder lookup (D-2: report mode must never create folders)."""
    try:
        for f in inbox.Folders:
            if f.Name == name:
                return f
    except Exception:
        pass
    return None


def process_inbox(app, ns, email, apply):
    inbox = get_inbox(ns, email)
    if inbox is None:
        print(f"[{email}] INBOX NOT FOUND")
        return None
    waiting = ensure_folder(inbox, F_WAITING)
    someday = ensure_folder(inbox, F_SOMEDAY)
    ref = ensure_folder(inbox, F_REF)
    deleted = inbox.Store.GetDefaultFolder(3)  # olFolderDeletedItems (H-1: PER STORE)

    counts = {"ACTION": 0, "WAITING": 0, "SOMEDAY": 0, "REFERENCE": 0, "NOISE": 0}
    actions = []
    waiting_items = []
    moved = 0
    for item in list(inbox.Items):
        try:
            cls = classify(item)
            counts[cls] += 1
            subject = (item.Subject or "")[:90]
            try:
                sender = (item.SenderEmailAddress or "")
            except Exception:
                sender = ""
            try:
                rec = item.ReceivedTime
                if hasattr(rec, "tzinfo") and rec.tzinfo is not None:
                    rec = rec.astimezone().replace(tzinfo=None)
                rec_s = rec.strftime("%Y-%m-%d %H:%M")
            except Exception:
                rec_s = "?"
            if cls == "ACTION":
                snippet = ""
                try:
                    snippet = (item.Body or "")[:160]
                except Exception:
                    pass
                actions.append({"from": sender, "subject": subject, "received": rec_s, "snippet": snippet})
                if apply:
                    try:
                        item.FlagStatus = 2  # olFlagMarked (red flag)
                        item.UnRead = True   # S-2: ACTION stays unread (attention surface)
                        item.Save()
                    except Exception:
                        pass
                continue
            if cls == "WAITING":
                waiting_items.append({"from": sender, "subject": subject, "received": rec_s})
            dest = {"WAITING": waiting, "SOMEDAY": someday, "REFERENCE": ref, "NOISE": deleted}[cls]
            if apply:
                try:
                    item.UnRead = False  # S-1: moved items read (no unread badges in GTD folders)
                    item.Save()
                    item.Move(dest)
                    moved += 1
                except Exception as e:
                    print(f"  MOVE FAIL {subject[:50]}: {e}")
            else:
                print(f"  [{cls:8s}] {rec_s} | {sender[:30]:30s} | {subject}")
        except Exception as e:
            print(f"  SKIP (error) {e}")
    print(f"[{email}] counts={counts} moved={moved} inbox_remaining_action={counts['ACTION']}")
    return {"account": email, "counts": counts, "actions": actions, "waiting": waiting_items, "moved": moved}


def cmd_report(ns):
    for email in ACCOUNTS:
        inbox = get_inbox(ns, email)
        if inbox is None:
            print(f"[{email}] inbox not found")
            continue
        total = 0
        unread = 0
        flagged = 0
        for item in inbox.Items:
            total += 1
            try:
                if item.UnRead:
                    unread += 1
            except Exception:
                pass
            try:
                if item.FlagStatus == 2:
                    flagged += 1
            except Exception:
                pass
        print(f"[{email}] inbox total={total} unread={unread} flagged={flagged}")
        for fname in GTD_FOLDERS:
            try:
                f = find_folder(inbox, fname)
                if f is None:
                    print(f"   {fname}: (not created)")
                    continue
                n = 0
                for _ in f.Items:
                    n += 1
                print(f"   {fname}: {n}")
                if fname == F_WAITING:
                    for it in f.Items:  # D-1: enumerate waiting items w/ dates for weekly review
                        try:
                            rec = it.ReceivedTime
                            if hasattr(rec, "tzinfo") and rec.tzinfo is not None:
                                rec = rec.astimezone().replace(tzinfo=None)
                            print(f"      WAIT {rec:%Y-%m-%d} | {(it.Subject or '')[:80]}")
                        except Exception:
                            pass
            except Exception:
                pass


def _rotate_triage_log():
    """Keep the triage log bounded (D-4: last 500 lines)."""
    try:
        lines = open(TRIAGE_LOG, encoding="utf-8").read().splitlines()
        if len(lines) > LOG_ROTATION:
            open(TRIAGE_LOG, "w", encoding="utf-8", newline="\n").write(
                "\n".join(lines[-LOG_ROTATION:]) + "\n")
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()  # D-3: modes never combine
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--report", action="store_true")
    args = ap.parse_args()

    os.makedirs(LOG_DIR, exist_ok=True)
    app, started = get_outlook()
    try:
        ns = app.GetNamespace("MAPI")
        if args.report:
            cmd_report(ns)
            return
        results = []
        for email in ACCOUNTS:
            try:  # S-3: per-account fault isolation
                r = process_inbox(app, ns, email, apply=args.apply)
                if r:
                    results.append(r)
            except Exception as e:
                print(f"[{email}] ACCOUNT FAILURE: {e}")
                results.append({"account": email, "error": str(e)})
        if args.apply:
            state = {"run_at": dt.datetime.now().isoformat(timespec="seconds"),
                     "accounts": results}
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=1, ensure_ascii=False)
            with open(TRIAGE_LOG, "a", encoding="utf-8") as f:
                line = (f"{state['run_at']} | " +
                        " | ".join(f"{r['account']}: A{r['counts']['ACTION']} "
                                   f"W{r['counts']['WAITING']} S{r['counts']['SOMEDAY']} "
                                   f"R{r['counts']['REFERENCE']} N{r['counts']['NOISE']} "
                                   f"(moved {r['moved']})" for r in results))
                f.write(line + "\n")
            _rotate_triage_log()
            print("STATE:", STATE_FILE)
    finally:
        if started:
            try:
                app.Quit()
            except Exception:
                pass


if __name__ == "__main__":
    main()
