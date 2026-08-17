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


---

## 2026-08-15 — Proactive outreach (user mandate 2026-08-15: proactive + dedup + master list; REVERSES v2.18 detection-only)

**User mandate (2026-08-15):** "BE MORE PROACTIVE REACHING OUT TO RESEARCHERS... initiate contact with high-value, highly relevant researchers (only 1 email per researcher/name/email, never contact the same email twice unless replying). Keep a master list for coordination across all scheduled tasks/LLM processes. Only surface actionable followup requiring user decision. Good vibes only." This REVERSES the v2.18 detection-only mandate (2026-08-13). Frontmatter `autonomous` set back to `true`.

**Papers + contacts (3 sent, all NEW, emails VERIFIED from arXiv source tarballs):**

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | D1 id | Status |
|---|-----------|--------------|---------------------|------------------|------------|-------|--------|
| 1 | Enrico Santamato (INFN Naples) | VERIFIED from arXiv source 2511.13360 (`enrico.santamato@na.infn.it` in 2025_-_Spin_statistics.tex) | The Intrinsic Angular-Momentum of Particles and the spin-statistics connection (2511.13360) | Spin-statistics from intrinsic angular momentum vs the Boson/Fermion structural-invariant reading | 2f6cbceb-e8fa-4291-a9d5-e4be5706c0da | 154 | sent |
| 2 | Mahdi Naser-Moghadasi (brightmind-ai) | VERIFIED from arXiv source 2605.17831 (`mahdi@brightmind-ai.com`) | Agentic Cost-Aware Query Planning with Knowledge Distillation (2605.17831) | Cost-aware agentic planning = the same quantity JPCUB joules-per-solution formalizes | b3237b72-e23e-4422-8db8-42792d15ce27 | 155 | sent |
| 3 | Aske Plaat (Leiden) | VERIFIED from arXiv source 2503.23037 (`aske.plaat@gmail.com` in agenticllm4.tex) | Agentic Large Language Models, a survey (2503.23037) | Agentic-LLM taxonomy + joules-per-solution efficiency axis | 21386c58-5567-4637-976a-d3bd450e576e | 156 | sent |

**Paper 1 target:** *The Boson/Fermion Distinction: Spin-Statistics as Structural Invariant* — DOI 10.5281/zenodo.21944401 (2026-08-15).
**Paper 2 targets:** *Joules-per-Solution for Stochastic and Agentic Inference: Benchmarking Frontier and Agentic LLMs Against the Human Brain* — DOI 10.5281/zenodo.21944533 (2026-08-15).

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=153 → rwnquni@outlook.com (own mailbox), message_id a8954ee1-a9d8-4b67-9b03-85e35317f737, status=sent.

**Verified but NOT contacted (single-contact-per-group, outreach-strategy §1):**
- Francesco De Martini (francesco.demartini2@gmail.com, co-author of 2511.13360 with Santamato).
- Faezeh Ghederi (faezeh.ghederi@mavs.uta.edu, co-author of 2605.17831 with Naser-Moghadasi).

**CONNECTION-POINT-UNVERIFIED-1 (no email in source tarball, deferred):**
- Inference-Time Agentic Decision Rules Beat Longer Evolving Search (2607.27564) — source had NO emails.
- Agentic Reasoning for LLMs (2601.12538, 30-author survey) — no author emails in source.

**Dedup check (no-repeat-contact mandate):** all 3 verified against D1 master list (32 external recipients, ids 1-152). Zero prior contact. First contact each.

**Follow-up eligibility:** Santamato / Naser-Moghadasi / Plaat → first eligible **2026-08-29** (14d), one max each, pending response.


---

## 2026-08-15 — Delivery-monitoring note (SOFT-1 / MESSAGE-ID-NE-DELIVERY-1 remediation)

