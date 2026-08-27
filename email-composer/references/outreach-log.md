# QNFO Outreach Log

Log of all outbound outreach sends via the qnfo-email Worker /send endpoint.
Per research skill v2.88: log recipient, status, message_id. D1 `emails` table is the authoritative record.

---

## 2026-08-10 — Batch 1: Qudit Advantage paper-sharing (Monday scan)

**Paper:** *The Qudit Advantage: System-Level Joules-per-Solution Comparison of a Qudit Architecture Against 17 Conventional Platforms* — DOI **10.5281/zenodo.21827737** (2026-08-06)
**Sender:** rowan.quni@qwav.tech (NOTE: qnfo.org Email Sending is broken platform-side — CF error 10002 email.sending.error.internal_server on ALL qnfo.org addresses, verified via Worker binding + REST API + wrangler CLI 2026-08-10; qwav.tech/qwav.org verified working with full SPF/DKIM/DMARC. Qudit Advantage is QWAV-branded JPCUB work, so qwav.tech sender is thematically consistent. FLAGGED for user awareness; switch back to rowan.quni@qnfo.org when Cloudflare resolves.)

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | D1 id | Status | Sent (UTC) |
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


---

## 2026-08-17 (evening) — Proactive outreach: Klaas Landsman (Entropy lectures → Measurement Stratigraphy)

**NEW CONTACT (1 of remaining daily cap).** Sender: rowan.quni@qnfo.org (canonical).

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | D1 id | Status |
|---|-----------|--------------|---------------------|------------------|------------|-------|--------|
| 1 | Klaas Landsman (Radboud Univ.) | VERIFIED from arXiv source tarball 2608.14523 (`landsman@math.ru.nl` in author block of OLEv1.tex) | The Okinawa Lectures on Entropy (2608.14523) | Relative-entropy-first structure (Shannon/vN as special cases with uniform prior) + modular theory for subsystem relative entropy ↔ Measurement Stratigraphy's conditional "Entropic Enclosure" forecast (priors as first-class citizens; Gaussian e^{−πx²} as Fourier-invariant uncertainty shape); type III no-canonical-prior obstruction question | 69419064-da1f-4863-8b4c-d871d95a0209 | 196 | sent |

**QNFO paper cited:** The History and Future of Measurement Stratigraphy, Number Theory, and Valuation Theory — DOI **10.5281/zenodo.21705220** (v3.0; verified via Zenodo API 2026-08-17: title + creator Quni-Gudzinas, Rowan Brad).

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=195 → rwnquni@outlook.com (own mailbox), subject "[PREVIEW] Re: The Okinawa Lectures on Entropy — ...", message_id 4f314e00-cd61-4021-b2b2-63a07a7a7f9b, status=sent. Send-guard scripted gate: `--mode test` exit 0; `--mode send` warning-only for external recipient (expected; identity tarball-verified).

**Dedup check (no-repeat-contact mandate):** ledger 41 entries + D1 probes (`q=landsman`, `q=math.ru.nl` → count:0; recent-100 scan clean of ru.nl). Zero prior contact. First contact. Also NOT contacted (single-contact-per-group, §1): Riccardo Rossi (co-author of 2608.14476 — Carleo group, not pursued this cycle; Carleo 2608.14476 considered + deferred: two-determinant/antisymmetry-cost connection to B/F Distinction judged weaker than Landsman's stratigraphy resonance).

**Daily cap accounting 2026-08-17:** 4 new outreach sends (An 189, Heiblum 190, Kubischta 191, Landsman 196) + in-thread replies (Kauffman 188, UvA 194) + 3 test/preview sends (187, 193, 195). New-outreach count 4/5 ≤ cap. No further outreach today.

**Send verification (Tool-Call Execution Mandate):** ids 195-196 confirmed status=sent via GET /emails/recent (canonical sent-classification: sender rowan.quni@qnfo.org + external recipient).

**Follow-up eligibility:** Landsman → first eligible **2026-08-31** (14d), one max, pending response.


---

## 2026-08-18 — Batch: Locale Framework paper-sharing (UMP.012 p4, QPL 2026 boundary authors — wave 1)

**Paper:** *Locale Framework Applied to Quantum Computing Innovations & Practical Applications* — DOI **10.5281/zenodo.21991270** (v0.4; concept 10.5281/zenodo.21985455)
**Sender:** rowan.quni@qnfo.org (canonical, restored 2026-08-10)
**Cycle:** CMD CONTINUE 2026-08-18, session xVlb7IkMioxr4yIUx366M (UMP.012 p4 outreach — first wave of the post-publication red-team remediation)

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | Status | Sent (UTC) |
|---|-----------|--------------|---------------------|------------------|------------|--------|------------|
| 1 | Alex Maltesson | VERIFIED from arXiv source tarball 2510.08546 (`maltesson.alex@gmail.com`) | Equivalence of CV/DV gate-based QC with finite energy (2510.08546, QPL 2026 plenary) | Their theorem epsilon <= 1286 K n^2 E*^2 / sqrt(d) anchors Table 1 rows 1-2 (energy seam); constant re-verified against the arXiv full text 2026-08-18 (citation-audit SOFT flag CLOSED) | b7a9470c-1763-4972-bad6-cb0a3b4df4f9 | 202 | sent | 2026-08-18T08:48:59.031Z |
| 2 | Manuel Mekonnen | VERIFIED from arXiv source tarball 2502.17576 (`manuel.mekonnen@oeaw.ac.at`) | Invariance under quantum permutations rules out parastatistics (2502.17576) | Table 1 "statistics could be non-standard" boundary + Section 7 Statistics | 4fdd00d0-e7b5-4cc0-8ff8-7902f508344f | 203 | sent | 2026-08-18T08:49:02.087Z |
| 3 | Timothée Hoffreumon | VERIFIED from arXiv source tarball 2603.19208 (`t.hoffreumon@gmail.com`) | Real-valued quantum theory cannot be experimentally falsified (2603.19208) + Quantum theory does not need complex numbers (2504.02808) | Table 1 "complex amplitudes are essential" boundary + Section 7 Real-valued QT | ca891357-829e-459e-889a-34cce503f970 | 204 | sent | 2026-08-18T08:49:05.401Z |

**Test-send:** id 201 `rwnquni@outlook.com` [PREVIEW] (own mailbox first, TEST-SEND-EXTERNAL-1) — message_id b038f76c-3eef-405c-a55b-a284961a2ea3.
**Dedup:** contact-ledger.md + D1 `emails` checked BEFORE send — zero prior contact for all 3 recipients (first-contact wave; single contact per group — Calcluth/Rodung same paper as Maltesson NOT contacted).
**Daily cap:** 3 sends (cap 3-5) — 2026-08-18 had zero prior outbound sends.
**Paper-share pre-flight:** DOI-archived ✓ (21991270 v0.4, DataCite findable); 3 verified researchers ✓; personalized connection points ✓; DB-canonical current-version DOI cited ✓.
**Incident (non-send):** first POST attempt 403/1010 Cloudflare BIC — Python client lacked browser User-Agent (VECTORIZE-403-MISDIAGNOSIS class). Fixed with browser UA; ZERO emails lost (all 403s were edge-blocked, nothing reached the Worker).
**D1 verification:** ids 202-204 status=sent ✓ (API 200 was the first signal, D1 read-back the last — Tool-Call Execution Mandate).
**Deferred pool (verify-before-send, wave 2):** Brenner/Dias/Koenig (2509.18854 — no email in source tarball); Deaconu/Gargava/Kalra/Mosca/Yard (2510.11526, IQC Waterloo — group contact policy); Koch (QPL 2026 talk, not on arXiv yet); Calcluth et al. GKP (same group as Maltesson). **HALTED 2026-08-18 (user directive):** do NOT email anyone who may be at QPL 2026 while the user is attending in person (confusing/embarrassing to email + meet in person); wave 2 frozen until after the conference (~2026-08-22), then re-evaluate against in-person contacts actually made.
**Follow-up eligibility:** 14-21 days after send → window opens 2026-09-01, closes 2026-09-08. ONE follow-up max, only on silence.
**Log note:** this section is UNCOMMITTED pending the concurrent session's ledger/log commit (GIT-OWNERSHIP-1 — the files carry another session's uncommitted outreach work; no mixed commit made).

---

## 2026-08-18 — Wave 2: in-thread replies (Heiblum, Landsman) + new outreach (Camino, Jipdi)

**Sender:** rowan.quni@qnfo.org (canonical per mandate) — NOTE/ERRATA: `/send` payloads omitted `from:` so the Worker defaulted to qnfo@qnfo.org (D1 sender column shows qnfo@qnfo.org for ids 214-218; wave 1 ids 202-204 show rowan.quni@qnfo.org because that session passed `from` explicitly). All 4 recipients still received mail from a canonical qnfo.org address with full SPF/DKIM/DMARC; **absorbed as errata, NO resend** (no-repeat-contact mandate — same class as v2.21 EMAIL-SIGNATURE-PLAIN-1 handling). Future `/send` calls MUST pass `"from": "rowan.quni@qnfo.org"`.
**Cycle:** CMD CONTINUE 2026-08-18 (email+outreach agent, session tfRpmza-s0y5lUQXnWczm); QPL HALT respected — both new recipients are definitively non-QPL (UCL chemistry consortium; Cameroon EP-braiding group).

