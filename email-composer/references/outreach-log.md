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
