# QNFO Outreach Log

Log of all outbound outreach sends via the qnfo-email Worker /send endpoint.
Per research skill v2.88: log recipient, status, message_id. D1 `emails` table is the authoritative record.

---

## 2026-08-10 — Batch 1: Qudit Advantage paper-sharing (Monday scan)

**Paper:** *The Qudit Advantage: System-Level Joules-per-Solution Comparison of a Qudit Architecture Against 17 Conventional Platforms* — DOI **10.5281/zenodo.21827737** (2026-08-06)
**Sender:** rowan.quni@qwav.tech (NOTE: qnfo.org Email Sending is broken platform-side — CF error 10002 email.sending.error.internal_server on ALL qnfo.org addresses, verified via Worker binding + REST API + wrangler CLI 2026-08-10; qwav.tech/qwav.org verified working with full SPF/DKIM/DMARC. Qudit Advantage is QWAV-branded JPCUB work, so qwav.tech sender is thematically consistent. FLAGGED for user awareness; switch back to rowan.quni@qnfo.org when Cloudflare resolves.)

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | Status | Sent (UTC) |
|---|-----------|--------------|---------------------|------------------|------------|--------|------------|
| 1 | Tirthak Patel (Rice) | VERIFIED from arXiv source tarball 2608.02815 (`tp53@rice.edu`) | PaQit: Energy-Runtime-Fidelity Co-Optimization for Neutral Atom Quantum Computers (2608.02815) | System-level energy-runtime-fidelity co-optimization parallels JPCUB joules-per-solution system-level comparison | 3a0ec65a-352d-4777-847b-4c93d6f65db1 | sent | 2026-08-10T11:33:14Z |
| 2 | Pierre-Emmanuel Emeriau (Quandela) | VERIFIED from arXiv source tarball 2601.08068 (`pe.emeriau@quandela.com`) | Quantum Energetic Advantage before Computational Advantage in Boson Sampling (2601.08068) | Energetic advantage preceding computational advantage = JPCUB thesis in boson sampling | 391562a5-4bb4-4d54-b2d4-3c017953ccc4 | sent | 2026-08-10T11:33:19Z |

**Also verified but NOT contacted (avoid multi-contact of same group):** Jason Ludmir (jzl2@rice.edu — PaQit co-author with Patel; single contact per group per outreach strategy §1).

**Verified pool, deferred (no email in arXiv source tarball — flagged verify-before-send):**
- Michele Mosca / Jon Yard / Mark Deaconu (IQC Waterloo) — Buildings for Synthesis with Clifford+R (2510.11526) → Paper B: Ultrametric Code Spaces (10.5281/zenodo.21824396)
- Ling-Yan Hung / Lin Chen / Xirong Liu (Fudan) — Bending the Bruhat-Tits Tree I/II + Emergent Einstein Equation (2102.12023/24/22) → Paper B
- Marco Pezzutto / Yasser Omar (IST Lisbon) — Cat-qubit 2605.19854 + Rydberg energetics 2601.03141 → Paper A

**Send verification (Tool-Call Execution Mandate):** Both sends confirmed in D1 `emails` table via GET /emails/recent: id=61 (tp53@rice.edu, status=sent), id=62 (pe.emeriau@quandela.com, status=sent). Canonical sent-classification rule satisfied (sender qnfo/qwav domain + external recipient).

**Dedup check (per user mandate — no repeat contact without permission):** Prior batch 2026-08-06 (D1 ids 30-32, 38-43) contacted: kohteckseng@ntu.edu.sg, kelvin.onggadinata@ntu.edu.sg, arghyamaityphysics@gmail.com, lzihan9175@gmail.com, mheydema@caltech.edu, ita@zurich.ibm.com, kais@purdue.edu, martin.ringbauer@uibk.ac.at. **None overlap with this batch.** No repeats.


---

## 2026-08-10 — CORRECTION: Patel test-email repair (contact #3, user-approved)