- 200 + message_id = ACCEPTED by the worker (crypto.randomUUID), NOT delivery proof (MESSAGE-ID-NE-DELIVERY-1).
- D1 `status=sent` remains the canonical send verification (Tool-Call Execution Mandate).
- Read-only Cloudflare Email Sending REST checks run 2026-08-15:
  - limits: {"quota": {"value": 1000, "unit": "day"}, "usage": {"sent": 5, "over_quota": false, "resets_at": "2026-08-15T21:03:46Z"}}
  - suppression list: 0 suppressed (empty = healthy); items: []
- Per-message delivery events are not queryable via CF REST without a delivery webhook. SOP: run the deliverability
  checks (cloudflare-email-service references/deliverability.md) weekly as part of Daily/Weekly ops, and re-verify
  engagement for Santamato / Naser-Moghadasi / Plaat at the 2026-08-29 follow-up window.


---

## 2026-08-16 — Proactive outreach (daily briefing session; user mandate 2026-08-15 stands)

**Paper 1 target:** *The Exchange Phase as a Logical Scalar: R = e^(2 pi i s) from the Re-Entrant Calculus* — DOI **10.5281/zenodo.21963930** (v1.1, 2026-08-16).
**Paper 2 target:** *The Boson/Fermion Distinction: Spin-Statistics as Structural Invariant* — DOI **10.5281/zenodo.21962904** (v1.5, 2026-08-16).

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | D1 id | Status |
|---|-----------|--------------|---------------------|------------------|------------|-------|--------|
| 1 | Louis H. Kauffman (UIC) | VERIFIED from arXiv source tarball 2605.29246 (`loukau@gmail.com` in ws-rv9x6.tex) | The Q-Calculus: A Quaternion-Based Laws of Form System (2605.29246) | Q-Calculus LoF extension ↔ Exchange-Phase paper's re-entrant-mark derivation; Kauffman's mark-to-fermion-algebra (1301.6214) cited as closest prior art | c83eba9b-9e94-4fb1-a414-c1fb06eaafe1 | 168 | sent |
| 2 | Matthias Thamm (Leipzig) | VERIFIED from arXiv source tarball 2606.24831 (`thamm@itp.uni-leipzig.de` in main.tex) | Anyon Exchange Phase from Antidot Interferometry (2606.24831) | Bare anyon exchange-phase extraction ↔ R = e^(2 pi i s) as structural invariant | 61e35236-0da1-44d8-8439-d576e7cefacb | 169 | sent |
| 3 | Yu-An Chen (Peking U) | VERIFIED from arXiv source tarball 2607.02280 (`yuanchen@pku.edu.cn`, contact author in main.tex) | Bockstein braiding statistics (2607.02280) | Universal statistical-process invariants ↔ exchange-phase/topological-spin invariant | 19d12f3f-8ef2-481b-a8cb-8acc95d901e6 | 170 | sent |
| 4 | Kejun Liu (Soochow U) | VERIFIED from arXiv source tarball 2607.11867 (`kjliu@suda.edu.cn` in main.tex) | Paraparticles intrinsically exhibit Hardy-space breakdown (2607.11867) | Non-unitary exchange statistics testability ↔ boson/fermion dichotomy as derived shadow | 9380d117-d38f-44e7-848d-fe3573264835 | 171 | sent |

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=167 → rwnquni@outlook.com (own mailbox), message_id a382aa10-7494-40f9-8a27-3b5aaac7073b, 2026-08-16T08:09:19Z, status=sent. Send-guard scripted gate passed (exit 0).

**Verified but NOT contacted (single-contact-per-group, outreach-strategy §1):** Arthur M. Collings (otter@mac.com, co-author of 2605.29246 with Kauffman); Felix Puster / Bernd Rosenow (Leipzig co-authors of 2606.24831); Po-Shen Hsin (co-author of 2607.02280).

**CONNECTION-POINT-UNVERIFIED-1 (no email in source tarball, deferred):** Zhiyuan Wang / Kaden Hazzard (2607.26351 R-parastatistics — no emails in tarball, excluded).

