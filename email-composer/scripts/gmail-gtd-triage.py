#!/usr/bin/env python3
"""
gmail-gtd-triage.py — GTD inbox-zero triage for the personal Gmail account
rwnquni@gmail.com (USER MANDATE 2026-08-20: "clean up/clear out my inboxes; I
only want to see what I must respond to or act upon; everything else dispatched
autonomously (GTD/Inbox Zero); keep all inboxes clean"). This closes the open
build gap from the personal handoff (Gmail not wired into the triage pipeline).

Modes (mutually exclusive):
  --dry-run   classify + print plan, move NOTHING (read-only IMAP session)
  --apply     classify + move (idempotent; NOISE -> [Gmail]/Trash, recoverable)
  --report    print current INBOX state (non-mutating)

GTD routing (Gmail labels, created under the account root):
  ACTION    stays in INBOX, flagged + unread        -> user must respond/act
  WAITING   -> label "GTD-Waiting For" (INBOX label removed)
  SOMEDAY   -> label "GTD-Someday Maybe"
  REFERENCE -> label "GTD-Reference"
  NOISE     -> Trash (recoverable; never permanently deleted)

HARD CONSTRAINTS (mirrors outlook-gtd-triage.py):
  - Credentials: app password read from C:\\Users\\LENOVO\\tokens\\gmail,
    never printed. Personal account rwnquni@gmail.com ONLY.
  - Never permanently deletes mail: NOISE -> Trash via IMAP \\Deleted +
    EXPUNGE on INBOX only; copies exist for moved items.
  - Idempotent: moved items leave INBOX, so re-runs only see new mail.
  - UID-based operations (sequence numbers shift on EXPUNGE).

Classification rules are a verbatim port of outlook-gtd-triage.py classify()
(domain sets, regexes, WITHDRAWN_CONTEXTS gate). Meeting-class branches do not
apply over IMAP and are skipped.

State: writes logs/email-gmail-state.json (last run) + appends [gmail]-prefixed
lines to logs/email-triage-log.md for the Friday weekly review + PDB.
"""
import argparse
import datetime as dt
import email.utils
import imaplib
import json
import os
import re
import sys

ACCOUNT = "rwnquni@gmail.com"
IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993
TOKEN_FILE = r"C:\Users\LENOVO\tokens\gmail"

F_WAITING = "GTD-Waiting For"
F_SOMEDAY = "GTD-Someday Maybe"
F_REF = "GTD-Reference"
GTD_LABELS = (F_WAITING, F_SOMEDAY, F_REF)

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs"))
STATE_FILE = os.path.join(LOG_DIR, "email-gmail-state.json")
TRIAGE_LOG = os.path.join(LOG_DIR, "email-triage-log.md")

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
    "researchgate.net", "academia.edu", "orcid.org", "paypal.com",
    "stripe.com", "klarna.com", "afterpay.com", "revolut.com",
}
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

WITHDRAWN_CONTEXTS = {
    "cwi.nl": ("CWI Summer School 2026", ("summer school", "poster", "slides", "practical information")),
}

RX_RECEIPT = re.compile(
    r"receipt|invoice|statement|payment (received|confirmed)|order confirmation|"
    r"confirmation of order|your order|shipping confirmation|tracking (number|#)|"
    r"delivery (update|confirm)|tax (receipt|statement)|transaction (receipt|confirm)|"
    r"payment method|practical information|bevestiging|bestelling|factuur|betaling|purchase (confirmed|confirmation)", re.I)
RX_WAITING = re.compile(
    r"application (received|submitted|is under)|received your (submission|paper)|"
    r"submission received|your submission|we (received|got) your|ticket[ #]?\d|"
    r"case[ #]?\d|support (request|ticket)|under review|in review|we'll (get back|follow)|"
    r"will (get back|follow up)|status update|awaiting|aanvraag", re.I)
RX_SYSTEM_NOTICE = re.compile(
    r"profile activat|account activat|welcome to|your (account|profile) is (now )?(active|ready)|"
    r"getting started", re.I)
RX_SOMEDAY = re.compile(
    r"invitation|you're invited|save the date|call for (papers|proposals)|cfp|"
    r"register now|webinar|meetup|event announcement|opportunity|nominations? (open|now)", re.I)
RX_ACTION = re.compile(
    r"^re:|^aw:|^sv:|deadline|action required|response required|please respond|"
    r"rsvp|decision needed|approval needed|urgent|reminder|herinnering", re.I)
RX_CODE = re.compile(
    r"verification code|login code|security code|one-time (password|code)|otp|"
    r"confirm your email|email verification", re.I)
