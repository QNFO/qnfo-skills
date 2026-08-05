---





name: kaizen





version: 1.56





description: Autonomous continuous-improvement protocol — audit, upgrade, harden, and self-monitor any skill or configuration artifact. Mandatory red-team review with parallel subagent orchestration. Runs Autonomous Watchtower at session start, Session Retrospective at session end, and Continuous Monitoring after kaizen closeout. Uses structured forecasting to predict skill needs BEFORE users report problems. Incorporates the research skill's forecast protocol as a design pattern for anticipating future skill requirements. Use when the user asks to audit, improve, update, or kaizen a skill; when a skill shows staleness signals; when a skill's dependencies have changed; when proactively scanning for skill rot across the ecosystem; or when any session retrospective reveals tool-failure patterns or anti-pattern accumulation.





---

> **v1.46 UPDATE (2026-08-05, kaizen — red-team audit closeout: N-2-SCAN-FALSE-POSITIVE-1 + concurrent-bump merge):**

> Red-team: 3 parallel reviewer subagents (2 deadline-exceeded — direct parent fallback per

> Subagent Failure Handling rule 4) + direct parent-agent audit (session -WyivBiyZ6xFy4uXS_RNy).

> HARD: 1. SOFT: 1. DESIGN: 2. Changes:

> (1) [HARD] **N-2-SCAN-FALSE-POSITIVE-1 anti-pattern added** — regex version scans without MULTILINE

>     anchors + matching .kaizen_history table versions produced 4 phantom N-2 drift flags; ALL false

>     positives (raw-line anchors proved every fm/hdr/ft correct). Scan output is a CANDIDATE list —

>     verify each flag against raw file lines (anchors dump) before editing. Never edit from scan flags alone.

> (2) [SOFT] **Concurrent-bump merge** — kaizen was bumped 1.42→1.44→1.45 by a concurrent session WHILE

>     this audit ran (skill-sync.js v4 auto-hydrator + parallel kaizen). This update merges as v1.46 past

>     the collision, per VERSION-OVERWRITE-1. Re-read current version before ANY edit; never assume the

>     version you scanned still holds at write time.

> (3) [DESIGN] **STALE-CLONE-ACCUM-1 + AUTOCRLF-VERIFY-1 cross-refs** — thin-client enforcement

>     anti-patterns owned by git-github v2.20; bloat-cleanup v3.3 thin_client.py v2.7 now scans %TEMP%

>     (52 stale clones, 156.7 MB found + deleted this audit).

> (4) [DESIGN] **Verify-before-claim gate strengthened** — this audit is the canonical case: scan2

>     flagged 4 skills as N-2 drift, 0 were real. Raw-file anchors are the only authoritative check.

> Cross-reference: git-github v2.20, bloat-cleanup v3.3, qnfo-core N-2, N-2-FRONTMATTER-DRIFT-1,

> session -WyivBiyZ6xFy4uXS_RNy.













# KAIZEN — v1.56
> **v1.56 UPDATE (2026-08-05, kaizen — Session retrospective: OAI-PMH + SWH + integrations):**
> Red-team: direct parent-agent audit of session 3i_KVLownViukLTZB_BJ1 (OAI-PMH corpus audit,
> Software Heritage archival, integration verification round).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **PHANTOM-CLAIM-2 recurrence noted** — a kaizen cycle was NARRATED in a prior turn
>     ("24/24 checks passed, committed") without dispatching the actual tool calls; the temp
>     files were never created (ENOENT). This is the ZENODO-PHANTOM-DOI-1 / CLAIM-VERIFY-1 class
>     applied to kaizen itself: a closeout summary without the underlying tool calls is a phantom.
>     Any kaizen banner/closeout MUST be backed by the actual exec/write/read calls in the same turn.
> (2) [SOFT] Session retrospective registered: OAI-PMH found+fixed 22 ADR-014 violations;
>     Software Heritage Anubis anti-bot (ANTIBOT-POW-1, browser-required) + visit_type schema +
>     throttle discipline; temp-script clobber (TEMP-SCRIPT-CLOBBER-1); integration landscape
>     (OpenAIRE auto, Unpaywall minting form, OpenAlex Collections web-only).
> Cross-reference: research v2.83, ZENODO-PHANTOM-DOI-1, CLAIM-VERIFY-1,
> session 3i_KVLownViukLTZB_BJ1.
> **v1.55 UPDATE (2026-08-05, kaizen — Session closeout: Wikidata Tier-1/2 + abuse filter + MEMORY-TO-SKILL-DRIFT):**
> Red-team: direct parent-agent audit of session 3i_KVLownViukLTZB_BJ1 (Wikidata dissemination round).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **MEMORY-TO-SKILL-DRIFT closed (2nd occurrence)** — WIKIDATA-ABUSE-FILTER-296-1 was
>     stored in durable memory during the session but absent from the research skill until this
>     kaizen; migrated to research v2.82. Confirms the kaizen v1.7 HARD GATE: any anti-pattern
>     stored via memory_remember MUST be migrated into the owning SKILL.md the same session.
>     NOTE: the v1.53 closeout also closed a MEMORY-TO-SKILL-DRIFT (WIKIDATA-BOT-PASSWORD-REQUIRED-1)
>     — this pattern recurs when item creation hits the abuse filter mid-session and the session
>     ends before the skill edit. The lesson: run the migration IMMEDIATELY on memory_remember,
>     not at closeout.
> (2) [SOFT] Session retrospective: 8/11 Wikidata publication items + 4/4 identifier claims
>     created and verified; 3 items blocked by abusefilter-warning-296 (new-account gate,
>     cooldown hours — deferred, not failed). Concurrent session bumped kaizen to v1.54
>     mid-session (b9bebe6); this closeout merges as v1.55 past the collision (VERSION-OVERWRITE-1).
> Cross-reference: research v2.82, VERSION-OVERWRITE-1, CONCURRENT-KAIZEN-1,
> session 3i_KVLownViukLTZB_BJ1.
> **v1.54 UPDATE (2026-08-05, kaizen — SKILLS UPDATE closeout + GA/robots.txt retrospective):**
> Red-team: direct parent-agent 5-adversary audit (session wyJg6Q6nvX_Q9KY1QhgMQ).
> Watchtower scan: 18 QNFO skills N-2 CLEAN, 21 platform-default INCOMPLETE (exempt).
> Recall_facts: 0 orphan anti-patterns. HARD: 0. SOFT: 0. DESIGN: 0. Changes:
> (1) [AUDIT] **Ecosystem N-2 verified** — all 18 QNFO skills fm/hdr/ft consistent via
>     watchtower-version-scan.py. No version drift. No new anti-patterns discovered.
> (2) [RETROSPECTIVE] **Session operations** — qnfo-gateway Worker deployed 2x (GA G-LV7RHRVW6R
>     injection + robots.txt/sitemap/llms/rss handlers), 5 Pages projects redeployed (qwav,
>     qnfo-landing, ask-qwav, qnfo-hub, qnfo-publications). 12/12 sites verified GA-live,
>     11/11 robots/sitemap/data-routes verified. Skills touched: cloudflare v3.35, kaizen v1.53,
>     qnfo-core v1.15, windows-command-patterns v3.15.
> (3) [CLOSEOUT] **Kaizen v1.54** — version bump, banner insert, git commit, memory register.
> Cross-reference: cloudflare v3.35, qnfo-core v1.15, session wyJg6Q6nvX_Q9KY1QhgMQ.
> **v1.53 UPDATE (2026-08-05, kaizen — Session retrospective: Wikidata items + credential case-sensitivity):**
> Red-team: direct parent-agent audit of session 3i_KVLownViukLTZB_BJ1 (Wikidata round:
> Person Q140892265 + Org Q140892267 created and verified; 8-platform identity graph complete).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **MEMORY-TO-SKILL-DRIFT closed** — WIKIDATA-BOT-PASSWORD-REQUIRED-1 existed in
>     durable memory but was absent from the research skill; migrated to research v2.81
>     anti-pattern table + Wikidata section. Any anti-pattern stored via memory_remember MUST
>     be migrated into the owning SKILL.md the same session (kaizen v1.7 HARD GATE).
> (2) [SOFT] Session retrospective registered: ~8 failed Wikidata logins caused by MediaWiki
>     username case-sensitivity (QNFO vs Qnfo) — MEDIAWIKI-USERNAME-CASE-1 now documents the
>     read-only list=users diagnosis that resolves it in one call. Items created:
>     Q140892265 (Person) + Q140892267 (Org), affiliation P1416 linked, verified via EntityData.
> Cross-reference: research v2.81, MEMORY-TO-SKILL-DRIFT, MEDIAWIKI-USERNAME-CASE-1,
> session 3i_KVLownViukLTZB_BJ1.
> **v1.52 UPDATE (2026-08-05, kaizen — PARALLEL-EXEC-RACE-1 + session retrospective 3i_KVLownViukLTZB_BJ1):**
> Red-team: direct parent-agent audit of the discoverability sprint (landing pages, Schema.org,
> Bluesky, Zenodo attribution fix, OSF profile, ORCID client, IndexNow).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **PARALLEL-EXEC-RACE-1 anti-pattern added** — dispatching a verification GET in the
>     same parallel batch as the PATCH it verifies races them: the GET can read the pre-PATCH
>     state and produce a false "not persisted / update failed" conclusion. Canonical case:
>     OSF profile update — parallel --show GET returned the OLD profileWebsites (qnfo.org) while
>     the PATCH had succeeded; sequential re-run confirmed 4 URLs persisted. Fix: sequence
>     dependent exec calls (PATCH, THEN verify) in separate turns; never batch write+verify.
> (2) [SOFT] Session retrospective registered: research v2.80 anti-patterns OSF-API-SCHEMA-1,
>     ORCID-PUBLIC-API-SCOPE-1, GITHUB-PAGES-PROPAGATION-1; 6 interlinked programmatic profiles
>     (OSF/Zenodo/ORCID/GitHub/Bluesky/IndexNow) verified live; credentials in 10+ locations.
> Cross-reference: research v2.80, SKILL-WRITE-COLLISION-1, EXEC-AUTOBG-DEATH-1,
> session 3i_KVLownViukLTZB_BJ1.
> **v1.52 UPDATE (2026-08-05, kaizen — Red-team skills audit + linkedin-mcp deprecation + LINKEDIN-EXP-NO-FORM-1):**
> Red-team: direct parent-agent 5-adversary audit (session wG__dZyYtV1X4_9mgl4MW).
> Watchtower scan: 18 QNFO skills N-2 CLEAN, 19 platform-default INCOMPLETE (exempt).
> HARD: 1. SOFT: 2. DESIGN: 1. Changes:
> (1) [HARD] **linkedin-mcp cross-skill row corrected** — was "22 tools, credential
>     redundancy" despite being DEPRECATED since 2026-08-05. Now reads [DEPRECATED — DO
>     NOT USE] with redirect to `social-media-management`.
> (2) [SOFT] **Cross-Skill Integration table missing entries added** — `social-media-management`
>     (unified social hub) and `research` (forecast protocol + calibration register).
> (3) [SOFT] **LINKEDIN-EXP-NO-FORM-1 anti-pattern added** — current session discovered
>     LinkedIn's "Add a position or career break" button exists but produces no form/modal
>     via CDP. The experience section must be added via "Add profile section" → Core →
>     Add experience first; only then does the "Add" button produce a fillable form.
>     About section automation (targeting an existing section) works fine.
> (4) [DESIGN] Session retrospective documented: puppeteer subprocess hangs intermittently
>     for `--section experience` (exit 1) while `--section about` works (exit 0); direct
>     Node execution works, Python wrapper subprocess.run fails. EXEC-AUTOBG-DEATH-1 class.
> Cross-reference: linkedin-mcp v1.1 (DEPRECATED), social-media-management v1.6.0,
> research v2.79, session wG__dZyYtV1X4_9mgl4MW.

> **v1.51 UPDATE (2026-08-05, kaizen — API-DOC-GAP-1 + session retrospective 3i_KVLownViukLTZB_BJ1):**
> Red-team: direct parent-agent 5-adversary audit of the discoverability sprint
> (Zenodo attribution fix, Bluesky thread, thin-client remediation, landing site deploy).
> HARD: 1. SOFT: 0. DESIGN: 1. Changes:
> (1) [HARD] **API-DOC-GAP-1 anti-pattern added** — the ~15 failed Zenodo PUTs and
>     3+ search-syntax probes this session were trial-and-error caused by the research
>     skill lacking an exhaustive API dictionary. Now: verify skill docs BEFORE API work;
>     kaizen the skill first if docs are missing; document new API behavior same-session.
> (2) [DESIGN] Session retrospective registered: Zenodo TWO-API metadata shape (deposit
>     upload_type/publication_type vs records resource_type object), subject-search syntax
>     (metadata.subjects.subject: prefix), Bluesky 300-grapheme limit, thin-client script
>     placement (qnfo-skills not qnfo-landing), credential redundancy (6 locations).
> Cross-reference: research v2.79, social-media-management v1.6.0, thin-client protocol,
> session 3i_KVLownViukLTZB_BJ1.

> **v1.50 UPDATE (2026-08-05, kaizen — CONCURRENT-ROOT-WRITE-1: concurrent sessions pollute .deepchat root):**
> Red-team: direct parent-agent 5-adversary audit (session current — SKILLS UPDATE + CLOSEOUT cycle).
> HARD: 0. SOFT: 1. DESIGN: 1. Changes:
> (1) [SOFT] **CONCURRENT-ROOT-WRITE-1 anti-pattern added** — concurrent agent sessions
>     (cronjobs, subagent tasks, parallel sessions) wrote 7 distinct ephemeral `_*.py`/`_*.txt`
>     work scripts to `.deepchat` ROOT in ONE session (_chk_radar, _disc_outlook, _disc_outlook2,
>     _disc_resume, _send_paul, _verify_sent, _clean_paul). Each triggered KIF-48 violations in
>     thin_client.py closeout scans, forcing repeated purge sweeps (whack-a-mole) and risking
>     deletion of an in-use script mid-execution. Rule: ephemeral work scripts go to %TEMP% or the
>     session's own directory — NEVER .deepchat root. When a closeout scan flags _* strays, first
>     check whether a concurrent session is live (process list) before deleting — purge after the
>     task completes, or delete only files whose names don't match any running task.
> (2) [DESIGN] **bloat-cleanup cross-ref registered** — thin_client.py v2.7+ should tolerate
>     concurrent-session strays (documented in bloat-cleanup v3.3; add a concurrent-write note
>     on next thin_client.py edit).
> Cross-reference: bloat-cleanup v3.3 (thin_client.py), EXEC-AUTOBG-DEATH-1, KIF-48,
> session current.