**Send verification (Tool-Call Execution Mandate):** all 5 rows confirmed in D1 via GET /emails/recent: ids 167-171 status=sent. Canonical sent-classification rule satisfied (sender rowan.quni@qnfo.org + external recipient).

**Dedup check (no-repeat-contact mandate):** all 4 verified against contact-ledger.md (34 entries) + D1 master list (ids 1-166). Zero prior contact. First contact each.

**Follow-up eligibility:** Kauffman / Thamm / Yu-An Chen / Kejun Liu → first eligible **2026-08-30** (14d), one max each, pending response.


---

## 2026-08-16 — QPL 2026 registration logistics (NOT research outreach; conference-logistics contact)

**Context:** User found QPL 2026 registration CLOSED on aanmelder.nl ("Registration has been closed by the organizers", no waitlist/subscribe). Conference starts 2026-08-17 08:45 (UvA Roeterseiland campus, Nieuwe Achtergracht 168-184).

**Contact:** Kevin Koenrades (UvA events coordinator, QPL 2026 Organising Committee) — email **VERIFIED from live UvA profile page** (uva.nl/en/profile/k/o/k.koenrades/, `K.Koenrades@uva.nl`). NOT a research contact — excluded from research contact ledger; classified as conference-logistics.

| # | Recipient | Email source | Subject | Message ID | D1 id | Status |
|---|-----------|--------------|---------|------------|-------|--------|
| 1 | Kevin Koenrades (UvA) | VERIFIED from UvA profile page | QPL 2026 - registration closed, inquiry about late/on-site attendance options | d2203614-f172-48a7-8e01-3e99ebd3374f | 174 | sent |

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=173 → rwnquni@outlook.com (own mailbox), message_id f5e2ecae-c7bf-48b5-bfa5-3bed2cd1ecd1, status=sent. Send-guard scripted gate passed (exit 0).

**Ask:** (1) on-site/late registration possible? (2) waitlist? (3) day-attendance arrangement? Full late rate EUR 360 offered. User is Amsterdam-based (zero travel).

**Send verification (Tool-Call Execution Mandate):** ids 173+174 confirmed status=sent via GET /emails/recent.

**Follow-up eligibility (SUPERSEDED by the UPDATE below — reply received 2026-08-17, thread closed, no follow-up sent):** if no reply within 3 days → one follow-up 2026-08-19 (conference days 2-3), then archive (no-repeat-contact discipline). On-site registration desk opens Mon 08:45-09:30 — user can also try walk-up.

**UPDATE (2026-08-17):** REPLY RECEIVED id=192 (received_at 2026-08-17T14:00:12Z) — Zara Eijkman, UvA Conferences & Events (congresbureau@uva.nl): "The registration form is closed as the conference has commenced; however, I have now manually opened it. Kindly register using the following link: https://www.aanmelder.nl/174107/registration. Please note that it is no longer possible to pay via invoice." **USER ACTION: register at the link (EUR 360 full rate, card payment — no invoice).** Courtesy thank-you reply sent in-thread id=194 (message_id d81a96a7-35fb-4819-9bec-66cf2f3ff42a, status=sent; test-pair id=193 → rwnquni@outlook.com, message_id e9ea9378-93f3-4f92-bfba-f817ffc68c5d, status=sent — TEST-SEND-EXTERNAL-1 compliant, send-guard exit 0). id=192 auto-marked replied. Follow-up not needed; thread closed (no-repeat-contact discipline: no further contact to UvA logistics unless user asks).

**Alternative channels verified (unused):** Stephanie Mak (s.n.mak@uva.nl, UvA events coordinator — second coordinator, NOT contacted to avoid double-contact of the same organising group); PC chair John van de Wetering (j.m.m.vandewetering@uva.nl — deliberately NOT used: high-value ZX research target, one-email rule preserved).

---

## 2026-08-17 — Kauffman reply + proactive outreach batch (CST / Exchange Phase / B-F papers)