**Recipient:** Tirthak Patel (tp53@rice.edu)
**Incident:** id=66 (11:54:48Z) — EMAIL-SENDING-DOMAIN-10002 isolation matrix sent "MATRIX E" test payload to a real external recipient (TEST-SEND-EXTERNAL-1 violation; second contact to Patel, who had already received genuine outreach id=61 at 11:33:14Z).
**User decision:** Send short clarification (explicit approval for contact #3).
**Repair send:** id=69 (12:40:57Z) — subject "Re: PaQit - a system-level energy metric for neutral-atom quantum computers" (threads with the genuine message); body asks Patel to disregard the MATRIX E test email and points to the genuine outreach. No re-pitch, no attachments.
**Test-send first:** id=68 (12:40:52Z) → rwnquni@outlook.com (user's own mailbox, TEST-SEND-EXTERNAL-1 compliant).
**Verification:** both id=68 and id=69 status=sent in D1 /emails/recent.
**HARD RULE AFTER THIS:** NO fourth contact to Patel ever — no follow-up, no re-send (no-repeat-contact mandate).
**Anti-patterns referenced:** TEST-SEND-EXTERNAL-1 (email-composer v2.16), OUTREACH-SENT-AS-ARCHIVED-1.


---

## 2026-08-14 — Friday check (DETECTION-ONLY): reply + hygiene + unlogged-send audit

**REPLY RECEIVED (positive/engaged) — ACTION REQUIRED (user):**
- **Mercatus Center Emergent Ventures** (emergentventures@mercatus.gmu.edu → rowan.quni@qwav.tech, id=131, 2026-08-13T18:16Z): "You must complete an application for consideration https://mercatus.tfaforms.net/5099527 — Best, The EV Team". Reply to the user's own application-introduction email (sent 08-13 13:05 local — NOTE: parent send NOT present in D1, tracking gap). User action: complete the EV application form at that URL. Status set to `read` (kept visible, NOT archived). NO auto-reply sent (human reply → user handles).

**HYGIENE (archived same-session, verified in D1):**
- id=135 sunny6v5@gmail.com "A Journal to Consider..." → spam (predatory journal)
- id=134 networking@scijournals.live "Your Response Would Be Greatly Appreciated" → spam (World Journal of Tourism Management, APC $999 — predatory)
- id=130 Google DMARC report (qwav.tech) → archived; ids 128/126 briefing bounce copies → archived

**UNLOGGED OUTBOUND SENDS DETECTED (not in this log — attribution unknown, likely pre-mandate sessions):**
- 08-10: ids 71-73 (Mosca/Ivaldi/Perrone "Re:" follow-ups), 75-77 (Hung/Cociobotaru/Okunishi, Bruhat-Tits papers)
- 08-12: ids 103-105 (Dragovich/ep295/Ebert, p-adic CMB paper), 113/115-125 (standards batch: Meier, Kerjean, Fellous-Asiani ×2 [116+120], Banbury ×2 [117+122], Lange ×2 [118+121], QuantumConsortium, von Kistowski, NLnet, FNAL)
- 08-14: id=133 → matilde@caltech.edu (Marcolli, branch-depth paper) 2026-08-14T01:00Z — **POST-DETECTION-ONLY-MANDATE SEND** (flag for user)
- **DUPLICATE-CONTACT VIOLATIONS:** klaus.lange@hpe.com ×2 (4min apart), cbanbury@g.harvard.edu ×2, fellous.asiani.marco@gmail.com + marco.fellous-asiani@inria.fr (same person ×2) — all 08-12, same batch.

**FOLLOW-UP ELIGIBILITY (Fri 08-14): NONE.** Oldest outreach = 08-06 batch (8d < 14d). First eligible wave: **2026-08-20** (08-06 batch: kohteckseng/onggadinata/maity/lzihan9175/heydema/ita/kais/ringbauer — ONE follow-up each, pending user approval). Patel (tp53@rice.edu): permanently closed (3 contacts already — no follow-up ever).

---

## 2026-08-14 — DUP-RESOLUTION (user mandate: "duplicate contact pairs are your problem to resolve"): LOG-ONLY, NO NEW EMAILS

**Ruling (Repair-Send Protocol Step 0/1):** all three pairs are REDUNDANT (same content sent twice to the same person) → NO new email, stop, log only. A repair/consolidation email would be a THIRD contact (no-repeat-contact mandate — explicit permission required; not granted). Detection-only mandate (2026-08-13) also forbids sends.

**Incident 1 — Klaus Lange (HPE):** ids 118 (18:06:36Z) + 121 (18:10:45Z), 2026-08-12, identical standards-question subject. Contact count: **1** (dedup for eligibility).
**Incident 2 — Chris Banbury (Harvard):** ids 117 (18:06:33Z) + 122 (18:10:49Z), 2026-08-12, identical. Contact count: **1**.
**Incident 3 — Marco Fellous-Asiani (same person, two addresses):** ids 116 (fellous.asiani.marco@gmail.com, 18:06:32Z) + 120 (marco.fellous-asiani@inria.fr, 18:10:41Z), 2026-08-12, identical. Canonical address for future contact: **marco.fellous-asiani@inria.fr** (institutional). Contact count: **1**.

**Follow-up eligibility ledger (dedup applied):** all three count as ONE contact each, eligibility measured from the EARLIEST send of the pair (2026-08-12 18:06Z) → first eligible **2026-08-26** (14d), one follow-up max, pending user approval.
**Root-cause note for future batches:** the 08-12 standards batch was sent in two bursts (18:06 + 18:10) with a recipient-list overlap — dedup must run against D1 recipient+subject BEFORE each burst, not once per day (SEARCH-Q-EMAIL-TOKEN-1: use bare tokens or recipient filter, never full-address q=).

---

## 2026-08-14 — EV APPLICATION EXECUTION RECORD (user mandate: "YOU DECIDE... I will not fill out forms manually")

**Context:** EV reply id=131 (08-13) instructed: "You must complete an application for consideration https://mercatus.tfaforms.net/5099527".
**Prior-application check (user lead):** full Outlook COM scan (invisible) of BOTH accounts (rwnquni@ + rowan.quni@, ~1,000 items: Inbox/Sent/Archive/Deleted/Drafts/Junk + bodies, depth 4) for "emergen/mercatus/tfaforms/george mason" → **ZERO prior Emergent Ventures correspondence** (all 23 hits were false positives: "emergent gravity" paper titles, Fidelity mail). No duplicate-application conflict.
**Form execution (YoBrowser CDP):** filled 18/19 fields (all except required phone) with user's own verified data — Rowan B. Quni-Gudzinas, rowan.quni@qwav.tech (personal), Europe / Netherlands / Amsterdam, proposal = user's 08-13 intro text verbatim (QNFO ~1,000 DOIs, JPCUB joules-per-correct-answer, DOI evidence 21901984/21901983/21922589/21905166), budget $25,000-30,000 USD + breakdown, multimedia https://papers.qnfo.org, 3/3 consents. ALL VALUES VERIFIED in DOM before submit.
**BLOCKERS (hard, not deferrable by agent):**
1. **reCAPTCHA enterprise image challenge** — triggered by automation detection (checkbox click registered → challenge displayed at viewport 355,120). Unsolvable without vision/human; no captcha-service credentials; no bypass attempted (integrity).
2. **Required phone field (tfa_1118)** — no phone number exists in memory, facts, configs, or Outlook (never fabricate contact details — mem-Fxh_-dTzt0FT).
**Terminal state:** submission NOT completed. Application data staged exactly as above; user may finish in ~60s (captcha click + phone + submit) at the URL. Email id=131 remains status=read (visible, unarchived).

---

## 2026-08-14 — RED-TEAM REMEDIATION (3-reviewer aggregate audit; all log-only, NO sends)

**Verdict:** 0 HARD behavioral violations; 1 scoped HARD record-keeping finding (Mosca Re:); 5 SOFT doc/tracking gaps — remediated below. Cross-ref: email-composer v2.18 banner.

**1. Unlogged test-to-OWN-mailbox sends (TEST-SEND-EXTERNAL-1 COMPLIANT — not outreach contacts):**
- id=74 (08-10 13:02:46Z) "Worker send verify post-fix" → rwnquni@outlook.com
- id=114 (08-12 18:01:08Z) "Outreach path check" → rwnquni@outlook.com
- id=132 (08-14 01:00:44Z) "On the branch-depth reading..." → rwnquni@outlook.com (test-pair of id=133, 2s earlier — correct test-first pattern)
All three went to the user's own mailbox; NOT external contacts; now recorded for completeness.

**2. D1 ids 107-110 deletion gap:** rows 107-110 absent from /emails/recent and /emails/body (HTTP 404), window 08-12 ~10:08-13:12Z (between id=106 DMARC report and id=111 archived spam); no API access to deleted rows — documented, no further action possible.

**3. Mosca (michele.mosca@uwaterloo.ca, id=71) "Re:"-prefix flag:** first contact in the D1 record carries "Re:" with NO prior thread in D1 (Mosca sat in the 08-10 "deferred, verify-before-send" pool). Possible Outlook-era prior contact (pre-Worker 08-03, undiscoverable from D1). FLAGGED for user; no action without user word. Eligibility: first contact 08-10 → follow-up window 08-24..08-31, ONE max, pending approval.

**4. Follow-up eligibility ledger (COMPLETE):**
- 08-06 batch (8: kohteckseng/onggadinata/maity/lzihan9175/heydema/ita/kais/ringbauer) → **08-20** (first wave, ONE each, pending approval)
- 08-10: Emeriau (id=62) → **08-24**; Bruhat-Tits batch Hung/Cociobotaru/Okunishi (75-77) → 08-24; Mosca (71) → 08-24..31 (flagged above); Ivaldi (72)/Perrone (73) = ACTIVE threads (replies received 08-05/08-06) — no follow-up needed
- 08-12: CMB batch Dragovich/ep295/Ebert (103-105) → **08-26**; standards singles Meier/Kerjean/QuantumConsortium/vonKistowski/NLnet/FNAL (113/115/119/123/124/125) → 08-26; dup pairs Lange/Banbury/Fellous-Asiani (deduped to 1 contact each, from earliest send 18:06Z) → 08-26
- 08-14: Marcolli (133) → **08-28** (subject to user disposition of the post-mandate-send flag)
Patel: permanently closed (3 contacts: 61/66/69 — no follow-up ever). ONE follow-up max per contact, never twice, never a 4th contact.

**5. id=133 (matilde@caltech.edu, 08-14 01:00:46Z) disposition:** attribution UNKNOWN (cronjob 3851f539 verified detection-only; Mercatus intro parent send 08-13 13:05 local also absent from D1 — consistent with a non-Worker send path, e.g., Cloudflare Email Sending REST). USER DECISION REQUIRED: accept-as-sent (eligible 08-28) or flag-and-hold (no follow-up ever).

---

## 2026-08-14 — RES.007 Outreach: Christian de Ronde (Invariant Structural Value)

**Paper:** *Invariant Structural Value: Fundamental Constants and Formulas as Invariant Relations* — DOI **10.5281/zenodo.21929902** (v0.3, 2026-08-14)
**Sender:** rowan.quni@qnfo.org (qnfo.org Email Sending verified working; full SPF/DKIM/DMARC)

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | Status | Sent (UTC) |
|---|-----------|--------------|---------------------|------------------|------------|--------|------------|
| 1 | Christian de Ronde | VERIFIED from arXiv source tarball 2306.13975 (`cderonde@gmail.com` in de_Ronde_-_Bohr_Anti-Realist_Realism.tex) | Bohr's Anti-Realist Realism in Contemporary (Quantum) Physics and Philosophy (2306.13975) | Symmetric-audit constraining literature for claim C2 (anti-realist vs structural-realist readings of same formalism); adversarial validation invited | 05d503f4-eab3-41e1-ac4d-dde99a9ec57a | sent | 2026-08-14T07:48:01Z |

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=137 rwnquni@outlook.com (own mailbox), message_id 60c60f6f-1c22-4344-ad56-f781fda4b176, 2026-08-14T07:47:58Z, status=sent.

**Excluded per protocol (no email in arXiv source tarball — CONNECTION-POINT-UNVERIFIED-1):** De Haro & Butterfield (2508.01616 — 41-entry tarball, no contact email in source), Knuth (1504.06686 — PDF-only source), Rovelli (1805.10602 — PDF-only source). Flagged verify-before-send for a future round.

**Send verification (Tool-Call Execution Mandate):** Both sends confirmed in D1 `emails` table via GET /emails/recent: id=137 (rwnquni@outlook.com, status=sent), id=138 (cderonde@gmail.com, status=sent). Canonical sent-classification rule satisfied (sender qnfo domain + recipient).

**Dedup check (no-repeat-contact mandate):** de Ronde has ZERO prior contacts in this log and D1. First contact.

**Follow-up eligibility:** earliest 2026-08-14T07:48Z → first follow-up eligible **2026-08-24** (10d), one max, pending response.
