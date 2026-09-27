---
name: kaizen-cycle-2026-09-27
description: "Kaizen draft from the 2026-09-27 git+Cloudflare sync cycle + its CMD RED TEAM audit. Five evidence-backed lessons: a guard fix that reaches the client stores and the guard working-trees but never git HEAD (and never the prompt prose) is not a fix; a guard that parses source with a happy-path regex manufactures phantom drift; a self-contradicting guard docstring is a live defect; 'delivered' is time-bounded when a concurrent session shares the repo; and Temp-scratch clones are a real, unaudited git surface."
---

# Kaizen Cycle — 2026-09-27 (git/Cloudflare sync + red-team remediation)

## 1. SPEC-DRIFT-WITHOUT-MIRROR (RC-1) → SPEC-VS-GUARD-1
The DeepChat default-key fix reached the four live client stores AND all four guard working
copies, but never git HEAD, and never the system-prompt prose. Result: the committed guards
enforced `AI-GATEWAY/openai/gpt-4.1` while every live surface enforced `QNFO-OPS/ops`, and the
HOLISTIC CMD template instructed future cycles to *revert* the live value. `AI-GATEWAY` is absent
from the runtime provider registry (0 of 77) so the prompt's value was unresolvable.
Root mechanism: `GUARD-TRIPLICATE-CONSISTENCY-1` compares the three guards to EACH OTHER —
nothing compared them to the spec text. Permanent gate added: `SPEC-VS-GUARD-1` inside
`prompt-store-verify.py` (FATAL), asserting DESIRED_KEY == DESIRED_KEYS == MODEL_DICT **and** that
the system prompt's live default statement names exactly that pair. Falsified: pointed at a
divergent prompt copy it returns False (fails closed).

## 2. GUARD-WRITTEN-FOR-THE-HAPPY-PATH (RC-3)
`deploy-drift-guard.py` parsed `(?:var|let|const)\s+(?:QNFO_)?VERSION\s*=\s*"([^"]+)"`: the
optional `QNFO_` prefix matched composite ids and the double-quote-only class missed
single-quoted constants. 4 of 5 reported "drifts" were artefacts. Measured: `sync 25→30`,
`drift 5→0`. A regex written against one convention becomes a false-alarm generator against a
fleet that has several — always test a parser against the whole corpus before trusting its signal.

## 3. SELF-CONTRADICTING GUARD DOCSTRING (C4)
`model_guard.py`'s docstring said "model key: QNFO-OPS / ops-frontier ... in ALL four DeepChat
keys" while the constant it documented enforced `QNFO-OPS/ops`. Same class as the stale
`DESIRED_KEYS` comment fixed hours earlier — the first sweep was partial because it targeted one
file. When sweeping retired vocabulary, grep the WHOLE guard set for the retired id and classify
each hit as *data alias* (keep) vs *prose claim* (fix).

## 4. DELIVERED IS TIME-BOUNDED UNDER A SHARED REPO (RC-5)
"0/0 in sync, clean" was verified true, and ~25 minutes later `qnfo-workers` main had advanced
twice (`901a4dc` by a concurrent session, then `b17d4e6`/`6e01564` ci-watchdog red-team work).
The commit I pushed survived as an ancestor (no clobber — CONCURRENCY-WORKER-CLOBBER-1 passes),
but the *statement* "in sync" decayed. Report sync with its measurement timestamp, and re-pull
before reporting.

## 5. TEMP SCRATCH CLONES ARE A REAL GIT SURFACE (C1)
13 git clones were living under `AppData/Local/Temp` (multi-hundred-MB each), outside the
audited census and outside the FILE-HYGIENE rule that Temp is same-turn-only. Four carried a
commit on no remote. Remediation: bundle the unique work durably, then remove; keep any clone
touched today (a concurrent session may be using it). Lesson: any repo census that starts at
`$HOME` with a depth bound will miss scratch clones; enumerate Temp explicitly.

## Adversarial reasoning (ADVERSARIAL-REASONING-1)

- DISAGREE-WITH-EVIDENCE: the strongest counter to lesson 1 is that the two "sides" of the
  conflict were both authoritative (a user directive vs observed runtime), so the correct move
  may have been to *register* AI-GATEWAY rather than converge the guards; the resolution is
  recorded as the cycle's single judgement call, not as an established fact.
- SEEK-DISCONFIRMATION: each lesson here generalises from one cycle. Re-test the mechanism
  (does the gate actually fail closed? does the parser actually cover the corpus?) before
  applying it fleet-wide.
- EXPOSE-FAILURE-MODES: SPEC-VS-GUARD-1 compares *this* pair of identifiers only; a different
  future default-key sub-system (ChatBox, another client) is not covered.
- LABEL-UNCERTAINTY: the "concurrent session" attribution rests on commit authorship, branch
  dates and file mtimes, not on a session registry; confidence 0.85.