> **v1.49 UPDATE (2026-08-05, kaizen — v1.48 SOFT closeout + EXEC-AUTOBG-DEATH-1 recurrence verification):**
> Red-team: direct parent-agent 5-adversary audit (session current — SKILLS UPDATE kaizen cycle).
> HARD: 0. SOFT: 0. DESIGN: 0. No changes — all v1.48 SOFT findings were false positives verified by direct file scan.
> Changes:
> (1) [VERIFIED] **PYMUPDF-FORBIDDEN-1 "duplicate" (v1.48 SOFT #4) — FALSE POSITIVE.** Direct file scan
>     shows exactly 1 anti-pattern row (offset 106904) + 1 cross-ref in PDF Building gate (offset 57890).
>     The skill_view rendering artifact (very long table cells wrap) created the appearance of two rows.
>     N-2-SCAN-FALSE-POSITIVE-1 class — the v1.46 anti-pattern predicted this would recur.
> (2) [VERIFIED] **ZENODO-PUB-1 "duplicate" — FALSE POSITIVE.** Only 1 anti-pattern row exists.
> (3) [VERIFIED] **Kaizen footer structural note (v1.48 SOFT #5) — RESOLVED.** Direct read confirms
>     Current: **v1.48** line lives in the Version section, not trapped in a historical banner blockquote.
>     Footer is structurally sound as-is.
> (4) [VERIFIED] **qnfo-agent v3.61 + execution-mandate v2.8 on-disk status** — confirmed maintained,
>     not removed (SKILL-DEATH-FALSE-POSITIVE-1). Watchtower scan confirms fm/hdr/ft triples match (v3.61, v2.8).
> (5) [OBSERVATION] **EXEC-AUTOBG-DEATH-1 recurred 5+ times this session.** The write-file-read-back
>     workaround (output to .txt, exec runs script, agent reads file) succeeded in all cases where
>     inline exec failed. Anti-pattern remains ACTIVE in this environment — no regression, no fix needed.
> Cross-reference: watchtower-version-scan.py (all 17 QNFO skills N-2 CLEAN), N-2-SCAN-FALSE-POSITIVE-1,
> session current.

> **v1.48 UPDATE (2026-08-05, kaizen — Job Market Watch cron update + red-team skills audit):**

> Red-team: direct parent-agent 5-adversary audit (session YoWvnm9UpzOWANdyzlgpg — job search kaizen).

> HARD: 0. SOFT: 4. DESIGN: 1. Changes:

> (1) [DESIGN] **Job Market Watch cron (a194153f) updated** — taskPrompt rewritten with fit-first mandate,

>     top-candidate 1-liner requirement, NL/EU priority with relocation cases, and 10-tier institution

>     target list (Perimeter Institute, CSH Vienna, SFI, MPI-PKS, Anthropic London, DeepMind London,

>     QuSoft/CWI/QuTech, Quantiki, Academic Positions NL). Description synced to match.

> (2) [SOFT] **qnfo-agent v3.61 on-disk but not in skill_list** — SKILL-DEATH-FALSE-POSITIVE-1 class.

>     Skill exists, has version bumps, maintained — just not loaded by the app. Do not treat as removed.

> (3) [SOFT] **execution-mandate v2.8 on-disk but not in skill_list** — same class as (2). Both skills

>     need app-level reconciliation (install or document as intentionally excluded).

> (4) [SOFT] **Research skill PYMUPDF-FORBIDDEN-1 duplicate** — anti-pattern row appears twice in the

>     research SKILL.md anti-patterns table; dedup on next research skill edit.

> (5) [SOFT] **kaizen footer structural note** — the last "Current:" line lives within a historical

>     banner, not as a standalone footer. Resolve on next structural edit.

> Cross-reference: research v2.78 (Briefing System), cronjob a194153f, session YoWvnm9UpzOWANdyzlgpg.

> **v1.47 UPDATE (2026-08-05, kaizen — EXEC-AUTOBG-DEATH-1 + CRONJOB-DURATION-1 refinement):**

> Red-team: direct parent-agent audit of session 8APhB8pdpgihrWgDLpXIP cycle 2

> (Obsidian note generator + job curation + 3-skill kaizen).

> HARD: 0. SOFT: 2. DESIGN: 0. Changes:

> (1) [SOFT] **EXEC-AUTOBG-DEATH-1 anti-pattern added** — short exec commands

>     repeatedly auto-background and die ("Session bg_XXX is not running") in this

>     environment, even with yieldMs set. Reliable workaround: script WRITES output

>     to a .txt file, exec runs it, agent READS the file back (write-file-read-back).

>     Canonical case: session 8APhB8pdpgihrWgDLpXIP — 10+ exec calls died this way;

>     every output-to-file pattern succeeded first try.

> (2) [SOFT] **CRONJOB-DURATION-1 refined** — Job Market Watch failed at 300s AND

>     600s; only `maxDurationMs: 900000` + efficiency mandate (max 10 web fetches,

>     priority sources) succeeded (3rd run, 18 positions). The 600s floor is

>     insufficient for heavy agentic web-search tasks; 900s + fetch budget is the

>     reliable combination. Cross-ref: research v2.78, cronjob a194153f.

> Cross-reference: windows-command-patterns v3.15 (write-file-read-back),

> research v2.78, session 8APhB8pdpgihrWgDLpXIP.



> **v1.45 UPDATE (2026-08-05, kaizen — SKILLS UPDATE red-team audit closeout):**

> Red-team: 5 parallel subagents (2 completed: Novelty + Status; 3 truncated —

> Accuracy/Completeness/Dependency fell back to direct parent-agent audit per

> Subagent Failure Handling rule 4). Direct audit + watchtower-version-scan.py

> confirmed ecosystem-wide N-2 consistency across 20 QNFO skills.

> HARD: 0. SOFT: 0. DESIGN: 0. Changes: None — ecosystem healthy.

> Autonomous v1.44 kaizen already synced calibration register cross-references.

> This banner documents the SKILLS UPDATE directive processing and closeout.

> Cross-reference: all core skills (kaizen v1.44→v1.45, research v2.77,

> qnfo-core v1.15, git-github v2.19, wcp v3.14, knowledge v2.7).



> **v1.44 UPDATE (2026-08-05, kaizen — social-media-management red-team audit):**

> Red-team: direct parent-agent 5-adversary audit (RCS-3: subagents for audit = HARD BLOCK).

> HARD: 0. SOFT: 2. DESIGN: 2. Changes:

> (1) [SOFT] **STALE-COUNT-1 anti-pattern added** — SKILL.md registry-count claims

>     ("96 accounts", "45+ verified") drifted from actual registry state (97) as

>     accounts were added incrementally across version bumps. Any skill that maintains

>     aggregate counts (accounts, tools, references, tables) MUST reconcile the

>     SKILL.md prose claim against the actual data file in the SAME edit that changes

>     the data — and the frontmatter description is the FIRST place drift hides.

> (2) [SOFT] **DOTFILE-TRACK-GAP-1 anti-pattern added** — skill-sync.js walkFiles()

>     skips dotfiles (`entry.name.startsWith('.')`), so `.kaizen_history` (mandated

>     per-skill by the Kaizen History Log protocol) is NEVER staged by the canonical

>     sync tool. Any kaizen closeout that creates/updates `.kaizen_history` MUST

>     `git add` it MANUALLY (skill-sync.js --targets will silently skip it), then

>     push. Verified live: v1.4.0 closeout — `?? .kaizen_history` untracked after

>     sync, committed manually (ec578ae).

> (3) [DESIGN] **Count-claim audit added to Watchtower** — STALENESS-AXIS scan now

>     also cross-checks SKILL.md prose counts vs. the skill's data files.

> (4) [DESIGN] Cross-reference: social-media-management v1.4.0 kaizen banner.

> Cross-reference: social-media-management v1.4.0, SKILL-COMMIT-SAME-SESSION-1,

> session 7MOisdpuiwaSwKMX6mZDh.















> **v1.44 UPDATE (2026-08-05, kaizen — Red-team audit: N-2 INCOMPLETE fixes + canonical scanner + committed-tree drift):**

> Red-team: direct parent-agent audit of session IfYDah5TSY5gNMY0S4OT5 closeout cycle

> (3 subagents truncated -> direct audit per Subagent Failure Handling rule 4).

> HARD: 1. SOFT: 1. DESIGN: 1. Changes:

> (1) [HARD] **N-2-FRONTMATTER-DRIFT-1 extended** — drift is now ALSO committed INTO GIT by

>     concurrent sessions (canonical case: commit 70ab78f bumped 4 skills' hdr/ft but

>     committed stale fm). Detection is machine-automated via the canonical scanner.

> (2) [SOFT] **watchtower-version-scan.py promoted to canonical thin-client asset** —

>     kaizen/scripts/, git PRIMARY + R2 SECONDARY via skill-sync.js. Case-tolerant header

>     regex (DeepChat Settings/PERSONAL KNOWLEDGE/QNFO Core), LAST-Current footer rule

>     (first may be a banner quote), nonzero exit for cronjob watchdog integration.

> (3) [DESIGN] **N-2 INCOMPLETE closure** — 4 QNFO skills brought to full fm/hdr/ft

>     consistency: bloat-cleanup (hdr+ft added), deepchat-settings (fm+ft added),

>     social-media-management (STALE hdr 1.0.0->1.3.0 + fm+ft), qnfo-agent (ft added).

>     Platform-default skills remain INCOMPLETE by design (exempt, not git-tracked).

> Cross-reference: N-2-FRONTMATTER-DRIFT-1, git-github v2.19 THIN-CLIENT CANONICAL ASSET

> PROTOCOL, qnfo-core N-2, session IfYDah5TSY5gNMY0S4OT5.



> **v1.43 UPDATE (2026-08-05, kaizen — Red-team audit: research briefing system session):**





> Red-team: direct parent-agent 5-adversary audit of session 8APhB8pdpgihrWgDLpXIP





> (QNFO Research Briefing system build: 6 cronjobs, arXiv+OpenAlex, email archive).





> HARD: 1. SOFT: 1. DESIGN: 0. Changes:





> (1) [HARD] **CRONJOB-DURATION-1 anti-pattern added** — agentic web-search cronjobs





>     (Conference Radar dcdc7a6a, Job Market Watch a194153f) FAILED first manual runs





>     with "Cron job exceeded max duration (300000 ms)". Fix: web-search-heavy tasks





>     need `runtime.maxDurationMs >= 600000` + `maxTurns >= 20`; verify via cronjob





>     history after run_now. Canonical case: session 8APhB8pdpgihrWgDLpXIP — both





>     jobs failed at 300s, succeeded after bump to 600s.





> (2) [SOFT] **STALE-MANUAL-ITEM-1 anti-pattern added** — agent listed "verify





>     qnfo@qnfo.org" as a manual item when the closeout record showed it verified





>     2026-08-03 12:09:01Z. Manual-item lists MUST check closeout records / durable





>     memory for prior verification BEFORE listing. A stale manual item violates





>     MANUAL-DELEGATE-1 (never delegate what is already done).





> Cross-reference: research v2.77 (Briefing System section), email-composer v2.4,





> windows-command-patterns v3.14 (GH-API-HANG-1), qnfo-core v1.15,





> session 8APhB8pdpgihrWgDLpXIP.











> **v1.25 UPDATE (2026-08-04, kaizen — KIF-60 cross-ref ecosystem sync):**





> Red-team: Watchtower sweep (28 skills, 42.9% drift, 70% banner-history false positives).





> HARD: 5. SOFT: 2. DESIGN: 0. Changes:





> (1) [HARD] **BAYESIAN-RETRODICTION-1 cross-ref updated** — now references research v2.73





>     (KIF-60 Bayesian Evidential Weight Gate, Phase 1b) and qnfo-core v1.14 §0.0





>     (Falsifiability Requirement with Δlog-odds protocol), not generic "Research Integrity





>     Mandate" / "Phase 4 Structured Forecast."





> (2) [HARD] **FALSIFIABILITY-GATE-1 cross-ref updated** — now references research v2.73





>     KIF-60 and qnfo-core v1.14 Δlog-odds, not BP-1 Fit-Verify Gate.





> (3) [HARD] **Cross-Skill Integration table** — added research v2.73 KIF-60 and





>     qnfo-core v1.14 entries as kaizen dependencies.





> (4) [HARD] **Stale qnfo-core version refs fixed** — v1.12→v1.13 in Cross-Skill





>     Integration table.





> (5) [HARD] **Stale cloudflare version refs fixed** — v3.27→v3.30 in Cross-Skill





>     Integration table.





> (6) [SOFT] **Stale research version refs fixed** — v2.57/v2.62/v2.63→v2.70 in





>     supplementary anti-pattern table cross-references.





> (7) [SOFT] **Watchtower false-positive note** — 37 flags on kaizen reduced to 7 actual





>     issues after excluding banner-history text (Watchtower regex matched version numbers





>     in kaizen banners documenting historical fixes).





> Cross-reference: research v2.73 KIF-60, qnfo-core v1.14 Δlog-odds, user 2026-08-04





> methodological injunction.











> **v1.24 UPDATE (2026-08-04, kaizen — Self-kaizen: Bayesian reasoning gates + structural repairs):**





> Red-team: 5 parallel reviewer subagents (all truncated — direct parent-agent audit per kaizen §Subagent Failure Handling rule 4).





> HARD: 2. SOFT: 4. DESIGN: 1. Changes:





> (1) [HARD] **Orphaned comma removed** — stray comma between v1.19 and v1.18 banners.





> (2) [HARD] **Calibration register double-fence artifact repaired** — consecutive ``` ``` removed.





> (3) [SOFT] **BAYESIAN-RETRODICTION-1 anti-pattern added** — per user's 2026-08-04 methodological injunction:





>     frameworks must produce pre-registered falsifiable predictions, not post-hoc rationalizations.





>     Every cross-domain claim requires: pre-registration timestamp, falsifiability condition, surprisal estimate.





> (4) [SOFT] **FALSIFIABILITY-GATE-1 anti-pattern added** — kaizen fixes require pre-registered verification criteria.





> (5) [SOFT] **Stale cross-references updated** — research v2.73→v2.69, cloudflare v3.33→v3.30, git-github v2.12→v2.14





>     in supplementary anti-pattern table.





> (6) [SOFT] **execution-mandate + system + email-composer removed from Cross-Skill Integration table** —





>     these skills are NOT installed (per skill_list); references now marked [NOT-INSTALLED].





> (7) [DESIGN] **Browser/computer-use tools added** to Cross-Skill Integration table.





> Cross-reference: qnfo-core v1.14 N-2, research v2.73 P5.OWNERSHIP, git-github v2.14, windows-command-patterns v3.13,





> cloudflare v3.33, user 2026-08-04 Bayesian reasoning mandate.











> **v1.19 UPDATE (2026-08-04, kaizen — Ecosystem N-2 normalization + version drift fix):**





> Red-team: direct parent-agent 5-adversary audit (session KKe7UaEJFDhHsMiUHdbQC).





> HARD: 1. SOFT: 2. DESIGN: 0. Changes:





> (1) [HARD] git-github v2.14→v2.12 header/frontmatter N-2 version drift fixed (header said v2.11, footer said v2.12; frontmatter+header now both v2.12).





> (2) [SOFT] linkedin-mcp header normalized: "LinkedIn MCP — Operations Guide — v1.1" → "LINKEDIN MCP — v1.1" (removed "Operations Guide" per N-2).





> (3) [SOFT] windows-command-patterns header normalized: removed "(Python-First Protocol)" parenthetical from version header per N-2.





> Cross-reference: qnfo-core v1.14 N-2, git-github v2.14, research v2.73.











> **v1.18 UPDATE (2026-08-04, kaizen — WBS canonical registry relocation):**





> Red-team: direct parent-agent audit (session vy97NnZcIGFjkhebn1DPU).





> HARD: 1. SOFT: 0. DESIGN: 0. Changes:





> (1) [HARD] WBS canonical docs reference updated: `QNFO/qnfo-ops:WBS/WBS.TAXONOMY.md` +





>     `WBS-AGENT-PROTOCOL.md` (live governance repo) replace archived





>     `QNFO/wbs-6-synthesis:docs/` (retained as historical record, 2026-08-04).





> Cross-reference: qnfo-core v1.14 N-1, git-github v2.14, research v2.73.











> **v1.15 UPDATE (2026-08-04, kaizen — WBS protocol wiring + nomenclature standard):**





> Red-team: ecosystem-wide skills audit for consistent taxonomy/nomenclature.





> HARD: 1. SOFT: 1. DESIGN: 0. Changes:





> (1) [HARD] **WBS INTEGRATION note added to Kaizen Pipeline** — every update_plan





>     step in a kaizen run carries `[{WBS}.P{N}]` (qnfo-core N-4, WBS-AGENT-PROTOCOL





>     §2, ADR-2026-007). A kaizen run without WBS-coded steps fails its own





>     Watchtower standard. Resolve from D1 program_registry; never invent codes.





> (2) [SOFT] **Nomenclature**: version-header delimiter standardized to em-dash





>     `—` per qnfo-core N-2 (2026-08-04 ecosystem audit); `--` and `(vX.Y)`





>     formats deprecated.





> Cross-reference: qnfo-core N-2/N-4, research v2.73, execution-mandate v2.8,





> WBS-AGENT-PROTOCOL.md, session dXXJ3TxRQ1VHzGdAyp-lo.











> **v1.14 UPDATE (2026-08-04, kaizen — Red-team session closeout ktmz7cqk: full publication pipeline forensic audit):**





> Red-team: direct parent-agent retrospective audit of session ktmz7cqk





> (odr-thesis v2 + quasiparticle v2: authoring → PDF build → Zenodo publish → skill kaizen).





> HARD: 7. SOFT: 5. DESIGN: 3. Changes:





> (1) [HARD] **CONCURRENT-KAIZEN-1** — two sessions kaizening the same skill file produce





>     interleaved writes; version strings and banners collide. serialize per-skill kaizen.





> (2) [HARD] **SKILL-WRITE-COLLISION-1** + **FILE-WRITE-RACE-1** — filesystem caching





>     and concurrent writes produce stale reads. All kaizen edits MUST be a single atomic





>     Python script (read→modify→write→re-read verify).





> (3) [HARD] **BACKGROUND-PROCESS-HANG-1** — 4 of 10+ background processes hung in session.





>     Poll every 15-30s; kill after 2 no-progress polls. Never assume process is still alive.





> (4) [HARD] **PROCESS-MANAGEMENT-1** — 10+ background processes require lifecycle mgmt:





>     process list at phase start, kill stale sessions, cap 2 concurrent, explicit close().





> (5) [HARD] **SESSION-TURNOUT-1** — PDF build phase consumed ~60 tool calls debugging





>     Chrome/MathJax before reaching Zenodo. Pre-flight checklist at session start: Chromium





>     check → MathJax CDN test → pandoc version → puppeteer import test. Early BLOCK = 30+





>     diagnostic calls saved.





> (6) [HARD] **BROWSER-PROCUREMENT-1** — Chrome procurement as Phase 0 gate. One-time





>     download per machine; cached at `%USERPROFILE%\.cache\puppeteer\chrome\`.





> (7) [HARD] **MATHJAX-CDN-HEADLESS-2** — all CDN deps unreachable from Chrome headless;





>     download locally + inline before CDP.





> (8) [SOFT] **CHROME-HEADLESS-1** — canonical Chrome headless args documented (--no-sandbox,





>     --disable-gpu, --disable-dev-shm-usage). page.pdf() margin units = cm for A4.





> (9) [SOFT] **PANDOC-PATH-QUOTE-1** — pandoc not on PATH; cmd.exe PATH-prepend quoting fails.





>     Reference full canonical path directly.





> (10) [SOFT] **TEMP-VOLATILITY-3** — cross-reference to research TEMP-VOLATILITY-2 +





>     git-github SAME-TURN-COMMIT. Temp files evicted between any two agent turns.





> (11) [SOFT] **VERSION-OVERWRITE-1** — version line is the most fragile in any skill file.





>     Concurrent kaizen → check .kaizen_history for active sessions first.





> (12) [SOFT] **SESSION-KAIZEN-DISCOVERY-1** — retrospective MUST audit ALL skills touched





>     during the session, not just the primary loaded skill.





> (13) [DESIGN] **PIPELINE-CROSS-SKILL-DRIFT-1** — cross-skill pipeline fixes must





>     back-propagate to supporting skills. Research v2.55 got /actions/newversion 404 fix;





>     kaizen v1.14 now gets the equivalent pattern.





> (14) [DESIGN] **Pre-flight checklist pattern** — BROWSER-PROCUREMENT-1 + CDN check +





>     toolchain verification as a reusable gate for any publication pipeline.





> (15) [DESIGN] **Atomic skill-edit pattern** — read→modify→write→re-read in single Python





>     script as the ONLY safe pattern for multi-edit kaizen.





> Cross-reference: research v2.73, git-github v2.14, windows-command-patterns S0.0,





> session ktmz7cqkhPnG6pyZEvEMB.

















> **v1.13 UPDATE (2026-08-04, kaizen — Zenodo D1 backfill incident + ownership gate):**





> Red-team: direct parent-agent forensic audit of session dXXJ3TxRQ1VHzGdAyp-lo.





> HARD: 3. SOFT: 2. DESIGN: 1. Changes:





> (1) [HARD] **ZENODO-LINK-OWNERSHIP-1/2 + NULL-ID-UPDATE-1 anti-patterns added** —





>     blanket `zenodo_url = 'https://doi.org/'||doi WHERE doi LIKE '%zenodo%'`





>     backfill created 1,245+ fake links (external citations + garbage); rollback





>     papers 503→277, paper_ids 468→248. Research v2.71 P5.OWNERSHIP gate is the





>     enforcement mechanism; `scripts/zenodo-ownership-check.py` is the audit tool.





> (2) [HARD] **ZENODO-INPLACE-EDIT-1 heuristic added** — published-record metadata





>     edits work IN PLACE via deposit-API edit→PUT→publish (same DOI, verified on





>     322 records 2026-08-04). No newversion churn for metadata-only changes.





> (3) [SOFT] **STUB-RECORD-1 finding** — 122/293 QNFO Zenodo records (42%) are





>     contentless 105-byte README stubs (auto-indexed chapter placeholders,





>     concepts 210168xx-210171xx). Needs content backfill or PLACEHOLDER annotation.





> (4) [SOFT] **SUBAGENT-DEADLINE-1** — red-team subagents hit the 300s runTimeout





>     on API-heavy audits; re-run with runTimeoutMs ≥ 900000 for fetch-heavy tasks.





> (5) [DESIGN] **Enforcement script pattern** — gate + script + anti-pattern trio





>     (P5.OWNERSHIP + zenodo-ownership-check.py + ZENODO-LINK-OWNERSHIP-1).





> Cross-reference: research v2.73, session dXXJ3TxRQ1VHzGdAyp-lo.











> **v1.14 UPDATE (2026-08-04, kaizen — rollback execution lessons from the D1 zenodo_url incident):**





> Red-team: direct parent-agent forensic audit of the rollback execution in session dXXJ3TxRQ1VHzGdAyp-lo.





> HARD: 2. SOFT: 1. DESIGN: 0. Changes:





> (1) [HARD] **BACKFILL-PREVIEW-1 anti-pattern added** — any bulk D1 write that DERIVES





>     values (e.g., `zenodo_url = 'https://doi.org/'||doi`) MUST first run a read-only





>     classification preview (owned/external/garbage counts from the live API, printed





>     BEFORE any write) and gate the write on it. The 2026-08-04 backfill went straight





>     to UPDATE (1,245+ fake links); the rollback succeeded precisely because it





>     previewed first.





> (2) [HARD] **D1-UPDATE-SUCCESS-NE-ROWS-CHANGED anti-pattern added** — D1 returns





>     success for UPDATE calls that matched 0 rows (NULL-key WHERE clauses no-op).





>     Rollback reported "385 ok, 0 failed" while papers only dropped 503→341 (162 of





>     226 targets changed). Fix: verify with COUNT(*) before/after against the exact





>     target count + inspect response meta `changes`/`rows_written`; trust only those.





> (3) [SOFT] **NULL-ID-UPDATE-1 fix refined** — keyed rollback passes failed twice





>     (NULL identifiers); the RELIABLE pattern is keyless bulk





>     `UPDATE ... WHERE lower(zenodo_url) IN (SELECT lower('https://doi.org/'||doi) ...)





>     AND lower(doi) NOT IN (<owned list>)` — go straight to it, skip keyed passes.





> Cross-reference: research v2.73, ZENODO-LINK-OWNERSHIP-1, NULL-ID-UPDATE-1,





> session dXXJ3TxRQ1VHzGdAyp-lo.











> **v1.11 UPDATE (2026-08-03, kaizen — Session Retrospective: ecosystem audit restart cascade lessons):**





> Red-team: direct parent-agent 5-adversary audit of session YCigiA-pQ-lp7Bk83RCfK.





> HARD: 3. SOFT: 3. DESIGN: 1. Changes:





> (1) [HARD] RESTART-CASCADE-1: schtasks /create /sc once failed 3/3 times on Win11.





>     InteractiveToken + one-shot trigger never fires. Added anti-pattern.





> (2) [HARD] RESTART-CASCADE-2: Two detached restart processes created 13 zombie





>     DeepChat.exe processes + terminal pop-up loop. Added anti-pattern + lock-file protocol.





> (3) [HARD] EXEC-DEAD-1: exec tool permanently broken (powershell.exe ENOENT, -4058)





>     after restart cascade. Added anti-pattern + survival protocol.





> (4) [SOFT] AGENT-DB-STALE-1: System skill's 'agent.db' cache location is wrong —





>     actual skill registry is agent_settings.acp.skills JSON array. Documented.





> (5) [SOFT] CROSS-REF-ROT-1: 5/20 skills had stale refs after 9 deletions/merges.





>     Watchtower DRIFT-AXIS never caught it (dependency graph never built). Added anti-pattern.





> (6) [SOFT] EXEC-MANDATE-AUTOLOAD-1: execution-mandate v2.6 was on disk but not in init chain.





>     Wired into system v2.8. Added anti-pattern.





> (7) [DESIGN] WATCHTOWER-CAL-DATE-1 + NONEXEC-SURVIVAL-1: calibration comparator used





>     hardcoded future date; Watchtower step 0 needs read/skill_view fallback when exec broken.





> Cross-reference: system v2.8, execution-mandate v2.6, qnfo-core §0.6.











> **v1.10 UPDATE (2026-08-03, kaizen — subagent prohibition softened):**





> Red-team: direct parent-agent audit (subagent dispatch demonstrated, systemic truncation persisted).





> HARD: 0. SOFT: 1. DESIGN: 1.





> Changes:





> (1) [SOFT] Subagent Failure Handling HARD GATE softened: FORBIDDEN → tiered dispatch-with-fallback.





>     Subagents are now permitted for all task types with mandatory fallback protocols.





>     The tiered table replaces the v1.2.5 blanket prohibition. This resolves the direct





>     contradiction with execution-mandate v2.3 which mandates reviewer subagent dispatch.





> (2) [DESIGN] Cross-Skill Integration: added execution-mandate v2.3 for canonical subagent





>     orchestration patterns. Both skills now cross-reference each other.





> Cross-reference: execution-mandate v2.3, code v2.2.

















> (2) [HARD] **WBS-TAXONOMY-GAP closed (iteration-2 red-team)** — WBS INTEGRATION note





>     now carries a CONCRETE [QNFO.RES.001.P9]-style example in addition to the





>     [{WBS}.P{N}] template. Cross-ref qnfo-core v1.14 §N-4, research v2.73, git-github v2.14.





> **v1.20 UPDATE (2026-08-04, kaizen — self-kaizen: structural corruption repair + session retrospective):**





> Red-team: direct parent-agent audit of session 1tz85-vMiqh2TyFySznBA (IPR publication pipeline).





> HARD: 1. SOFT: 1. Changes:





> (1) [HARD] **Anti-pattern table structural corruption repaired** — ZENODO-PUB-1 row was





>     orphaned (its description cell merged into BLAME-EXTERNAL-1's line as a dangling





>     `|: Publication state fabricated...` cell). Restored as its own row. This is the





>     same copy-paste artifact class as the v3.8 windows-command-patterns duplicate §S-1.0.2.





> (2) [SOFT] Cross-skill audit findings: GIT-COMMIT-M-QUOTE-1 + EXEC-TOOL-QUOTE-1-PY





>     (windows-command-patterns v3.13), WBS-REGISTRY-STALE-1 + VECTORIZE-WEBHOOK-VERIFY-1





>     (research v2.73 + cloudflare v3.33), §0.7.1 Trap 4 (qnfo-core v1.14).





> Cross-reference: windows-command-patterns v3.13, research v2.73, qnfo-core v1.14,





> cloudflare v3.33, session 1tz85-vMiqh2TyFySznBA.











> **v1.22 UPDATE (2026-08-04, kaizen — Self-kaizen: structural repairs + cross-ref drift):**





> Red-team: direct parent-agent 5-adversary audit (session current, Watchtower-triggered).





> HARD: 3. SOFT: 2. DESIGN: 1. Changes:





> (1) [HARD] **Duplicate # KAIZEN — v1.19 header removed** — stray duplicate header/banner





>     from the v3.8/v3.9 infrastructure audit banner sequence (copy-paste artifact class





>     identical to windows-command-patterns v3.13 duplicate §S-1.0.2).





> (2) [HARD] **ZENODO-PUB-1 orphaned anti-pattern row repaired** — row had no closing pipe





>     or description cell; merged into BLAME-EXTERNAL-1's line as a dangling cell.





>     Restored as its own row with ZENODO-PUB-1 description from research v2.73.





> (3) [HARD] **Cross-reference version drift fixed** — all 4 ecosystem refs stale:





>     research v2.73→v2.67, git-github v2.12→v2.14, windows-command-patterns v3.13→v3.10,





>     qnfo-core v1.14→v1.12. DRIFT-AXIS would have scored 0.8 under Watchtower.





> (4) [SOFT] **SSESSION-KAIZEN-DISCOVERY-1 typo fixed** — double-S → single-S.





> (5) [SOFT] **Recall_facts anti-pattern gap** — recall_facts(category="anti_pattern")





>     returned empty despite 7+ anti-patterns stored via memory_remember.





>     MEMORY-DRIFT-AXIS gated: cannot scan memory→file orphans without facts data.





> Cross-reference: research v2.73, qnfo-core v1.14, windows-command-patterns v3.13,





> git-github v2.14.











> **v1.21 UPDATE (2026-08-04, kaizen — Session retrospective: Zenodo community curation):**





> Red-team: direct parent-agent audit of session 5o2rozKJQecKGz4MGRB6A.





> HARD: 0. SOFT: 2. DESIGN: 0. Changes:





> (1) [SOFT] **TOKEN-DISCOVERY-FAILURE-1 anti-pattern added** — agent asked user





>     for Zenodo token stored at C:\Users\LENOVO\tokens\zenodo and ZENODO_TOKEN env var.





>     Discovery order: tokens dir → env vars → memory → tapes → THEN user.





> (2) [SOFT] **ZENODO-CLOSED-SUBMISSION-1 anti-pattern added** — Zenodo community





>     submissions fail when record_submission_policy is "closed". Error "only allowed





>     to community members" is misleading. Check community access settings first.





> Cross-reference: qnfo-core v1.14, research v2.73, windows-command-patterns v3.13.











> **v1.23 UPDATE (2026-08-04, kaizen — Ecosystem cross-reference drift sync):**





> Red-team: direct parent-agent Watchtower-triggered audit (session current).





> HARD: 1. SOFT: 2. DESIGN: 0.





> Changes:





> (1) [HARD] **Cross-reference version drift fixed** — research v2.73 → v2.69





>     (12 occurrences: banners, anti-patterns, calibration register). Actual





>     research is v2.69; kaizen was 6 versions behind.





> (2) [SOFT] **Calibration register corrected** — "currently v2.38" → "currently





>     v2.69" (stale by 31 minor versions).





> (3) [SOFT] **cloudflare cross-refs updated** — cloudflare v3.33 → v3.30





>     (2 occurrences; cloudflare was kaizened to v3.30 in same session).





> Cross-reference: research v2.73, cloudflare v3.33, qnfo-core v1.14.











> **v1.28 UPDATE (2026-08-04, kaizen — Cross-reference ecosystem drift sync + session retrospective):**





> Red-team: direct parent-agent 5-adversary audit (session sTE5xgQ5axNas3bO_hf9 — full QNFO.RES.001 pipeline).





> HARD: 1. SOFT: 1. DESIGN: 0.





> Changes:





> (1) [HARD] **Cross-reference version drift fixed** — 4 of 5 ecosystem refs stale:





>     research v2.73→v2.71, cloudflare v3.33→v3.33, qnfo-core v1.12/v1.13→v1.14,





>     windows-command-patterns v3.10→v3.11. 15+ banner+table+anti-pattern occurrences updated.





>     DRIFT-AXIS score 0.8 captured and remediated in same session.





> (2) [SOFT] **Session retrospective** on sTE5xgQ5axNas3bO_hf9 — QNFO.RES.001 falsifiability-crisis





>     pipeline (Phases 0-7, 7 git tags, DOI 10.5281/zenodo.21791457). 0 new anti-patterns;





>     all tool failures (cmd quoting, urllib PUT, Crossref search) matched existing anti-patterns.





>     Heuristic: Edge headless PDF with --virtual-time-budget=30000 + inlined MathJax works





>     reliably (190 KB PDF).





> Cross-reference: research v2.73, cloudflare v3.33, qnfo-core v1.14, windows-command-patterns v3.13,





> git-github v2.14 (no drift).











> **v1.31 UPDATE (2026-08-05, kaizen — Windows admin elevation + TrustedInstaller registry lesson; session VBvCOsXhzlQJUubBqtdFz):**











> **v1.30 UPDATE (2026-08-04, kaizen — Zenodo phantom-DOI enforcement + deposit-API/multipart/bot-403 migration):**





> Red-team: direct parent-agent audit of session ZDdTu9QfTZKY_kJALlXY_ (Consilience Framework real





> publication, DOI 10.5281/zenodo.21803159). HARD: 1. SOFT: 1. DESIGN: 0. Changes:





> (1) [HARD] **ZENODO-PUB-1 refined → ZENODO-PHANTOM-DOI-1 enforced** — publication state claims





>     ("published / DOI issued / files uploaded") REQUIRE a same-turn tool call showing the API





>     response. The DataCite API (`api.datacite.org/dois/{doi}`) is the authoritative Zenodo-DOI





>     check: HTTP 404 is definitive proof no record exists. Fabricated DOI 10.5281/zenodo.21804582





>     in session ZDdTu9Qf was exposed by DataCite 404 and replaced with the real 10.5281/zenodo.21803159.





> (2) [SOFT] **Cross-skill migration** — ZENODO-DEPOSIT-API-LIVE-1, ZENODO-UPLOAD-MULTIPART-1,





>     ZENODO-BOT-403-1 anti-patterns migrated to research v2.74 (owning skill).





> Cross-reference: research v2.74, windows-command-patterns v3.12 (S-1.0.6), session ZDdTu9QfTZKY_kJALlXY_.











> **v1.29 UPDATE (2026-08-04, kaizen — Session Retrospective ZDdTu9QfTZKY_kJALlXY_ + red-team skills audit):**





> Red-team: direct parent-agent 5-adversary audit of session ZDdTu9QfTZKY_kJALlXY_





> (Consilience Framework synthesis — 11 deliverables, 9 memories, MCP server 7/7 tests).





> HARD: 0. SOFT: 2. DESIGN: 1. Changes:





> (1) [SOFT] **PANDOC-FONT-QUOTE-1 anti-pattern migrated to windows-command-patterns v3.12**





>     — pandoc `-V mainfont="DejaVu Serif"` fails on Windows cmd.exe (space-splitting);





>     fix is omit font flags or use Python subprocess bypass.





> (2) [SOFT] **WBS-BANNER-ALIAS-DRIFT calibration entry added** — kaizen's concrete WBS





>     examples (UMP.002, RES.001, CFE.002 from qnfo-core N-1) don't match canonical





>     WBS.TAXONOMY.md §3 (UF, CON, ADL, SR). PANDOC-FONT-QUOTE-1 calibration entry added.





> (3) [DESIGN] **Monitoring entries** for windows-command-patterns v3.12 and kaizen v1.29





>     registered for Phase 6 continuous monitoring.





> Cross-reference: windows-command-patterns v3.12, WBS.TAXONOMY.md §3, WBS-AGENT-PROTOCOL.md,





> session ZDdTu9QfTZKY_kJALlXY_.











> **v1.42 UPDATE (2026-08-05, kaizen — Red-team audit: system skill N-2 drift + template artifact):**





> Red-team: direct parent-agent 3-adversary audit of session IfYDah5TSY5gNMY0S4OT5





> cycle 2 (3 subagents truncated -> direct audit per Subagent Failure Handling rule 4).





> HARD: 1. SOFT: 1. DESIGN: 0. Changes:





> (1) [HARD] **system skill N-2 drift fixed** — header `# SYSTEM — 2.12` + footer





>     `Current: **2.12**` vs frontmatter `version: 2.13`. The v2.13 banner existed but





>     header/footer were never bumped — the **5th occurrence** of the frontmatter-drift





>     class, confirming N-2-FRONTMATTER-DRIFT-1 (v1.41) is systemic across QNFO skills.





>     Direction was REVERSE this time (frontmatter bumped, header/footer stale).





> (2) [SOFT] **system skill template artifact fixed** — `# SKILL TITLE -- v1.0` (the





>     skill-authoring template in the system skill) used the DEPRECATED `--` delimiter;





>     normalized to `—` per qnfo-core N-2 so new skills model the canonical format.





> (3) [DESIGN] **N-2-FRONTMATTER-DRIFT-1 canonical-case list extended** — now covers





>     personal-knowledge (1.0->1.3), git-github (2.16->2.18, 2.18->2.19), research





>     (2.75->2.76), system (2.12->2.13): ANY direction of drift is possible; every bump





>     MUST verify all three locations regardless of which was edited first.





> Cross-reference: qnfo-core N-2, N-2-FRONTMATTER-DRIFT-1, system v2.13,





> session IfYDah5TSY5gNMY0S4OT5.











> **v1.41 UPDATE (2026-08-05, kaizen — Red-team skills audit closeout + N-2 frontmatter drift fixes):**





> Red-team: direct parent-agent 3-adversary audit of session IfYDah5TSY5gNMY0S4OT5





> (rwnq8 profile README deploy + skill updates; 3 subagents truncated -> direct audit).





> HARD: 2. SOFT: 2. DESIGN: 1. Changes:





> (1) [HARD] **N-2-FRONTMATTER-DRIFT-1 anti-pattern added** — version bumps kept





>     forgetting the frontmatter `version:` field. 3 skills drifted this session





>     (personal-knowledge fm=1.0/hdr=1.3, git-github fm=2.16/hdr=2.18, research





>     hdr=2.75/fm=2.76). Every bump must edit fm+header+footer in ONE atomic script.





> (2) [HARD] **personal-knowledge frontmatter 1.0->1.3** + **git-github header





>     v2.18->v2.19** + **research header v2.75->v2.76** fixed.





> (3) [SOFT] **kaizen mid-file v1.31 header artifact normalized** to banner quote





>     (was the only '# KAIZEN —' line — real header missing entirely; added).





> (4) [SOFT] **personal-knowledge footer added** (had no Current: line).





> (5) [DESIGN] Watchtower scan upgraded to check fm/hdr/ft triple — the v1.39





>     single-regex scan missed frontmatter drift.





> Cross-reference: qnfo-core N-2, VERSION-OVERWRITE-1, git-github v2.19,





> research v2.76, personal-knowledge v1.3, session IfYDah5TSY5gNMY0S4OT5.











> **v1.40 UPDATE (2026-08-05, kaizen — Mined QNFO/qm: independent review, durable-by-default):**





> Red-team: direct parent-agent mining of QNFO/qm (11,420★ multiplayer agent





> harness, the parent of the 0★ yc-qm fork the user listed). Forked + cloned.





> HARD: 0. SOFT: 0. DESIGN: 1. Changes:





> (1) [DESIGN] **QM patterns added to Mined Workflow Patterns** — independent-review





>     mandate (never self-review in authoring context; reviewer has last word),





>     blast-radius-by-callers, fix-every-instance, durable-by-default (extends





>     thin-client protocol to process-memory level), security postures.





> Cross-reference: QNFO/qm fork, git-github v2.17 Thin-Client Protocol,





> user 2026-08-05 mining directive.











> **v1.39 UPDATE (2026-08-05, kaizen — VERSION-OVERWRITE-1 merge):**





> Two concurrent sessions both bumped kaizen to v1.38 with different content.





> Per VERSION-OVERWRITE-1, merged to v1.39 past the collision:





> (a) this session (IZbk2G9P2aA0JH0f0yQjj) — Mined Workflow Patterns (3-tier





>     architecture, WAT model, stakes-calibrated caution, orchestrator+specialists,





>     connections registry) from QNFO/gaios + QNFO/claude-code-tresor + QNFO/claude-code-aso-skill;





> (b) session IfYDah5TSY5gNMY0S4OT5 — PROFILE-README-FABRICATE-1, MANUAL-DELEGATE-1,





>     GITHUB-CDN-PROPAGATION-1 anti-patterns (GitHub profile deployment runbook).





> No content lost — both contributions verified present. Cross-reference:





> VERSION-OVERWRITE-1 (kaizen v1.14), SKILL-COMMIT-SAME-SESSION-1.











> **v1.38 UPDATE (2026-08-05, kaizen — Mined Workflow Patterns from the alirezarezvani ecosystem):**





> Red-team: direct parent-agent mining of QNFO/gaios (AIOS blueprint, 31★),





> QNFO/claude-code-tresor (3-tier architecture, 762★), QNFO/claude-code-aso-skill





> (orchestrator fleet, 408★). All forked separately, upstream wired, NEVER in





> DeepChat runtime dirs (EXTERNAL-SKILL-FORK-1).





> HARD: 0. SOFT: 0. DESIGN: 1. Changes:





> (1) [DESIGN] **Mined Workflow Patterns section added** — 5 adoptable patterns:





>     A. 3-tier Skills→Sub-Agents→Commands architecture + escalation; B. WAT model





>     (probabilistic reasons, deterministic executes); C. stakes-calibrated caution





>     (reversible → act + surface assumption; irreversible → confirm); D. master





>     orchestrator + specialist agents with validated deliverables; E. connections





>     registry (track reachable systems with last-checked status).





> Cross-reference: QNFO/gaios, QNFO/claude-code-tresor, QNFO/claude-code-aso-skill forks,





> user 2026-08-05 mining directive.











> **v1.37 UPDATE (2026-08-05, kaizen — SKILL-CHURN-1: churn is create→delete→recreate cycles, NOT content iteration):**





> Red-team: direct parent-agent audit (session IZbk2G9P2aA0JH0f0yQjj, user clarification).





> HARD: 1. SOFT: 0. DESIGN: 1. Changes:





> (1) [HARD] **SKILL-CHURN-1 anti-pattern added** — skill churn is DEFINED as the





>     repeated cycle of creating a skill, declaring it obsolete/unnecessary, deleting





>     it, then usually recreating it. Continuous refinement of a skill's content





>     (instructions, references, scripts, version bumps, kaizen passes) is the OPPOSITE





>     of churn — it is the mandatory, expected mode of skill maintenance. Never label





>     content iteration as churn; never avoid improving a skill out of churn-phobia.





> (2) [DESIGN] **Skill Churn vs Content Iteration section added** — definitive





>     discrimination table + rules. Content refinement is always authorized.





> Cross-reference: LANGUAGE-CONSISTENCY-1, CMD-LEGACY-1, user 2026-08-05 clarification.











> **v1.36 UPDATE (2026-08-05, kaizen — Mined Skill Best Practices: fork QNFO/claude-skills, mine don't reinvent):**





> Red-team: direct parent-agent mining of alirezarezvani/claude-skills (345 skills,





> 23,845 stars, MIT) — forked to QNFO/claude-skills (separate repo, upstream wired).





> HARD: 0. SOFT: 2. DESIGN: 1. Changes:





> (1) [DESIGN] **Mined Skill Best Practices section added** — 10 authoring patterns,





>     production pipeline quality gates (eval >=85%, delta >=30%, real-world verify),





>     quality tiers (POWERFUL/SOLID/GENERIC/WEAK), reference separation <=10KB,





>     strict-api verification. User directive: mine wisdom, don't reinvent the wheel.





> (2) [SOFT] **EXTERNAL-SKILL-FORK-1 anti-pattern added** — large third-party skill





>     repos must be forked to a SEPARATE repo (never qnfo-skills), kept OUT of





>     DeepChat runtime dirs (app slowdown/crash), and MINED for best practices.





> (3) [SOFT] **Reference-separation finding** — our skills are LARGE (kaizen 136KB,





>     cloudflare 127KB, research 118KB) vs the <=10KB standard; recognized gap,





>     refactor opportunistically (do NOT bulk-rewrite).





> Cross-reference: QNFO/claude-skills fork, git-github v2.16, user 2026-08-05.











> **v1.35 UPDATE (2026-08-05, kaizen — SKILL-COMMIT-SAME-SESSION-1: version control is 100% the agent's responsibility):**





> Red-team: direct parent-agent audit (session IZbk2G9P2aA0JH0f0yQjj, user mandate).





> HARD: 1. SOFT: 0. DESIGN: 0. Changes:





> (1) [HARD] **SKILL-COMMIT-SAME-SESSION-1 anti-pattern added** — every skill file





>     change (create/update/kaizen) MUST be committed to the qnfo-skills git repo





>     (C:\Users\LENOVO\Documents\GitHub\qnfo-skills) and pushed to origin in the





>     SAME session. Canonical case: kaizen v1.31->v1.34, system v2.11->v2.13,





>     knowledge v2.5->v2.7, email-composer v2.2->v2.3 were edited on disk for days





>     without git commits; personal-knowledge v1.0 was NEVER committed. Version





>     control is 100% the agent's responsibility — the user must never have to ask.





> (2) [HARD] **Sync direction documented** — live skills dir (.deepchat\skills) is





>     the app's load source; git repo (Documents\GitHub\qnfo-skills) is the





>     canonical version store. After ANY skill edit: copy live -> git, commit,





>     push origin. The rwnq8 mirror is archived/read-only (403) — origin only.





> Cross-reference: deepchat-settings v1.3, git-github SAME-TURN-COMMIT, user 2026-08-05.











> **v1.34 UPDATE (2026-08-05, kaizen — SKILL-DEATH-FALSE-POSITIVE-1: skill_list is the ONLY truth source; never infer skill removal from loader absence):**





> Red-team: direct parent-agent forensic audit (session IZbk2G9P2aA0JH0f0yQjj).





> HARD: 1. SOFT: 1. DESIGN: 0. Changes:





> (1) [HARD] **SKILL-DEATH-FALSE-POSITIVE-1 anti-pattern added** — execution-mandate





>     v2.8 was on disk + actively kaizened (2026-08-04) but never loaded by the app





>     (file written directly, not installed via app flow). kaizen v1.24 declared





>     `[NOT-INSTALLED]` from skill_list absence alone — a false "removal" that caused





>     user-visible skill churn. Rule: skill_list is the ONLY truth. Before declaring





>     a skill removed, check (a) skill_list, (b) .kaizen_history recency, (c) on-disk





>     state, (d) distinguish never-loaded vs was-loaded-then-removed.





> (2) [SOFT] **Cross-reference updated** — deepchat-settings v1.3 Skill Registry





>     Truth-Source section is the canonical reconciliation procedure.





> Cross-reference: deepchat-settings v1.3, user 2026-08-05 skill-churn directive.











> **v1.33 UPDATE (2026-08-05, kaizen — Language Consistency Check: remove contradictory/obsolete/ambiguous language when updating skills):**





> Red-team: direct parent-agent audit (session IZbk2G9P2aA0JH0f0yQjj, user directive).





> HARD: 0. SOFT: 2. DESIGN: 1. Changes:





> (1) [DESIGN] **Language Consistency Check section added** — regular audit of all





>     skills for deleted-script refs, non-installed skill refs, undefined KIF tags,





>     contradictions, obsolete tools, duplicate banners. Runs during every kaizen





>     closeout + Watchtower scan. User directive: "contradictory, confusing, obsolete,





>     or ambiguous language in any skill" should be a regular check.





> (2) [SOFT] **LANGUAGE-CONSISTENCY-1 anti-pattern added** — touching a skill without





>     scanning it for stale language leaves rot.





> (3) [SOFT] **CMD-LEGACY-1 anti-pattern added** — 17 /CMD slash commands in





>     custom_prompts.json referenced non-existent skills/scripts; disabled.





> (4) [SOFT] **PowerShell example fixed** → cmd.exe — PowerShell deleted 2026-08-03.





> Cross-reference: deepchat-settings v1.2, user 2026-08-05 language-consistency directive.











> **v1.32 UPDATE (2026-08-05, kaizen — Prompt Review Protocol: prompts drive agent behavior, stale prompts = stale execution):**





> Red-team: direct parent-agent audit of session IZbk2G9P2aA0JH0f0yQjj (custom prompt improvement).





> HARD: 0. SOFT: 1. DESIGN: 1. Changes:





> (1) [DESIGN] **Prompt Review Protocol added** — new AUTOMATIC subprocess in Phase R





>     (retrospective) and Phase 5 (closeout) that audits and improves custom user prompts.





>     Agent behavior is prompt-driven; stale prompts produce stale execution. 





> (2) [SOFT] **STALE-PROMPT-1 anti-pattern added** — custom prompts not reviewed for 10+





>     sessions accumulate drift as skills evolve around them.





> Cross-reference: execution-mandate, windows-command-patterns, user 2026-08-05 prompt-design injunction.











> **v1.31 UPDATE (2026-08-05, kaizen — Windows admin elevation patterns + TrustedInstaller registry lesson):**





> Red-team: direct parent-agent 5-adversary audit of session VBvCOsXhzlQJUubBqtdFz





> (bloat extermination: Edge, Office ClickToRun, Widgets; admin elevation through





> ShellExecute "runas" UAC pattern).





> HARD: 0. SOFT: 3. DESIGN: 0. Changes:





> (1) [SOFT] **WIN-ELEVATION-PARTIAL-1 anti-pattern added** — ShellExecute "runas"





>     admin elevation works for `sc`, most `reg add`, and `taskkill` but fails for





>     TrustedInstaller-protected registry keys (HKLM\Dsh, HKCU\Feeds on Windows 11).





>     When blocked, use PolicyManager MDM path or Settings GUI.





> (2) [SOFT] **Stale cross-refs fixed** — windows-command-patterns v3.13/v3.12→v3.13





>     in 8+ banner occurrences.





> (3) [SOFT] **MEMORY-DRIFT resolved** — TrustedInstaller key futility was in durable





>     memory (mem-6oSDkVvqMA4L) but absent from kaizen anti-pattern table; migrated.





> Cross-reference: windows-command-patterns v3.13, session VBvCOsXhzlQJUubBqtdFz.

















> **v1.28 UPDATE (2026-08-04, kaizen — Cross-reference ecosystem drift sync + session retrospective):**





> Red-team: direct parent-agent bias audit (session iH66zCEWF85XB0FQPfta4). HARD: 1. SOFT: 0. DESIGN: 0.





> Changes:





> (1) [HARD] **REACTIVE-ADVERSARIAL-1 anti-pattern added** — audit pipelines must be





>     adversarial by default (symmetric review of incumbents/alternatives), not only





>     when the user demands it.





> (2) [SOFT] Self-Kaizen Protocol adversarial-symmetry check added.





> Cross-reference: research v2.73, qnfo-core v1.14, user 2026-08-04 injunctions.

















> **v1.26 UPDATE (2026-08-04, kaizen — Session Retrospective: personal-life build + skill-sync git path):**





> Red-team: direct parent-agent audit of session 5ptZtvKLdqr3GzAykql8G.





> HARD: 4. SOFT: 3. DESIGN: 1. Changes:





> (1) [HARD] **SESSION-TURNOUT-2 (1102 saga):** ~35 tool calls spent bisecting the personal-life indexer





>     1102 before the root cause — a chunkText infinite loop — was found via D1 stage-logging. Lesson:





>     for ANY worker 503/1102, deploy the D1 stage-logging diagnostic FIRST (write progress row before





>     each stage; query after the 503). Never guess from debug routes that use synthetic/tiny inputs —





>     they pass while real content dies (the debug routes never chunked real files).





> (2) [HARD] **ROOT-CAUSE-CLASS-1:** "every individual op is fast, but the composition 1102s" usually =





>     an infinite loop or O(n^2) on REAL input sizes. Check for missing `break` at loop end FIRST.





> (3) [HARD] **SYNC-VERIFY-GAP:** skill-sync.js reported "GitHub + R2 in sync" while git ops silently





>     failed (cwd not a repo). Verify syncs by reading BACK from the destination, never trust the tool's





>     own success message (cross-ref system v2.13 SKILL-SYNC-GITPATH-1).





> (4) [HARD] **DESKTOP-BOUNDARY-1** cross-ref: user mandate — no Desktop/Documents writes without consent.





> (5) [SOFT] Heuristic: D1 stage-logging (debug_progress table) is the canonical 1102/worker-death bisect.





> (6) [SOFT] Heuristic: Vectorize batch ops — bulk upsert 500, string metadata, 64B IDs, {text:[]} embed





>     (see cloudflare v3.33).





> (7) [SOFT] Cross-ref: cloudflare v3.33, system v2.13, windows-command-patterns v3.13, git-github v2.14.





> (8) [DESIGN] Personal-life layer (d-drive + personal-life Vectorize/D1/Workers) is now a first-class





>     isolated ecosystem — document in cloudflare v3.33 §Vectorize Indexing Gotchas.























> **v1.17 UPDATE (2026-08-04, kaizen — infrastructure audit cross-skill anti-patterns):**





> Red-team: direct parent-agent session CGS_BRT26CX64OuSP1xJg (Cloudflare audit).





> HARD: 1. SOFT: 1. DESIGN: 0.





> Changes:





> (1) [HARD] **EXEC-TOOL-QUOTE-1 + npm-CONFIG-QUOTE-1 cross-reference**: exec tool





>     wraps absolute paths in quotes and prepends workspace path. Migrated to





>     windows-command-patterns v3.13 S-1.0.7 with full diagnosis + fix patterns.





> (2) [SOFT] **Version banner repair**: duplicative v1.15 version clause cleaned





>     (two descriptions merged on one line — copy-paste artifact).





> Cross-reference: windows-command-patterns v3.13, cloudflare v3.33,





> session CGS_BRT26CX64OuSP1xJg, session PMH0kzte.

















> **v1.9 UPDATE (2026-08-03, kaizen — GREP-SCOPE tool-failure remediation):**





> Trigger: `grep` tool denied `Access denied - path outside allowed directories:





> C:\Users\LENOVO\.deepchat\skills\...` — the grep tool is WORKSPACE-SCOPED





> (C:\Program Files\DeepChat only) while skills live under `C:\Users\LENOVO\.deepchat\skills\`.





> This breaks every protocol that instructs "grep the owning skill's SKILL.md" (Watchtower





> MEMORY-DRIFT step, Dependency-Graph build protocol). Confirmed live in session





> SHEfIEGiQvA2LI5xAPkon while kaizening research v2.73 + qnfo-core v1.5.





> Changes:





> (1) [HARD] **GREP-SCOPE-1 anti-pattern + §Tool-Scope table added** — grep tool = workspace-only.





>     For skill files use: `read` with offset pagination, `exec` python (open + in-memory





>     search), or `skill_view` (full rendered content). NEVER call grep on





>     `C:\Users\LENOVO\.deepchat\skills\**` — it returns Access denied, not results.





> (2) [HARD] **Watchtower MEMORY-DRIFT step rewritten** (was "grep the owning skill's





>     SKILL.md") → verified exec-python pattern.





> (3) [HARD] **Dependency-Graph build protocol rewritten** (was "read SKILL.md, grep for





>     cross-reference patterns") → read + python substring scan.





> (4) [SOFT] Calibration register entry added.





> Cross-reference: research v2.73 (P3.AUTHOR-GATE), qnfo-core v1.7, session





> SHEfIEGiQvA2LI5xAPkon.

















> **v1.2–v1.8 COLLAPSED HISTORY (13 banners, kaizen de-bloat 2026-08-03):**





> Historical version banners collapsed into summary. Full content in skills-archive + git history.





  - v1.8: 2026-08-03, kaizen — ODR v3.0 publication forensics





  - v1.7: 2026-08-03, kaizen — memory-to-skill drift detection + 6-axis Watchtower





  - v1.6: 2026-08-02, kaizen — ACRP infrastructure hardening





  - v1.5: 2026-08-02, kaizen — skill_manage install trap + skill-bloat metrics





  - v1.2.5: 2026-08-01, RCS + subagent audit HARD BLOCK + competing D1 scripts





  - v1.2: 2026-07-30, kaizen — autonomous CI/CD infrastructure





  - v1.2.1: 2026-07-31, sync-kaizen — gitignore allowlist gap





  - v1.2.3: 2026-07-31, calibration-drift fix





  - v1.2.5: 2026-07-31, kaizen — LinkedIn MCP session retrospective





  - v1.2.4: 2026-07-31, deferred-items closeout gate





  - v1.2.2: 2026-07-31, red-team dependency-drift fix





  - v1.4: 2026-08-02, self-kaizen — numeracy monitoring + numeracy anti-patterns





  - v1.3: 2026-07-31, deferred-item enforcement











>





> **v1.39 UPDATE (2026-08-05, kaizen — GITHUB-CDN-PROPAGATION-1 corrected: "Share to Profile" is the real fix):**





> Red-team: direct parent-agent forensic audit of session IfYDah5TSY5gNMY0S4OT5





> (rwnq8 profile README not appearing despite correct config).





> HARD: 1. SOFT: 0. DESIGN: 0. Changes:





> (1) [HARD] **GITHUB-CDN-PROPAGATION-1 REVISED** — the "5-30 min CDN wait" was wrong.





>     CLI/API-created profile repos are not auto-promoted; clicking **"Share to Profile"**





>     on the repo page promotes them IMMEDIATELY. Wait/force-push/visibility-toggle do





>     NOT help. Canonical case: rwnq8/rwnq8 — repo page rendered for 40+ min, profile





>     page empty; after clicking "Share to Profile", profile README live instantly.





> Cross-reference: personal-knowledge v1.2, git-github v2.16, session IfYDah5TSY5gNMY0S4OT5.

















## Overview











Kaizen is a continuous-improvement protocol for skills and configuration





artifacts. It has **three modes**:











1. **Reactive kaizen** — triggered by user request ("audit X skill", "update Y





   for Z change"). This is the minimum baseline.





2. **Proactive kaizen** — triggered by detecting drift signals BEFORE the user





   notices. This is the target state. The research skill's forecast integration





   (v2.31) is the canonical case study: the improvement (Forecast Integration





   Map) was NOT a user-requested fix — it was an architectural insight that





   made the "seamless weaving" of forecasting into research explicit and





   auditable.





3. **Autonomous kaizen** — runs WITHOUT user prompting. The Autonomous Watchtower





   scans all skills at session start, the Session Retrospective mines completed





   sessions for patterns, and Continuous Monitoring verifies fixes across





   subsequent sessions. This mode turns kaizen from a tool you call into an





   infrastructure that runs itself — the agent proactively maintains the skill





   ecosystem, surfacing drift and incidents before they cause failures.











### The Autonomous CI/CD Loop











```





Session Start ──► Autonomous Watchtower (Phase -1)





     │                    │





     │              Prioritized candidate list





     │                    │





     ▼                    ▼





Session Body ────► Triggered kaizen (if Watchtower flagged HARD candidates)





     │                    │





     │              Phases 0-5 (Standard Pipeline)





     │                    │





     ▼                    ▼





Session End ────► Session Retrospective (Phase R)





     │                    │





     │              Patterns → Heuristic Accumulation → Memory





     │                    │





     ▼                    ▼





Next Session ────► Continuous Monitoring (Phase 6)





     │                    │





     │              Verify fixes held; escalate if regression





     │                    │





     └────────────────────┘





     (loop: Watchtower picks up retrospective findings)





```











## Autonomous Watchtower Protocol (Phase -1, MANDATORY at session start)











**Runs at the start of EVERY session where the kaizen skill is loaded.**





This is the autonomous trigger — the agent doesn't wait to be asked.











### Watchtower Scan (6-axis health scoring)











```





For each installed skill:





  1. STALENESS-AXIS:    days since last kaizen (from .kaizen_history or memory_recall)





                        0-30 days = 0.0 | 30-60 = 0.4 | 60-90 = 0.7 | >90 = 1.0





  2. INCIDENT-AXIS:     recent session failures traced to this skill (from memory_recall





                        query: "<skill-name> failure incident")





                        0 incidents = 0.0 | 1 = 0.3 | 2-3 = 0.6 | >3 = 1.0





  3. DRIFT-AXIS:        version mismatch in cross-references (from dependency graph)





                        No drift = 0.0 | minor drift = 0.4 | major drift = 0.8





  4. CALIBRATION-AXIS:  overdue calibration register predictions (from memory_recall)





                        None overdue = 0.0 | 1 overdue = 0.3 | >1 overdue = 0.6





  5. NUMERACY-AXIS:     numeracy-related anti-patterns detected in recent sessions





                        (from memory_recall query: "<skill> numeracy OR false-precision





                        OR sigma-traceability OR derived-quantity")





                        0 flags = 0.0 | 1-2 = 0.3 | 3-5 = 0.6 | >5 = 1.0





  6. MEMORY-DRIFT-AXIS: anti-patterns stored in durable memory (recall_facts category=anti_pattern)





                        whose owning SKILL.md lacks the pattern text — memory-to-file drift.





                        0 orphans = 0.0 | 1-2 = 0.3 | 3-5 = 0.6 | >5 = 1.0





  COMPOSITE: (STALENESS × 0.32) + (INCIDENT × 0.22) + (DRIFT × 0.18) +





             (CALIBRATION × 0.10) + (NUMERACY × 0.10) + (MEMORY-DRIFT × 0.08)





```











### Watchtower Execution (MANDATORY steps)











```





0. memory_recall({query: "anti-pattern OR discovered in session"}) + 





   recall_facts(category="anti_pattern") — enumerate ALL anti-patterns in durable memory





   that name a skill. For each, search the owning skill's SKILL.md for that pattern text





   via `exec python` (open(skill_path, encoding='utf-8') + substring scan) — the grep TOOL





   is workspace-scoped and CANNOT read C:\Users\LENOVO\.deepchat\skills\** (GREP-SCOPE-1);





   `read`-with-offset and `skill_view` are alternatives.





   If absent from the skill file → MEMORY-DRIFT-AXIS score increment. This catches





   patterns that the Session Retrospective → Memory pipeline handled but the





   Memory → Skill migration pipeline missed (MEMORY-TO-SKILL-DRIFT anti-pattern).





1. skill_list() — get all installed skills and their descriptions





2. For EACH skill with score > 0.0:





   a. memory_recall({query: "<skill-name> kaizen failure incident"})





   b. Check if .kaizen_history exists and parse last kaizen date





   c. Check Calibration Register predictions for overdue entries





3. Build Skill Dependency Graph (see §Automated Skill Dependency Graph)





4. For EACH skill with cross-references:





   a. Check if referenced skill version matches actual version





   b. If drifted, compute DRIFT-AXIS score





5. Produce WATCHTOWER REPORT:





   - Top 5 skills by composite score (most fragile first)





   - Any skill with score > 0.5: flag as "kaizen candidate"





   - Any skill with score > 0.8: flag as "IMMEDIATE — HARD candidates"

   - Count-claim reconciliation: for skills with aggregate counts in prose, compare against the data file (STALE-COUNT-1)





   - Any HARD incident markers: auto-trigger kaizen without user prompt





6. memory_remember(category="task_outcome", content="Watchtower scan: N skills scanned, M flagged.")





7. If any HARD candidates exist: display watchtower report and begin Phase 0 for the highest-scoring skill.





```











### Watchtower Gate











- If **NO skill scores > 0.5:** Report "Watchtower: all skills healthy" — no action.





- If **any skill scores > 0.5 but < 0.8:** Report "Watchtower: N kaizen candidates" — queue for next session, do NOT block current session.





- If **any skill scores > 0.8:** Report "Watchtower: M IMMEDIATE candidates" — ask user with `deepchat_question`: "Kaizen on <skill> (score X.X)? Or defer?"





- If **INCIDENT-AXIS > 0.5 on any skill:** Auto-trigger kaizen — do not ask.











## Session Retrospective Protocol (Phase R, MANDATORY at session end)











**Runs at the end of EVERY session where the kaizen skill is loaded,**





or when `tape_handoff` is written. Mines the completed session for patterns.











### Retrospective Data Sources











| Source | Tool | Signal Extracted |





|:-------|:-----|:-----------------|





| **Conversation Summary** | Read from session context | Tool failures, anti-patterns mentioned, skills loaded |





| **Tape Anchors** | `tape_anchors()` | Handoff markers, kaizen sessions, incident anchors |





| **Tape Search (failures)** | `tape_search({query: "error OR failed OR 401 OR 403 OR 404 OR timeout OR truncated"})` | Tool-call failures, API errors, subagent truncations |





| **Tape Search (kaizen)** | `tape_search({query: "kaizen OR fix OR stale OR drift OR anti-pattern"})` | Prior kaizen activity, deferred fixes |





| **Memory Recall** | `memory_recall({query: "session failure OR tool error OR anti-pattern"})` | Durable patterns from prior sessions |





| **Conversation History** | `search_conversations({query: "<skill-name>", limit: 5})` | Recent sessions involving this skill |











### Retrospective Execution











```





1. Parse conversationSummary for:





   - Any mention of tool failures (e.g., "401", "403", "timeout", "truncated")





   - Any mention of anti-patterns discovered





   - Skills that were kaizened during the session





2. tape_search for failure patterns:





   - Count unique failing tool calls





   - Map each failure to the skill that would own the fix





3. For each failure → skill mapping:





   - If skill has an existing anti-pattern for this failure: note "known pattern"





   - If skill has NO anti-pattern for this failure: flag "NEW PATTERN"





4. Produce RETROSPECTIVE REGISTER:





   ```markdown





   # Session Retrospective: {session_id} @ {date}





   ## Patterns Discovered





   - [NEW] <pattern>: <skill> — <tool> failed with <error> (N occurrences)





   - [RECURRING] <pattern>: <skill> — prior fix may not have held





   ## Skills Affected





   - <skill>: <N> failure patterns, <M> new anti-patterns





   ## Kaizen Candidates (auto-escalated to Watchtower)





   - <skill>: triggered by new anti-pattern discovery





   ```





5. memory_remember(category="heuristic", content="<pattern>: <skill> — <tool> failed N times in session <id>. Root cause: <analysis>.")





6. memory_remember(category="anti_pattern", content="<skill>: discovered anti-pattern '<pattern>' in session <id>.")





7. If new patterns discovered for any skill: update that skill's Watchtower INCIDENT-AXIS score.





8. Review custom user prompts for effectiveness in this session:





   a. Did the default/user prompt trigger structured execution (update_plan, WBS codes)?





   b. Did it trigger verification and red-team review?





   c. Were there prompt-related failures (ambiguous trigger, missing gate)?





   d. If gaps found: flag for Phase 5 prompt improvement closeout.





```











### Retrospective Gate











- If **0 new patterns:** "Retrospective: clean session." Log only.





- If **1-2 new patterns:** Queue for next Autonomous Watchtower scan. Do not block.





- If **3+ new patterns OR any RECURRING pattern:** Auto-escalate to Watchtower HARD candidate.





- If **prompt review finds gaps (>0):** Queue prompt improvements for Phase 5 closeout. Do not block. Begin Phase 0 for the highest-scoring affected skill in the NEXT session.











## Continuous Monitoring Phase (Phase 6, AUTOMATIC after kaizen closeout)











After a kaizen session closes (Phase 5), the fix does NOT disappear — it enters





a lightweight monitoring window across 1-3 subsequent sessions.











### Monitoring Protocol











```





For each skill kaizened in the last 3 sessions (from memory_recall + .kaizen_history):











1. SESSION +1 (next session after kaizen):





   a. Check Session Retrospective for ANY recurrence of the fixed anti-pattern





   b. If recurrence detected → MONITORING-ALERT: escalate severity, queue full re-kaizen





   c. If no recurrence → MONITORING-PASS: log checkpoint











2. SESSION +2:





   a. Same check as +1





   b. If still clean → MONITORING-CLEAN-2: reduce monitoring intensity











3. SESSION +3:





   a. Final check





   b. If still clean → MONITORING-RESOLVED: remove from active monitoring





   c. If recurrence after +2 clean → MONITORING-REGRESSION: escalate to full re-kaizen





```











### Monitoring Registry











Maintained in durable memory with category `task_outcome`:





```





memory_remember(category="task_outcome",





  content="Monitoring checkpoint: <skill> v<N> fix #<id> | Session +1/+2/+3 | Status: PASS/ALERT/CLEAN/REGRESSION | Evidence: <from retrospective>")





```











### Escalation Rules











| Signal | Action |





|:-------|:-------|





| Recurrence at +1 | Full re-kaizen, escalate severity (SOFT → HARD) |





| Recurrence at +2 (was clean at +1) | Full re-kaizen, investigate intermittent failure |





| Recurrence at +3 (was clean at +1,+2) | Full re-kaizen, possible environmental trigger |





| Clean through +3 | Close monitoring, log MONITORING-RESOLVED |











**Adversarial-symmetry check (2026-08-04):** When kaizen audits any skill in the





research/evidence domain, the audit MUST additionally apply the symmetric-adversarial





lens — does the skill grade incumbents (GR, SM, ΛCDM, string theory) with the same





kill-criteria + null-equivalence standard it applies to new frameworks? A skill that





is adversarial only toward new theories and deferential toward established ones is





confirmation-biased (PRO-INCUMBENT-BIAS-1, research v2.73 / qnfo-core v1.14).











## Self-Kaizen Protocol (MANDATORY when kaizen audits itself)











When the kaizen skill is kaizening itself (self-kaizen), the agent MUST:











1. **Read the skill independently** — do not rely solely on subagent outputs; subagent_orchestrator truncation can lose audit findings. The parent agent must also read the full SKILL.md directly.





2. **Cross-verify every version reference** — the canonical case study (research skill) must be live-verified via `skill_view("research")` to confirm the version header matches. Never trust a `skill_list` description field for version numbers; those are separate metadata that may drift independently of the actual SKILL.md heading.





3. **Test every tool name claim** — the Runtime Context block may reference tools that were available at creation time but could have been renamed/deprecated. Verify each tool name against the current available tools list.





4. **Use `update_plan` from Phase 0** — track progress through Phases 0-5 with the progress checklist tool so the self-kaizen execution is auditable.











## Subagent Failure Handling (MANDATORY)











**v1.10 UPDATE (2026-08-03):** Subagent prohibition softened. The execution-mandate





skill (v2.3) provides the canonical subagent orchestration patterns: dispatch at every





phase with tiered fallback (non-blocking advisory for Phases 0/1/4, blocking-with-fallback





for Phases 2/3.5). The systemic truncation finding remains true — subagents ARE unreliable





for complete output — but the correct response is NOT prohibition; it is **dispatch with





mandatory fallback.** Every subagent dispatch for audit MUST include: (a) a fallback





protocol (default: direct parent-agent audit), (b) a timeout, and (c) a non-blocking





path for the parent to continue. See `execution-mandate` §Multi-Phase Subagent Orchestration





for the full decision matrix.











**Tiered subagent usage (replaces v1.2.5 HARD GATE):**











| Task Type | Subagent? | Mode | Fallback |





|---|---|---|---|





| **Complete audit findings** (red-team, verification) | YES — dispatch, wait, fall back | `parallel` | Direct parent-agent audit if ALL truncate |





| **Partial audit** (explorer pre-scan, assumption challenge) | YES — non-blocking advisory | `parallel` | Skip if unavailable, log gap |





| **Parallel search/exploration** | YES — primary use case | `parallel` | Parent runs sequential search |





| **Implementation of independent components** | YES — with caution | `parallel` | Parent re-implements if output truncated |











**Previously (v1.2.5, now RETIRED):** Subagents were FORBIDDEN for audit tasks.





This prohibition created a contradiction with the execution-mandate skill (v2.2+)





which MANDATES reviewer subagent dispatch. The tiered approach resolves this:





dispatch subagents, expect truncation, always have a parent-agent fallback.











When subagent_orchestrator outputs are truncated, the parent agent MUST:











1. **Assume findings were lost** — truncated output is equivalent to "subagent did not complete." Do not treat partial output as a findings report.





2. **Fall back to direct audit** — the parent agent reads the target skill directly and performs the audit dimensions itself. The explorer/reviewer roles are assigned as perspectives the parent agent adopts sequentially, not as subagent delegations that can silently fail.





3. **Report the failure** — in the kaizen closeout banner, note: "N subagents attempted, M completed with full output; (N-M) fell back to direct parent-agent audit due to truncation."





4. **Fall back immediately — do not poll repeatedly** — when a subagent's output shows file-reads but produces no findings beyond that, the signal is clear: truncation occurred. Fall back on the **second** tool call (first poll to confirm truncation pattern, then direct audit), not on the tenth. Repeated polling of stuck subagents wastes tool calls and delays the audit. A subagent that reads input files but produces zero findings by the second poll is a truncated subagent — pivot immediately.











## Kaizen Pipeline (Standard Execution)











**WBS INTEGRATION (v1.15):** Per qnfo-core N-4 + WBS-AGENT-PROTOCOL.md §2





(ADR-2026-007), every `update_plan` step in a kaizen run carries a canonical WBS





code prefix `[{WBS}.P{N}]` (e.g., `[QNFO.KAIZEN.P1]`). Kaizen phases map to WBS





P9-extension semantics (audit/update/verify/closeout) but the code resolves to





the TARGET SKILL's WBS registration, not a research phase. Resolve the code from





D1 `program_registry` or use `[{WBS}.P{N}]` template form; never invent codes.











**CONCRETE EXAMPLE (v1.18, iteration-2 kaizen):** a kaizen run on the Ultrametric





Physics program's git skill uses `[QNFO.UMP.002.P9]` prefixes; a kaizen run on the





research skill itself uses `[QNFO.RES.001.P9]`. The program code (UMP, RES, ...) is





the TARGET skill's owning program from qnfo-core §N-1 — resolve before starting.











```python





update_plan([





  {"step": "[QNFO.RES.001.P9] Kaizen P0: trigger detection + pre-flight memory_recall", "status": "in_progress"},





  {"step": "[QNFO.RES.001.P9] Kaizen P1: skill audit (explorer)", "status": "pending"},





  {"step": "[QNFO.RES.001.P9] Kaizen P2: red-team review (5 adversaries)", "status": "pending"},





  {"step": "[QNFO.RES.001.P9] Kaizen P3-P5: fixes, verification, closeout", "status": "pending"},





])





```





Canonical docs: `QNFO/qnfo-ops:WBS/WBS.TAXONOMY.md` +





`QNFO/qnfo-ops:WBS/WBS-AGENT-PROTOCOL.md` (live governance repo). The Watchtower's plan-step audit (INCIDENT-AXIS)





checks for these prefixes — a kaizen run without WBS-coded steps fails its own





standard.











### Phase 0: Trigger Detection











**Pre-flight checks (run BEFORE Phase 1):**





- `memory_recall({query: "<skill-name> kaizen"})` — check for prior kaizen sessions on this skill. Log the most recent session date and version.





- `tape_info()` — inspect current session tape for related kaizen activity.





- `tape_anchors()` — check for recent kaizen handoff anchors.





- **Check Autonomous Watchtower report** — if this kaizen was triggered by Watchtower, log the trigger score and axes.





- **Check Session Retrospective** — if this kaizen was triggered by retrospective pattern discovery, log the pattern and occurrence count.





- If a prior kaizen session completed within the last 24 hours on the same skill, flag `[RECENT-KAIZEN: <date>, v<version>]` and confirm the user wants to kaizen again. Double-kaizen (two consecutive kaizen sessions with no user changes between them) is an anti-pattern.











Kaizen initiates from one of these signals:











| Signal | Example | Reactive / Proactive / Autonomous |





|:-------|:--------|:----------------------------------|





| **User directive** | "Audit X skill" | Reactive |





| **Cross-skill version drift** | Skill A references Skill B v2.3, but B is now v3.0 | Proactive |





| **Tool capability change** | New MCP server available, skill doesn't use it | Proactive |





| **Dependency retirement** | Script deleted in a parent skill, child skill still references it | Proactive |





| **Self-audit interval** | Any skill not kaizen'd in >30 days | Proactive |





| **Forecast signal** | Structured forecast predicts a skill will need update within N weeks | Proactive |





| **Incident-triggered** | A session failed because a skill was wrong (e.g., stale token, deleted script) | Reactive |





| **Watchtower HARD candidate** | Autonomous Watchtower scores skill > 0.8 | Autonomous |





| **Watchtower INCIDENT-AXIS > 0.5** | Session retrospective found tool failures traced to this skill | Autonomous |





| **Retrospective new pattern** | Session retrospective discovered 3+ new anti-patterns | Autonomous |





| **Continuous monitoring regression** | Phase 6 monitoring detected fix recurrence at +1/+2/+3 | Autonomous |











> **Disambiguation:** Where this skill says "Phase 4 (Structured Forecast)," it refers to the **research skill's** Phase 4 (Deep Research & Structured Forecast Protocol). The kaizen skill's own Phase 4 is "Verification Gate." Context determines which is meant: the case study and forecast protocol sections reference the research skill; the pipeline phases reference kaizen itself.











### Phase 1: Skill Audit (Explorer Subagent)











Delegate to an **explorer** subagent: read the target skill end-to-end, produce





a structured audit report.











**SUBAGENT FILE-SCAN MANDATE (v1.12, write-then-exec):** When the subagent must





scan skill files outside the workspace, the prompt MUST state verbatim:





"Write the Python to a temp .py file (C:\Users\LENOVO\AppData\Local\Temp\_scan.py),





exec python <file>, then delete the file. NEVER use inline python -c." Inline





`python -c` (a) streams the full script into the UI as the exec payload, and





(b) violates windows-command-patterns S0.0 (inline -c = ABORT). Verified in





session SmmvWPPw (SUBAGENT-INLINE-PYTHON-1, 2026-08-03).











**Audit dimensions:**











1. **Staleness Audit** — Does the skill reference deleted scripts, deprecated





   tool names, retired endpoints, or stale version numbers?





2. **Contradiction Audit** — Does any section contradict another? Does the





   `execute_plan` match what phase sections actually describe?





3. **Completeness Audit** — Are all gates covered? Missing verification steps?





   Missing anti-patterns?





4. **Cross-Skill Dependency Audit** — Does this skill reference other skills





   that have version-drifted? Do those skills still have the sections/versions





   referenced?





5. **Structural Audit** — Duplicate sections? Copy-paste artifacts?





   Anti-patterns appearing multiple times? Banners that restate the same thing?





6. **Capability Gap Audit** — Are there new tools, MCP servers, or patterns





   this skill should leverage but doesn't?











**Output:** A structured audit report with line numbers, severity ratings





(HARD/SOFT/DESIGN), and proposed fixes for each finding.











### Phase 2: Red-Team Review (Reviewer Subagents — PARALLEL)











**MANDATORY for every kaizen.** Run 3-5 reviewer subagents in parallel, each





assigned one adversarial perspective:











| Reviewer Role | Core Question | Assignment |





|:--------------|:--------------|:-----------|





| **Accuracy Auditor** | Are the skill's factual claims still true? (endpoints, tool names, file paths, script existence, version numbers) | Verify every external reference |





| **Completeness Auditor** | What's missing? (gates, anti-patterns, edge cases, new capability integration) | Gap analysis against ecosystem |





| **Dependency Auditor** | Do cross-skill references resolve correctly? Have referenced skills drifted? | Cross-reference all `See X skill vN.M` claims |





| **Novelty Auditor** | What new capabilities should this skill leverage? (new MCP servers, new tools, new patterns from other skills) | Capability-matrix gap scan |





| **Status Auditor** | Are all version banners accurate? Is the closing banner current? Are KIF tags consistent? | Banners + metadata reconciliation |











**Orchestration pattern:**





```





subagent_orchestrator(operation="run", mode="parallel", tasks=[





  {slotId: "reviewer", title: "Accuracy", ...},





  {slotId: "reviewer", title: "Completeness", ...},





  {slotId: "reviewer", title: "Dependency", ...},





  {slotId: "reviewer", title: "Novelty", ...},





  {slotId: "reviewer", title: "Status", ...},





])





```











**Gate:** Phase 3 (apply fixes) MUST NOT begin until ALL reviewer subagents





have returned findings. This is a HARD GATE — partial review is no review.











**Minimum bar:** At least 3 of the 5 roles must complete. If only 2 can run





(insufficient subagent slots), run the remaining roles sequentially in the





parent session. Never skip a role.











### Phase 3: Apply Fixes (Implementer — SEQUENTIAL after Phase 2)











Collate all audit findings (Phase 1 + Phase 2) into a prioritized fix list:











| Priority | Definition | Action |





|:---------|:-----------|:-------|





| **HARD** | Would cause a session failure if not fixed (stale endpoint, deleted script, wrong tool name) | Fix immediately, before any other change |





| **SOFT** | Degrades quality but doesn't break execution (duplicate text, formatting, missing anti-pattern) | Fix in this kaizen session |





| **DESIGN** | Architectural improvement (new section, restructured workflow, forecast integration) | Fix in this kaizen session; document rationale |











Apply fixes using the `edit` tool (surgical) or `write` (full rewrite). After





each fix, verify with `read` that the change landed correctly.











**Implementation principle:** Batch related fixes when safe, but NEVER fix





multiple HARD issues in one edit — each HARD fix gets its own tool call so





a partial failure doesn't leave the skill in an unknown state.











### Phase 4: Verification Gate











After all fixes applied:











1. **Self-verification:** Re-run the audit checks from Phase 1 against the





   updated skill. Confirm every finding is resolved.





2. **Red-team re-review:** Run at least ONE reviewer subagent against the





   updated skill with a fresh prompt: "Verify all fixes from [kaizen session]





   were applied correctly. Find any remaining gaps."





3. **Cross-skill sync check:** If this kaizen involved cross-skill changes,





   verify the OTHER skill's version/references are updated too.





4. **Critical gate:** If any HARD finding is not verifiably fixed, BLOCK





   the closeout. Do not declare kaizen complete with unresolved HARD issues.











### Phase 5: Closeout











**STEP -2 — SKILL-GIT-COMMIT GATE (HARD, added 2026-08-05):**





Before ANY closeout, verify every skill touched this session is committed to git:











```





1. List all skills edited this session (SKILL.md files written/edited)





2. For EACH: verify git repo (Documents\GitHub\qnfo-skills) has the change:





   git -C <repo> status --short  -> must be clean (0 uncommitted skill changes)





3. If any skill change is uncommitted: copy live -> git, commit, push origin





4. Gate: closeout is BLOCKED until git status shows 0 skill changes





```











Version control is 100% the agent's responsibility. A closeout that leaves





skill changes uncommitted is a FAILED closeout (SKILL-COMMIT-SAME-SESSION-1).











**STEP -1 — PROMPT REVIEW GATE (added 2026-08-05):**





Before the deferred-items gate, audit the session's custom user prompts:











```





1. List all configured custom user prompt templates (from DeepChat Settings → Prompts)





2. For each prompt, check alignment with current skill capabilities:





   - Does it trigger structured execution (update_plan, WBS codes)?





   - Does it trigger verification gates (VERIFY/RED-TEAM)?





   - Does it trigger subagent deployment for parallel work?





   - Is it concise enough to be "brainless" (usable without thinking)?





3. If prompts are suboptimal:





   a. Propose improved prompt text





   b. Guide user to apply in Settings → Prompts





   c. Register change in closeout banner





4. If prompts are clean: log "Prompt review: all prompts align with current capabilities."





```

















**STEP 0 — DEFERRED-ITEM GATE (HARD, MANDATORY — added 2026-07-31):**





Before ANY closeout is declared successful, the agent MUST audit all deferred items from





prior sessions and this session:











```





1. memory_recall({query: "deferred OR pending OR not started OR remains"})





2. Parse the session's own deferred items (anything marked DEFERRED/PENDING/BLOCKED)





3. For EACH deferred item:





   a. EXECUTE it now if possible (CLI/API/command-line only — no Dashboard, no manual UI)





   b. If genuinely blocked, document EXACTLY why (missing credential, external dependency,





      API limitation) with evidence, and set a concrete follow-up trigger





4. If ANY deferred item remains unexecuted WITHOUT a documented blocker: CLOSEOUT IS BLOCKED.





   Do not declare kaizen complete.





```











**GATE:** Closeout is successful ONLY when zero deferred items remain, OR every remaining





item carries a documented blocker with an evidence trail and a follow-up trigger. A





"deferred" list that survives a closeout without resolution is a FAILED closeout.











```





1. VERSION BUMP: Increment the skill's version in the SKILL.md header





   (e.g., "# SKILLNAME -- v1.0" → "# SKILLNAME -- v1.1")





2. KAIZEN BANNER: Insert a dated banner summarizing ALL changes, including





   which red-team roles found what. Format:





   > **vN.M UPDATE (YYYY-MM-DD, kaizen):**





   > Red-team review: N parallel subagents + direct forensic audit.





   > Changes: (1)... (2)... (3)...





   > Cross-reference: [any related skill updates].





3. MEMORY: `memory_remember(category="task_outcome")` with a summary of





   changes and the new version.





4. TAPE: `tape_handoff(name="kaizen/<skill-name>-vN.M", summary="...")`





5. SYNC: If this is a live-installed skill, ensure the on-disk file is





   current. No git commit required for skill files outside a repo.





6. KAIZEN HISTORY LOG: Append entry to `.kaizen_history` or `kaizen-history.json`.





7. CALIBRATION REGISTER: Update the skill's calibration register with new





   fragility predictions.





8. KNOWLEDGE GRAPH: If applicable, create/update KG edges for cross-skill





   impact tracing (see §Knowledge Graph Feedback Loop).





9. MONITORING REGISTRY: Register this fix in the Continuous Monitoring





   registry for Phase 6 follow-up.





```











### Phase 5 Step 0: Deferred-Items Closeout Gate (HARD GATE — MANDATORY)











**Effective: 2026-07-31 (v1.2.4). A kaizen closeout is NOT successful if any





deferred item remains unresolved.**











Before declaring any closeout "successful," execute the Deferred-Items Audit:











```





1. ENUMERATE: list every item deferred during the session (deferred fixes,





   blocked tasks, pending verifications, waiting credentials/rate-limits).





2. ATTEMPT RESOLUTION: for each item, attempt to resolve it NOW. Do not





   assume "it will be handled next session."





3. CLASSIFY each item as:





   - RESOLVED: completed and verified in this session





   - EXTERNAL-BLOCK: genuinely blocked by an external condition (rate limit,





     missing credential, service outage) that cannot be cleared this session





   - UNRESOLVED: could be resolved but was not





4. DECLARE:





   - ALL items RESOLVED → closeout is "successful" ✅





   - Any EXTERNAL-BLOCK → closeout MUST read:





     `[CLOSEOUT-INCOMPLETE: <item> blocked by <reason> — retry scheduled]`





     and produce a continuation handoff for the next session.





   - Any UNRESOLVED → closeout is BLOCKED. Resolve now, or re-classify as





     EXTERNAL-BLOCK with evidence, or the closeout is a FAILURE.





```











**Anti-pattern:** declaring "closeout successful" while a deferred item list





exists anywhere in the session. The word "deferred" and the word "successful"





are mutually exclusive in a closeout declaration.











### Phase 6: Continuous Monitoring Registration (MANDATORY after every kaizen closeout)











After Phase 5 completes, register the fix for monitoring:











```





1. memory_remember(category="task_outcome",





   content="Monitoring entry: <skill> v<N> | Fixes: <list of fix IDs> | 





            Session +0: kaizen complete | Next check: session +1")





2. Set a Watchtower calibration register prediction:





   "[CHECK: <date + 3 sessions>] <skill> v<N> fixes will hold through +3 monitoring checkpoints.





    Recurrence risk: [LOW/MODERATE/HIGH] based on fix type."





```











## Proactive Kaizen: The Forecast-Driven Model











### Why Reactive-Only Kaizen Fails











Reactive kaizen (waiting for the user to say "audit X") has a systematic blind





spot: it only finds problems the user already suspects. Problems the user





doesn't know about — stale references in skills they haven't loaded recently,





cross-skill version drift, new capabilities not yet integrated — accumulate





silently until they cause a session failure.











### The Forecast-Driven Alternative











For skills that are part of an active ecosystem (multiple interdependent skills





evolving in parallel), run a **proactive kaizen forecast** at regular intervals





or after any significant ecosystem change (major skill version bump, new MCP





server deployment, tool retirement).











**Protocol (adapted from the research skill's Structured Forecast Protocol):**











1. **Domain Assessment:** Map the skill ecosystem. Which skills depend on which





   others? What external dependencies (MCP servers, APIs, tools) does each





   skill have?











2. **Drift Candidate Identification:** For each skill, identify:





   - Cross-references to other skills with specific version numbers





   - References to scripts in other skills





   - References to tools/APIs that might change





   - Anti-patterns that reference deprecated workflows











3. **Assumption Audit:** For each cross-reference, ask: "What would have to





   change in the referenced skill to make THIS skill's reference stale?"





   Flag every assumption.











4. **Red-Team Challenge:** "What is the MOST LIKELY thing to break in this





   skill within the next 30 days?" Run the answer through the 5-adversary





   framework from Phase 2.











5. **Calibration Register:** For each identified risk, register a dated





   prediction: "[CHECK: YYYY-MM-DD] Skill X will need update because





   dependency Y will change by [date]."











6. **Effort Allocation:** Rank skills by predicted fragility. Most-fragile





   skills get kaizen'd first.











**Case Study: Research Skill v2.31 Forecast Integration**











The Forecast Integration Map added in v2.31 was a proactive kaizen finding.





It was NOT triggered by a user complaint or a broken reference — it was





triggered by the observation that:











- Phase 4 (Structured Forecast) was mandatory for ALL research projects





- But there was no explicit map showing HOW forecast outputs fed into





  Phases 1-8





- An agent could treat forecasting as a standalone deliverable to "check off"





  rather than the analytical engine generating the paper's claims











This finding was discovered by applying the **Novelty Auditor** perspective:





"What structural improvement would make the integration so explicit that no





agent could misunderstand it?" The answer was a cross-reference table mapping





every forecast stage to its publication-phase integration point.











The user's feedback ("I like how forecasting is seamlessly woven in") confirmed





the value of this proactive approach. Reactive kaizen would never have





suggested this — only proactive gap-scanning did.











### When to Run Proactive Kaizen











| Trigger | Action |





|:--------|:-------|





| Any skill reaches a major version bump (v2.0 → v3.0) | Kaizen all skills that reference it |





| New MCP server deployed | Scan all skills for capability gaps |





| Tool deprecation announced | Kaizen all skills that use the deprecated tool |





| >30 days since last kaizen on any skill | Run the proactive forecast protocol |





| Session failure traced to a stale skill reference | Kaizen the failing skill + all skills that reference it |





| **Scheduled audit (daily)** | Use `cronjob` to run Autonomous Watchtower scan of all installed skills; review HARD candidates before next session |





| **Watchtower score > 0.5** | Queue for next available session; do not block |





| **Watchtower score > 0.8** | Immediate kaizen — begin Phase 0 |











## Red-Team Integration (MANDATORY)











### The 5-Adversary Framework











Every kaizen MUST include ALL five adversary perspectives. No skipping "because





this is a simple update." A simple update can hide a complex oversight.











| # | Adversary | Question | Assignment to Subagent |





|:--|:----------|:---------|:----------------------|





| 1 | Accuracy Auditor | "These claims are wrong — here's why" | `slotId: "reviewer"` |





| 2 | Completeness Auditor | "This is missing critical gates — here's what's absent" | `slotId: "reviewer"` |





| 3 | Dependency Auditor | "Cross-references are broken — skill X moved to v3, this still says v2" | `slotId: "reviewer"` |





| 4 | Novelty Auditor | "This skill is outdated — it should use [new capability] but doesn't" | `slotId: "reviewer"` |





| 5 | Status Auditor | "Version banners are contradictory — v2.3 claims a fix that v2.4 says was reverted" | `slotId: "reviewer"` |











### Subagent Configuration











```





Subagent slots:





- reviewer × 5 (for parallel red-team audit)





- explorer × 1 (for initial skill audit in Phase 1)





- implementer × 1 (for applying fixes in Phase 3, if needed — 





  usually the parent agent does this directly)











Parallel mode: Phase 2 (all 5 reviewers run concurrently)





Sequential dependency: Phase 2 MUST complete before Phase 3 begins





```











### Minimum Viable Red-Team (when subagent slots are limited)











If only 2 reviewer slots exist:





1. **First wave (parallel):** Accuracy + Completeness





2. **Second wave (parallel):** Dependency + Novelty





3. **Third wave (direct):** Status audit (parent agent)











If only 1 reviewer slot exists:





1. Run all 5 sequentially





2. Each gets a FRESH subagent session (no context contamination)





3. This is slower but still complete — speed is sacrificed, not thoroughness











## Knowledge Graph Feedback Loop (MANDATORY for autonomous CI/CD)











Kaizen findings create structured Knowledge Graph edges for cross-skill impact





tracing. This makes the skill ecosystem navigable — when skill A is kaizened,





the agent can query which skills depend on A and assess cascade risk.











### Edge Types











| Edge | From | To | Meaning |





|:-----|:-----|:---|:--------|





| `KAIZENED_IN` | Skill node | Session node | This skill was kaizened in this session |





| `DEPENDS_ON` | Skill A | Skill B | Skill A references Skill B in its cross-skill integration table |





| `TRIGGERED` | Incident node | Kaizen session | This incident triggered this kaizen |





| `MONITORED_BY` | Skill (version) | Monitoring entry | This fix is under continuous monitoring |





| `DISCOVERED_IN` | Anti-pattern node | Session node | This anti-pattern was discovered in this session |





| `REGISTERED_IN` | Calibration prediction | Skill node | This prediction belongs to this skill |











### Protocol (run during Phase 5 closeout)











```





1. If the target skill has a KG node: add KAIZENED_IN edge to current session





2. For each cross-skill reference found during dependency audit:





   a. Verify or create DEPENDS_ON edge between skills





   b. If version drift was detected: annotate edge with drift metadata





3. If the kaizen was triggered by an incident: add TRIGGERED edge





4. If new anti-patterns were discovered: create anti-pattern node + DISCOVERED_IN edge





5. If calibration register updated: create REGISTERED_IN edge





6. Update skill's KG node with: latest version, last kaizen date, composite health score





```











### Dependency Graph Maintenance











The Automated Skill Dependency Graph (built by the Watchtower) maps all





`DEPENDS_ON` edges between skills. This graph enables:











- **Impact analysis:** "If I kaizen skill A, which other skills need cascade updates?"





- **Drift detection:** "Skill B references A v2.0, but A is now v3.0 — drift."





- **Fragility ranking:** "Skill C depends on 5 other skills — highest cascade risk."











**Build protocol (Watchtower run):**





```





1. skill_list() → get all skill paths





2. For each skill: read SKILL.md (or `skill_view`), then scan for cross-reference patterns





   via `exec python` (open + substring scan — grep TOOL is workspace-scoped, cannot read





   C:\Users\LENOVO\.deepchat\skills\** per GREP-SCOPE-1):





   - "See `X` skill vN.M"





   - "Load `X` for..."





   - "Cross-Skill Integration" table entries (excluding tools)





3. Build DEPENDS_ON edges in the dependency graph





4. Store in durable memory for rapid lookup:





   memory_remember(category="project_fact", content="Skill dependency graph: <skill> DEPENDS_ON [list]")





```











## Heuristic Accumulation Protocol (AUTOMATIC)











Sessions produce heuristics continuously — an anti-pattern discovered during





a research session, a workaround for a PowerShell bug, a new validation gate.





The Heuristic Accumulation Protocol ensures these don't disappear when the





session ends.











### Protocol (run during Session Retrospective)











```





For each pattern discovered during the session:











1. Determine the skill that OWNS this pattern:





   - If tool-failure pattern: the skill that instructs use of that tool





   - If anti-pattern: the skill that would be improved by documenting it





   - If workaround: the skill whose instructions need the workaround











2. memory_remember(category="anti_pattern",





   content="<skill-name>: <pattern description>. Discovered in session <id>. 





            Occurrences: <N>. Root cause: <analysis>.")





   — OR —





   memory_remember(category="heuristic",





   content="<skill-name>: <workaround or improvement>. Discovered in session <id>.")











3. Increment the owning skill's Watchtower INCIDENT-AXIS counter:





   - This makes the Watchtower more likely to trigger a kaizen on that skill











4. If pattern has 3+ occurrences across sessions (check via memory_recall):





   - Auto-escalate to Watchtower HARD candidate





   - Flag: "[ACCUMULATED-PATTERN: <pattern> has N occurrences across sessions]"





```











### Heuristic Categories











| Category | Storage | Watchtower Impact | Example |





|:---------|:--------|:------------------|:--------|





| `anti_pattern` | memory_remember(category="anti_pattern") | INCIDENT-AXIS +0.3 | "cmd.exe inline python -c fails with nested quotes" |





| `heuristic` | memory_remember(category="heuristic") | Low (documentation) | "Use write→exec→delete pattern for multi-line Python" |





| `task_outcome` | memory_remember(category="task_outcome") | Monitoring only | "Fix #3 held through +2 checkpoints" |





| `project_fact` | memory_remember(category="project_fact") | Dependency graph | "Skill dependency graph snapshot" |











## Prompt Review Protocol (AUTOMATIC)











The agent's behavior is driven by prompts — system prompts, custom user prompts,





and skill-level prompt templates. **An agent is only as good as the prompts that





drive it to execute and act.** Stale, verbose, or misaligned prompts degrade agent





performance across ALL tasks. This protocol ensures prompts are continuously





reviewed and improved as part of the kaizen CI/CD loop.











### Prompt Health Signals











| Signal | Meaning | Action |





|:-------|:--------|:-------|





| Session produced no update_plan usage | Prompt didn't trigger structured execution | Add PLAN/EXECUTE language to default prompt |





| Session produced phantom claims | Prompt lacks verification gates | Add VERIFY/RED-TEAM gates to default prompt |





| Session raced without pre-flight | Prompt lacks context-gathering mandate | Add PRE-FLIGHT language to default prompt |





| User repeatedly pastes verbose template | Prompt is too long to remember | Simplify to brainless trigger (≤1 word) |





| Subagents not used despite parallel work | Prompt lacks subagent deployment mandate | Add subagent dispatch language |





| Session produced 0 tool-call-backed claims | Prompt doesn't mandate evidence | Add "every claim requires tool call" gate |











### Two-Prompt Architecture (canonical as of 2026-08-05)











The QNFO ecosystem uses exactly TWO reusable prompt templates:











| Template | Purpose | Canonical Text |





|:---------|:--------|:---------------|





| **Default (Continuation)** | Brainless session progression — plan → execute → verify → iterate | `CONTINUE` |





| **Process Improvement** | Trigger full kaizen cycle — red-team audit → skill updates → closeout | Per SKILLS UPDATE template |











The default prompt must be "brainless" — one word, no thinking required. The agent's





system prompt already encodes structured execution, verification, red-teaming, and





subagent deployment. The user prompt is a trigger, not a specification.

















## Mined Skill Best Practices (from QNFO/claude-skills, added 2026-08-05)











**Source:** `alirezarezvani/claude-skills` (345 skills, 23,845 stars, MIT) — forked





to **`QNFO/claude-skills`** (separate repo, upstream wired, NOT in qnfo-skills,





NOT in DeepChat runtime dirs). Local clone: `C:\Users\LENOVO\Documents\GitHub\claude-skills`.





The repo is a MINING SOURCE — read its `SKILL-AUTHORING-STANDARD.md` and





`SKILL_PIPELINE.md` for the full text. Key wisdom distilled below.











### The 10 Authoring Patterns (apply when creating/updating skills)











1. **Context-First** — check for a domain context file before asking questions;





   ask only for what's missing, one section at a time.





2. **Practitioner Voice** — open with "You are an expert in X. Your goal is Y."





   Opinionated, direct ("Do X" beats "You might consider X"). Rewrite anything





   that sounds like Wikipedia/marketing copy.





3. **Multi-Mode Workflows** — design 2-3 entry points: Build from Scratch /





   Optimize Existing / Situation-Specific. Each self-contained.





4. **Related Skills Navigation** — 3-7 curated references with WHEN and WHEN-NOT





   disambiguation; bidirectional cross-refs.





5. **Reference Separation** — SKILL.md <=10KB (workflow + decisions); heavy





   knowledge in `references/` (loaded on demand, self-contained); templates/;





   stdlib-only scripts/. If SKILL.md is longer, move content to references.





6. **Proactive Triggers** — 4-6 "surface this without being asked" conditions,





   format: condition -> flag -> recommended action. Trigger on hidden risks.





7. **Output Artifacts** — map common requests to concrete deliverables





   (scorecard, matrix, plan, audit) with explicit formats.





8. **Quality Loop** — self-verify (source attribution, assumption audit,





   confidence scoring); peer-verify cross-functional claims; confidence tags.





9. **Communication Standard** — BOTTOM LINE first -> WHAT (max 5 bullets) ->





   WHY THIS MATTERS -> HOW TO ACT (owner + deadline) -> YOUR DECISION (options





   with trade-offs). No process narration; results only.





10. **Python Tools** — stdlib-only (zero deps), CLI-first, JSON output,





    embedded sample data, one tool one job, 0-100 scoring scale.





    Naming: `snake_case_verb_noun.py`.











### Production Pipeline Quality Gates (from SKILL_PIPELINE.md)











```





Intent -> Research -> Draft -> Eval -> Iterate -> Compliance -> Package ->





Deploy -> Verify -> Rollback-Ready





```











- **Eval gate:** pass rate >=85% with-skill; delta vs baseline >=+30%; variance





  <20% (no flaky evals). Save evals to `evals/evals.json` (test cases + assertions).





- **Iteration limits:** max 5 iterations / 3 hours per skill eval loop, then escalate.





- **Real-world verification NEVER SKIP:** install test, trigger test (3 should /





  2 should-not), functional test (scripts with sample data), bug-fix protocol





  (fix immediately, document in CHANGELOG, re-run evals).





- **Rollback protocol:** `git revert` fast-merge; document `### Reverted` in CHANGELOG.





- **Semver:** patch 2.1.x (improvements), minor 2.7.0 (new skills), major 3.0.0 (breaking).





- **CHANGELOG per commit** — every change, every fix. Category README + CLAUDE.md





  updated per commit; root README + docs per release.











### Quality Tiers (rate skills; only ship POWERFUL)











| Tier | Score | Criteria |





|:-----|:-----:|:---------|





| **POWERFUL** | 85%+ | Expert-level, scripts, refs, evals pass, real-world utility |





| **SOLID** | 70-84% | Good knowledge, some automation, useful |





| **GENERIC** | 55-69% | Too general, needs domain depth |





| **WEAK** | <55% | Reject or complete rewrite |











### Strict-API Verification (adopt in code-writing skills)











Before writing any function call/import/method: **"Does this exist in the version





the user is running?"** If "probably"/"I think so" -> STOP, say so. Blocks





made-up methods (`fs.readFileLines()`, `csv.read_csv()`), framework confusion





(Flask render_template vs Django render), deprecated APIs. Flag uncertain with





inline comment; prefer verbose-but-correct over terse-but-wrong.











### Efficiency Ladder (minimalist skill — adopt in code skills)











Before writing new code, stop at first rung that holds:





YAGNI -> Reuse existing -> Standard library -> Native platform -> Existing





dependency -> One-liner -> Minimum code. No unrequested abstractions, no





unnecessary dependencies, no boilerplate, no unrequested comments/logging.











### Known Gap (recognized, NOT bulk-fixing)











Our skills are LARGE vs the <=10KB standard: kaizen ~136KB, cloudflare ~128KB,





research ~118KB. Reference-separation is the fix but bulk refactoring risks





regression (SKILL-WRITE-COLLISION-1). Apply opportunistically: when a skill is





next edited for another reason, split heavy content into references/ at that





time. Do NOT launch a mass rewrite.

















## Skill Churn vs Content Iteration (DEFINITIVE, added 2026-08-05)











**User clarification:** "Skill churn" PRIMARILY refers to repeated cycles of skill





CREATION then DELETING the same skill as obsolete or unnecessary (then usually





RECREATING it again as necessary!). It does NOT refer to the continuous process of





skill content refinement and iteration (instructions, references, scripts, other





directory contents/files).











### The Discrimination











| Activity | Is It Churn? | Verdict |





|:---------|:------------:|:--------|





| Edit a skill's instructions, add a section, bump version, fix wording | ❌ NO | **MANDATORY** — this is kaizen's core purpose. Always authorized. |





| Refactor a skill: split into references/, restructure sections, migrate content | ❌ NO | **MANDATORY** — content iteration. Do it freely (with verification gates). |





| Add new anti-patterns, gates, or best practices to an existing skill | ❌ NO | **MANDATORY** — the skill grows by iteration. |





| Create a NEW skill | ❌ NO | Normal — when genuinely needed (a real gap, not a duplicate). |





| Declare a skill obsolete, DELETE it, then recreate it weeks later | ✅ **YES** | **THE anti-pattern.** Never delete-and-recreate. |





| Disable a legacy prompt/command system that wires to nothing | ❌ NO | Correct removal (CMD-LEGACY-1) — removal of dead weight is not churn. |





| Expunge platform-default skills from git per user mandate | ❌ NO | Correct policy compliance — not churn (they were never "ours"). |











### The Rules











1. **Content iteration is ALWAYS authorized.** Editing, refining, restructuring,





   version-bumping, and extending a skill's files is the normal, expected, mandatory





   mode of maintenance. Never hesitate to improve a skill out of fear of "churn."





2. **Churn is ONLY the create→delete→recreate cycle.** The harm is the deletion of





   accumulated knowledge and the wasted re-creation effort. If a skill is genuinely





   obsolete, its content should be ARCHIVED or MIGRATED (content preserved), never





   deleted-and-recreated later.





3. **Deletion requires: (a) confirmed never-loaded or genuinely superseded,





   (b) content preserved in git history or migrated, (c) no expected near-term





   recreation.** If you can foresee recreating it, do not delete it — iterate it.





4. **Never label improvement as churn.** If a session does 10 iterative refinements





   to a skill, that is 10 kaizen wins, not 10 churn events.





5. **Never avoid editing a skill because "it was just updated."** Iteration is the





   point. (Double-kaizen on UNCHANGED content is still wasteful — that is a





   different anti-pattern; iteration on CHANGED content is always correct.)

















## Mined Workflow Patterns (from alirezarezvani ecosystem, added 2026-08-05)











**Sources (all forked to QNFO, upstream wired, mined 2026-08-05 per user directive):**





- `QNFO/gaios` (31★) — AI Operating System blueprint: second brain + Chief of Staff





- `QNFO/claude-code-tresor` (762★) — 3-tier architecture: Skills → Sub-Agents → Commands





- `QNFO/claude-code-aso-skill` (408★) — master orchestrator + specialist agent fleet





- `QNFO/claude-skills` (23,845★) — skill authoring + pipeline standards (mined into v1.36)











### F. Independent Review & Durability (qm — 11.4k★ multiplayer agent harness)











**Source:** `QNFO/qm` (11,420★, MIT — the parent of the 0★ yc-qm fork). A multiplayer





agent harness with scoped memory/files/keychain per person and room, security postures,





and durable sandboxes. Its AGENTS.md coding standards are gold:











1. **Independent-review mandate (HARD):** *"Never merge to main without a fresh-context





   pass that tries to break the change. Not a blessing — hunt for the bug, the missed





   edge case, the unstated assumption. Always dispatch an independent review agent that





   did not watch you write the change: the context that produced a diff already believes





   it is correct, and that belief is the bias review exists to defeat. Never self-review





   in the authoring context, however small the diff; a green CI run is not review either."*





   → This sharpens our Phase 4 gate: the implementer's own verification is insufficient





   (kaizen already says this) — extend to: reviewer, not author, has the LAST WORD on





   depth, and escalates on its own initiative when it spots risk it wasn't scoped for.





2. **Blast radius by callers:** judge a change's risk by checking CALLERS, not by





   counting files — "a one-line edit to a helper with fifty importers is not a small





   change." A narrow blast radius warrants one reviewer at modest effort; core control





   flow / auth / data loss / concurrency / spend / public API contracts warrant several





   reviewers with distinct lenses.





3. **Fix every instance:** *"one autocorrected call site with five untouched siblings is





   a regression waiting to be rediscovered"* — grep the whole ecosystem for the same





   pattern and fix all of it in the same change. (Extends LANGUAGE-CONSISTENCY-1.)





4. **Durable by default (HARD):** never stash state the system later reads back in





   process memory (in-memory Map/ring buffer is per-instance, wiped by every deploy).





   Anything read back later — audit, logs, resolved config, queued/in-flight work — must





   live in a DURABLE store. RAM-only is fine only as a cache in front of a durable store,





   or for genuinely disposable re-derivable state. **This is the code-level twin of the





   Thin-Client Canonical Asset Protocol (git-github v2.19):** local/process state is





   ephemeral; durable state lives in git/R2/D1/Postgres.





5. **Security postures:** Strict (every tool call pauses for human approval except





   no-effect turn-enders) / Auto (default — classifier screens provenance-labelled





   external data before it reaches the model) / Dangerous (no screening). Plus a





   **predeclared command policy** — approval rules and hard denials for recursive





   deletes and destructive SQL. Maps to stakes-calibrated caution (gaios C): calibrate





   approval to destructiveness.











### A. 3-Tier Architecture (tresor) — the right tool per task











| Tier | Name | Invoked by | Characteristics | Our Equivalent |





|:-----|:-----|:-----------|:----------------|:---------------|





| 1 | **Skills** | Agent automatically | Context-activated, lightweight, non-blocking, single-purpose | kaizen skills auto-loading on context |





| 2 | **Sub-Agents** | User explicitly (`@agent`) | Manual deep analysis, separate context, full tools, expert depth | subagent_orchestrator (explorer/reviewer/implementer) |





| 3 | **Commands** | User triggers (`/command`) | Multi-agent orchestration, end-to-end workflows, aggregated report | prompt templates (SKILLS UPDATE, CONTINUE) |











**Escalation pattern (tresor):** skill alerts → user decides to investigate → sub-agent deep-dives →





command orchestrates multiple sub-agents in parallel → aggregated prioritized report with line





numbers, severity, and fixes. Adopt: our red-team pipeline already dispatches parallel reviewers;





add the explicit skill-alert → escalate → orchestrate → aggregate-report chain.











### B. WAT Model (gaios) — probabilistic reasons, deterministic executes











**Workflows · Agents · Tools.** "Probabilistic AI reasons; deterministic code executes."





- **Workflows** = the SOPs (skills + heavier references)





- **Agents** = read the SOP, call tools in order, recover from failures, ask when unsure





- **Tools** = deterministic operations (Python scripts, MCP servers); credentials in `.env` only





- **Reuse before building; on failure → fix the tool → verify → update the SOP.**





- **Log decisions** to `decisions/log.md` — every decision is auditable.











Adopt: our SKILL-COMMIT-SAME-SESSION-1 + verification gates already encode "fix → verify → update";





add the decision-log discipline (every material decision logged with rationale).











### C. Stakes-Calibrated Caution (gaios) — the operating discipline











1. **Think before acting.** Don't assume, don't hide confusion. If the ask has multiple readings,





   name them — don't silently pick. If a simpler path exists, say so and push back.





2. **Calibrate caution to stakes + reversibility:**





   - **Reversible/internal** (drafts, notes, plans) → produce your best version + surface the





     assumption and alternative, so you can be redirected in one line. **Produce, don't pester.**





   - **External/irreversible/regulated** → stop and confirm first.





3. **Simplicity first.** Minimum that solves it, nothing speculative. Test: "would a senior person





   call this overcomplicated?" — if yes, cut it. Simplicity in form only, never in safety.





4. **Surgical changes.** Touch only what the task requires.











Adopt: this is the missing nuance in our execution-mandate — "produce, don't pester" on reversible





work + "stop and confirm" on irreversible. Canonical: our verify-then-claim gates (ZENODO-PHANTOM-DOI-1)





are the irreversible side; plan/draft work should ship + surface assumptions without confirmation loops.











### D. Master Orchestrator + Specialists (aso-skill) — validated deliverables











**aso-master** orchestrates specialist agents (research → optimizer → strategist), each with





explicit model selection and a defined output contract. Every deliverable is **character-validated**





(Apple 30/30/100, Google 50/80/4000 limits enforced) — output passes a validation gate before





handoff. Includes a **47-item pre-launch checklist with success criteria** and real calendar dates.











Adopt: our subagent slots already separate explorer/reviewer/implementer; add the





**validation-gate-before-handoff** discipline — every subagent deliverable passes a format/limits





check (like our evals ≥85% gate from claude-skills) before the next phase consumes it.











### E. Connections Registry (gaios) — know what you can reach











A single table tracking every system the agent can reach: domain, tool, mechanism (mcp/script/





export/key+ref), auth, **last checked**. `/audit` checks this file for coverage + freshness.





Secrets never persist in the repo — connections pull live at use time.











Adopt: maintain a similar registry for our MCP tool inventory + tokens (extend





TOKEN-DISCOVERY-1 — the discovery order already exists; add the freshness/last-checked column so





stale connections are visible).

















## Language Consistency Check (AUTOMATIC, added 2026-08-05)











Skills accumulate contradictory, obsolete, or ambiguous language as they evolve.





A stale reference to a deleted script, an undefined KIF tag, or a contradictory





version banner silently degrades every future session that loads the skill.











### Scan Protocol (run during every kaizen closeout + Watchtower scan)











For each audited skill SKILL.md, check:











1. **Deleted-script references** — does the skill reference scripts that no





   longer exist? (Historical banners are exempt — they describe what existed





   at that version.)





2. **Non-installed skill references** — does `skill_view("X")` / `skill_run("X")`





   reference a skill that is NOT in the installed list? (Check against





   `skill_list()` — kaizen itself marks removed skills `[NOT-INSTALLED]`.)





3. **Undefined KIF tags** — are referenced KIF-NN codes defined anywhere?





4. **Contradictory sections** — does one section instruct what another forbids?





   (e.g., a subagent HARD BLOCK that a later section mandates.)





5. **Obsolete tool references** — deleted tools (PowerShell), retired endpoints,





   renamed tools referenced by old names.





6. **Duplicate/ambiguous banners** — version banners that restate each other





   or reference versions that never existed (copy-paste artifacts).











### Language Audit Dimensions (from user directive 2026-08-05)











- Contradictory language: same concept described differently across sections





- Confusing language: ambiguous instructions that admit multiple readings





- Obsolete language: references to deleted skills/scripts/tools





- Ambiguous language: triggers that don't map to a clear action











**Fix rule:** When a skill is updated for ANY reason, scan it for these four





classes of language problems and remove/repair them in the same pass. Do not





leave stale language behind when you touch a file.











**Canonical case (2026-08-05):** The 17 `/CMD` slash commands in





`custom_prompts.json` referenced non-existent skills (`qnfo-agent`, `system`)





and a non-existent script (`skill-hygiene.js`) — a dead legacy system that





appeared to work but wired to nothing. All disabled; superseded by the





Two-Prompt Architecture (CONTINUE + SKILLS UPDATE).

















## Tape & Conversation Mining Protocol (AUTOMATIC)











### Tape Mining (run during Session Retrospective)











```





1. tape_search({query: "error OR failed OR 401 OR 403 OR 404 OR timeout OR truncated",





                 kinds: ["tool_result", "tool_call"]})





   → Extract: tool name, error message, owning skill











2. tape_search({query: "kaizen OR fix OR stale OR drift OR anti-pattern",





                 kinds: ["anchor", "message"]})





   → Extract: what was kaizened, what fixes were applied, what's deferred











3. tape_anchors()





   → Extract: handoff anchors that reference kaizen activity











4. Group by skill, count occurrences, feed into Retrospective Register





```











### Conversation History Mining (run during Autonomous Watchtower)











```





1. search_conversations({query: "<skill-name> failure OR error OR broken", limit: 5})





   → Scan recent conversations for incidents involving this skill











2. get_conversation_history({conversationId: "<id>"}) OR get_conversation_stats()





   → If an incident conversation is found, extract the failure pattern











3. Feed findings into Watchtower INCIDENT-AXIS scoring





```











### Conversation Summary Mining (run at session start)











```





The conversationSummary field in the session context contains a summary of





the prior session's activity. Parse it for:











1. "Kaizen on <skill>" → that skill was recently kaizened; check monitoring status





2. "Deferred: <items>" → these items are pending; queue for current session if still relevant





3. "<N> HARD, <M> SOFT" → unresolved findings; check if owner skill needs kaizen





4. Any mention of tool failures, session failures, or broken references





```











## Concrete cronjob Protocol (AUTONOMOUS trigger)











### Daily Watchtower Scan











```





cronjob(action="create", job={





  name: "kaizen-watchtower-daily",





  description: "Autonomous Watchtower scan of all installed skills. 





                Scores each skill on staleness/incident/drift/calibration axes.





                Flags any skill with score > 0.7 for immediate kaizen.",





  cronExpr: "0 9 * * *",       // 9:00 AM daily





  timezone: "America/Chicago",  // or user's timezone





  agentId: "<current-agent-id>",





  taskPrompt: "Run Autonomous Watchtower Protocol (kaizen skill Phase -1). 





              Scan all installed skills with 4-axis health scoring. 





              Store watchtower report in durable memory. 





              Flag any skill with composite score > 0.7. 





              If any HARD candidates (score > 0.8): begin Phase 0 kaizen on the highest-scoring skill.",





  taskSystemInstruction: "You are the Kaizen Watchtower. Your ONLY task is to run the Autonomous Watchtower Protocol as defined in the kaizen skill. Do NOT engage in conversation. Produce a structured Watchtower Report and persist it.",





  enabled: true,





  runtime: { maxDurationMs: 300000, maxTurns: 20, concurrencyPolicy: "skip" },





  delivery: { suppressSuccessNotification: true, notifyOnFailure: true }





})





```











### Weekly Deep Scan











```





cronjob(action="create", job={





  name: "kaizen-deep-scan-weekly",





  description: "Weekly deep scan: full cross-skill dependency audit. 





                Reads every installed SKILL.md, builds dependency graph, 





                checks every cross-reference for version drift.",





  cronExpr: "0 10 * * 1",      // 10:00 AM every Monday





  timezone: "America/Chicago",





  agentId: "<current-agent-id>",





  taskPrompt: "Run a DEEP kaizen scan: read ALL installed skill SKILL.md files. 





              Build the full skill dependency graph. 





              Check every cross-reference for version drift. 





              Update the calibration register for any skill > 30 days without kaizen. 





              Report: 'Deep Scan: N skills, M drift events, K stale references.'",





  enabled: true,





  runtime: { maxDurationMs: 600000, maxTurns: 40, concurrencyPolicy: "skip" },





  delivery: { suppressSuccessNotification: false, notifyOnFailure: true }





})





```











### Retrospective Sweep











```





cronjob(action="create", job={





  name: "kaizen-retrospective-sweep",





  description: "Weekly sweep of session retrospectives. 





                Aggregates heuristic accumulation, identifies top 3 most-fragile skills, 





                updates Watchtower scores with accumulated incident data.",





  cronExpr: "0 18 * * 5",      // 6:00 PM every Friday





  timezone: "America/Chicago",





  agentId: "<current-agent-id>",





  taskPrompt: "Run Session Retrospective sweep: aggregate all heuristic/anti-pattern memories 





              from the past week. Update Watchtower scores for affected skills. 





              Identify the top 3 most-fragile skills. 





              Report: 'Retrospective Sweep: N patterns accumulated, top 3 fragile skills: [list].'",





  enabled: true,





  runtime: { maxDurationMs: 300000, maxTurns: 15, concurrencyPolicy: "skip" },





  delivery: { suppressSuccessNotification: false, notifyOnFailure: true }





})





```











## Incident-to-Fix Pipeline (AUTOMATIC)











When a session fails because a skill was wrong, the pipeline auto-routes the





failure into a kaizen candidate.











### Pipeline Flow











```





Session Failure → Session Retrospective detects failure pattern





                       │





                       ▼





              Heuristic Accumulation stores anti-pattern in durable memory





                       │





                       ▼





              Watchtower INCIDENT-AXIS score increments for affected skill





                       │





                       ▼





              Next Watchtower scan flags skill if INCIDENT-AXIS > 0.5





                       │





                       ▼





              Auto-triggered kaizen (Phase 0-5) if score > 0.8





                       │





                       ▼





              Continuous Monitoring (Phase 6) verifies fix across +1/+2/+3 sessions





```











### Pipeline Gate











- If the same failure pattern recurs **after** a kaizen fix: escalate severity.





  HARD finding → IMMEDIATE re-kaizen with escalated HARD priority.





- If the same failure pattern appears in a **different** session: this is a





  systemic issue, not a one-off. Flag as `[SYSTEMIC-PATTERN]` and kaizen ALL





  skills that reference the failing tool/endpoint, not just the one that failed.











## Anti-Patterns











| **N-2-SCAN-FALSE-POSITIVE-1: Editing skills based on regex-scan flags without raw-line verification (2026-08-05)** | **HARD GATE.** Version scans (fm/hdr/ft) are CANDIDATE lists, not findings. A scan without MULTILINE anchors + a regex that matched `.kaizen_history` table versions flagged 4 phantom N-2 drifts (bloat-cleanup, deepchat-settings, qnfo-agent, social-media-management) — ALL false positives; raw-line anchors proved every version correct. Before editing ANY skill for an N-2 flag: dump the actual header/footer lines (read/anchors, not regex counts) and confirm the mismatch exists. Never bump/repair a version from scan output alone. Canonical case: session -WyivBiyZ6xFy4uXS_RNy kaizen v1.46 — scan2 flagged 4 skills, 0 were real; a hasty edit would have introduced churn. Cross-ref: N-2-FRONTMATTER-DRIFT-1 (real drift class), CLAIM-VERIFY-1 (verify before claim), qnfo-core N-2. |

| Anti-Pattern | Correct |





|:-------------|:--------|





| **Closing out with unresolved deferred items from prior sessions** | **HARD GATE (v1.3):** Before ANY closeout, run the Deferred-Item Gate (Phase 5 STEP 0) — memory_recall for deferred/pending items, execute every item that is executable via CLI/API/command-line, and document a blocker with evidence for anything genuinely stuck. A closeout with unexecuted deferred items that lack documented blockers is a FAILED closeout — the deferred list must be zero or fully evidenced. This rule exists because the 2026-07-31 session lost cloudflare v3.12/v3.13 kaizen changes to a concurrent `git pull --rebase` + `git reset` (uncommitted work wiped), and multiple prior sessions deferred items (branch merges, Buffer posts, D1 VACUUM) that silently accumulated. |





| **Skipping red-team review because "it's a simple update"** | ALL kaizen includes red-team. A "simple" update that introduces a wrong version number in a cross-reference can silently break another skill. |





| Running only 1-2 adversary roles because "the skill is small" | All 5 roles. A small skill can have all the same failure modes as a large one. |





| Applying fixes without re-verifying with a fresh reviewer subagent | Phase 4 re-review is mandatory. The implementer's own verification is insufficient — the same agent that made the error is the worst auditor of its fix. |





| Deferring DESIGN findings because "they're not critical" | DESIGN findings are architecture improvements — they prevent future HARD findings. Defer them once, but never twice. |





| Not updating cross-referenced skills when a dependency changes | If Skill A's kaizen changes a shared reference (e.g., a script path), immediately audit Skill B (which also references it). Cross-skill drift is the #1 source of stale references. |





| Writing a kaizen banner that says only "various fixes" | Every kaizen banner MUST itemize changes with numbered entries and red-team provenance. A future agent reading the banner should know exactly what changed and why. |





| Reactive-only kaizen — never scanning for drift | Run the proactive forecast protocol at least monthly, or after any major ecosystem change. Skills rot silently. |





| Treating the forecast as an optional "nice to have" | Forecast-driven gap detection (like the research skill v2.31 Forecast Integration Map) finds improvements that reactive kaizen never would. It's not optional — it's how you avoid accumulating technical debt. |





| Not storing kaizen outcomes in durable memory | Every kaizen closeout writes to `memory_remember(task_outcome)`. Future sessions need to know what was changed and why. |





| Kaizening a skill without first checking its history log | Read `.kaizen_history` or `kaizen-history.json` first — duplicate kaizen on unchanged code is wasted effort. |





| Running kaizen without `update_plan` tracking | Use `update_plan` from Phase 0 through Phase 5 — untracked kaizen is unauditable kaizen. |





| Treating subagent truncation as successful audit completion | Truncated subagent output = subagent did not complete. Fall back to direct parent-agent audit per Subagent Failure Handling section. |





| Skipping `memory_recall` before starting kaizen | Check for prior kaizen sessions in durable memory — a skill kaizened 2 hours ago with no intervening changes does not need a re-kaizen. |





| Never scheduling proactive kaizen | Use `cronjob` to run daily Watchtower scans — skills rot silently without scheduled vigilance. |





| No calibration register after kaizen closeout | Register dated fragility predictions per the Calibration Register section — so future agents know what to watch for. |





| **Skipping Autonomous Watchtower at session start** | Phase -1 Watchtower scan is MANDATORY at every session start when the kaizen skill is loaded. The 30 seconds it takes prevents hours of debugging stale references. |





| **Skipping Session Retrospective at session end** | Phase R retrospective is MANDATORY at every session end. A session with 15 tool failures that doesn't produce a retrospective is a lost learning opportunity. |





| **Not registering fixes in Continuous Monitoring** | Every kaizen fix MUST enter Phase 6 monitoring. A fix that's never verified is indistinguishable from a fix that was never applied. |





| **Discovering the same anti-pattern twice without escalating** | If the Session Retrospective finds a pattern that was already documented in durable memory, escalate — the prior fix didn't hold. |





| **Watchtower INCIDENT-AXIS at 0 because session failures weren't tagged to a skill** | Every tool failure in a session retrospective MUST be tagged to the skill that owns the tool usage. Unattributed failures are invisible to the Watchtower. |





| **Dependency graph is stale (manual, not auto-maintained)** | The Watchtower rebuilds the dependency graph on every scan. Never trust a dependency graph that's more than one session old. |





| **Declaring closeout successful with unresolved deferred items** | **HARD GATE (v1.2.4):** every closeout runs the Deferred-Items Audit first. "Deferred" and "successful" are mutually exclusive in a closeout declaration. External blockers (rate limits, missing credentials) must be declared `[CLOSEOUT-INCOMPLETE: <item> blocked by <reason>]` with a continuation handoff — never silently deferred while claiming success. |





| **Conversation summary mentions "kaizen on X" but the .kaizen_history wasn't updated** | Phase 5 closeout MUST update .kaizen_history. The conversation summary is human-readable; the history log is machine-verifiable. |





| **Heuristic stored without skill ownership tag** | Every heuristic/anti-pattern in durable memory MUST include a `<skill-name>:` prefix so the Watchtower can attribute it for INCIDENT-AXIS scoring. |





| **MEMORY-TO-SKILL-DRIFT: Session retrospective discovers a pattern, stores it in memory, but NEVER migrates it into the owning skill's anti-pattern table (2026-08-03)** | **HARD GATE (v1.7):** After every session retrospective that stores a new anti-pattern (memory_remember category=anti_pattern), the agent MUST immediately migrate that pattern into the owning skill's SKILL.md anti-pattern table. Closing a retrospective without completing the memory→file migration is a BLOCKED closeout. Case: D1-BIND-1 and VECTORIZE-SILO-1 discovered in session bWLdtP54 (2026-08-02), stored as memories, but absent from cloudflare skill until v3.20 (next session). The Watchtower MEMORY-DRIFT-AXIS (step 0) now auto-detects orphan patterns at session start. |





| **cronjob kaizen tasks created but never monitored for failure** | Check cronjob history weekly. A failing Watchtower cron that silently 404s for 30 days is worse than no Watchtower at all — it creates a false sense of security. |





| **Skill installed by DeepChat but not added to gitignore allowlist** | The `.gitignore` has an explicit allowlist (ADR-026). When DeepChat installs a new skill (xlsx, skill-creator, windows-command-patterns, etc.), sync it to `.gitignore` in the same turn. As of 2026-07-31, 14 of 28 installed skills (50%) were gitignored — their kaizen histories and scripts exist on disk but are invisible to the git repo. Run `skill_list` vs `git ls-files -- */SKILL.md` cross-reference as part of the Watchtower scan. |





| **Subagent reads input files but parent treats file-read-only as "audit complete"** | When a subagent reads the target file but its output is truncated before it produces findings, the parent MUST fall back to direct audit. The subagent READING a file is NOT evidence that it COMPLETED the audit. The signal is: subagent reads input files in log → no findings produced → truncated. See §Subagent Failure Handling rule 4: fall back on the SECOND poll, not the tenth. |





| **Repeated polling of subagents that produced zero findings** | When subagent output shows file-reads but no findings after the first poll, do NOT poll again. The subagent is truncated — polling again wastes tool calls. One poll confirms the truncation pattern. Fall back to direct audit immediately on the second tool call. |





| **Pasting LinkedIn cookies expecting MCP auth to work** | In linkedin-mcp-tools v2.0.3, `LINKEDIN_COOKIE` is schema-only and never injected (zero addCookies/cookieSet calls). Use the persistent-profile `--login` flow and set `LINKEDIN_PROFILE_DIR`. See `linkedin-mcp` skill. |





| **Starting long-running browser/login processes via plain exec** | Exec-session reaping kills them (KIF-12). Use the S1.6 detached-process pattern from windows-command-patterns v3.13. |





| **RCS-1: Producing audit findings from assumed subagent completion while tasks are still `running`/`queued`** | **HARD GATE:** After dispatching subagents or background exec, call `info`/`wait`/`log`. If ANY task is `running`, response MUST read `[BLOCKED: N tasks still running]`. Findings may only be claimed from READ output. |





| **RCS-2: Treating tool dispatch confirmation ("Subagent run started: queued") as completion** | After `subagent_orchestrator(operation: "run")`, explicitly call `info` to `wait` to `log` in sequence. If `wait` times out, call `info` for final status, read `log` for completed tasks, report which completed vs. cancelled. |





| **RCS-3: Using subagents for time-sensitive red-team audit tasks when truncation is a KNOWN systemic anti-pattern** | Subagents for audit tasks = HARD BLOCK. Only parallel search tasks may use subagents. All audit/finding tasks use direct parent-agent execution with actual script output. |





| **SCS-1: Running competing scripts targeting the same write destination, committing the wrong one** | One D1 write target, one approach. If a backup approach fails, DELETE it immediately. Never leave two scripts alive targeting the same row. After any D1 write, re-read the committed row and content-verify it contains the INTENDED content, not just "update succeeded." |





| **TOKEN-DISCOVERY-FAILURE-1: Agent asks for credentials stored on disk instead of checking discoverable locations first (2026-08-04)** | The discovery workflow MUST check: (A) `C:\Users\LENOVO\tokens\` directory, (B) environment variables, (C) memory_recall, (D) tape_search — in that order — before asking the user. All tokens must be stored in multiple redundant, discoverable locations per the user's standing instruction. Canonical case: session 5o2rozKJQecKGz4MGRB6A — Zenodo token was in `tokens/zenodo` and `ZENODO_TOKEN` env var but agent asked the user anyway. |





| **ZENODO-CLOSED-SUBMISSION-1: Zenodo community submissions fail with misleading "only allowed to community members" error when the real issue is closed submission policy (2026-08-04)** | Zenodo communities default to `record_submission_policy: "closed"` and `review_policy: "closed"`. Before submitting records, check `GET /communities/{slug}` → `access.record_submission_policy` and `access.review_policy`. If closed, update via `PUT /communities/{slug}` with FULL body: `{slug, metadata, access}` — missing slug/metadata fields cause 400. Canonical case: session 5o2rozKJQecKGz4MGRB6A — QNFO and QWAV communities had closed policies; 200+ tool calls wasted diagnosing before finding the root cause. |





| **ZENODO-204: json.load() on empty DELETE response body** (v1.6) | Zenodo's DELETE file API returns HTTP 204 (No Content) with zero-length body. Always check `resp.code == 204` or `len(body) == 0` BEFORE `json.load()`. Canonical case: 2026-08-02 consilient-synthesis upload crashed on DELETE. |





| **ZENODO-RAW-UPLOAD-CT-1: api() function sets NO Content-Type when raw=True — Zenodo bucket rejects uploads with HTTP 415 (2026-08-05)** | When uploading binary files to Zenodo deposit bucket via PUT, the api() helper correctly skipped Content-Type: application/json for raw=True calls but FAILED to set Content-Type: application/octet-stream. Zenodo bucket endpoint REQUIRES this header; without it, all binary uploads fail with HTTP 415: "Invalid Content-Type header. Expected one of: application/octet-stream." Fix: when raw=True, set headers[Content-Type] = application/octet-stream. Canonical case: session yHXrIYDvUfwQ6twlIaWG5 — resume v3.11 published with old v3.10 PDF; v3.12 fix set proper Content-Type header. Cross-ref: BLAME-EXTERNAL-1 (the bug is ALWAYS your code until proven otherwise), windows-command-patterns S-1.0.6, ZENODO-204. |





| **ZENODO-DRAFT-CONFLICT: newversion 400 files.enabled when a draft already exists with files** (v1.6) | Before `actions/newversion`, check `links.latest_draft`. If a draft exists with files, delete files first (or reuse the draft). Canonical case: 2026-08-02, three ACRP newversions stuck on leftover drafts. |





| **ZENODO-METADATA-REQUIRED: partial metadata PUT rejected** (v1.6) | Zenodo validates the FULL metadata on PUT: `upload_type`+`publication_type`+`creators` are required even for newversion metadata updates. Send complete metadata or a PATCH, never a partial PUT. |





| **PANDOC-PATH: `where pandoc` empty but binary exists at non-standard path** (v1.6) | Pandoc lives at `C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe` — NOT on PATH. Use the full path or add to PATH in build scripts. Never conclude "pandoc not installed" from a PATH lookup alone. |





| **XHTML2PDF-CSS: `:not(:hover)` pseudo-selector crashes xhtml2pdf parser** (v1.6) | Strip `:not(...)`/`:hover` rules from pandoc-generated HTML before feeding xhtml2pdf: `re.sub(r':not\(:hover\)\s*{[^}]*}', '', html)`. Validated fallback: pandoc→HTML→strip CSS→xhtml2pdf (38,977-byte PDF, 6 papers built 2026-08-02). |





| **WIN-ELEVATION-PARTIAL-1: ShellExecute "runas" admin elevation works for `sc`, most `reg add`, and `taskkill` but FAILS for TrustedInstaller-protected registry keys (2026-08-05)** | Some Windows 11 registry keys (e.g., `HKLM\SOFTWARE\Policies\Microsoft\Dsh`, `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Feeds`) are owned by TrustedInstaller, not Administrators. Even UAC elevation via ShellExecute "runas" cannot write to them. When blocked: (A) use the MDM/PolicyManager alternative path (`HKLM\SOFTWARE\Microsoft\PolicyManager\default\...`); (B) fall back to the Settings GUI; (C) do NOT waste tool calls on icacls/takeown. Canonical case: session VBvCOsXhzlQJUubBqtdFz — 20+ elevation attempts on Dsh/Feeds all failed; PolicyManager path succeeded first try. Cross-ref: windows-command-patterns v3.13 S-1.0.8, WIN-TRUSTEDINSTALLER-REG-1. |





| **SKILL-WRITE-EPERM: writing skill files to `C:\Program Files\DeepChat\` → EPERM** (v1.6) | Use `C:\Users\LENOVO\AppData\Local\Temp\` for all temp scripts/artifacts. Program Files is read-only for the agent. |





| **SUBAGENT-WORKSPACE: subagent file paths differ from parent, breaking file resolution** (v1.6) | Subagents inherit the parent cwd but may resolve paths differently. Pass absolute paths in prompts, or use direct parent-agent execution for file-dependent audits (per v1.2.5 HARD GATE). |











| **ZENODO-PUB-1: Publication state fabricated from plan memory (2026-08-03)** | Agent claimed "Zenodo completed (21755425)" but that ID belongs to a DIFFERENT paper. Fix: publication state requires live re-query. |





| **BLAME-EXTERNAL-1: Assuming API failure is infrastructure (rate-limit/WAF/token) before checking your own HTTP method (2026-08-04)** | Agent spent hours diagnosing Zenodo 403 as "token write-scope issue" when the root cause was `urllib.request.Request(method="DELETE")` silently sending GET. The API-Failure Self-Diagnosis Protocol (windows-command-patterns S-1.0.6) MUST run BEFORE any external diagnosis: STOP, VERIFY your HTTP method/headers, COMPARE with curl, THEN (and only then) consider infrastructure. The bug is ALWAYS in your code until proven otherwise. Canonical case: session zESRNRQLF76EBvTbldEev (2026-08-04) — every Zenodo 403 was DELETE sent as GET. Cross-ref: windows-command-patterns S-1.0.5/S-1.0.6, research REQUESTS MANDATE. |





| **ZENODO-PUB-1: Publication state fabricated from plan memory (2026-08-03)** | Agent claimed "Zenodo completed (21755425)" but that ID belongs to a DIFFERENT paper (ODR v3.0), never executed in the current pipeline. Fix: publication state requires live `curl` record-ID re-query against the Zenodo API — never trust plan memory or prior-session narrative for publication status. Kaizen audits on publication flows MUST re-query live state. Cross-ref: research v2.73 P5.FRESH. |





| **ZENODO-PHANTOM-DOI-1: Claiming a DOI was issued / record published without a same-turn API-response tool call (2026-08-04)** | **HARD GATE.** Every publication claim requires a tool call in the SAME turn showing the API response (create → upload → publish HTTP codes + DOI field). The **DataCite API** (`api.datacite.org/dois/{doi}`) is the authoritative Zenodo-DOI verification: HTTP 404 = definitively no record exists (and is independent of Zenodo's CDN/bot filter — works when zenodo.org 403s). Canonical case: session ZDdTu9Qf — fabricated DOI 10.5281/zenodo.21804582 had zero backing tool calls; DataCite 404 exposed it; real deposit 21803159 created via API, verified state=findable. Cross-ref: research v2.74 ZENODO-PHANTOM-DOI-1, Tool-Call Execution Mandate (git-github v2.14), qnfo-core Rule 14. |





| **ZENODO-DUP-1: Duplicate deposit when paper YAML already has live DOI (2026-08-03)** | Pipeline created fresh deposit while YAML already held a live `doi:` address. Fix: kaizen audit on any Zenodo-publishing pipeline MUST check paper YAML `doi:` field BEFORE assuming a fresh deposit is needed. If YAML doi: exists AND resolves → BLOCK fresh deposit. Cross-ref: research v2.73 P5.DUPCHECK. Case: ODR v3.0 pipeline — 21761802 duplicate while canonical 21758752 was live. |





| **CLAIM-VERIFY-1: File-identity claims made without checksums (2026-08-03)** | Agent claimed "byte-identical duplicate" for two Zenodo deposit files without producing checksums. User challenge forced forensic diff: documents differed by 9 bytes. Fix: ALL file-identity claims ("identical", "byte-identical", "same file", "unchanged") require SHA-256 or md5 checksum evidence. Narrative identity = UNVERIFIED. Kaizen audits MUST reject unverified identity claims as HARD findings. Case: ODR v3.0 forensic closeout. |





| **NUMERACY-1: Derived quantity claimed with false precision (v1.4)** | When computing a derived quantity (e.g., Koide Q from mass fits), recompute from exact rational arithmetic before stating precision. ACRP-04 session: claimed 0.02% deviation; actual: 0.00289% — factor ~7× error. Trigger research BP-6 gate. |





| **NUMERACY-2: Sigma reported without traceable uncertainty source (v1.4)** | Every σ must cite a specific PDG edition, table, value ± uncertainty, and propagation method. ACRP-04: "9,138σ" untraceable; best reconstruction 8,943σ. Trigger research BP-7 gate. |





| **NUMERACY-3: Density gate applied selectively to structurally identical claims (v1.4)** | When §7.2 is tested but §6 (same numerology class) is not, it's confirmation bias. Research BP-8 classifies claims into 5 types — all of the same type must receive the same gate. |





| **GREP-SCOPE-1: Calling the `grep` tool on skill files outside the workspace (2026-08-03)** | The `grep` TOOL is WORKSPACE-SCOPED — it denies `C:\Users\LENOVO\.deepchat\skills\**` with "Access denied - path outside allowed directories" (verified live in session SHEfIEGiQvA2LI5xAPkon). NEVER grep skill paths. Use: (a) `exec python` script — `open(path, encoding='utf-8').read()` + in-memory substring scan (works on any path); (b) `read` with offset/limit pagination; (c) `skill_view` for full rendered content. This is not a permission failure to work around — it is the tool's documented scope. |





| **ZENODO-LINK-OWNERSHIP-1: Blanket-deriving `zenodo_url` from `doi LIKE '%zenodo%'` (2026-08-04)** | **HARD GATE (research v2.73 P5.OWNERSHIP):** `zenodo_url = 'https://doi.org/'||doi WHERE doi LIKE '%zenodo%'` mints fake QNFO linkage for external citations, URL-prefixed doi values, and placeholders. Only ~500 QNFO-owned DOIs exist; the blanket backfill claimed 1,245+ rows. Fix: build the owned-DOI set from the live API (creator search + person-name variant) and write links ONLY for owned DOIs; re-verify 0 non-owned links after any backfill; run `research/scripts/zenodo-ownership-check.py` as the gate. Case: session dXXJ3TxRQ1VHzGdAyp-lo — rollback papers 503→277, paper_ids 468→248. |





| **ZENODO-LINK-OWNERSHIP-2: Assuming `doi LIKE '%zenodo%'` means "QNFO-owned record" (2026-08-04)** | D1 `papers` and `paper_ids` tables contain EXTERNAL literature citations (other researchers' Zenodo records ingested from external-search) alongside QNFO publications. A zenodo-pattern DOI ≠ QNFO-owned. Confirm ownership per-DOI via the live API before treating a row as QNFO-published. |





| **NULL-ID-UPDATE-1: Keyed UPDATEs skip rows with NULL identifiers — under-clearing data (2026-08-04)** | `UPDATE ... WHERE identifier = ?1` never matches rows where identifier IS NULL. Rollback passes 1-2 skipped 58 papers rows this way. Fix: use keyless bulk `UPDATE ... WHERE lower(zenodo_url) IN (SELECT lower('https://doi.org/'||doi) ...) AND lower(doi) NOT IN (<owned list>)`, or handle NULL keys explicitly via a fallback column (`id`). Verify final counts match the target, not just "N ok" from keyed loops. |





| **SUBAGENT-DEADLINE-1: Red-team subagents hitting the 300s default runTimeout on API-heavy audits (2026-08-04)** | Red-team subagent tasks that fetch 100s of API records (Zenodo paginated search, D1 scans) hit the 300000ms default runTimeoutMs and are cancelled mid-audit with zero partial output. Fix: for fetch-heavy subagent tasks set `runTimeoutMs: 900000+`; for the fastest signal, run the audit directly in the parent agent with scripts writing to files (verified faster in session dXXJ3TxRQ1VHzGdAyp-lo). |





| **ZENODO-INPLACE-EDIT-1: Assuming published-record metadata edits require newversion (2026-08-04)** | Published Zenodo record metadata (keywords, notes, related_identifiers) CAN be edited IN PLACE via the deposit API cycle: POST `/api/deposit/depositions/{id}/actions/edit` (201, same DOI, state=inprogress) → PUT full metadata → POST `/actions/publish` (202, same DOI, no new record). Verified on 322 records (254 enrichment + 18 duplicates + 50 notes-fix), 2026-08-04. Use this for metadata-only changes; newversion only for file changes. |





| **STUB-RECORD-1: 122/293 QNFO Zenodo records (42%) are contentless 105-byte README stubs (2026-08-04)** | Concepts 210168xx-210171xx are auto-indexed chapter placeholders ("# QNFO Research Paper / Full text at qnfo.org / auto-indexed") with zero actual content. Red-team finding: metadata enrichment annotated shells, not papers. Action: either backfill real content or add explicit `PLACEHOLDER` keyword + errata note distinguishing them from real publications. One record (21017164) already returns 410 GONE — partial cleanup precedent exists. |





| **BACKFILL-PREVIEW-1: Executing a bulk derived-value D1 UPDATE without a read-only classification preview (2026-08-04)** | Any bulk write that DERIVES values (e.g., `zenodo_url = 'https://doi.org/'||doi`) MUST first run a read-only classification pass: build the authoritative ownership set from the live API (creator search + person-name variant + project `.zenodo_versions.json`/paper YAML DOIs), compute owned/external/garbage counts IN MEMORY, and print the preview (counts + sample rows + garbage list) BEFORE any write. Gate the write: 0 garbage AND 0 external-derived targets, else BLOCK. The 2026-08-04 incident happened because the backfill went straight to UPDATE (1,245+ fake links: 225 papers + 219 paper_ids external citations, 8 double-prefix/PENDING garbage); the rollback succeeded precisely because it previewed first. Cross-ref: research P5.OWNERSHIP, ZENODO-LINK-OWNERSHIP-1. |





| **D1-UPDATE-SUCCESS-NE-ROWS-CHANGED: Treating per-call UPDATE "ok" as rows actually changed (2026-08-04)** | D1 returns success for an UPDATE that matched 0 rows (WHERE clause no-op on NULL keys). The rollback reported "385 ok, 0 failed" yet papers only dropped 503→341 (162 of 226 targets actually changed — NULL-key rows matched nothing). Fix: after any bulk D1 write, verify with COUNT(*) before/after against the EXACT target count AND inspect the response meta `changes`/`rows_written`. Never claim "N rows updated" from "N UPDATE calls succeeded." Reliable pattern: skip keyed passes entirely, use keyless bulk `UPDATE ... WHERE lower(zenodo_url) IN (SELECT lower('https://doi.org/'||doi) ...) AND lower(doi) NOT IN (<owned list>)`. Cross-ref: NULL-ID-UPDATE-1. |























| **FALSIFIABILITY-GATE-1: Kaizen audit claims improvement without pre-registered success criteria (2026-08-04)** | A kaizen banner that claims "fixed X" without stating what observation would prove the fix FAILED to hold is indistinguishable from a cosmetic change. Every kaizen fix MUST include: (A) a pre-registered test (what tool call or scenario would have triggered the old anti-pattern); (B) a verification script or query that PROVES the fix works; (C) a continuous monitoring checkpoint (Phase 6) that will detect regression. Without these, a kaizen closeout is a narrative, not an improvement. Cross-ref: research v2.73 (KIF-60 Bayesian Evidential Weight Gate), qnfo-core v1.14 §0.0 (Δlog-odds), BAYESIAN-RETRODICTION-1. |





| **REACTIVE-ADVERSARIAL-1: Audit pipelines become adversarial only when the user demands it (2026-08-04)** | The research skill's KIF-60 gate was added reactively to the user's 2026-08-04 methodological injunction, not proactively. A skill whose own gates do not produce adversarial symmetry (auditing incumbents with equal severity) until user pressure is itself confirmation-biased. Fix: every kaizen audit MUST include symmetric adversarial review of alternatives/incumbents, and Phase 2 red-team MUST audit whether the skill's gates are adversarial-by-default, not reactive. Canonical case: session iH66zCEWF85XB0FQPfta4 — GR/SM graded A until user injunction. Cross-ref: research v2.73 (Symmetric Audit Requirement), qnfo-core v1.14 (PRO-INCUMBENT-BIAS-1). |





| **BAYESIAN-RETRODICTION-1: Treating post-hoc rationalization as prediction — "the framework explains everything we already know" (2026-08-04)** | A framework that claims to "explain" known observations without producing pre-registered, falsifiable predictions has zero Bayesian weight: P(data | theory, context_then) >> P(data | theory, context_now) for genuine predictions. Fix: every cross-domain correspondence claim MUST include: (A) a pre-registration timestamp (what was predicted BEFORE observation); (B) a falsifiability condition (what observation WOULD have broken the framework); (C) a surprisal estimate — what is P(match | random structure) under a null model. Without these three items, a claimed "prediction" is indistinguishable from post-hoc curve-fitting. Canonical case: the user's 2026-08-04 methodological injunction — the entire QNFO research pipeline now gates on this. Cross-ref: research v2.73 (KIF-60 Bayesian Evidential Weight Gate, Phase 1b), qnfo-core v1.14 §0.0 (Falsifiability Requirement — Δlog-odds). |











| **STALE-PROMPT-1: Custom user prompts not reviewed for 10+ sessions despite accumulating execution gaps (2026-08-05)** | Prompts drive agent behavior; stale prompts produce stale execution patterns. Review all configured prompts during every kaizen closeout (Phase 5 STEP -1) and session retrospective (Phase R). A prompt that hasn't been reviewed in 10+ sessions while the skills it references have been kaizened multiple times is drift risk — the prompt may encode old assumptions about tool behavior, verification gates, or execution patterns. Canonical case: the PLAN-UPDATE-EXECUTE template predated the kaizen skill's red-team verification gates, producing sessions that planned and executed without adversarial review. |

















| **SKILL-COMMIT-SAME-SESSION-1: Editing a skill file on disk without committing it to the qnfo-skills git repo in the same session (2026-08-05)** | **HARD GATE.** Every skill change (create/update/kaizen/version-bump) MUST be committed + pushed to origin in the SAME session. Version control is 100% the agent's responsibility — the user must never need to ask "is this in git?" Sync direction: live skills dir (C:\Users\LENOVO\.deepchat\skills) is the app's load source; git repo (C:\Users\LENOVO\Documents\GitHub\qnfo-skills) is the canonical version store. After ANY skill edit, run: copy live -> git, `git add -A`, `git commit`, `git push origin master`. The rwnq8 mirror is archived (403) — push origin only. Canonical case (2026-08-05): kaizen v1.31→v1.34, system v2.11→v2.13, knowledge v2.5→v2.7, email-composer v2.2→v2.3 edited for days without commits; personal-knowledge v1.0 never committed until this session's master sync. Cross-ref: deepchat-settings v1.3, git-github SAME-TURN-COMMIT. |











| **SKILL-DEATH-FALSE-POSITIVE-1: Declaring a skill "removed"/"NOT-INSTALLED" from skill_list absence alone, without checking .kaizen_history or on-disk state (2026-08-05)** | skill_list (the app's live loader) is the ONLY truth for "is this skill active." Absence from skill_list ≠ removed — it may be: (a) never loaded (file written directly, not installed via app flow), (b) disabled, (c) genuinely removed. Before declaring death: (1) check .kaizen_history — a fresh entry means actively maintained, NOT removed; (2) check on-disk SKILL.md exists + valid; (3) distinguish "never loaded" from "loaded then removed"; (4) if on-disk + maintained but not in skill_list, flag "on-disk but not loaded by app" and reconcile via the app's skill management — do NOT rewrite or delete the file. Canonical case: execution-mandate v2.8 (session IZbk2G9P2aA0JH0f0yQjj) — kaizen v1.24 declared [NOT-INSTALLED] while the skill was being actively kaizened on disk. Cross-ref: deepchat-settings v1.3 Skill Registry Truth-Source. |











| **EXTERNAL-SKILL-FORK-1: Loading a large third-party skill repo into DeepChat runtime dirs or qnfo-skills instead of forking separately + mining (2026-08-05)** | Large third-party skill collections (e.g., alirezarezvani/claude-skills, 345 skills, 23k stars) MUST be forked to a SEPARATE repo (QNFO/<name>) with upstream wired — NEVER copied into qnfo-skills, NEVER into DeepChat runtime dirs (hundreds of skills slow down/crash the app). The fork is a MINING SOURCE: read its standards (SKILL-AUTHORING-STANDARD.md, SKILL_PIPELINE.md), distill best practices, incorporate selectively into our own skills — don't reinvent the wheel. Canonical case (2026-08-05): QNFO/claude-skills fork created; 10 authoring patterns + quality gates mined into kaizen v1.36. Cross-ref: git-github v2.16. |











| **SKILL-CHURN-1: Create→delete→recreate cycles — declaring a skill obsolete/deleting it, then recreating it later (2026-08-05)** | Skill churn is DEFINED as the repeated cycle: create skill → declare obsolete/unnecessary → delete → (usually) recreate. It is NOT content refinement — continuous iteration on a skill's instructions and directory contents is MANDATORY and never churn. Never delete a skill you can foresee recreating; instead iterate/refactor it (content preserved). If genuinely obsolete: archive or migrate content, never delete-and-recreate. Canonical cases: (a) execution-mandate — created, flagged [NOT-INSTALLED], then restored; the correct move was iteration from the start; (b) any skill deleted then re-derived from scratch weeks later. Cross-ref: Skill Churn vs Content Iteration section, LANGUAGE-CONSISTENCY-1. |











| **LANGUAGE-CONSISTENCY-1: Updating a skill without scanning it for contradictory/obsolete/ambiguous language (2026-08-05)** | When ANY skill file is touched (kaizen, fix, feature), scan it in the same pass for: deleted-script references, non-installed skill references, undefined KIF tags, contradictory sections, obsolete tool references, duplicate banners. Fix what you find before closing the edit. A skill updated without a language scan accumulates rot — each edit adds new language on top of stale language. Canonical case: the CMD slash commands in custom_prompts.json referenced `qnfo-agent`/`system`/`skill-hygiene.js` (all non-existent) for weeks before the 2026-08-05 audit caught it. |





| **CMD-LEGACY-1: Maintaining a large set of slash-command prompts that wire to nothing (2026-08-05)** | The 17 `/CMD` commands in `custom_prompts.json` duplicated the Two-Prompt Architecture and referenced non-existent skills/scripts. Removing such a dead system is NOT churn — it is correct removal of dead weight (removal is not the create→delete→recreate cycle; the system was never recreated). Canonical architecture: exactly TWO reusable templates — `CONTINUE` (brainless continuation) + `SKILLS UPDATE` (kaizen trigger). When adding a prompt, ask: would the user use this daily? Does it wire to an existing skill? If not, don't add it. |











| **PROFILE-README-FABRICATE-1: Inventing tool/skill badges (MATLAB, Docker, Qiskit, Cirq, etc.) in a profile README with zero resume evidence (2026-08-05)** | **HARD GATE.** Every tool, skill, or technology badge in a personal/landing page README MUST be attested by the user's actual resume or portfolio. Never generate a badge from your training data — every badge requires a same-turn tool call showing the exact phrase in the resume. Fabricating a tool badge (e.g., adding "Docker" or "MATLAB" to a tech stack when the resume never mentions them) is the SAME CLASS as ZENODO-PHANTOM-DOI-1, CLAIM-VERIFY-1, and bibliographic hallucination. Canonical case: session IfYDah5TSY5gNMY0S4OT5 — rwnq8 profile README initially contained badges for MATLAB, Docker, Qiskit, Cirq that the resume never attested; user corrected the agent. Fix: before any badge, `grep the resume/portfolio for the tool name; if absent → NEVER badge it. Cross-ref: qnfo-core §0.0 Bibliographic Integrity, research P3.AUTHOR-GATE. |





| **MANUAL-DELEGATE-1: Asking the user to perform CLI/git/GitHub operations that the agent can execute autonomously (2026-08-05)** | **HARD GATE.** The user has repeatedly mandated FULLY AUTONOMOUS execution — the agent never delegates manual steps to the user unless the step genuinely requires a web Dashboard, OAuth approval, or a physical action. git clone, git push, gh repo create, editing files, and deploying are ALL agent-executable. Commanding the user to "create the repo named rwnq8" or "copy and push the file" when the agent has `exec`, `gh`, and `git` tools available is a violation. Canonical case: session IfYDah5TSY5gNMY0S4OT5 — agent initially told the user to create the repo and push the file; user corrected the agent; agent executed autonomously with gh CLI + Python deploy script. Fix: every task resolution MUST assume the agent is the executor — escalate a `deepchat_question` ONLY for genuine user-preference decisions, never for tool-executable steps. Cross-ref: git-github SAME-TURN-COMMIT, SKILL-COMMIT-SAME-SESSION-1. |





| **GITHUB-CDN-PROPAGATION-1: Profile README not appearing on profile page for CLI/API-created repos — REVISED 2026-08-05 (NOT a CDN wait)** | **The 5-30 min "CDN propagation" theory was WRONG.** Root cause: repos created via `gh repo create` (CLI/API) are NOT auto-promoted to the profile page even though the repo page renders the README and the editor says "is a special repository." **The fix: click "Share to Profile" on the repo page** (`github.com/{user}/{user}`) — the README appears on the profile IMMEDIATELY, server-side rendered (verified via curl on 2026-08-05: rwnq8/rwnq8). Do NOT wait, force-push, or toggle visibility — click the button. Verify: `curl -s https://github.com/{user} | grep profile-readme` returns a match. Cross-ref: https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme, personal-knowledge v1.2 |











| **EXEC-AUTOBG-DEATH-1: Short exec commands auto-background and die ("Session bg_XXX is not running") in this environment (2026-08-05)** | Observed 10+ times in session 8APhB8pdpgihrWgDLpXIP: `exec` on short Python scripts returns "Error: Session bg_XXX is not running" — the output is lost and the script appears not to run (it may have run; output is unrecoverable). Even `yieldMs` does not reliably prevent it. **Reliable workaround — write-file-read-back:** the script WRITES its output to a `.txt` file (e.g., `C:\Users\LENOVO\.deepchat\_result.txt`), `exec` runs it, then the agent `read`s the file back. This pattern succeeded every time. For single-shot diagnostics, make the script print a sentinel to the file and read the file. Cross-ref: windows-command-patterns v3.15, PYTHON-BUFFERING-1. |

| **API-DOC-GAP-1: Trial-and-error API usage when the owning skill lacks exhaustive endpoint/field documentation (2026-08-05)** | Canonical case: session 3i_KVLownViukLTZB_BJ1 — ~15 failed Zenodo PUT attempts (deposit vs records metadata shape), 3+ subject-search syntax probes, and a 322-char Bluesky post rejection. ALL would have been avoided by reading a complete API dictionary first. Fix: (1) before ANY external API work, verify the owning skill documents the EXACT endpoint + field names + error signatures (research v2.79 TWO-API METADATA SHAPE DISTINCTION, Zenodo SUBJECT-SEARCH syntax, BSKY-300-GRAPHEME-1); (2) if the skill is missing the documentation, STOP and kaizen the skill BEFORE proceeding — the trial-and-error IS the anti-pattern; (3) after discovering any new API behavior, document it in the owning skill in the SAME session (SKILL-COMMIT-SAME-SESSION-1). This is the execution-side twin of strict-API verification (kaizen v1.36). Cross-ref: research v2.79, social-media-management v1.6.0, SKILL-COMMIT-SAME-SESSION-1. |

| **CONCURRENT-ROOT-WRITE-1: Concurrent sessions writing ephemeral `_*.py`/`_*.txt` scripts to `.deepchat` root (2026-08-05)** | **SOFT.** Concurrent agent sessions (cronjobs, subagent tasks) write work scripts to `.deepchat` ROOT instead of %TEMP% or their session dir. Every such file triggers a KIF-48 violation in thin_client.py closeout scans, forcing whack-a-mole purge sweeps and risking mid-execution deletion. Observed in ONE session: 7 distinct files (_chk_radar, _disc_outlook, _disc_outlook2, _disc_resume, _send_paul, _verify_sent, _clean_paul). Rule: ephemeral scripts go to %TEMP% — never `.deepchat` root. When closeout flags `_*` strays, check `process list` for a live concurrent session FIRST; purge strays whose names don't match any running task, or wait for the task to finish. Cross-ref: bloat-cleanup v3.3 thin_client.py, KIF-48, EXEC-AUTOBG-DEATH-1. |

| **CRONJOB-DURATION-1: Agentic web-search cronjobs fail with "Cron job exceeded max duration" at 300s default (2026-08-05)** | Conference Radar (dcdc7a6a) + Job Market Watch (a194153f) both FAILED first manual runs at `maxDurationMs: 300000`. Web-search-heavy agentic tasks (multiple curl/browser fetches + synthesis) routinely exceed 5 minutes. Fix: set `runtime: {maxDurationMs: 600000, maxTurns: 20}` for any cronjob whose prompt includes web search; after `run_now`, check `cronjob history` for `status: failed` + error text. Canonical case: session 8APhB8pdpgihrWgDLpXIP — both jobs re-ran successfully at 600s. |





| **STALE-MANUAL-ITEM-1: Listing a task as "manual user item" when closeout records show it already done (2026-08-05)** | Agent listed "verify qnfo@qnfo.org" as the last manual item; durable memory showed it verified 2026-08-03 12:09:01Z (user clicked link during email infra closeout). Every manual-item list MUST be cross-checked against closeout records + memory_recall BEFORE being presented. Presenting a stale manual item is a phantom-work violation (user must never redo completed work) and contradicts MANUAL-DELEGATE-1. Canonical case: session 8APhB8pdpgihrWgDLpXIP — corrected same session; live email routing verified (5 rules + catch-all → worker:qnfo-email). |





| **N-2-FRONTMATTER-DRIFT-1: Version bump updates header/footer but forgets the FRONTMATTER version field (2026-08-05)** | **HARD GATE.** Three skills drifted the same way in session IfYDah5TSY5gNMY0S4OT5: personal-knowledge fm=1.0 vs hdr=v1.3 (survived 3 bumps), git-github fm=2.16 vs hdr=2.18 (v2.17/v2.18 bumped header/footer only), research hdr=2.75 vs fm=2.76. The frontmatter `version:` line is the FIRST place N-2 scans check — a stale frontmatter breaks machine version detection (Watchtower DRIFT-AXIS, dependency graph). Fix: EVERY version bump must edit ALL THREE locations in the SAME atomic script (frontmatter `version:` + header `# SKILL — vX.Y` + footer `Current: **vX.Y**`), then re-verify all three match before commit. Same class as VERSION-OVERWRITE-1 (version string fragility). Canonical case: session IfYDah5TSY5gNMY0S4OT5 — 6 fixes across 4 skills. EXTENSION (2026-08-05): drift is also committed INTO GIT by concurrent sessions — commit 70ab78f bumped kaizen v1.43/research v2.77/qnfo-core v1.15/wcp v3.14 headers+footers but committed STALE frontmatter (fm 1.42/2.76/1.14/3.13). Detect via kaizen/scripts/watchtower-version-scan.py (canonical thin-client asset) which checks fm/hdr/ft triple with case-tolerant regex + LAST-Current rule; run it at session start or via cronjob. Cross-ref: qnfo-core N-2, VERSION-OVERWRITE-1, CONCURRENT-KAIZEN-1. |













| **STALE-COUNT-1: SKILL.md aggregate-count claims drift from the actual data file as content grows incrementally (2026-08-05)** | Any skill that states aggregate counts (account registry sizes, tool counts, reference counts) MUST reconcile the prose claim against the actual data file in the SAME edit that changes the data. The frontmatter description is the FIRST place staleness hides — social-media-management's description said "45+ verified" through 4 version bumps while the registry grew to 97. Fix: after any registry/data change, grep the SKILL.md for the old count and update every occurrence (description, banners' current-state sections, table rows) before commit. Cross-ref: LANGUAGE-CONSISTENCY-1, social-media-management v1.4.0. |

| **DOTFILE-TRACK-GAP-1: Kaizen closeout creates/updates `.kaizen_history` but the canonical skill-sync.js never stages dotfiles (2026-08-05)** | skill-sync.js walkFiles() skips `entry.name.startsWith('.')`, so `.kaizen_history` (mandated by the Kaizen History Log protocol) is silently excluded from both git staging and R2 upload. Fix: after ANY kaizen closeout that writes `.kaizen_history`, run `git add <skill>/.kaizen_history` + commit + push MANUALLY — do not rely on skill-sync.js. R2 exclusion is by design (history is git-only). Canonical case: social-media-management v1.4.0 — `?? .kaizen_history` untracked post-sync, committed manually (ec578ae). |

| **LINKEDIN-EXP-NO-FORM-1: LinkedIn's "Add a position or career break" button exists but produces no form/modal via CDP browser automation (2026-08-05)** | Canonical case: session wG__dZyYtV1X4_9mgl4MW — puppeteer-core clicked `button[aria-label="Add a position or career break"]` on `/details/experience/` (confirmed via evaluate + exact aria-label match). Button click succeeded but no dialog, modal, or form fields appeared — the URL didn't change, `div[role="dialog"]`/`.artdeco-modal` both empty, and `querySelectorAll('input,[contenteditable],textarea,select')` returned only page-header elements (Search, language SELECT). LinkedIn's SPA "Add section" popup also eludes CDP detection (popup renders outside detectable containers). Fix: LinkedIn experience-adding requires pre-existing experience section on profile; "Add profile section" → Core → Add experience flow needs the section to be initialized first. The about section automation works fine — it targets an existing section. |



## Cross-Skill Integration











| Skill / Tool | Load at Phase | Purpose |





|:-------------|:-------------|:--------|





| `skill-creator` | Phase 0 (if creating a new skill) | Skill structure, progressive disclosure patterns |





| `git-github` | Phase 5 (closeout, if skill lives in a repo) | Conventional commits for kaizen changes |





| `knowledge` | Phase 5 (closeout) | KG/D1 logging of skill state changes |





| `knowledge` | Phase 5 (closeout), Phase R (retrospective) | Durable memory for kaizen outcomes, heuristic accumulation |





| `update_plan` | Phase 0 (and all phases) | Progress tracking and auditability of kaizen execution |





| `cronjob` | Phase 5 (closeout), Phase -1 (Watchtower scheduling) | Schedule recurring Watchtower scans, deep audits, retrospective sweeps |





| `execution-mandate` | [NOT-INSTALLED — removed] | This skill is NOT in the installed skill list; protocol text incorporated inline in §Subagent Failure Handling |





| `query_graph` | Phase 5 (KG feedback loop), Phase -1 (dependency graph) | Cross-skill impact tracing, DEPENDS_ON edge maintenance |





| `search_conversations` | Phase -1 (Watchtower incident mining), Phase R (retrospective) | Conversation history mining for skill failure patterns |





| `get_conversation_history` | Phase R (retrospective deep-dive) | Deep-dive into incident conversations |





| `skill_view` | Phase 0 (cross-reference verification) | Live-verify referenced skill versions |





| `skill_list` | Phase -1 (Watchtower scan) | Enumerate all installed skills for health scoring |





| `linkedin-mcp` | [DELETED 2026-08-05] | Skill deleted per user mandate. Survivors migrated to `social-media-management`. |





| `memory_recall` | Phase 0, Phase -1, Phase R | Pre-flight checks, Watchtower incident mining, retrospective |





| `memory_remember` | Phase 5, Phase R | Durable memory for outcomes, heuristics, anti-patterns |





| `tape_info` | Phase 0, Phase R | Session context, retrospective data |





| `tape_anchors` | Phase 0, Phase R | Handoff context, kaizen anchors |





| `tape_search` | Phase R (retrospective) | Mine session tape for failure patterns |





| `tape_handoff` | Phase 5 | Durable session handoff with kaizen outcomes |





| `browser_navigate` / `browser_click` / `browser_type` | Phase 2 (red-team live verification), Phase 4 (verification gate) | Live web verification of cross-references, DOI resolution, API endpoint reachability |





| `computer-use` skill | Phase 2 (GUI-driven audits) | Desktop app automation for skills that drive native applications |
| `social-media-management` | Phase 5 (closeout), LinkedIn ops | UNIFIED social hub — Bluesky/Mastodon follow mgmt, LinkedIn browser-automation, Buffer MCP posting. Supersedes `linkedin-mcp` (deprecated 2026-08-05) |
| `research` | Phase 0 (forecast protocol), Phase 5 (publication) | Structured Forecast Protocol drives proactive kaizen; calibration register pattern; publication pipeline anti-pattern source |











## Kaizen History Log (MANDATORY per-skill tracking)











Every kaizen session writes an entry to a per-skill history log. For skills





inside a git repo, the log is `kaizen-history.json` at the repo root. For





standalone skills (like this one), the log is a `.kaizen_history` file in





the skill directory. Format:











```json





{





  "skill": "kaizen",





  "entries": [





    {





      "version": "v1.0",





      "date": "2026-07-30",





      "type": "creation",





      "red_team_roles": 5,





      "hard_findings": 0,





      "soft_findings": 5,





      "design_findings": 4,





      "watchtower_triggered": false,





      "summary": "Initial creation. Red-team: 5 parallel subagents + direct parent-agent audit."





    }





  ]





}





```











**Purpose:** Future kaizen sessions read this log to understand what was





already fixed, what remains open, and whether the skill is on a predictable





improvement trajectory. A skill with no history log is indistinguishable





from one that has never been audited.











**New fields (v1.2):**





- `watchtower_triggered`: boolean — was this kaizen triggered by Autonomous Watchtower?





- `retrospective_triggered`: boolean — was this kaizen triggered by Session Retrospective?





- `monitoring_status`: "active" | "clean" | "regression" | "resolved" — Phase 6 monitoring state





- `watchtower_score`: number — composite Watchtower score at time of kaizen trigger











## Calibration Register (DESIGN — forward-looking fragility predictions)



```

[CHECK: 2026-08-12] N-2-SCAN-FALSE-POSITIVE-1 will hold through +3 monitoring checkpoints: no skill

version will be edited based on regex-scan flags alone without raw-line anchor verification. Risk of

regression: [MODERATE] — regex scans are convenient; the verify step adds friction.

Likelihood: [HIGH] — canonical case (scan2 phantom drifts) documented in v1.46 banner + anti-pattern table.



[CHECK: 2026-08-12] STALE-CLONE-ACCUM-1 will hold: thin_client.py v2.7 %TEMP% scan will flag any future

stale clone at closeout (52 clones/156.7MB found at introduction). Risk of regression: [LOW] — scan

category now part of the standard audit; proven live same-session.

Likelihood: [HIGH] — the scan found 52 immediately; the enforcement loop is closed.



[CHECK: 2026-08-12] AUTOCRLF-VERIFY-1 will prevent at least one false 'skill out of sync' claim: no

raw-byte diff will be used to declare git/live drift on Windows. Risk of regression: [MODERATE] — git

status output is habitually trusted.

Likelihood: [HIGH] — 21 of 24 copied files were proven blob-identical in the canonical case.

```









For skills in an active ecosystem, the kaizen closeout produces fragility





predictions. These function like the research skill's Calibration Register:





dated, falsifiable claims about skill drift risk.











- The Autonomous Watchtower and Session Retrospective protocols are new (v1.2);





  their first real-world usage may reveal gaps in trigger thresholds or scoring.





- The cronjob protocol references concrete cron expressions and agent IDs that





  must be tuned to the user's timezone and agent configuration.





- The research skill (currently v2.77) is actively evolving; the canonical





  case study claim may need updating when research reaches v3.0.





Likelihood: [MODERATE] — new autonomous infrastructure, needs burn-in.





```











```





[CHECK: 2026-09-15] Watchtower will have flagged at least one skill with





score > 0.7 within 45 days, given:





- 28 installed skills, many with cross-references





- Research skill is at v2.77 with many version banners — high drift surface area





- Cloudflare MCP servers may versions-shift independently





Likelihood: [HIGH] — large skill ecosystem with active development.





```











```











```





[CHECK: 2026-09-01] MEMORY-DRIFT-AXIS will have caught at least one orphan anti-pattern





(memory stored but not in skill file) within 30 days, given:





- 7+ anti-patterns stored across sessions, some without skill migration





- Cloudflare skill gap (D1-BIND-1, VECTORIZE-SILO-1) = first confirmed case





- 145 conversations in the last 7 days = high session volume





Likelihood: [HIGH] — proven gap already exists.





```











```





[CHECK: 2026-10-01] CLAIM-VERIFY-1 will have flagged its first unverified





file-identity claim within 60 days, given:





- Publication pipelines regularly produce "identical" claims





- Byte-for-byte identity is often assumed without checksum verification





- 145 conversations in the last 7 days = high session volume with file operations





Likelihood: [HIGH] — pattern already observed in R8ZWb04K session.





```











```





[CHECK: 2026-12-01] No further "Access denied - path outside allowed directories"





incidents on skill-path scans — all Watchtower/dependency-graph steps now use exec-python





substring scans or skill_view instead of the workspace-scoped grep tool.





Likelihood: [HIGH] — GREP-SCOPE-1 documented in v1.9 anti-pattern table.





```











```





[CHECK: 2026-08-11] BACKFILL-PREVIEW-1 + D1-UPDATE-SUCCESS-NE-ROWS-CHANGED will hold





through +3 monitoring checkpoints: no bulk derived-value D1 write (zenodo_url/zenodo_doi





or any 'https://doi.org/'||doi pattern) executes without a read-only classification





preview, and no "N rows updated" claim is made from per-call UPDATE "ok" without





COUNT(*) before/after verification. Risk of regression: [LOW] — the 2026-08-04 incident





(1,245+ fake links) is the canonical failure; both anti-patterns + research v2.73





ENFORCED BACKFILL PROTOCOL (preview→gate→execute→verify) now gate the path.





Likelihood: [HIGH] — enforcement documented in two skills with a concrete 4-step protocol.





```











```





[CHECK: 2026-08-11] GIT-COMMIT-M-QUOTE-1 + EXEC-TOOL-QUOTE-1-PY will hold through +3





monitoring checkpoints: no `git commit -m "msg with special chars"` and no





`python -c "nested quotes"` / quoted `python <abs-path>.py` invocations in future





sessions without the documented -F / cd-relative fixes. Risk of regression: [MODERATE]





- agent habit loops take 1-3 sessions to break.





Likelihood: [HIGH] - both failures occurred 4-5x in session 1tz85-vMiqh2TyFySznBA;





the -F pattern worked every time it was used.





```











```





[CHECK: 2026-09-15] WBS-REGISTRY-STALE-1 will have triggered at least one reconciliation





(INSERT of a missing canonical program row into D1 program_registry) within 45 days,





given 6 canonical programs (UMP/SLB/INM/CFE/RES/PLT/DEM) were missing from D1 at





session 1tz85-vMiqh2TyFySznBA and new papers are created regularly.





Likelihood: [HIGH] - proven gap, reconciliation pattern documented in research v2.73.





```











```





[CHECK: 2026-09-01] VECTORIZE-WEBHOOK-VERIFY-1 will prevent at least one false





"paper not indexed" / "search_papers empty = failure" claim within 30 days.





Likelihood: [HIGH] - VECTORIZE-SILO-1 confirmed again in session 1tz85-vMiqh2TyFySznBA





(IPR paper: search_papers "OK" while webhook confirmed 26 chunks indexed).





```











```





[CHECK: 2026-10-01] Ostrowski Trap 4 will prevent at least one false positive





"5-smooth dominance / Pythagorean semigroup" claim from decimal-computed valuations





within 60 days. Risk of regression: [MODERATE] - numerology bias is persistent.





Likelihood: [HIGH] - REG-IPR-003 is the canonical null result; the trap is now





documented in qnfo-core v1.14 Self-Check item 7.











[CHECK: 2026-09-15] Kaizen skill's concrete WBS code examples (v1.28 banners 





reference UMP.002, RES.001, CFE.002 — qnfo-core N-1 pillar aliases) will have 





been reconciled with canonical WBS.TAXONOMY.md §3 program codes (UF, CON, ADL, 





SR) or a single-source-of-truth decision documented. Current state: Kaizen's WBS





CONCRETE EXAMPLE uses [QNFO.RES.001.P9] and [QNFO.UMP.002.P9] prefixes while 





WBS.TAXONOMY.md §3 registers QNFO.CON.xxx and QNFO.UF.xxx. Cross-reference 





drift between the two authoritative registries — any agent resolving from the 





taxonomy finds no matching entries for kaizen's example codes. Discovered in 





session ZDdTu9QfTZKY_kJALlXY_ (Consilience Framework synthesis — all deliverables 





re-mapped from pillar aliases to CON.002). Risk: HIGH.





Likelihood: [HIGH] — qnfo-core N-1 updates don't auto-propagate to skill examples.











[CHECK: 2026-10-01] PANDOC-FONT-QUOTE-1 will have triggered at least once more





within 60 days — any pandoc PDF build with -V mainfont="Font Name With Spaces"





fails on Windows cmd.exe. Risk: MODERATE — publication pipelines regularly use





pandoc font flags.





Likelihood: [HIGH] — PDF building is a frequent operation; fix now documented in





windows-command-patterns v3.12.











[CHECK: 2026-09-01] ZENODO-PHANTOM-DOI-1 will hold through +3 monitoring checkpoints: no "published/DOI issued"





claim will appear without a same-turn DataCite-verifiable tool call. Risk of regression: [MODERATE] — agent





habit of narrating success from plan memory is the exact ZENODO-PUB-1 failure mode.





Likelihood: [HIGH] — the DataCite-404 exposure in session ZDdTu9Qf is now the canonical enforcement example.











[CHECK: 2026-09-01] ZENODO-UPLOAD-MULTIPART-1 + ZENODO-BOT-403-1 will hold: all future Zenodo uploads use





POST /files multipart and full browser headers. Risk of regression: [LOW] — documented in research v2.74





with verified HTTP codes.





Likelihood: [HIGH] — 5-file deposit via multipart succeeded 2026-08-04.





```











[CHECK: 2026-09-15] STALE-PROMPT-1 will have triggered at least one prompt improvement





within 45 days, given: (a) prompts drive all agent behavior; (b) skills evolve faster





than prompts are reviewed; (c) 257 sessions in 30 days = frequent prompt usage.





Likelihood: [HIGH] — the two-prompt architecture is new; the default prompt will need





tuning after the first 10+ sessions of "brainless" CONTINUE usage.

















## Version

















> **v1.38 UPDATE (2026-08-05, kaizen — Session retrospective + red-team anti-pattern discovery):**





> Red-team: direct parent-agent 3-adversary audit of session IfYDah5TSY5gNMY0S4OT5





> (rwnq8 profile README deployment, QNFO/resume→rwnq8/resume transfer).





> HARD: 0. SOFT: 3. DESIGN: 0. Changes:





> (1) [SOFT] **PROFILE-README-FABRICATE-1 anti-pattern added** — agent fabricated





>     tool badges (MATLAB, Docker, Qiskit, Cirq) in profile README with zero resume





>     evidence. Every badge now requires a same-turn grep of the actual resume/portfolio.





> (2) [SOFT] **MANUAL-DELEGATE-1 anti-pattern added** — agent must never ask user to





>     perform tool-executable steps (gh repo create, git push, file copy). User mandate





>     enforced: FULLY AUTONOMOUS execution unless step requires physical action.





> (3) [SOFT] **GITHUB-CDN-PROPAGATION-1 anti-pattern added** — new profile README repos





>     take 5-30 min for GitHub CDN to activate on profile page. Verified: repo page





>     renders correctly, profile page follows. Not a bug to fix.





> Cross-reference: qnfo-core §0.0 Bibliographic Integrity, research P3.AUTHOR-GATE,





> git-github SAME-TURN-COMMIT, session IfYDah5TSY5gNMY0S4OT5.











Current: **v1.56** (kaizen — SKILLS UPDATE closeout + GA/robots.txt retrospective; 2026-08-05)











| **CONCURRENT-KAIZEN-1: Two kaizen sessions on the same skill file collide; writes interleave unpredictably (2026-08-04)** | A scheduled background pipeline (Watchtower, backfill, cronjob) can modify a SKILL.md while the current session's kaizen is also editing it. Symptom: version string changed to unexpected content between writes, banner text replaced with unrelated content. Fix: (A) all kaizen edits to a skill file MUST be done in a SINGLE atomic Python script (read→modify→write, no tool-call interleaving); (B) immediately after write, re-read the file to verify your content landed; (C) if content was overwritten, the file was concurrently modified — re-read the current state and re-apply edits against it. Canonical case: session ktmz7cqk — research v2.73 version string overwritten between apply_kaizen.py write and verify_final.py read. |





| **SKILL-WRITE-COLLISION-1: Sequential write+read to same skill file by two independent processes produces stale reads (2026-08-04)** | When agent A writes a skill file and agent B reads it milliseconds later, agent B may read the OLD content (filesystem caching, write delays). The version string and anti-pattern table are the most vulnerable sections. Fix: (A) prefer `write` (atomic overwrite) over `edit` (surgical replace) for skill-file kaizen; (B) after writing, flush and re-read in the SAME Python script that did the write (ensures filesystem has committed); (C) for cross-process verification, the reader must open the file fresh (no cached handles). |





| **FILE-WRITE-RACE-1: Two Python scripts writing to the same file path within the same turn produce an indeterminate winner (2026-08-04)** | When two `write()` tool calls target the same skill file in the same turn, the second write may silently complete before the first write is committed, or vice versa. The read that follows may see either state. Fix: serialize all writes to the same file path within a turn — never dispatch two parallel writes. A single Python script that performs all edits sequentially is the ONLY safe pattern for multi-edit kaizen. |





| **BACKGROUND-PROCESS-HANG-1: Background exec sessions hang indefinitely without error — killed only by agent timeout (2026-08-04)** | `npx puppeteer browsers install chrome` hung for 120s+ without output. `node puppeteer-core CDP render` hung for 90s+ waiting for MathJax CDN. Chrome download via Python urllib produces no progress output for minutes. Pattern: (A) poll with `process poll` every 15-30s; (B) if 2 consecutive polls show NO new output → process is stuck, kill it; (C) for network downloads, use Python with progress callback; (D) for Chrome launches, always set `timeout` parameters on `page.goto()` and `page.waitForFunction()`. Never wait longer than 2 polls without progress. |





| **PROCESS-MANAGEMENT-1: Session ktmz7cqk created 10+ background processes; 4 hung, 3 needed manual kill (2026-08-04)** | A publication pipeline spawns many background processes: Chrome downloads, CDP renders, Zenodo API calls, pandoc builds. Without active management: orphaned processes consume memory, Chrome instances accumulate, hung processes block subsequent steps. Fix: (A) `process list` at start of every major phase; (B) `process kill` any sessionId from a stale/failed attempt; (C) after CDP render, explicitly close Chrome (`browser.close()`) — don't rely on process timeout; (D) cap concurrent background processes at 2 for system stability. |





| **SESSION-TURNOUT-1: Publication pipeline session consumed ~60 tool calls on Chrome/PDF debugging before reaching Zenodo (2026-08-04)** | The PDF build phase consumed disproportionate tool calls because each failure required manual diagnosis. Fix: (A) the HARD GATE for Chromium availability must be checked ONCE at session start, not after each phase transition; (B) the MathJax CDN check should run BEFORE the first CDP render, not discovered by timeout; (C) pre-flight checklist: Chromium binary check → MathJax CDN test → pandoc version → puppeteer-core import test. Any pre-flight failure = early BLOCK with clear diagnosis, preventing 30+ diagnostic tool calls later. |





| **BROWSER-PROCUREMENT-1: No Chromium browser exists on this machine at session start; procurement must be a Phase 0 gate (2026-08-04)** | Edge, Chrome, Brave are all absent. Chrome for Testing must be downloaded (~194 MB, 2-5 min). The `@puppeteer/browsers` install() method hangs — use Python `urllib.request.urlretrieve()`. Cache at `%USERPROFILE%\.cache\puppeteer\chrome\chrome-win64\chrome.exe`. This is a ONE-TIME setup per machine — after first download, the cache persists across sessions. Cross-reference: research v2.73 Step 1. |





| **MATHJAX-CDN-HEADLESS-2: Chrome headless cannot reach any CDN; all external dependencies must be inlined (2026-08-04)** | `page.goto(fileUrl, {waitUntil: 'networkidle0'})` with CDN-dependent HTML hangs forever. All JS dependencies must be downloaded locally via Python (urllib works) and inlined into the HTML before CDP capture. This applies to MathJax, KaTeX, D3, or any external JS library. Test: `page.goto(html, {waitUntil: 'load', timeout: 15000})` then check `document.readyState`. Cross-reference: research v2.73 Step 4. |





| **CHROME-HEADLESS-1: Chrome headless rendering has undocumented quirks on this Windows machine (2026-08-04)** | (A) `--no-sandbox` required (no user namespace in headless Windows); (B) `--disable-gpu` required (no GPU in headless mode on some hardware); (C) `--disable-dev-shm-usage` required (avoids /dev/shm dependency on Windows); (D) `page.pdf()` margin units are centimeters when using A4 format; (E) `page.waitForFunction(() => window.MathJax?.startup?.promise)` is the canonical MathJax-ready check. Cross-reference: research v2.73 Step 5 render script. |





| **PANDOC-PATH-QUOTE-1: Pandoc binary not on PATH; cmd.exe PATH-prepend quoting fails (2026-08-04)** | Pandoc is at `C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe` — not on PATH. `cmd /c "set PATH=... && pandoc ..."` with nested quotes is NOT valid cmd.exe syntax. Always reference the full canonical path directly: `C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe --mathjax --standalone ...`. No PATH manipulation. Cross-reference: windows-command-patterns S0.0. |





| **TEMP-VOLATILITY-3: Between authoring phase and PDF-build phase, all temp files evicted on Windows (2026-08-04)** | Windows %TEMP% is volatile across agent turns. Paper .md files committed to Git are the ONLY safe persistence layer. After a phase transition: (A) NEVER assume `%TEMP%\paper.md` still exists; (B) ALWAYS `git clone` or `git checkout` from remote to a fresh temp directory; (C) delete the temp clone immediately after commit+push per git-github SAME-TURN-COMMIT mandate. Cross-reference: git-github KIF-32 TEMP Volatility HARD GATE, research v2.73 TEMP-VOLATILITY-2. |





| **VERSION-OVERWRITE-1: Version string in skill SKILL.md overwritten by concurrent process mid-kaizen (2026-08-04)** | The version line (`Current: **vN.MM** (...)`) is the most fragile line in any skill file — every kaizen session writes to it. When two sessions kaizen the same skill concurrently, the version string in the file after both writes reflects the LAST writer, not the union. Fix: (A) kaizen sessions on the same skill MUST serialize — check `.kaizen_history` for active sessions before starting; (B) if a concurrent write is detected (version string changed between read and write), merge changes and bump the version past both intended versions. Canonical case: ktmz7cqk v2.55 → backfill protocol v2.55 → merged into v2.56. |





| **SESSION-KAIZEN-DISCOVERY-1: Red-team session closeouts must audit ALL skills touched, not just the primary target (2026-08-04)** | Session ktmz7cqk touched research (primary), git-github (clone/push), windows-command-patterns (cmd.exe quirks), cloudflare (D1 verification), knowledge (memory). The red-team audit should cover ALL touched skills for new anti-patterns, not just the primary. For each touched skill: check if this session's failures would have been prevented by an existing anti-pattern in that skill. If not → new anti-pattern for that skill. |





| **WBS-TAXONOMY-GAP: Skills without WBS-coded routing tables make multi-project/phase execution untraceable across sessions — v1.17, 2026-08-04** | Before the v2.10/v2.60/v1.10 taxonomy update, no skill mapped program repos to WBS codes or enforced `{prog}/{type}/{slug}` branch naming. Every plan item, branch, and project was a free-text island — zero cross-session traceability. The fix: (1) qnfo-core §N-1 now lists ALL program codes (`UMP`,`SLB`,`INM`,`CFE`,`RES`,`PLT`,`DEM` + `ADL`,`CON`,`SR`,`AUT`) with canonical repo URLs and branch prefixes; (2) git-github v2.10 routing table includes the WBS code column; (3) research v2.60 Phase 0.1 uses `{prog}/{type}/{slug}` branch naming. The canonical codes are: `UMP` (Ultrametric Physics), `SLB` (Laws of Form), `INM` (Infomatics), `CFE` (CFPE), `RES` (QNFO Research), `PLT` (QWAV Platform), `DEM` (QWAV Demos). A branch or plan item without a WBS program code prefix is un-auditable — it cannot be linked to its program, cross-referenced across skills, or dependency-tracked. The `WBS-NO-CODE` and `WBS-INVENT-CODE` anti-patterns in git-github v2.10 now HARD-GATE this. Canonical case: the pre-consolidation state where 45+ repos each used generic `feature/phase0-scaffold` branch names with no program namespace — zero cross-project traceability, zero WBS integration, unmanageable at scale. |





| **CONSOLIDATION-OWNER-RESOLVE-1: `gh repo create` without owner prefix resolves to org (not personal account) — v1.16, session PMH0kzte, 2026-08-04** | `gh repo create <name> --public` with no owner prefix can create the repo in the QNFO org rather than the authenticated user's personal account. The resolution depends on the environment (git remote, GH_REPO env, local config). This causes `gh repo archive rwnq8/<name>` to archive the canonical org repo via GitHub 301 redirect (same repo id, different owner prefixes resolve to the same repo). **Fix:** Always use EXPLCIT owner prefixes: `gh repo create rwnq8/<name>` or `gh repo create QNFO/<name>`. Never rely on default resolution. Verify repos actually exist under the intended owner via `user/repos?affiliation=owner` paginated list. Canonical case: session PMH0kzte — consolidate scripts created cfpe/laws-of-form/ultrametric-physics in QNFO org (discovered because both `repos/rwnq8/<name>` and `repos/QNFO/<name>` returned the same repo id `1322383106`). |





| **PYTHON-BUFFERING-1: Python background scripts produce empty poll output because stdout is buffered without TTY — v1.16, session PMH0kzte, 2026-08-04** | When a Python script is run in the background (`exec` with `background: true`), stdout is NOT attached to a terminal → Python's default line-buffering switches to block-buffering. `process poll` returns empty or truncated output until the script completes (or the buffer fills). This makes background process monitoring useless for diagnostics. **Fix:** Always launch background Python scripts with `python -u` (unbuffered) OR add `print("...", flush=True)` after every status line. Polls can then show real-time progress. Canonical case: session PMH0kzte — 10+ background Python scripts showed `"output":""` in polls despite actively running (subtree merges completing, PR API calls succeeding).

















## DeepChat Runtime Context





- Skill root: `C:\Users\LENOVO\.deepchat\skills\kaizen`.





- Relative paths mentioned by this skill are relative to the skill root unless stated otherwise.





- When this skill needs script execution, prefer `skill_run` over `exec`.





- No bundled scripts detected for this skill.





- Do not guess script paths or change directories to locate skill files.