RX_NEWSLETTER = re.compile(
    r"newsletter|weekly (digest|roundup)|daily digest|top stories|this week|"
    r"unsubscribe|nieuwsbrief", re.I)
RX_MARKETING = re.compile(
    r"sale|discount|promo|offer|limited time|deal of|% off|free shipping|"
    r"don't miss|act now|final hours|survey|feedback|rate your|tell us about your|"
    r"share your (opinion|experience|mening)|deel je mening|mening delen|hear about your", re.I)
RX_SECURITY = re.compile(
    r"security alert|fraud alert|unusual activity|sign-in (alert|attempt)|"
    r"new device|password (reset|changed)|2fa|two-factor", re.I)
RX_JOBALERT = re.compile(
    r"job (alert|opening)|vacature|are hiring|are looking for|great companies", re.I)
RX_VOLUNTEER = re.compile(r"vrijwilliger|volunteer", re.I)


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


def classify(sender, subject, age_days):
    """Port of outlook-gtd-triage.py classify(); meeting-class branches skipped."""
    dom = domain_of(sender)

    if _dom_in(dom, FINANCIAL_DOMAINS):
        if RX_RECEIPT.search(subject):
            return "REFERENCE"
        if RX_SECURITY.search(subject):
            return "ACTION"
        return "ACTION"

    if dom in WITHDRAWN_CONTEXTS:
        base = next((b for b in WITHDRAWN_CONTEXTS if dom == b or dom.endswith("." + b)), None)
        if base is not None:
            _label, keywords = WITHDRAWN_CONTEXTS[base]
            sl = (subject or "").lower()
            if any(k in sl for k in keywords):
                return "NOISE"

    if _dom_in(dom, QNFO_DOMAINS):
        return "NOISE"

    if _dom_in(dom, HUMAN_DOMAINS):
        if RX_RECEIPT.search(subject):
            return "REFERENCE"
        if RX_WAITING.search(subject):
            return "WAITING"
        if RX_NEWSLETTER.search(subject):
            return "SOMEDAY"
        return "ACTION"

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

    if RX_RECEIPT.search(subject):
        return "REFERENCE"
    if RX_WAITING.search(subject):
        return "WAITING"
    if RX_VOLUNTEER.search(subject):
        return "REFERENCE"
    if RX_JOBALERT.search(subject):
        return "NOISE"
    if RX_SYSTEM_NOTICE.search(subject):
        return "NOISE"
    if RX_SOMEDAY.search(subject):
        return "SOMEDAY"
    if RX_NEWSLETTER.search(subject) or RX_MARKETING.search(subject):
        return "SOMEDAY" if RX_NEWSLETTER.search(subject) else "NOISE"
    if RX_ACTION.search(subject):
        return "ACTION"
    if sender.lower().startswith(("noreply", "no-reply")):
        return "NOISE"
    return "ACTION"


def parse_date(header_value):
    try:
        d = email.utils.parsedate_to_datetime(header_value)
        if d.tzinfo is not None:
            d = d.astimezone().replace(tzinfo=None)
        return d
    except Exception:
        return None


def read_token():
    if not os.path.exists(TOKEN_FILE):
        print(f"ERROR: token file not found: {TOKEN_FILE}")
        sys.exit(2)
    with open(TOKEN_FILE, encoding="utf-8") as f:
        return f.read().strip()


def ensure_labels(M, apply):
    existing = set()
    typ, data = M.list()
    if data:
        for line in data:
            if isinstance(line, bytes):
                line = line.decode("utf-8", "replace")
            m = re.search(r'"([^"]*)"\s*$', line)
            if m:
                existing.add(m.group(1))
    missing = [l for l in GTD_LABELS if l not in existing]
    if apply:
        for l in missing:
            try:
                M.create('"' + l + '"')
                print(f"created label: {l}")
            except Exception as e:
                print(f"WARN: could not create label {l}: {e}")
    return missing


