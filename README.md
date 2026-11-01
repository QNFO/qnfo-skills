# qnfo-skills

QNFO DeepChat skills: 28 skills including cloudflare-deployer, qnfo-agent and publication-publisher. Redundant backup for disaster recovery.

## Status: deprecated, kept for rollback

[_DEPRECATED-NO-LOCAL-SKILLS-1.md](_DEPRECATED-NO-LOCAL-SKILLS-1.md) (NO-LOCAL-SKILLS-1, 2026-09-28) records that the client loads no skills and that all domain capability is server-side. This repository is retained only because it also hosts two prompt-store locations that the verifier reads, and as rollback evidence. It is never consulted for capability.

- Do not call `skill_list()` or `skill_view()`, and do not pull, enumerate or add skills.
- Rollback: set `enableSkills=true` and restore from the `*.bak-noskills-*` files.

## Where things live now

The fleet, its documentation and its governance records are in [QNFO/qnfo-workers](https://github.com/QNFO/qnfo-workers). [docs/REPO-MAP.md](https://github.com/QNFO/qnfo-workers/blob/main/docs/REPO-MAP.md) there lists what every QNFO repository holds.

Licence: QNFO Unified License Agreement v2.1 (see [LICENSE](LICENSE)).