### In-thread replies (not counted against daily outreach cap)

| # | Recipient | Replied to | Classification | Thread reply | Message ID | D1 id | Status |
|---|-----------|-----------|----------------|--------------|------------|-------|--------|
| 1 | Moty Heiblum (Weizmann) | id=198 (2026-08-18T07:14:33Z, "I am an experimentalist, had difficulty understanding your email... happy to hear it") | Type 1/4-leaning — engaged but jargon-blocked; plain-language rewrite + one experiment-anchored question | RE: Time-domain braiding of non-Abelian anyons at nu=5/2 — exchange phase as a logical scalar | 4a220bbd-9a42-4159-a786-543ee32fc37c | 215 | sent |
| 2 | Klaas Landsman (Radboud) | id=199 (2026-08-18T07:32:42Z, "thanks! I will try to take a look at this as soon as possible") | Type 4 (I'll Read It Later) — courtesy acknowledgment, no follow-up ever | Re: The Okinawa Lectures on Entropy — relative entropy and the 'entropic enclosure' question | 94cd6237-4813-4971-90d1-8b52727810a8 | 216 | sent |

**Follow-up eligibility:** Heiblum + Landsman follow-up lines (would have opened 2026-08-31) **SUPERSEDED by these replies** (THREAD-RESOLUTION-SUPERSEDED-1) — do NOT schedule follow-ups for either.
**Status update:** id=198 + id=199 PATCHed to status=replied (verified 200 + read-back).

### New outreach (wave 2 — cap accounting: 3 used by wave 1 + 2 here = 5/5 at cap)

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | D1 id | Status |
|---|-----------|--------------|---------------------|------------------|------------|-------|--------|
| 1 | Bruno Camino (UCL Chemistry, first + corresponding author) | VERIFIED from arXiv source tarball 2608.16568 (`b.camino@ucl.ac.uk` in author block; also c.r.a.catlow@ucl.ac.uk, scott.woodley@ucl.ac.uk — NOT contacted, single-contact-per-group) | Scientific Applications of Quantum Computing: Challenges and Opportunities (2608.16568, 17-author UK consortium) | Their closing standard — QC valuable only after FULL costs (state prep, measurement, error handling, coupling to classical simulation) — ↔ JPCUB joules-per-solution metric (six cost components, five-phase protocol); open question: single energy accounting across noisy/error-mitigated/early-FT/fully-FT regimes? | 45c0afa1-dacf-4225-bd13-5dd97141def7 | 217 | sent |
| 2 | M. N. Jipdi (U. Bamenda, first author; only email in tarball) | VERIFIED from arXiv source tarball 2608.15829 (`jmichaelnicky@yahoo.fr`) | Topologically Protected Learning from Exceptional Point Braiding: Toward Braid Programming (2608.15829) | Their braid-programming reformulation (discrete search over braid group replacing gradient descent) ↔ Exchange Phase as a Logical Scalar (R = e^(2πis) = (e^(iπ))^(2s) = (−1)^(2s); phase gates in their a=0 case as instances of the scalar family); open question: is their EP braiding phase quantized per R = e^(2πis) or path-dependent? | 64378bbd-0d91-44dd-9da9-f30bdee8afdc | 218 | sent |

**QNFO papers cited (DB-canonical current-version DOIs):** JPCUB P0 "The Joules-per-Solution Metric..." = 10.5281/zenodo.21637028; "The Exchange Phase as a Logical Scalar" = 10.5281/zenodo.21964104.

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=214 → rwnquni@outlook.com "[PREVIEW] reply batch (Heiblum, Landsman) + outreach batch (Camino, Jipdi)", message_id 7fa143aa-1161-4cf8-bebe-de1a7e06ff12, status=sent (verified). Scripted guard: `--mode test` exit 0; `--mode send` warning-only for the 4 external recipients (expected — identities tarball-verified).

**Dedup:** contact-ledger.md (47 entries post-update) + D1 searches (q=camino, q=jmichaelnicky, q=jipdi, q=yahoo.fr, q=ucl.ac.uk → all count:0) + recent-100 scan clean. Zero prior contact for Camino + Jipdi. First contacts.

**QPL HALT compliance:** Camino (UCL chemistry/materials consortium) and Jipdi (Cameroon EP-braiding group) are definitively NOT QPL 2026 attendees — halt respected; frozen pool (Koch, Calcluth/GKP, Deaconu/Mosca/Yard, Brenner) untouched.

**D1 verification (Tool-Call Execution Mandate):** ids 214-218 status=sent via GET /emails/recent read-back; id=198/199 status=replied.

**Follow-up eligibility:** Camino + Jipdi → window opens 2026-09-01, closes 2026-09-08 (14-21d). ONE follow-up max, only on silence. No prior follow-ups.

**Inbox hygiene note (non-actionable):** id=164 GitHub OAuth notice (figshare app authorized 08-16) — informational/benign per user's own workflow; id=213 (rowan@qnfo.org → iocph2026@mdpi.com, IOCPh 2026 late-abstract) is another session's send, not outreach, no action.

### RED-TEAM ADDENDUM (2026-08-18, POST-PUBLICATION ADVERSARIAL ANALYSIS GATE — 3-parallel reviewer audit of this wave)

**Verdict: 0 HARD across all three reviewers; each PASS-WITH-SOFT-FINDINGS. No resend, no repair-send (content delivered cleanly).**

| Reviewer | Delegation | Verdict | Key findings |
|---|---|---|---|
| Accuracy | nejE4O3EBlVY36QnXa6YS | PASS-WITH-SOFT | All checkable claims VERIFIED (R=e^{2πis} verbatim; C's 6 components/5-phase/14 benchmarks verbatim; D's braid-search/a=0/invariants verbatim). SOFT: C adds "only when" over abstract's "when" (necessity reading, defensible); E4 identity not in reviewer's truncated quote — parent-verified: full abstract contains "R = (e^{iπ})^{2s} = e^{2πis} = (−1)^{2s}" verbatim. Parent resolutions: JPCUB P0 DOI 21637028 = DB record ✓; Exchange Phase 21964104 = DB-canonical per skill v2.21 rule ✓ (v1.3 frontmatter 21964359 is version-level, watch item); arXiv:2608.12897 = Heiblum nu=5/2 ✓ (08-17 ledger row). |
| Completeness | w2TKAyAeY6aKSWNTrL1Ua | PASS-WITH-SOFT | Heiblum's 3 raised elements (experimentalist / difficulty / invite comments) all addressed element-by-element; Landsman's 2 elements addressed; question answerable from lab experience alone; "whenever" = courtesy not pressure; no dangling obligations; no forced second round. SOFT: cosmetic jargon residue in E1 ("by-products of the algebra", "core scalar of the theory") after "plain terms" promise. |
| Dependency/Tone (Turing test) | fFeVsWoBkYRGEGWCtdru8 | PASS-WITH-SOFT | Turing 7/8/7/7 (E1-E4); reply probabilities: Heiblum MEDIUM, Landsman LOW, Camino MEDIUM, Jipdi MEDIUM-HIGH. No flattery/pressure/name-dropping; correct non-condescension to Global-South recipient. LLM-tells (future-draft fixes): recurring "One question…" opener; recurring "I would be glad to hear/expand…" closer + hedge-stacks; E1 8× length asymmetry vs 27-word inbound; apology partially performative; E3 "we" from solo signatory; E4 "re-entrant mark" un-onboarded. |

**Direct answer to user's Turing-test challenge:** yes-with-reservations — per-email content is human-grade and specific to each recipient's actual work; the corpus-level template skeleton (shared opener/closer patterns) is the only detectable tell. Fixes apply to FUTURE drafts only (listed in SKILL.md v2.23 banner + .kaizen_history).
**Watch items (no action now):** (1) never follow up Heiblum or Landsman — eligibility permanently CLOSED (only permitted future contact: in-thread plain-terms simplification if Heiblum reports continued difficulty); (2) "Re:" prefix on cold outreach = thread-mimicry/spam watch, template-consistent, policy change = user decision; (3) Exchange Phase DOI version identity (21964359 vs 21964104) to resolve at next pre-flight; (4) register-matching (e.g., "Hi Moty" on informal inbound) = sender-preference question for the user.
**Skill update:** SKILL.md bumped v2.22 → v2.23 (DEFAULT-SENDER-DRIFT-1 + LLM-tell list + design watches), .kaizen_history entry appended. UNCOMMITTED per GIT-OWNERSHIP-1 (working tree carries concurrent sessions' edits; commit belongs to the skills-update owner).


---

## 2026-08-19 — Batch: QCA Toy Model paper-sharing (daily briefing outreach wave)

**Paper:** *A Computational Toy Model of Non-Local Information Storage in a Quantum Cellular Automaton* — DOI **10.5281/zenodo.21993706** (2026-08-18, most recent QNFO record per Zenodo API)
**Sender:** rowan.quni@qnfo.org (canonical; `from` passed explicitly per DEFAULT-SENDER-DRIFT-1)
**Cycle:** daily briefing 2026-08-19 (this session)

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | D1 id | Status |
|---|-----------|--------------|---------------------|------------------|------------|-------|--------|
| 1 | Jian-Xin Zhong (Shanghai Univ.) | VERIFIED from arXiv source tarball 2605.18622 (`jxzhong@shu.edu.cn` in main.tex author block) | Fibonacci many-body scars in a decorated Rule-54 QCA (2605.18622) | Protected soliton skeleton vs thermalizing complement ↔ toy model's Fredkin-gate non-local storage; question: does protected sector preserve distant-site mutual information under erasure? | c4b0ef49-4bb2-4748-be4b-064b73d257f4 | 229 | sent |
| 2 | Zhong Wang (Tsinghua) | VERIFIED from arXiv source tarball 2606.19430 (`wangzhongemail@tsinghua.edu.cn` in main.tex) | Solving Nonequilibrium Dynamics via Influence Matrix Bootstrap: Floquet-PXP Model (2606.19430) | Hidden-Markov-order memory decomposition (finite-length vs long-range, split-index MPS) ↔ where toy model's erasure-robustness lives; question: would split-index representation classify Fredkin memory as long-range? | 482caa34-5a64-4661-b4f5-c4df4b060169 | 230 | sent |
| 3 | Yao Yao (South China Univ. of Technology) | VERIFIED from arXiv source tarball 2504.14453 (`yaoyao2016@scut.edu.cn` in word_v6.tex) | Quantum cellular automata for word statistics facilitated by quantum correlations (2504.14453) | Entanglement asymmetry as probe of cooperative evolution/scrambling ↔ toy model's entanglement + endpoint mutual information; question: gate-sampling prediction for Fredkin vs SWAP persistence? | 5a512657-9b9d-4911-ad82-b34825db2268 | 231 | sent |

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=228 → rwnquni@outlook.com "[PREVIEW] outreach batch 2026-08-19 (Zhong / Wang / Yao)", message_id 32836f51-d53b-4f54-a364-7f44efa5fdb5, status=sent. Send-guard: `--mode test` exit 0; `--check-recipient` external-forbidden for all 3 (expected — identities tarball-verified).
**Dedup:** contact-ledger.md (47 entries) + D1 searches (q=jxzhong, shu.edu.cn, wangzhongemail, tsinghua.edu.cn, yaoyao2016, scut.edu.cn → all count:0) + recent-100 scan clean. Zero prior contact for all 3. First contacts.
**QPL HALT compliance (08-18 → ~08-22):** all 3 recipients are China-based condensed-matter/QCA groups (Shanghai/Tsinghua/SCUT) — definitively NOT QPL 2026 attendees; frozen pool (Koch, Calcluth/GKP, Deaconu/Mosca/Yard, Brenner) untouched. Precedent: 08-18 wave 2.
**Daily cap:** 3 new outreach sends (cap 3-5) — 2026-08-19 had zero prior outbound. 3/5 used.
**Single-contact-per-group:** 2605.18622 (Li/Zhong → Zhong only), 2606.19430 (Yang/Wang/Wang → Zhong Wang only; whr21@mails.tsinghua.edu.cn NOT contacted), 2504.14453 (Chen/Yao → Yao only). 2602.05914 (Bachmann) + 2509.18103 (Dodgson, Ulam-spiral ML) scanned but NO email in source tarball → deferred verify-before-send, never fabricated.
**Paper-share pre-flight:** DOI-archived ✓ (21993706, DataCite via Zenodo API 200); one-sentence thesis ✓; 3 verified researchers ✓; personalized connection points ✓; DB-canonical DOI cited ✓.
**D1 verification (Tool-Call Execution Mandate):** ids 228-231 status=sent via GET /emails/recent read-back (sender rowan.quni@qnfo.org + external recipients for 229-231).
**Follow-up eligibility:** Zhong / Wang / Yao → window opens 2026-09-02, closes 2026-09-09 (14-21d). ONE follow-up max, only on silence.


---

## 2026-08-20 — Batch: p-adic / discrete-structure cluster paper-sharing (proactive outreach wave)

**Papers:** *The Trapped-Ion Ultrametric Testbed: A Falsifiability Register for Testing p-Adic Structure in Quantum Dynamics* — DOI **10.5281/zenodo.22017933** (2026-08-19); *One Table, Two Regimes: Standard-Model Particles and Condensed-Matter Excitations as Patterns on the Bruhat-Tits Tree* — DOI **10.5281/zenodo.22022313** (2026-08-19)
**Sender:** rowan.quni@qnfo.org (canonical; `from` passed explicitly per DEFAULT-SENDER-DRIFT-1)
**Cycle:** this session (2026-08-20)

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | D1 id | Status |
|---|-----------|--------------|---------------------|------------------|------------|-------|--------|
| R | Amal Whyte (CWI / QuSoft / HoQ) | in-thread reply to inbound id=240 (2026-08-19T15:31) | — (QPL 2026 follow-up) | Tour Thu 28 Aug 10:30 HoQ Amsterdam confirmed; topics: QCA toy model (10.5281/zenodo.21993706) + joules-per-solution metric; asked re CWI/QuSoft meeting arrangement | b359d9c4-46b7-431a-bba5-089d1674b291 | 246 | sent |
| 1 | W. A. Zúñiga-Galindo (UT Rio Grande Valley) | VERIFIED from arXiv source tarball 2607.00198 (`wilson.zunigagalindo@utrgv.edu` in Wigner_Paradox_6.tex) | Wavefunctions localization, and the Wigner's Friend Paradox in a Framework of Discrete-Space Hypothesis (2607.00198) | Discrete-space hypothesis + his p-adic Schrödinger analyses (2410.13048, 2508.06712) and QHCNN pattern formation (2603.27063) ↔ Trapped-Ion Ultrametric Testbed falsifiability register; question: which observable cleanly distinguishes p-adic vs real-valued Schrödinger evolution in an ion trap | c936bffc-af14-4a09-9116-acb11248811a | 247 | sent |
| 2 | Stefano Mancini (Univ. Camerino) | VERIFIED from arXiv source tarball 2601.13808 (`stefano.mancini@unicam.it` in Composing_p_adic_qubits.tex) | Composing p-adic qubits: from representations of SO(3)_p to entanglement and universal quantum logic (2601.13808) | p-adic qubit composition rules (SO(3)_p reps, entanglement, universal logic) ↔ Pattern-Particle Unification claim (particles as patterns on Bruhat-Tits tree, statistics as tree-automorphism phase); question: SO(3)_p measurement basis for discrete-space experiment | d35ac443-46b9-4dfd-9adb-8a2d2fa0b366 | 248 | sent |
| 3 | Tim Palmer (Oxford Physics) | VERIFIED from arXiv source tarball 2601.14941 (`tim.palmer@physics.ox.ac.uk` in HileyRevised.tex) | Impossible Counterfactuals, Discrete Hilbert Space and Bell's Theorem (2601.14941) | Discrete-space framework + impossible counterfactuals ↔ Testbed falsifiability register (whether discrete/p-adic state-space hypotheses differ measurably from continuum at reachable scales); question: predicted measurable deviation a testbed could register | 222578a1-5232-4328-b6b8-d0955145032f | 249 | sent |

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=245 → rwnquni@outlook.com "[PREVIEW] outreach batch 2026-08-20 (Zúñiga-Galindo / Mancini / Palmer)", message_id 54859c20-6116-404c-ad2b-af92a67cd2c9, status=sent (combined preview covering Amal reply + all 3 outreach drafts).
**Dedup:** contact-ledger.md (50 entries) + D1 searches (q=palmer, utrgv, unicam, physics.oxford, zunigagalindo, zuniga, mancini, svampa, winter, jepsen, an+huang, feng+qu, galindo → all count:0) + recent-100 scan clean. Zero prior contact for all 3. First contacts.
**QPL HALT compliance (08-18 → ~08-22):** all 3 recipients are p-adic/discrete-structure researchers (UTRGV Texas / Camerino Italy / Oxford UK) — definitively NOT QPL 2026 attendees (quantum programming languages conf.); frozen pool (Koch, Calcluth/GKP, Deaconu/Mosca/Yard, Brenner) untouched. Precedent: 08-19 wave.
**Daily cap:** 3 new outreach sends (cap 3-5) + 1 in-thread reply (uncapped). 2026-08-20 had zero prior outbound. 3/5 used.
**Single-contact-per-group:** 2601.13808 (Svampa/L'Innocente/Mancini/Winter → Mancini only; ilaria.svampa@uni-koeln.de, sonia.linnocente@unicam.it, andreas.winter@uni-koeln.de NOT contacted).
**Paper-share pre-flight:** DOI-archived ✓ (22017933 + 22022313, DB-canonical); one-sentence thesis ✓; 3 verified researchers ✓; personalized connection points ✓; one paper per email ✓; DB-canonical DOIs cited ✓.
**D1 verification (Tool-Call Execution Mandate):** ids 245-249 status=sent via GET /emails/recent read-back (sender rowan.quni@qnfo.org + external recipients for 246-249); id 240 status=replied (reply_to_id=240 processed by Worker); id 242 status=archived (EA Funds decline absorbed as errata, no email reply — they do not review by email; actionable = TAIF paperform https://av20jp3z.paperform.co/?fund=Transformative AI Fund, user decision).
**Inbound handling this cycle:** id=240 Amal Whyte (Type 1 positive, in-thread reply sent id=246); id=242 EA Funds (Type 2 decline w/ redirect → archived, errata); id=224 MDPI IOCPh (positive: late abstract accommodated via https://sciforum.net/submissions/IOCPH2026/link/3 — original unpublished work only; actionable = user submits abstract, decision); id=241 evalsignal newsletter (processed); 225/220/219 OpenReview duplicate-profile notifications (processed, informational); DMARC reports 244/243/236/233/232/223/222 (processed); 221 spam (processed).
**Sent timestamps (D1 received_at):** 245 preview 06:12:02Z; 246 Amal 06:12:14Z; 247 Zúñiga-Galindo 06:12:15Z; 248 Mancini 06:12:17Z; 249 Palmer 06:12:18Z (all 2026-08-20, preview strictly first per TEST-SEND-EXTERNAL-1).
**Post-audit repair (2026-08-20 red team, Completeness finding):** original append via bash `python -c` consumed backtick-wrapped content (address strings + `from` token) via shell command substitution; repaired via edit tool; verified addresses restored per tarball extraction. Red-team verdicts: Dependency-Tone PASS-WITH-FINDINGS (0 HARD), Completeness COMPLETE-WITH-GAPS (11/12 MET), Accuracy PASS (fallback direct verification: 6/6 arXiv IDs title/author-exact, 3/3 DOIs resolve HTTP 302). No resend, no re-contact.

---

## 2026-08-20 — IOCPh 2026 abstract submission: escalation to MDPI (user mandate: agent owns conference submissions to closeout)

**Context:** MDPI IOCPh 2026 accepted the late abstract request (inbound id=224, 2026-08-19: "submit your abstract via https://sciforum.net/submissions/IOCPH2026/link/3 — original unpublished content only"). User directive 2026-08-20: no manual user actions — agent follows conference submissions through to closeout.
**Attempted (autonomous, failed at captcha):** registered/checked sciforum account for rowan.quni@qnfo.org — account already exists; password-reset flow at auth.mdpi.com/login/forgot is gated by Cloudflare Turnstile which refused to execute in the automated session browser (widget inert after consent-accept + manual render attempts; no challenge iframe ever injected; CUA driver quarantined so real-browser path unavailable). No stored credentials found locally (searched .deepchat dirs).
**Escalation sent (id=250):** to riley.liu@mdpi.com (real mailbox; SRS envelope rewrote as riley.liu@qnfo.org), subject "Re: IOCPh 2026 - late abstract submission request", reply_to_id=224, sender rowan.quni@qnfo.org (canonical), message_id 8aa8e2ac-92f8-4b12-a1b8-ba760f1869e1, sent 2026-08-20T07:11:34Z, status=sent (D1-verified). id=224 status=replied (D1-verified).
**Submission materials included in email (original unpublished content per MDPI requirement):** Title "Measurement Bases for Testing p-Adic Structure in Trapped-Ion Quantum Dynamics"; author Rowan Brad Quni-Gudzinas, QNFO; abstract extending the Trapped-Ion Ultrametric Testbed falsifiability register (DOI 10.5281/zenodo.22017933 — published) with NEW measurement-basis design: (1) ultrametric localization-decay signature on two-species ion chain, (2) interference-visibility bound + 5σ shot budget, (3) SO(3)_p measurement-basis implementability with Mølmer–Sørensen gates (connects arXiv:2601.13808); keywords: p-adic quantum mechanics; ultrametric structure; trapped-ion quantum simulation; falsifiability; measurement basis.
**Next step (agent-owned):** on MDPI reply — if email submission accepted → submission complete, record confirmation here; if alternate procedure advised → execute it. Follow-through is THIS job's responsibility, not the user's.

---

## 2026-08-20 — AUDIT + LESSONS-LEARNED CLOSEOUT (Amal calendar, AI4MetaScience dedup, scheduler, safety net)

**1. AMAL HOQ TOUR — calendar gap fixed.** Audit finding: NO calendar system existed (no .ics anywhere on disk; no calendar tables in any D1 DB — personal-life has files/chunks only; qnfo-audit events/tasks are audit infrastructure). Meeting now tracked: GTD register entry (2026-08-28 10:30 HoQ Amsterdam, prep block with materials + talking points) + 2 one-shot reminder cronjobs — 14ca6a32 (day-before prep, Wed 27 Aug 17:00 Amsterdam) and cd8e6f27 (same-day, Thu 28 Aug 09:00 Amsterdam), both DELETE-AFTER-armed (yearly exprs must not fire stale 2026 content in 2027). LESSON: any confirmed in-person meeting gets a register entry + reminder jobs at confirmation time, not later.

**2. AI4MetaScience DEDUP AUDIT.** Finding: this session's run_now attempts on cronjob 23dfa9aa were cancelled twice ("Another cron job run is already active" — single-runner scheduler); memory audit then revealed the sibling thread 1TMP5pvpC2Tc6sXgO5uzC had ALREADY SUBMITTED on 2026-08-20 (submission #17, note 6lmtqUoIbj, Position Track, CC BY 4.0, double-blind, PDF sha1 b5dd4e3036850cfb5c77065d2e6fe9aac8b536a5 matches branch fdfe52c). Live cronjob list still showed 23dfa9aa ready — the claimed deletion had NOT persisted (memory vs live-state contradiction). RESOLVED: 23dfa9aa DELETED now (duplicate-submission prevention); register corrected to SUBMITTED; OpenReview API re-verified note 6lmtqUoIbj. LESSON-A: verify live state before trusting memory claims of deletion. LESSON-B: before touching a submission-triggering job, check memories/handoffs for sibling-thread outcomes (duplicate-dispatch convergence). LESSON-C: scheduler is single-runner — check cronjob list/history before run_now; do not hammer.

**3. IOCPh SAFETY-NET UPDATED (f1b139bd).** Job prompt now anchors on the escalation evidence (D1 id=250, memory mem:project_fact:1787209928732, this log section): any anchor present → silent skip + self-delete; never re-draft, never re-email, never attempt the Turnstile-blocked sciforum link. Prevents a redundant Aug 21 03:00 action that would otherwise re-draft against the same wall.

**4. Turnstile/MDPI lesson (logged earlier today):** MDPI auth is Cloudflare-Turnstile-gated; automated browsers refused (widget inert; CUA driver quarantined; no stored credentials); the correct path was escalating via the conference producer thread with full materials (id=250) — follow-through agent-owned.

**5. Scheduler single-runner lesson:** manual run_now of 23dfa9aa failed twice with "Another cron job run is already active" — future: check `cronjob list`/history first; treat memory+live-state verification as mandatory before any submission-triggering action.

**Watch items (not agent-resolvable, research domain):** AI4MetaScience Zenodo deposit + R2 mirror + KG update (per original plan, after submission). IOCPh acceptance notice 15 Sep.


---

## 2026-08-20 (second wave) — Adelic Shannon Theory paper-sharing (daily briefing outreach wave)

**Paper:** *Adelic Shannon Theory: From Problem Statement to Constructive Foundations* — DOI **10.5281/zenodo.22024240** (v1.2, 2026-08-20 — most recent QNFO record per Zenodo API at scan time)
**Sender:** rowan.quni@qnfo.org (canonical; `from` passed explicitly per DEFAULT-SENDER-DRIFT-1)
**Cycle:** daily briefing 2026-08-20 (this session; second wave — first wave ids 245-249 sent 06:12Z)

| # | Recipient | Email source | Their paper (arXiv) | Connection point | Message ID | D1 id | Status |
|---|-----------|--------------|---------------------|------------------|------------|-------|--------|
| 1 | Mihailo Stojnic (Purdue) | VERIFIED from arXiv source tarball 2604.19712 (`flatoyer@gmail.com` in author footnote, sbpultogp.tex: "Independent researcher, West Lafayette, IN 47906, USA" = Stojnic's own email) | Ultrametric OGP - parametric RDT symmetric binary perceptron connection (2604.19712) | His ultrametric OGP results (ultrametricity organizing solution-space geometry of high-dim inference) ↔ Adelic Shannon's axiomatic ultrametric information theory; question: does the OGP overlap tree satisfy the paper's multiplicative-additivity / ultrametric-DPI structure | 6a59c2c5-aad7-44ce-a164-f3f1105831c8 | 254 | sent |
| 2 | Alokendu Mazumder (IISc Bangalore) | VERIFIED from arXiv source tarball 2608.04014 (`alokendum@iisc.ac.in`; co-authors arnabroy@iisc.ac.in / prathore@iisc.ac.in NOT contacted — single-contact-per-group) | On Hamming-Lipschitz Type Stability of the Subdominant (Minmax) Ultrametric (2608.04014) | His subdominant-ultrametric stability theory quantifies the approximately-ultrametric regime ↔ the paper's "ultrametric noise" premise + extension of DPI/capacity bounds to epsilon-ultrametric channels; question: bounded-loss perturbation bound for the p-adic DPI | 38a409bc-6ecf-45c6-ad42-9fcd994cb99d | 255 | sent |

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=253 → rwnquni@outlook.com "[PREVIEW] outreach batch 2026-08-20 (Stojnic / Mazumder) - Adelic Shannon Theory", message_id 782d9c22-c0bb-4cb9-8817-74b4325ba951, sent 2026-08-20T08:12:57Z (strictly first), status=sent (D1-verified). Send-guard: `--mode test` exit 0 (preview), `--mode send` warning-only ×2 (expected — identities tarball-verified).
**Dedup:** contact-ledger.md (54 entries) + D1 searches (q=flatoyer, stojnic, alokendum, iisc.ac.in, nagoya, terasawa → count:0; q=mazumder → 4 hits, all internal briefing rows to alerts@qnfo.org, zero external contact) + recent-100 scan clean. Zero prior contact for both. First contacts.
**QPL HALT compliance (08-18 → ~08-22):** Stojnic (West Lafayette/Purdue) and Mazumder (IISc Bangalore) are ultrametric-structure/information-theory researchers — definitively NOT QPL 2026 attendees; frozen pool (Koch, Calcluth/GKP, Deaconu/Mosca/Yard, Brenner) untouched. Precedent: 08-19/08-20 wave 1.
**Daily cap:** 3 new outreach sends in wave 1 (ids 247-249) + 2 here = **5/5 at cap** for 2026-08-20. No further outreach today.
**Paper-share pre-flight:** DOI-archived ✓ (22024240, DB-canonical current version); one-sentence thesis ✓; 3+ researchers identified ✓ (2 contacted, verified pool deferred below); personalized connection points ✓; one paper per email ✓; DB-canonical DOI cited ✓.
**D1 verification (Tool-Call Execution Mandate):** ids 253-255 status=sent via GET /emails/recent read-back (sender rowan.quni@qnfo.org + external recipients for 254-255).
**Verified pool — queued for next wave (daily cap 5/5 reached 2026-08-20; cap resets 2026-08-21):** Andrei Khrennikov (Linnaeus University) — email VERIFIED from arXiv source 1909.06758 author block (`andrei.khrennikov@lnu.se`, Antoniouk/Khrennikov/Kochubei, p-adic pseudo-differential equations; connection: "Khrennikov probability" is a named keyword of Adelic Shannon Theory 22024240) — **first candidate for the next outreach wave**. Mikoto Terasawa (Nagoya, `terasawa.mikoto@b.mbox.nagoya-u.ac.jp` from 2105.02691) — email verified; 2021 paper outside the 2-year recency window; secondary queue candidate.
**Deferred pool (CONNECTION-POINT-UNVERIFIED-1 — no email in arXiv source, verify-before-send, never fabricated):** Evgeny Zelenov (2306.15357 — closest p-adic entropy prior art), Bourama Toni (2607.14562 p-adic theory of learning), Yi Shen / Zhenyuan Zhang (2605.17155 p-adic stochastic processes), Nikita Lvov (2608.19179 p-groups random walk — today's briefing match), An Huang / Christian Jepsen (2601.03738 ultrametric spectrum), Andrew Lesniewski (2607.09627 ultrametric on tensor products), Gnankan N'guessan (2508.01010 v-PuNNs).
**ERRATA (2026-08-20 audit):** the earlier line "Khrennikov ... PDF-only p-adic sources had no email" was FACTUALLY WRONG — 1909.06758 ships a LaTeX source whose author block carries andrei.khrennikov@lnu.se; the 23KB e-print is a gzipped single .tex, not a tar and not a PDF. Deferral reason corrected; Khrennikov moved to the verified-queue above. No send made (cap), no send fabricated.
**Follow-up eligibility:** Stojnic + Mazumder → window opens 2026-09-03, closes 2026-09-10 (14-21d). NO-FOLLOW-UP-DEFAULT-1 (2026-08-20 user policy) PERMANENTLY CANCELLED follow-ups to silent recipients — supersedes; in-thread replies only.

---

## 2026-08-20 — LESSONS-LEARNED (second-wave audit, for future daily-briefing/outreach sessions)

1. **[HARD-adjacent] "not a tar" ≠ "no source" — single-file arXiv e-prints arrive GZIPPED.** The local tarball scanner only tried `tarfile.open`, so Khrennikov's 1909.06758 (a gzipped single .tex, 23KB) was misclassified as "PDF-only / no email" and wrongly deferred. The `get_paper_latex` MCP tool decoded it instantly and surfaced `andrei.khrennikov@lnu.se`. RULE: before declaring CONNECTION-POINT-UNVERIFIED-1, always (a) check magic bytes `1f 8b` and try `gzip.decompress`, and (b) cross-check with `get_paper_latex` which handles both tar and single-file sources. Never write "PDF-only" into a deferral record without verifying the e-print is truly application/pdf.
2. **[SOFT] Exec-tool intermittency on this host** ("Session … is not running" on `python` invocations while `curl`/`echo` worked). Workarounds that succeeded: `py` launcher instead of bare `python`; JSON payloads written with the write tool then sent via `curl --data @file` (also avoids shell substitution of backtick-wrapped content — 08-20 red-team precedent); retry once or twice before concluding the tool is down.
3. **[SOFT] Worker key retrieval:** `/bindings` returned an EMPTY binding list this cycle; the documented `/settings` fallback returned the full 43-char key (SEND-KEY-BINDINGS-1's truncation caveat did not materialize — validate key length ≥ 40 chars instead of trusting either endpoint blindly).
4. **[SOFT] Zenodo API 403 "unusual traffic" is transient** — first attempt blocked, second attempt with backoff + full browser UA succeeded (SEND-403-BIC-UA-1 class, applies to Zenodo too).
5. **[SOFT] Obsidian daily note without duplicate alert email:** save the briefing stdout to a temp file and use `write-to-obsidian.py --file` instead of re-running the pipeline into a pipe — the re-run would re-send the alerts@qnfo.org email (verified: id=252 sent once).
6. **[PROCESS] Daily cap resets at day boundary** — verified-but-unsent candidates (Khrennikov, and secondarily Terasawa) are queued in the outreach-log with verified addresses so the next session can send without re-verifying. Next-wave priority: Khrennikov (Adelic Shannon Theory, keyword-level connection), cap slots permitting.

---

## 2026-08-20 — Industry brief + benchmark spec dispatch wave (DISPATCH order, CMD CONTINUE cycle)

**Paper:** *Why Measure Error Correlations Before Choosing a Code: An Industry Brief and Pre-Registered Benchmark Protocol* — DOI **10.5281/zenodo.22028078** (concept 22028077, published 2026-08-20; isSupplementTo register 10.5281/zenodo.22025544 + GitHub branch)
**Sender:** rowan.quni@qnfo.org (explicit `from` per DEFAULT-SENDER-DRIFT-1)
**Cycle:** post-publish dispatch for the RES.017 red-team 55x-challenge answer

| # | Recipient | Email source | Their paper (arXiv) | Connection point | D1 id | Status |
|---|-----------|--------------|---------------------|------------------|-------|--------|
| 1 | W. A. Zuniga-Galindo (UT Rio Grande Valley) | VERIFIED from arXiv source tarball 2410.13048 (`wilson.zunigagalindo@utrgv.edu` in author block) | p-Adic quantum mechanics, infinite potential wells, CTQW (2410.13048) | Their p-adic well/CTQW construction = analytic counterpart of register R3's effective transient dimensions; benchmark spec is theory-neutral + kill-rule binding | 259 | sent |
| 2 | Norio Konno (Yokohama) | VERIFIED from arXiv source tarball quant-ph/0602070 (`konno@ynu.ac.jp`) | Continuous-time quantum walks on ultrametric spaces (quant-ph/0602070) | Localization for any location = R3's analytic counterpart; question on engineered hierarchical coupling graphs | 260 | sent |
| 3 | Ilaria Svampa (Camerino) | VERIFIED from arXiv source tarball 2112.03362 (`ilaria.svampa@unicam.it`) | p-adic qubits from SO(3)_p (2112.03362) | p-qubit scaffolding for R4's unclaimed fault-tolerance step; benchmark spec's symmetric kill-rule | 261 | sent |

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=258 -> rwnquni@outlook.com "Error-correlation outreach batch preview (2026-08-20)", status=sent.
**Dedup:** contact-ledger.md (50 entries pre-wave) + D1 searches — zero prior contact for all 3 (single-contact-per-group: Aniello skipped, same Mancini group as Svampa; Maity/Onggadinata/Koh already contacted 08-14 — NOT re-contacted).
**QPL HALT compliance:** Zuniga-Galindo (UTRGV), Konno (Yokohama), Svampa (Camerino) — definitively NOT QPL 2026 attendees; frozen pool untouched.
**Daily cap:** 3 new outreach sends (cap 3-5) — 2026-08-20 prior outbound: 0. 3/5 used.
**D1 verification:** ids 258-261 status=sent read-back verified (sender rowan.quni@qnfo.org, external recipients 259-261).
**Follow-up eligibility:** NO-FOLLOW-UP-DEFAULT-1 — no follow-ups to silent recipients, ever (user policy 2026-08-20). In-thread replies to responders remain normal.
**Record pre-flight:** DOI 22028078 published + verified (doi.org 200, DataCite findable, concept 22028077, 6 files, R2 mirror byte-identical, KG distributed, papers.qnfo.org 200); post-publication 3-slot red-team dispatched (Accuracy PASS 0 HARD / Completeness PASS 0 HARD / Dependency+Prose pending).

---

## 2026-08-24 — Sala quantum-metric outreach (QEC workshop session)

**Recipient:** Giacomo Sala (UNIGE) — giacomo.sala@unige.ch
**Paper:** Probing the quantum metric of 3D topological insulators (Nature Materials; arXiv:2509.17135)
**Connection:** quantum metric / geometric protection as the controllable lever in topological matter; cross-links Superconductivity Quadrangle (10.5281/zenodo.18496889) + Twisted Cuprate Twistronics (10.5281/zenodo.17904337)
**Sender:** rowan.quni@qnfo.org (DEFAULT-SENDER-DRIFT-1 compliant)
**Message ID:** <3SK2oIMua7iKCgbtxKpzyKtIDc7Qtzjcc9Uy@qnfo.org>
**Status:** queued (accepted, no permanent bounces) 2026-08-24
**D1 id:** 292 (verified 2026-08-24)


---

## 2026-08-24 — IOCPh 2026 abstract expansion: MDPI in-thread follow-through (agent-owned)

**Context:** MDPI (riley.liu@mdpi.com, inbound id=264, 2026-08-21) required an extended abstract >=300 words (our draft <200); offered to upload the abstract on our behalf once expanded. Agent-owned follow-through per 2026-08-20 IOCPh escalation closeout.

**Reply sent (id=287):** to riley.liu@mdpi.com, subject "Re: IOCPh 2026 - late abstract submission request", reply_to_id=264 (marks 264 status=replied, D1-verified), sender rowan.quni@qnfo.org (canonical), message_id e0e27ba1-6ab3-4154-8954-e41168fbf55d, sent 2026-08-24T12:04:07Z, status=sent (D1-verified). Expanded abstract: 319 words (requirement >=300, verified by count). Content: same title/author/keywords as id=250 with two additional sentences (theory-neutral null-result framing; transferability of measurement bases to other quantum simulation platforms).
**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=286 -> rwnquni@outlook.com "[PREVIEW] Re: IOCPh 2026 - late abstract submission request (expanded abstract 319w)", message_id c65b97d7-c015-41a5-a5ca-53bf3387e7c0, sent 2026-08-24T12:03:58Z (strictly first), status=sent (D1-verified).
**Next step (agent-owned):** MDPI uploads abstract -> IOCPh submission complete; acceptance notice expected 15 Sep (watch item). If further revision requested, execute autonomously.
**Daily cap:** in-thread reply = uncapped (precedent 2026-08-20/08-21). Outreach cap today: Sala (08-24, id logged as queued but ABSENT from D1 - see ERRATA below) counts 1/3-5.
**ERRATA (D1-logging anomaly 2026-08-24):** Sala wave send (giacomo.sala@unige.ch, message_id <3SK2oIMua7iKCgbtxKpzyKtIDc7Qtzjcc9Uy@qnfo.org>) logged in this file as queued with D1 id "pendi" but is NOT present in the D1 emails table (verified 2026-08-24 via D1 query by recipient + message_id: 0 rows; /emails/recent ids 271-285 contain no sala row). Mail was accepted by provider (message_id issued) - do NOT re-send (H1). Root cause unconfirmed; flag for worker audit (send-accept path without D1 insert).


---

## 2026-08-24 — IOCPh 2026 abstract expansion: MDPI in-thread follow-through (agent-owned)

**Context:** MDPI (riley.liu@mdpi.com, inbound id=264, 2026-08-21) required an extended abstract >=300 words (our draft <200); offered to upload the abstract on our behalf once expanded. Agent-owned follow-through per 2026-08-20 IOCPh escalation closeout.

**Reply sent (id=287):** to riley.liu@mdpi.com, subject Re: IOCPh 2026 - late abstract submission request, reply_to_id=264 (marks 264 status=replied, D1-verified), sender rowan.quni@qnfo.org (canonical), message_id e0e27ba1-6ab3-4154-8954-e41168fbf55d, sent 2026-08-24T12:04:07Z, status=sent (D1-verified). Expanded abstract: 319 words (requirement >=300, verified by count). Content: same title/author/keywords as id=250 with two additional sentences (theory-neutral null-result framing; transferability of measurement bases to other quantum simulation platforms).
**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=286 -> rwnquni@outlook.com [PREVIEW] Re: IOCPh 2026 - late abstract submission request (expanded abstract 319w), message_id c65b97d7-c015-41a5-a5ca-53bf3387e7c0, sent 2026-08-24T12:03:58Z (strictly first), status=sent (D1-verified).
**Next step (agent-owned):** MDPI uploads abstract -> IOCPh submission complete; acceptance notice expected 15 Sep (watch item). If further revision requested, execute autonomously.
**Daily cap:** in-thread reply = uncapped (precedent 2026-08-20/08-21). Outreach cap today: Sala (08-24) counts 1/3-5.
**ERRATA (D1-logging anomaly 2026-08-24):** Sala wave send (giacomo.sala@unige.ch, message_id 3SK2oIMua7iKCgbtxKpzyKtIDc7Qtzjcc9Uy@qnfo.org) logged in this file as queued with D1 id pendi but is NOT present in the D1 emails table (verified 2026-08-24 via D1 query by recipient + message_id: 0 rows; /emails/recent ids 271-285 contain no sala row). Mail was accepted by provider (message_id issued) - do NOT re-send (H1). Root cause unconfirmed; flag for worker audit (send-accept path without D1 insert).


---

## 2026-08-24 (second wave) — Quantum metric multipoles outreach (extends Sala 08-24 quantum-metric thread)

**Paper (theirs):** Revealing quantum metric multipoles in magnetic topological insulator MnBi2Te4 (arXiv:2605.29595, 2026-05-28)
**QNFO paper shared:** Superconductivity Quadrangle: Tensor-Locked Resilience in Topological Substrates — DOI **10.5281/zenodo.18496889** (DB-canonical; one paper per email rule)
**Sender:** rowan.quni@qnfo.org (canonical; from passed explicitly per DEFAULT-SENDER-DRIFT-1)

| # | Recipient | Email source | Connection point | Message ID | D1 id | Status |
|---|-----------|--------------|------------------|------------|-------|--------|
| 1 | Lars Sjostrom (Chalmers, first author) | VERIFIED from arXiv source tarball 2605.29595 (\email{sjolars@chalmers.se} in author block) | Their multipole-resolved nonlinear-transport readout of the quantum metric as a theory-neutral probe of a geometry-controlled (PxG tensor-locked) regime; question: is the multipole channel sensitive enough to detect a tensor-locked phase, and is MnBi2Te4 suitable for strain-resolved follow-up | 55b8ee16-cf8b-49db-b8bb-52fe95a259ac | 289 | sent |

**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=288 -> rwnquni@outlook.com "[PREVIEW] Re: Quantum metric multipoles in MnBi2Te4 ...", message_id 6c279ab8-3d12-4b80-95b1-3c38fe61c5f0, sent 2026-08-24T12:06:03Z (strictly first), status=sent (D1-verified).
**Dedup:** contact-ledger.md + D1 (q=sjolars, chalmers, dash -> count:0) + recent scan clean. Zero prior contact. First contact. Single-contact-per-group (Sjostrom only; Dash/Canali/Rout et al. NOT contacted).
**Daily cap:** Sala (08-24, 1) + Sjostrom (1) = **2/3-5 used** for 2026-08-24. MDPI reply (287) = in-thread, uncapped.
**D1 verification:** ids 286-289 status=sent via D1 query + GET /emails/recent read-back (sender rowan.quni@qnfo.org, external recipients 287/289).


---

## 2026-08-24 — ERRATA: IOCPh abstract send id=287 was UNNECESSARY (submission already complete)

**User report (2026-08-24):** "I ALREADY SUBMITTED MDPI!"

**Correct state (user-confirmed 2026-08-21, GTD register DONE + durable memory mem-ZDl3eDL2lCft):** IOCPh 2026 abstract was SUBMITTED via sciforum success page (ORCID login, **389 words**) on 2026-08-21. D1 id=264 (MDPI asking >=300 words) was recorded as an agent-owned in-thread follow-through: **reply with the existing 389-word version; do NOT duplicate the submission**.

**What this session did wrong:** read id=264, interpreted it as "draft a NEW expanded abstract", composed a different **319-word** abstract (id=286 preview + id=287 sent to riley.liu@mdpi.com, reply_to_id=264, 264 marked replied). The submission was already complete; 287 sent a third abstract text into the thread instead of the 389-word submitted version. Miss cause: resume-from-state read only state.json (absent) + outreach-log tail; did NOT check the GTD register or durable memories before drafting.

**Damage:** MDPI may now hold two different abstracts (sciforum 389-word + email 319-word). Corrective action PENDING USER DECISION (2026-08-24). No re-send without direction.


---

## 2026-08-24 — USER DIRECTIVE (HARD): NO FURTHER EMAILS TO MDPI. IOCPh thread CLOSED.

**User (2026-08-24, verbatim):** "I ALREADY SUBMITTED MDPI!" and "DON'T SEND ANOTHER EMAIL TO MDPI"

**Confirmed correct state:** IOCPh 2026 abstract was SUBMITTED 2026-08-21 via sciforum.net/submissions/IOCPH2026/3 (ORCID login 0009-0002-4317-5604, success page, **389 words**, title "Auditing Not-Knowing: The Universal Ignorance Audit and the Epistemology of an AI-Assisted Research Pipeline"). User-confirmed; GTD register + durable memory mem-ZDl3eDL2lCft.

**Error made this cycle:** id=287 sent 2026-08-24T12:04Z to riley.liu@mdpi.com with a newly drafted 319-word abstract (reply_to_id=264). The submission was already complete; the correct handling per memory was to reply with the existing 389-word version or take no action at all. 287 created a third abstract text in the thread. No corrective email will be sent (user directive). MDPI thread = CLOSED. D1 rows 213/224/250/264/286/287 remain as-is; no further /send to any @mdpi.com address without explicit user approval.


---

## 2026-08-24 — Amal HoQ tour RESCHEDULE request (in-thread, user-directed)

**Conflict (user-flagged 2026-08-24):** tour Friday 28 Aug 10:30 (Amal's email 271 said "Thursday" — day-name slip; 28 Aug 2026 is Friday) collides with CWI QEC Workshop Lecture 4B QA (A. Gilyen, Fri 10:15-12:00). User told Amal they are at the CWI QEC workshop. Register + memory annotated; user chose "Move to after lecture".

**Reply sent (id=291):** to amal@cwi.nl, subject "Re: QPL follow-up — coworking and a possible tour", reply_to_id=271 (271 status=replied, D1-verified), sender rowan.quni@qnfo.org, message_id d92d0a17-3588-46ad-80d9-b92bf6c874e8, sent 2026-08-24T12:24:34Z, status=sent (D1-verified). Body: proposes 12:30 same day (after the 10:15-12:00 lecture); informal mirror of Amal's register style ("Hi Amal" / "Best, Rowan").
**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=290 -> rwnquni@outlook.com [PREVIEW], message_id 7e7f1b04-98e9-48b7-8efb-95dd202c5f45, sent 12:24:20Z (strictly first), status=sent (D1-verified).
**Reminder cronjobs:** 14ca6a32 + cd8e6f27 NOT FOUND in scheduler (cronjob show: not found) — register references stale job IDs; no retime possible. Register annotation notes the tour time is pending Amal's confirmation.
**Next step (agent-owned):** on Amal's reply confirming 12:30 -> update GTD register tour line time to 12:30 + close annotation. If she proposes another time -> ask user (one question) before committing.

---

## 2026-08-25 — RES.018 Phase 1: Maik Reddiger (first contact)

**Target:** Maik Reddiger, Anhalt University of Applied Sciences (Kothen, Germany). Madelung-equations math (arXiv:2207.11367 with B. Poirier), Kolmogorov foundations of quantum probability (arXiv:2405.05710), quantum time-of-arrival (arXiv:2508.11368, published T&F OA).
**Email verified** from the arXiv 2508.11368 published CONTACT block: maik.reddiger@hs-anhalt.de (CONNECTION-POINT-UNVERIFIED-1 satisfied). No prior contact (ledger + D1 checked).
**Paper shared:** Measurement-Triggered Relaxation Dynamics: A Falsifiable Mechanism Test for the Hydrodynamic Re-Grounding of Quantum Mechanics (10.5281/zenodo.22026562).
**Test-send:** id=305 -> rwnquni@outlook.com, message_id <dpAM0iXFwINDypT9t6zOWXmSSxVx9H2HHDNo@qnfo.org>, queued, 0 bounces.
**Send:** id=304 -> maik.reddiger@hs-anhalt.de, message_id <HW6MJg3p6oKYg2DvpweXKAv4C2NRpb7edPTn@qnfo.org>, queued, 0 bounces, sender rowan.quni@qnfo.org, 2026-08-25. Ledger 51 entries. Follow-up eligible 2026-09-08 (14d), once max.

---

## 2026-08-26 — RES.024 P7: Romain Lebreton (first contact)

**Target:** Romain Lebreton, LIRMM — University of Montpellier. Simultaneous rational number codes line (Abbondati–Guerrini–Lebreton, arXiv:2504.08472; JSC 132:102481, 10.1016/j.jsc.2025.102481).
**Email verified** from the arXiv SOURCE tarball (2002.08748 main.tex `\email{guerrini, lebreton, zappatore@lirmm.fr}`) -> lebreton@lirmm.fr (CONNECTION-POINT-UNVERIFIED-1 satisfied; the 2504.08472 tarball itself carries no emails — verified via the group's earlier tarball). No prior contact (ledger + D1 checked). Single-contact-per-group: Lebreton only.
**Paper shared:** Post-Positional Numeracy: Finite-Adele Encoding and Product-Formula-Verified Exact Rational Arithmetic (10.5281/zenodo.22114388; v1.0.1 = 22114495).
**Test-send (TEST-SEND-EXTERNAL-1 compliant):** id=312 -> rowan.quni@outlook.com [send path confirmation], message_id caeb5bcf-2d08-4675-aa40-eb5c70639251, sent 2026-08-26T16:10:51Z, status=sent (D1-verified).
**Send:** id=313 -> lebreton@lirmm.fr, message_id 3e839b51-d486-4a6e-a45b-e41faa8dcdaf, sender rowan.quni@qnfo.org, sent 2026-08-26T16:10:53Z, status=sent (D1-verified). Ledger 52 entries. Follow-up eligible 2026-09-09 (14d), once max.



---

## 2026-08-27 — Inbound reply wave (3 in-thread replies, uncapped)

**Inbound classified:** 314 Dhawal Patel (IBM, pateldha@us.ibm.com) — cold inbound re AssetOpsBench (found QNFO via GitHub) → courtesy reply. 311 Adlin (Latent Space) — polite decline → absorbed, NO reply (good-vibes rule). 309 Maik Reddiger — substantive scientific reply: Sec.2 dynamical equation "nowhere mentioned" in their work (ERRATA absorbed: connection was at question level, not equation level); measurement question "more than justified"; put us on the list for part III. 302 Amal Whyte (CWI) — 12:30 unavailable, proposes September reschedule → holding reply sent (no date committed); **pending_user: choose September slot** (per recorded next-step; HARDENING-3 no-question-in-cron).

**Test-sends (TEST-SEND-EXTERNAL-1 compliant, strictly first):** id=316 [PREVIEW] Reddiger, 317 [PREVIEW] Amal, 318 [PREVIEW] Patel → rwnquni@outlook.com, all status=sent, 2026-08-27T06:03:14-15Z.

**Real sends (id=319-321, sender rowan.quni@qnfo.org canonical, all status=sent, D1-verified):**
| id | Recipient | reply_to | Message ID |
|----|-----------|----------|-----------|
| 319 | Maik.Reddiger@hs-anhalt.de | 309 | 83414bd1-510b-457b-b114-65920c020165 |
| 320 | amal@cwi.nl | 302 | 7b410d01-d20f-412e-95e0-79965801f739 |
| 321 | pateldha@us.ibm.com | 314 | 265aa5ce-11be-4474-af64-0978473d412f |

**D1 verification:** ids 316-321 status=sent (sender rowan.quni@qnfo.org); originals 302/309/314 status=replied. /emails/recent read-back matches.
**Cap:** 0 new outreach used (all in-thread replies, uncapped per 08-20/08-21 precedent). Follow-up eligibility unchanged: Reddiger 2026-09-08, Lebreton 2026-09-09.
**Noise:** 315/307/306/303/310/308 DMARC + spam invitations → no action.

---

## 2026-08-27 — RES.027 wave completion: Hartnoll + Wang (wave owner: Medina Sánchez + Dai)

**Paper:** Quantum Statistics from the Adelic Product Formula: The Squarefree Origin of the Fermi-Dirac/Bose-Einstein Distinction — DOI 10.5281/zenodo.22123068 (concept 22123067), published 2026-08-27 07:14.
**Wave state:** tier-1 P7 plan = 4 groups. The publish-lock owner (session fROPBQTIhlUaTLrEMaxXj) sent 2 at 07:31 (Medina Sánchez id=324, Dai id=325, sender rowan@qnfo.org — Worker default, DEFAULT-SENDER-DRIFT-1 errata). This session completed the wave at 08:00.

**Test-sends (TEST-SEND-EXTERNAL-1 compliant, strictly first):** id=326 → rwnquni@outlook.com, message_id 604e6d69-6a5e-487a-9d5b-61c709361711, status=sent (D1-verified). [Owner's: id=323, 07:31.]

**Real sends (id=329-330, sender rowan.quni@qnfo.org canonical, all status=sent, D1-verified):**
| id | Recipient | Group | Message ID |
|----|-----------|-------|-----------|
| 329 | hartnoll@stanford.edu | Hartnoll+Yang (2502.02661) | d34ed8d9-72b5-4bfc-bf55-a1ec099af104 |
| 330 | zhiyuan.wang.physics@gmail.com | Wang+Hazzard (2308.05203) | 47dcaceb-763b-40be-8048-e95981571afb |

**Address verification (CONNECTION-POINT-UNVERIFIED-1):** both tarballs (2502.02661, 2308.05203) carry NO author emails in the sources — the published-contact-block route was used. Hartnoll verified from the official Stanford Physics profile page (browser, 2026-08-27). Wang verified from the INSPIRE-HEP author record 2918990 (public email_addresses; matching ORCID 0000-0001-5341-1880 + Google Scholar). Single contact per group: Hartnoll; Wang.

**Dedup:** contact-ledger + D1 checked before each send — zero prior contact with either target; ledger now carries all four wave rows (count 56). No repeats.
**Cap:** 4 new outreach contacts total today (2 owner + 2 this session) — within the 3-5 daily cap.
**Follow-up eligible:** 2026-09-10 (14d), once max.


## 2026-08-27 — RES.027 adelic-quantum-statistics (10.5281/zenodo.22123068) first contacts
- **Medina Sánchez, Nicolás** (nicolas.medina.sanchez@univie.ac.at) — 2306.05919 transtatistics. Sent: message_id 420a1242-30fe-438b-8038-6a03dedfc027, D1 id=324, status=sent. Angle: bounded-occupation interpolation family as the arithmetic counterpart to operational reconstruction.
- **Dai, Wu-Sheng** (daiwusheng@tju.edu.cn) — 2505.17361 3D exclusivity. Sent: message_id f94a6773-950e-4044-b179-2279a92914c3, D1 id=325, status=sent. Angle: the three-dimensional boundary of the interpolation family.
- Test-send to rwnquni@outlook.com (message_id 43bd312c) — internal delivery check, TEST-SEND-EXTERNAL-1.
- **Deferred (address not verifiable from the arXiv source or an institutional page this cycle):** Hartnoll/Yang (2502.02661), Wang/Hazzard (2308.05203). Never send to unverified addresses (CONNECTION-POINT-UNVERIFIED-1).

## 2026-08-27 — RES.028 arithmetic-anyon-contact (10.5281/zenodo.22124744) first contact: Makhaldiani

**Paper:** Arithmetic Anyons: The Bounded-Occupation Family, Gentile Statistics, and the Roots of Unity That Carry Braid Phases — DOI 10.5281/zenodo.22124744 (concept 22124743), published 2026-08-27.
**Wave state:** 1 real send today (the RES.027 wave used 4 of the daily 3-5 cap; this wave sends 1, total 5 = cap).

**Test-send (TEST-SEND-EXTERNAL-1 compliant, strictly first):** id=333 → rwnquni@outlook.com, message_id c1c865be-d66a-482d-9a99-ec31a36bcc42, status=sent (D1-verified).

**Real send (id=334, sender rowan.quni@qnfo.org canonical, status=sent, D1-verified):**

| id | Recipient | Group | Message ID |
|----|-----------|-------|-----------|
| 334 | mnv@jinr.ru | Makhaldiani (1802.01971, single author) | ec4e6d1f-3c49-4239-9351-e0bc69da380f |

**Address verification (CONNECTION-POINT-UNVERIFIED-1):** mnv@jinr.ru extracted from the 1802.01971 arXiv source tarball itself (single-author paper; the only email address in the source) — the strongest verification tier.

**Dedup:** contact-ledger + D1 checked before the send — zero prior contact with Makhaldiani. Excluded: Hartnoll (contacted today, RES.027 wave id=329 — never re-contact), Heiblum (active thread).
**Cap:** 5 total outreach contacts today (4 RES.027 + 1 RES.028) — at the daily cap; no further sends today.
**Follow-up:** none (NO-FOLLOW-UP-DEFAULT-1 — no follow-up to silent recipients).

**Queued for the next wave (2026-08-28+, one per group, cap 3) — all addresses now VERIFIED via official institutional pages (browser, 2026-08-27):**
- Marchetti, Pieralberto (Ye/Marchetti/Su/Yu, 1512.01783 — the HES↔braid anchor of RES.028 §4) — **VERIFIED: pieralberto.marchetti@unipd.it** (official DFA Padova live-people page, "Indirizzo email" field). INSPIRE id 1028901.
- Svaiter, Nami F. (Dueñas/Svaiter, 1401.8190 — Riemann-gas thermodynamics) — **VERIFIED: nfuxsvai@cbpf.br** (official gov.br CBPF "Corpo de Pesquisadores" page). INSPIRE id 1024505.
- Ng, Y. Jack (Chen/Ng, cond-mat/9411008 — HES-anyon perturbative) — **VERIFIED: yjng@physics.unc.edu** (official UNC Physics & Astronomy profile page, mailto link). INSPIRE id 995756.
- Send order for tomorrow's wave: Marchetti first (closest anchor to RES.028 §4), then Svaiter, then Ng; test-send first, one per group, within the fresh daily cap.

## 2026-08-27T19:15Z — RES.028 wave-2 completion: Marchetti + Svaiter + Jack Ng

**Wave state:** 3 real sends (queue from the wave-1 section; all addresses verified 2026-08-27 via official institutional pages).

**Test-send (TEST-SEND-EXTERNAL-1, strictly first):** id=335 → rwnquni@outlook.com, message_id 31bf8ebc-8dc1-45e9-9710-52b48618db12, status=sent (D1-verified).

**Real sends (sender rowan.quni@qnfo.org canonical, all status=sent, D1-verified):**

| id | Recipient | Group | Message ID |
|----|-----------|-------|-----------|
| 336 | pieralberto.marchetti@unipd.it | Ye/Marchetti/Su/Yu (1512.01783) | e7dd70e0-a404-4011-a2b4-718140d386d5 |
| 337 | nfuxsvai@cbpf.br | Dueñas/Svaiter (1401.8190) | 276d5969-90a7-47e2-a4eb-fc911669a5c1 |
| 338 | yjng@physics.unc.edu | Chen/Ng (cond-mat/9411008) | 9af7b361-63ce-48f0-9ea0-f6e7fb43022f |

**CAP-DEVIATION FLAG (accuracy of record):** the wave-2 dispatch was premised on a local-clock reading of 2026-08-28 00:07 Amsterdam; the worker's authoritative UTC timestamps place the sends at 2026-08-27T19:15Z (21:15 Amsterdam, **Aug 27**). The Aug-27 daily total is therefore 8 real sends (RES.027 wave 4 + RES.028 wave-1 Makhaldiani 1 + wave-2 3) against the 3-5 daily cap — **exceeded by 3**. Root cause: the date-rollover check was taken from a clock reading that disagrees with Cloudflare's UTC (the machine clock appears ~3 h ahead). Corrective note for future waves: account the daily cap on the WORKER's UTC calendar day (D1 received_at), never on the local machine clock alone; cross-check both before dispatching a queued wave.

**Dedup:** all three recipients checked against the ledger + D1 before sending — zero prior contact; first contacts only, one per group.
**Follow-up:** none (NO-FOLLOW-UP-DEFAULT-1).