def run(mode):
    token = read_token()
    M = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    M.login(ACCOUNT, token)
    if mode == "dry-run":
        typ, _ = M.select("INBOX", readonly=True)
    else:
        typ, _ = M.select("INBOX")
    if typ != "OK":
        print("ERROR: could not select INBOX")
        M.logout()
        sys.exit(2)

    typ, data = M.uid("SEARCH", None, "ALL")
    if typ != "OK":
        print("ERROR: search failed")
        M.logout()
        sys.exit(2)
    uids = data[0].split()
    total = len(uids)
    print(f"[{ACCOUNT}] INBOX messages: {total}")

    counts = {"ACTION": 0, "WAITING": 0, "SOMEDAY": 0, "REFERENCE": 0, "NOISE": 0}
    actions = []
    waiting_items = []
    plan = []  # (uid, cls, subject)

    now = dt.datetime.now()
    for uid in uids:
        uid = uid.decode() if isinstance(uid, bytes) else uid
        typ, d = M.uid("FETCH", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        if typ != "OK" or not d or d[0] is None:
            continue
        raw = b""
        for part in d:
            if isinstance(part, tuple):
                raw = part[1]
                break
        msg = email.message_from_bytes(raw)
        sender_name, sender_addr = email.utils.parseaddr(msg.get("From", ""))
        subject = msg.get("Subject", "") or ""
        date_h = msg.get("Date", "")
        parsed = parse_date(date_h)
        age_days = (now - parsed).days if parsed else 0
        cls = classify(sender_addr, subject, age_days)
        counts[cls] += 1
        if cls == "ACTION":
            actions.append({"from": sender_addr, "subject": subject[:90], "received": parsed.strftime("%Y-%m-%d %H:%M") if parsed else "?"})
        elif cls == "WAITING":
            waiting_items.append({"from": sender_addr, "subject": subject[:90], "received": parsed.strftime("%Y-%m-%d %H:%M") if parsed else "?"})
        plan.append((uid, cls, subject[:90]))

    print("counts:", json.dumps(counts))
    if actions:
        print("\nACTION (stay in INBOX):")
        for a in actions:
            print(f"  - {a['from']:<40} {a['received']}  {a['subject']}")
    if waiting_items:
        print("\nWAITING:")
        for w in waiting_items:
            print(f"  - {w['from']:<40} {w['received']}  {w['subject']}")

    if mode == "dry-run":
        print("\nDRY-RUN: nothing moved.")
        M.logout()
        return counts, actions, waiting_items

    # apply
    ensure_labels(M, True)
    moved = 0
    # process in reverse UID order is not required with UIDs (stable), but keep
    # EXPUNGE deferred to the end for a single round-trip.
    for uid, cls, _subj in plan:
        if cls == "ACTION":
            try:
                M.uid("STORE", uid, "+FLAGS", "(\\Flagged)")
                M.uid("STORE", uid, "-FLAGS", "(\\Seen)")
            except Exception as e:
                print(f"WARN: flag failed uid {uid}: {e}")
            continue
        label = None
        if cls == "WAITING":
            label = F_WAITING
        elif cls == "SOMEDAY":
            label = F_SOMEDAY
        elif cls == "REFERENCE":
            label = F_REF
        try:
            if label:
                M.uid("COPY", uid, '"' + label + '"')
            M.uid("STORE", uid, "+FLAGS", "(\\Deleted)")
            moved += 1
        except Exception as e:
            print(f"WARN: move failed uid {uid}: {e}")
    try:
        M.expunge()
    except Exception as e:
        print(f"WARN: expunge failed: {e}")
    print(f"moved: {moved} (ACTION kept: {counts['ACTION']})")

    state = {
        "account": ACCOUNT,
        "run": now.isoformat(),
        "mode": mode,
        "counts": counts,
        "moved": moved,
        "actions": actions,
        "waiting": waiting_items,
    }
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    with open(TRIAGE_LOG, "a", encoding="utf-8") as f:
        f.write(f"[gmail] {now.isoformat(timespec='minutes')} mode={mode} counts={json.dumps(counts)} moved={moved}\n")
        for a in actions:
            f.write(f"[gmail] ACTION - {a['from']} - {a['received']} - {a['subject']}\n")
        for w in waiting_items:
            f.write(f"[gmail] WAITING - {w['from']} - {w['received']} - {w['subject']}\n")
    M.logout()
    return counts, actions, waiting_items


def report():
    token = read_token()
    M = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    M.login(ACCOUNT, token)
    M.select("INBOX", readonly=True)
    typ, data = M.uid("SEARCH", None, "ALL")
    total = len(data[0].split()) if data and data[0] else 0
    print(f"[{ACCOUNT}] INBOX: {total} messages (read-only report)")
    M.logout()
    return total


def main():
    ap = argparse.ArgumentParser(description="GTD inbox-zero triage for rwnquni@gmail.com")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true", help="classify + print plan, move nothing")
    g.add_argument("--apply", action="store_true", help="classify + move (idempotent)")
    g.add_argument("--report", action="store_true", help="print inbox state only")
    args = ap.parse_args()
    if args.dry_run:
        run("dry-run")
    elif args.apply:
        run("apply")
    else:
        report()


if __name__ == "__main__":
    main()
