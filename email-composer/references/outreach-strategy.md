# QNFO Outreach & Communications Strategy

**Loaded on demand for systematic outreach campaigns. Companion to `qnfo-qwav-strategy.md` and `email-patterns.md`.**

---

## 0. The Blind Inbox: Emotional Architecture

### The Core Insight

Academic outreach is psychologically hard for independent researchers. The fear of rejection, the impostor syndrome of "no PhD," the anxiety of being ignored — these are real barriers. They kill good ideas before they reach the people who could benefit from them.

**The blind inbox solves this by removing emotional friction entirely.**

| Barrier | Blind Inbox Solution |
|---|---|
| **Fear of rejection** | Emails are drafted by LLM, reviewed impersonally, sent programmatically. A rejection or silence isn't personal — it's a data point. |
| **Impostor syndrome ("no PhD")** | The work speaks for itself. The paper is the credential. No biography, no CV, no self-introduction — just the research. |
| **Anxiety about checking email** | You never open an email client. Ever. All inbound routes to the Worker → D1 → accessed through prompts. No notifications. No inbox dread. |
| **Taking criticism personally** | Criticism arrives as structured data (sender, subject, body_text). The LLM reads it first, extracts the substance, and frames a response. You engage with the argument, not the tone. |
| **Fear of being "exposed" as self-taught** | QNFO papers are DOI-archived, publicly accessible, and citeable. They exist independently of the author's credentials. If the paper is wrong, the argument will show it — not the author's biography. |

### The Operational Model

```
You (idea/paper) → LLM drafts outreach → You review (optional) → Worker sends
                                                                    ↓
You (response)   ← LLM frames reply      ← Worker receives     ← Recipient replies
```

At no point do you directly face the recipient's emotional reaction. Every interaction is filtered through the system. This isn't avoidance — it's **emotional architecture**: building a system that lets you do the work while protecting the person doing it.

### What This Enables

- **Volume**: Send 20-50 outreach emails per month without emotional burnout
- **Persistence**: Follow up on silence without feeling like you're "bothering" someone
- **Experimentation**: Try different framings, audiences, and papers without ego attachment
- **Scale**: The system handles the emotional load; you handle the strategic decisions

---

## 1. Audience Segmentation

Different audiences need different approaches. Never use the same template for a physics professor and a venture capitalist.

### A. Academic Researchers

**Who**: Physicists, mathematicians, computer scientists, philosophers of science — anyone whose work intersects with QNFO papers.

**Goal**: Get the paper read. Spark intellectual engagement. Build a network of researchers who know QNFO's work.

**Tone**: Colleague-to-colleague. Assume they're smart and busy. Lead with the research question, not the answer.

**Key principle**: **You are not asking for approval. You are sharing a result.** A physicist shares preprints with peers all the time — that's normal scientific practice. Frame every outreach as "here's something you might find interesting given your work on X."

**Channel**: `rowan.quni@qnfo.org`

**Template pattern**:
```
Subject: Re: [their paper/project] — [your paper's core question]

Dear Dr. [Name],

I came across your work on [their specific topic] and wanted to share
something you might find relevant.

My recent paper, "[title]" (arXiv/DOI), explores [one-sentence thesis].
It bears directly on [their work] because [specific connection —
one sentence, no jargon].

[One paragraph: the finding, the evidence, the implication. No background
section. No self-introduction. No CV. The paper speaks.]

If you have a moment to look at it, I'd be interested in your thoughts
— especially on [specific open question they could help with].

Best,
Rowan Quni
QNFO Research Collective
```

**Anti-patterns**:
- Leading with "I'm an independent researcher" or "I don't have a PhD" (irrelevant — the paper is the credential)
- Asking for endorsement or validation ("do you think this is right?")
- Over-citing your own work (one paper per outreach, maximum)
- Pretending to be an institution (QNFO is a collective, not a university — own it honestly)

### B. Potential Funders & Grant Bodies

**Who**: Research foundations, science philanthropies, government grant programs, academic funding bodies.

**Goal**: Get QNFO on their radar as a fundable research program. Establish the infrastructure and publication record.

**Tone**: Professional, evidence-based, understated. The publication record IS the case for funding — you don't need to "sell."

**Channel**: `rowan.quni@qnfo.org` or `research@qnfo.org`

