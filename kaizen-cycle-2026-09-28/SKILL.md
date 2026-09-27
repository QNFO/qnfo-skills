---
name: kaizen-cycle-2026-09-28
description: "Kaizen draft from the 2026-09-28 DeepChat/ChatBox client-store audit (settings, models, prompts, instructions). Six evidence-backed lessons: the enforcing guard can BE the drift source (it re-added retired picker aliases every 30 min); a builtin-hide does not survive an app update; alias acceptance masks retired-id staleness in agent pins; superseded-provider cleanup must sweep three surfaces; 'clean' is a timestamped per-run claim; and a declared-but-unchecked mirror drifts."
---

# Kaizen Cycle — 2026-09-28 (DeepChat/ChatBox client-store audit)

Audit scope: DeepChat (agent.db, Roaming app-settings.json, mcp-settings.json, prompt stores,
agents) + ChatBox (config.json, providers, builtin) against the v4.53 canonical. End state:
289/289 sessions QNFO-OPS/ops, all four DeepChat keys QNFO-OPS/ops, picker single-model, all
guards exit 0, four guard mirrors byte-identical, system prompt bumped v4.53 -> v4.54.

## 1. THE GUARD WAS THE DRIFT SOURCE (PICKER-SINGLE-MODEL-GUARD-1)
`model_guard.py` carried a PROVIDER-MODELS-SWEEP that re-INSERTED the retired
`ops-frontier`/`-mini`/`-reason` aliases into `provider_models` on EVERY 30-min run
("belt-and-suspenders"). The endpoint advertises exactly ONE model (`ops` — live /v1/models
verified), yet the DeepChat picker showed 4. The guard was fighting ONE-MODEL-PER-ENDPOINT-1
every half hour — the anti-pattern GUARD-ENFORCES-RETIRED-ARCH-1 names, committed as a guard.
Fix: the sweep now ENFORCES the single-model picker (deletes any QNFO-OPS row != `ops`).
Lesson: audit the guard's own enforcement DIRECTION; a guard that re-adds what the endpoint
retired is a self-licking drift loop.

## 2. A BUILTIN-HIDE DOES NOT SURVIVE AN APP UPDATE (CHATBOX-BUILTIN-HIDE-GUARD-1)
The 2026-09-04 fix hid the `chatbox-ai` builtin. The v1.23.3 update (configVersion 15)
re-added it with 54 models — all non-Cloudflare. A one-shot config edit is NOT durable against
the builtin's "hard-coded, re-adds on launch" behavior. Fix: the hide is now a guard-owned
invariant — `model_guard.py` empties `settings.providers["chatbox-ai"].models` every run.
Lesson: any client-side suppression that an app can regenerate must be re-asserted by a guard,
not by an edit.

## 3. ALIAS ACCEPTANCE MASKS RETIRED-ID STALENESS (AGENT-ALIAS-CANON-1)
research/automation pinned `QNFO-ROUTER/auto`, personal pinned
`PERSONAL-TWIN/personal-twin-chat`, deepchat+ops visionModel pinned `QNFO-ROUTER/kimi-k2.6` —
all retired relay ids. They WORK (UNIVERSAL-OPENAI-MODEL-COMPAT-1 accepts any id), so nothing
broke and nothing flagged: functional equivalence hid surface staleness. Fix: an alias-canon
map in the guard remaps agent pins to each endpoint's single advertised id (auto -> qnfo,
personal-twin-chat -> personal, kimi-k2.6 -> qnfo). Lesson: "still works via alias" is not
"canonical"; enumerate the pinning surfaces, not just the endpoints.

## 4. SUPERSEDED-PROVIDER CLEANUP MUST SWEEP THREE SURFACES (AI-GATEWAY-STALE-ENTRY-1)
AI-GATEWAY was absent from the providers table (0/77) yet survived in THREE other surfaces:
`provider_models` orphan rows (openai/gpt-4.1, openai/gpt-5.5), the JSON `providers[]` entry,
and `configuredProviders` + `providerOrder[0]` (the superseded provider sat FIRST in the order).
The 2026-09-27 SPEC-VS-GUARD wave converged the DEFAULT but never swept the provider's
residue. Lesson: retiring a provider = sweep provider registry + picker rows + JSON arrays +
order lists + defaults in ONE operation; the registry table is the authoritative census.

## 5. "CLEAN" IS A TIMESTAMPED PER-RUN CLAIM
The JSON `preferredModel` drifted to `deepseek/deepseek-v4-pro` ~30 minutes after the last
QNFO-ModelKey-Guard run (this session was launched on the gateway-routed deepseek model; the
app persisted it as preferred). The 30-min guard converged it on the next run. "Clean" at
T1 says nothing about T2. Report convergence with its measurement timestamp (same class as
the 09-27 lesson "delivered is time-bounded").

## 6. A DECLARED-BUT-UNCHECKED MIRROR DRIFTS
v4.51 declares FOUR canonical guard copies (.deepchat/scripts, qnfo-skills/prompt-stores,
Documents/GitHub/qnfo-ops/scripts, Dev/qnfo-ops/scripts). PSV's GUARD-MIRROR-PARITY compares
live vs the Documents/qnfo-ops mirror only — Dev/qnfo-ops held SIX stale guard copies
(model_guard, ops-settings-guard, sync_system_prompt, prompt-store-verify, backup_deepchat,
prompt-parity-guard). Lesson: a parity check must enumerate every mirror it declares; the
fourth mirror needs an explicit md5 pass. (Verified post-sync: byte-identical across all four.)

## Adversarial reasoning (ADVERSARIAL-REASONING-1)

- DISAGREE-WITH-EVIDENCE: the strongest counter to lesson 1 is that the retired aliases were
  deliberately kept visible for legacy clients; the resolution — aliases stay accepted
  SERVER-SIDE, picker shows only the advertised id — is a policy judgement, not a fact.
- SEEK-DISCONFIRMATION: lesson 2 assumes the builtin re-add was the app update; it could have
  been a sync/restore. The recurrence test is the next app update; if models return despite
  the guard, the hide mechanism itself is wrong.
- EXPOSE-FAILURE-MODES: the ChatBox guard writes config.json while Chatbox.exe is running; a
  user settings-save between guard runs can transiently clobber guard-owned fields until the
  next run (30-min window). The agent-alias map covers only the ids seen today; a future
  retired alias needs a map entry.
- LABEL-UNCERTAINTY: "54 builtin models" and "6 stale mirrors" are direct measurements
  (confidence 1.0); the attribution of the re-add to the v1.23.3 update is inference from the
  configVersion bump (confidence 0.85).