**REPLY RECEIVED (Type 1: Positive/Engaged) — Louis H. Kauffman (loukau@gmail.com, id=181, 2026-08-17T10:03Z):** "Thank you for your letter. I shall look at your papers and get back to you." Shared 3 works (Fibonacci model phases; Chubb–Eskandarian–Harizanov; knot-logic/Majorana note). His viewpoint: all number systems (Cayley–Dickson, Clifford algebras, more) emerge from the LoF distinction framework; exact phases of models like the Fibonacci model arise naturally mathematically, but physics (e.g., Quantum Hall Effect) needs deeper understanding. **Handled autonomously** (courtesy + substantive reply, thread kept alive, ball left in his court).

**Paper targets:** (1) *Configuration-Space Topology and the Distinction Calculus: The Exchange Scalar, Its ±1 Shadow, and a Pre-Registered Derivation Program* — DOI **10.5281/zenodo.21962450** (v0.3; verified via Zenodo search API + doi.org 2026-08-17); (2) *The Exchange Phase as a Logical Scalar* — DOI **10.5281/zenodo.21964104** (verified via doi.org); (3) *The Boson/Fermion Distinction: Spin-Statistics as Structural Invariant* — DOI **10.5281/zenodo.21962904** (verified via doi.org).

**Sender:** rowan.quni@qnfo.org (canonical academic sender; qnfo.org Email Sending restored since 2026-08-10).

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | D1 id | Status |
|---|-----------|--------------|---------------------|------------------|------------|-------|--------|
| 1 | Louis H. Kauffman (REPLY to id=181) | in-thread (loukau@gmail.com) | — | Acknowledges his LoF-number-systems viewpoint + Quantum-Hall open direction; no new pitch | 15804aec-5622-45c1-821d-fa131747787b | 188 | sent (181 replied) |
| 2 | Byung Hee An (Kyungpook Nat'l U) | VERIFIED from arXiv source tarball 2608.14350 (`anbyhee@knu.ac.kr` in goldberg_extension_notes.tex) | Extending Goldberg's Exact Sequence to Braid Groups of Graphs and Simplicial Complexes (2608.14350) | Graph configuration spaces as counter-literature ↔ CST paper's scaffold-boundary map | 28518f0b-dce3-415a-a77b-ef773ba90d85 | 189 | sent |
| 3 | Moty Heiblum (Weizmann) | VERIFIED from arXiv source tarball 2608.12897 (`Moty.Heiblum@weizmann.ac.il`) | Observation of Time-Domain Braiding of Non-Abelian Anyons at ν=5/2 (2608.12897) | Measured braiding phase ↔ R = e^(2πis) as logical scalar | fa7fc6d2-b6c8-4742-bcb1-c71d018964e5 | 190 | sent |
| 4 | Eric Kubischta (Florida State) | VERIFIED from arXiv source tarball 2608.06339 (`ekubischta@fsu.edu`) | Nuclear-Spin Statistical Weights from Young Diagrams (2608.06339) | Young-diagram statistical weights ↔ B/F dichotomy as derived shadow | fb105ebe-0b1a-4cec-9d9a-434029622f2a | 191 | sent |

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=187 → rwnquni@outlook.com (own mailbox), message_id 137a84df-8903-4779-8520-e43573ce5f3a, status=sent. Send-guard scripted gate passed (exit 0). Preview body contained all 4 payloads.

**Verified but NOT contacted (single-contact-per-group, outreach-strategy §1):** Ian Teixeira (iteixeira@ucsd.edu, co-author of 2608.06339); Tomer Alkalay / Jinhong Park / Minseong Oh / Changki Hong (co-authors of 2608.12897 — Heiblum is the single contact for that group).

**CONNECTION-POINT-UNVERIFIED-1 (no email in source tarball, deferred):** Chetcuti/Goldman/Vignolo/Minguzzi (2608.05290), Schafer-Nameki/Zheng/Antinucci (2608.12303), Cohen/Pakianathan (2606.17193), Kita (2512.12071), Xue (2607.06279), Buican/Huston/Pachos (2607.10181) — no author emails in sources; excluded.

**Send verification (Tool-Call Execution Mandate):** ids 187-191 confirmed status=sent via GET /emails/recent; id=181 auto-marked status=replied (reply_to_id). Canonical sent-classification rule satisfied (sender rowan.quni@qnfo.org + external recipient).

**Dedup check (no-repeat-contact mandate):** all 3 new contacts verified against contact-ledger.md (38 entries → 41) + D1 master list. Zero prior contact. First contact each.

**Hygiene (same-session, verified in D1):** id=178 (jkoti9086@gmail.com, GRANJA JOURNAL predatory solicitation) → spam; ids 139/150/140/162 (newsletter + CF platform notices, incl. duplicate Workbench-legacy notice) + briefing bounces 186/179/165/151 + DMARC reports 182/177/176/175/172/163/161/157 → archived; id=164 (GitHub OAuth figshare notice) → read (kept visible — surfaced in closeout).

**Follow-up eligibility:** An / Heiblum / Kubischta → first eligible **2026-08-31** (14d), one max each, pending response. Kauffman: ACTIVE thread — no follow-up needed.

---

## 2026-08-17 — RED-TEAM REMEDIATION (direct parent-agent audit of the 08-17 batch; 0 HARD / 2 SOFT / 1 DESIGN)

**Verdict:** 0 HARD compliance violations (all 8 hard rules verified: one-email-per-researcher, ledger+D1 dedup, tarball-verified emails, test-send-first id=187 with send-guard exit 0, rowan.quni@qnfo.org sender, cap 4/5, single-contact-per-group, full logging + D1 verification). Both SOFT findings remediated/documented below.

**SOFT-1 — D1 ids 183/184 deleted-row gap (window 2026-08-17T10:17–10:37Z):** ids 183 and 184 absent from /emails/recent (between id=182 google DMARC 10:17 and id=185 briefing 10:37) and return HTTP 404 on /emails/body — deleted rows, same class as the documented ids 107-110 gap (2026-08-12). No API access to deleted rows; documented, no further action possible. Most plausible origin: briefing-pipeline staging rows or concurrent-session worker operations (concurrent skills-update commits 405f383/d7e92b1 today). Risk assessed LOW (no evidence of missed human inbound; all external threads accounted for).

**SOFT-2 — leftover processed DMARC reports (08-14):** ids 141/148/149 (Google/Microsoft DMARC, qwav.tech, arrived 08-14 after that day's hygiene run) remained status=processed and would have been re-surfaced. PATCHed → archived 2026-08-17, re-verified: ZERO rows remain in received/processed. Non-terminal set now = id=131 (Mercatus EV, user action pending — kept read/visible) + id=164 (GitHub OAuth figshare, user decision pending — kept read/visible) only.

**DESIGN-1 — Exchange Phase DOI version consistency (informational):** prior batch (Kauffman/Thamm/Yu-An Chen, 08-16) cited 10.5281/zenodo.21963930 (v1.1); today's Heiblum email cites 10.5281/zenodo.21964104 (current version per QNFO paper DB). Both resolve via doi.org; Kauffman thread remains on the v1.1 DOI. Future batches: cite the QNFO DB-canonical DOI (21964104) for new sends.

**Accuracy cross-check (CONNECTION-POINT-UNVERIFIED-1):** all connection points re-verified post-send — An (Goldberg strand map + graph config spaces as counter-literature in CST abstract), Heiblum (ν=5/2 braiding observation; R = e^(2πis) framing matches Exchange Phase abstract), Kubischta (2608.06339 abstract fetched 2026-08-17: permutation symmetry of identical nuclei, Schur-Weyl + Young tableaux → statistical weights — matches the email's claim that the paper shows which permutation representations are realized for composite systems of given nuclear spin). Kauffman reply quotes only his own email + the paper abstract. All DOIs resolve (doi.org 200).