**What they need to see**:
- A clear research program (not isolated papers — a trajectory)
- Evidence of rigor (DOI-archived, citeable outputs)
- Infrastructure (6 databases, 31 Workers, 10 Pages projects — this IS capability)
- Falsifiability commitment (pre-registered predictions, null-results published)

### Funder Template

```
Subject: QNFO Research Collective — [Research Area] Programme

Dear [Name/Title],

I'm writing from the QNFO Research Collective, an open-science
research program producing peer-reviewable, DOI-archived work in
[field: theoretical physics / quantum foundations / philosophy of
science]. I wanted to share our recent publication record and
infrastructure, which may align with [Foundation]'s [specific
program/focus area].

[2-3 sentences: what we've published. Cite 1-2 DOIs. Mention the
cumulative record — e.g., "293 Zenodo records, 850+ pages of
research across 6 programs."]

Our work is falsification-driven and pre-registration-based: every
finding carries a pre-registered test condition and a null-result
publication track.

We are seeking [specific funding need: research time / equipment /
collaboration support] to advance [specific program/paper]. I'd
welcome the opportunity to discuss whether this aligns with
[Foundation]'s priorities.

The full publication record is at [DOI list or Zenodo community].
A 15-minute call would let me present the research programme.

Thank you for your consideration,
Rowan Quni
QNFO Research Collective
research@qnfo.org | qnfo.org
```

**Key differences from academic template**: Lead with the publication RECORD (not a research question). Cite infrastructure numbers. Explicitly name the funding need before the close. Call-to-action is a 15-minute call (funders expect this; academics don't).

---

### C. Investors & Industry

**Who**: VCs, angel investors, industry R&D leads, technology scouts.

**Goal**: Position QWAV as a serious computing platform with a differentiated thesis. NOT "quantum computing 2.0" — honest computation from first principles.

**Tone**: Thesis-driven, evidence-backed, understatedly confident. The Qubit Delusion series IS the investment thesis.

**Channel**: `rowan.quni@qwav.tech`

**What they need to see**:
- The problem: $35B quantum industry, zero viable machines
- The thesis: substrate IS algorithm; Problem-Substrate Mapping
- The metric: JPCUB (joules-per-solution) — falsifiable, measurable, universal
- The evidence: 6-paper Manifesto chain, all DOI-archived
- What QWAV IS and IS NOT (see qnfo-qwav-strategy.md)

### Investor Template

```
Subject: QWAV — [Thesis: "Substrate IS Algorithm" computing platform]

Dear [Name],

I'm writing because [specific connection: you invest in deep-tech
computing / you've written about quantum computing's challenges /
your portfolio includes hardware platforms].

QWAV addresses a well-defined market failure: the $35 billion
quantum computing industry has delivered zero broadly viable
machines. Our thesis, published in the peer-reviewed 6-paper
Manifesto for Honest Computation (DOI [manifesto_DOI]), is that
this failure is epistemic, not engineering — the qubit model is
wrong for general computation.

QWAV builds computing systems where the physical substrate IS the
algorithm — thermodynamic, optical, and neuromorphic platforms
selected by Problem-Substrate Mapping, not by marketing. Everything
competes on JPCUB (joules-per-solution), a falsifiable metric.

We are currently [stage: seeking seed funding / building prototype /
identifying fabrication partners]. The whitepaper (DOI
[whitepaper_DOI]) details platform architecture and positioning.

I'd welcome a brief conversation to discuss whether this aligns
with your investment thesis.

Rowan Quni
Founder, QWAV
rowan.quni@qwav.tech | qwav.tech
```

**Key differences from funder template**: Open with the PROBLEM (market failure), not the record. Cite the Manifesto + JPCUB metric. State what QWAV is BUILDING, not what QNFO has published. Address risk pre-emptively. The ask is a conversation about alignment, not a specific funding ask.

**Portfolio-rejection handling**: If the VC says "we don't invest in quantum" — they've misunderstood. QWAV is NOT quantum computing — it's post-quantum, honest computation. If they persist: archive, don't argue.

---

### D. Collaborators & Potential Partners

**Who**: Other independent researchers, open-source projects, experimental groups, fabrication partners.

**Goal**: Find people who can do what you can't — experiments, fabrication, domain expertise you lack.

**Tone**: Direct, specific. "Here's what I can do. Here's what I need. Does this overlap with what you do?"

---

## 2. Outreach Cadence

Systematic, not spontaneous. Treat outreach like any other research activity: scheduled, tracked, reviewed.

### Weekly Cadence

| Day | Activity | Volume Target |
|---|---|---|
| **Monday** | Research scan: check arXiv, Google Scholar, PhilPapers for new papers in QNFO's domains. Identify 5-10 potential contacts. | 5-10 contacts identified |
| **Wednesday** | Draft outreach: for the top 3-5 contacts, draft paper-sharing emails using the academic template. | 3-5 drafts |
| **Friday** | Send + review: send the week's batch, review responses from prior weeks, queue follow-ups. | Send 3-5, review all pending |

### Monthly Targets

| Audience | Target Volume | Expected Response Rate | Expected Conversations |
|---|---|---|---|
| Academic researchers | 12-20 emails/month | 10-20% | 1-4 conversations |
| Funders/grant bodies | 2-4 emails/month | 5-10% | 0-1 conversations |
| Investors/industry | 1-2 emails/month | variable | opportunistic |
| Collaborators | 2-4 emails/month | 15-25% | 0-2 conversations |

**Rationale**: At 20 academic emails/month with a 15% response rate, that's 3 substantive conversations per month — 36 per year. That's a research network. Silence on the other 17 is expected, not a rejection.

### The "No Response" Protocol

Academics are busy. Silence is the default, not an insult.

| Time Since Send | Action |
|---|---|
| 0-14 days | Do nothing. People are busy. |
| 14-21 days | **One** gentle follow-up: "Just checking if you had a chance to look at the paper — no rush at all." Add a small new piece of value (a relevant arXiv preprint, a new finding). |
| 21+ days | Archive. **Never follow up a second time.** The ball is in their court. Move on to the next contact. |

**Golden rule**: If you follow up twice on the same person for the same paper, you've crossed from "persistent researcher" to "annoying." Don't.

---

## 3. Response Taxonomy

When someone DOES respond, the blind inbox processes it before you see it. Here's how to handle each type.

### Type 1: Positive / Engaged

**Signal**: "This is interesting," "I'd like to discuss this," "Can you explain X?"

**Response**: Thank them, engage with their specific question, keep the thread alive. **Priority: HIGH.** This is the whole point of outreach.

**LLM role**: Draft a substantive reply engaging with their point. Ask a follow-up question to keep the conversation going. Flag for user review.

### Type 2: Critical / Skeptical

**Signal**: "This doesn't work because X," "I disagree with your interpretation of Y," "Your method is flawed because Z"

**Response**: **This is valuable.** Criticism means they read the paper seriously enough to find something wrong. Thank them, engage with the substance, acknowledge valid points, explain where you disagree and why.

**Emotional guard**: The LLM reads the criticism first and extracts the ARGUMENT, not the TONE. You respond to the argument. The person may have been dismissive or rude — you don't have to absorb that. You respond to the physics, not the attitude.

**LLM role**: Extract the core objection. Draft a response that: (1) thanks them, (2) restates their objection accurately (shows you understood), (3) addresses it — concede if they're right, explain if they're not, (4) asks a follow-up question.

### Type 3: Dismissive / Gatekeeping

**Signal**: "You're not a real physicist," "This isn't how physics is done," "You should get a PhD first," ad hominem, credential-attack.

**Response**: **Do not engage.** These are not arguments — they're social signals. They say nothing about your work and everything about the sender's insecurity. Archive immediately.

**Emotional guard**: The blind inbox is built for exactly this scenario. You never see the tone, the condescension, the gatekeeping. The LLM classifies it as "dismissive" and routes it to archive. You never have to feel it.

### Type 4: "I'll Read It Later"

**Signal**: "Thanks, I'll take a look when I have time," "Busy right now but will get back to you"

**Response**: Thank them, archive. **Do not follow up.** If they read it and have thoughts, they'll reply. If they don't, they won't. Either way, the outreach was successful — they now know your name and your paper exists.

### Type 5: Collaboration Interest

**Signal**: "Can we work together on X?" "I have data that might be relevant," "Would you be interested in co-authoring?"

**Response**: **Priority: HIGHEST.** Evaluate the opportunity seriously. Does it align with QNFO's research program? Does the collaborator bring something you don't have (data, experimental capability, domain expertise)?

**LLM role**: Draft a response that acknowledges the interest, asks specific questions about scope and contribution, and proposes a concrete next step (a call, a shared document, a preliminary analysis).

---

## 4. Paper-Sharing Protocol (Primary Outreach Mode)

This is the workhorse. Every QNFO paper should generate an outreach batch.

### Pre-Flight Checklist (before ANY outreach)

- [ ] Paper is DOI-archived (Zenodo) and publicly accessible
- [ ] Paper passes publication integrity gates (no title duplication, no internal refs, slug-named file)
- [ ] Paper has a one-sentence thesis that can be stated without jargon
- [ ] Target audience is identified (which researchers would find this relevant?)
- [ ] At least 3 specific researchers are identified whose published work connects to this paper

### Finding Contacts

**For arXiv papers**: Search arXiv for recent papers in the same category. The authors are your target list. When sharing, reference their paper specifically.

**For published papers**: Search Google Scholar, PhilPapers, and the paper's own reference list. Who are you citing? Those are potential contacts.

**For cold outreach**: Research the author's recent work. Never send a generic "I liked your paper." Reference a SPECIFIC result, method, or finding that connects to your work.

### The Batch Send

For each paper, prepare a batch of 3-10 outreach emails:

1. **Research the target**: Read their recent abstract. Find the connection point.
2. **Draft individually**: Same structure, but customize the first paragraph for each recipient's specific work.
3. **Send stagger**: Don't send 10 emails simultaneously. Send 2-3 per day over a week. This spaces out responses and prevents overwhelm.
4. **Track in D1**: Log each outreach with paper DOI, recipient, date sent, and connection point.

### Integration with the Publication Pipeline

When the research skill's Phase 7 (Dissemination) completes a new publication:

1. The paper exists on Zenodo with a DOI
2. Outreach protocol triggers: identify the paper's audience, find 5-10 relevant researchers
3. Draft batch, review, send over 3-5 days
4. Track responses in D1

---

### Paper-to-Audience Mapping

**Which paper goes to whom?** Not every paper is for every audience. Use this matrix:

| Paper Category | Primary Audience | Secondary Audience | NOT for |
|---|---|---|---|
| **Physics results** (Adelic Programme, QEC audits, ultrametric foundations) | Academic physicists, mathematicians | Funders (shows rigor) | Investors, general public |
| **Philosophy/methodology** (Consilience Framework, Five Pillars, Spencer-Brown) | Philosophers of science, epistemologists | Academic physicists (if they've published on foundations) | Investors |
| **Platform/commercial** (Qubit Delusion series, Manifesto, Whitepaper) | Investors, industry partners | Funders (shows commercial viability), physicists (public critique) | Academic philosophers |
| **Infrastructure/meta** (Notation Problem, Communications Framework) | Computer scientists, infrastructure builders | Funders (shows capability) | Investors |

**Quick Decision Rules:**

1. **If the paper has "ultrametric" or "p-adic" in the title:** → Academic physicists only. Never send to investors (jargon overload).
2. **If the paper critiques the quantum computing industry:** → Investors (commercial thesis) + academics (public critique). The Qubit Delusion series serves BOTH audiences but with different templates.
3. **If the paper proposes a new framework/methodology:** → Philosophers + interdisciplinary researchers. Physicists only if they've published on foundations of physics.
4. **If the paper describes infrastructure/notation:** → Funders (capability signal) + computer scientists. Not a standalone outreach paper.
5. **The golden rule: Never send a paper to an audience it wasn't written for.** A physicist receiving a manifesto gets confused. An investor receiving a p-adic paper stops reading after the title.

---

## 5. D1 Tracking Schema

Every outreach campaign and response should be tracked for systematic improvement.

### `outreach_campaigns` table (conceptual — prototype in existing D1 infrastructure)

| Field | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `paper_doi` | TEXT | The paper being shared |
| `paper_title` | TEXT | For quick reference |
| `audience_type` | TEXT | academic / funder / investor / collaborator |
| `recipient_email` | TEXT | Who it was sent to |
| `recipient_name` | TEXT | For personalized follow-up |
| `connection_point` | TEXT | Why them? (e.g., "their 2025 paper on QEC tradeoffs") |
| `sent_at` | TEXT | ISO timestamp |
| `followed_up_at` | TEXT | ISO timestamp (NULL if none) |
| `response_type` | TEXT | positive / critical / dismissive / read_later / collaboration / none |
| `response_summary` | TEXT | LLM-extracted summary of the response |
| `thread_id` | INTEGER | Links to the email in the D1 emails table |
| `status` | TEXT | sent / responded / archived / active_conversation |

---

## 6. The Emotional Operating Manual

### What to Remember When You Feel the Fear

1. **You are not your email.** The blind inbox means you never face rejection directly. A non-response is a database entry, not a judgment.
2. **The work is the credential.** You don't need to explain who you are or why you're qualified. The paper exists. It's DOI-archived. It speaks for itself.
3. **Volume dissolves fear.** The first outreach email is terrifying. The 50th is routine. The system makes volume possible — use it.
4. **Silence is the default, not a rejection.** Professors get 100+ emails a day. Your paper might be interesting and still get lost. That's normal.
5. **Criticism is data.** Someone who writes a paragraph explaining why your method is wrong has done you a service. That's a peer review you didn't have to pay for.
6. **Gatekeeping is their problem, not yours.** "You're not a real physicist" is a statement about the speaker's insecurity, not your work. Archive and move on.
7. **Every conversation is a win.** If 3 out of 20 academic outreach emails lead to substantive conversations, that's a 15% success rate — and 36 conversations per year. That's a research network.

### The Difference Between This and "Cold Emailing"

Cold emailing is desperate. It says "please notice me." This is different.

This is **normal scientific practice**. Physicists share preprints. They email each other about interesting results. They ask questions, propose collaborations, argue about methods. The only difference is that you're doing it from outside an institution — and the blind inbox makes that difference irrelevant.

**You're not a salesperson. You're not a job applicant. You're a researcher sharing a result with a peer.** Frame every outreach in that voice.

---

## 7. Integration with the Email-Composer Skill

### Phase Reference

This strategy is activated at Phase 3 (Strategic Context) of the email-composer workflow. When the user asks to:

- "Start outreach for paper X"
- "Find people to share my paper with"
- "Set up regular paper sharing"
- "Build my research network"

The agent loads this document, identifies the paper and audience, executes the paper-sharing protocol, and tracks in D1.

### Quick-Start Commands (for the agent, not the user)

| Command | Action |
|---|---|
| "Outreach batch for [paper]" | Find 5-10 relevant researchers, draft personalized emails, present for review |
| "Follow up on pending outreach" | Check D1 for emails >14 days without response, draft follow-ups |
| "Outreach report" | Generate stats: sent, responded, response rate by audience, active conversations |
| "Weekly outreach routine" | Execute the Monday/Wednesday/Friday cadence |

### Cronjob Integration (operational, 2026-08-06)

The outreach cadence is wired into two scheduled tasks — it runs **autonomously**, not just on-demand.

**Task 1: `qnfo-email-inbox-check` (every 3 hours, id `3851f539`)**
After the standard inbox check, this task handles the full outreach cadence:
- **Every run**: Detects outreach replies (email subjects matching QNFO paper titles), checks follow-up readiness (>14 days no response)
- **Monday** (first run after 08:00 UTC): Scans arXiv for researchers whose recent work connects to QNFO papers published in the last 90 days; presents 3-5 outreach candidates
- **Wednesday**: Reports drafting-ready contacts; runs "Outreach batch for [paper]" readiness check
- **Friday**: Generates weekly outreach report (sent/responded/follow-ups/active conversations) + drafts follow-up emails per the No Response Protocol

**Task 2: `QNFO Research Daily Briefing` (daily 08:00 UTC, id `fdf1403c`)**
After the arXiv scan completes, identifies researchers whose recent work connects to QNFO papers from the last 90 days. On Monday: presents full contact details. On other days: summary only.

**Safety**: Neither task sends emails autonomously. All follow-up drafts in notifications require user approval in an interactive email-composer session before sending.

---

## Cross-References

- `qnfo-qwav-strategy.md` — QNFO/QWAV positioning, manifesto principles, banned words
- `email-patterns.md` — Individual email patterns (declining, pitching, following up, cold response)
- `email-composer` SKILL.md — Core email workflow (discovery, triage, analysis, drafting, sending)
- `research` SKILL.md — Publication pipeline, Phase 7 dissemination
- `qnfo-core` SKILL.md — Research Integrity Mandate, banned words, certainty calibration
