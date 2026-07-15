# Self-Improvement Architecture — The 5-Layer Metacognitive Framework

> Load this reference from `kaizen-autonomous-update` when designing or auditing the system's ability to improve itself.

---

## 5-Layer Architecture

```
LAYER 5: VALIDATION  → Did it help? before/after metrics, A/B testing
LAYER 4: APPLICATION → Safe auto-apply (model configs) / Review-required (skills)
LAYER 3: PRESCRIPTION→ EV-ranked improvement portfolio via deep-research
LAYER 2: DIAGNOSIS   → Pattern detection across skills, CF health, prompt drift
LAYER 1: MONITORING  → Skill usage telemetry, CF health telemetry, error rates
```

## Layer 1: Monitoring

| Source | What | Where |
|:-------|:-----|:------|
| closeout-manager §2.7 | skills_used, tool_errors, phantom_claims, execution_ratio | D1 audit_sessions |
| infrastructure-audit | R2 object count, D1 row counts, Worker status | R2 health JSON |
| agent.db | Session history, message patterns | Local SQLite |

## Layer 2: Diagnosis

- **kaizen_engine.py**: Conversation patterns, model config gaps, template gaps, prompt drift
- **prompt-audit**: 19 design pattern checks per skill
- **infrastructure-audit**: R2 orphans, D1 drift, Worker errors, resource leakage

## Layer 3: Prescription

```
SKILL ERRORS → kaizen_engine.py → IMPROVEMENT CANDIDATES → deep-research EV ranking
                                                                    ↓
                                                            OPTIMAL PORTFOLIO
                                                            (Bayesian cascade)
```

## Layer 4: Application

| Change Type | Auto-Apply? | Tool |
|:-----------|:----------:|:-----|
| Model configs | ✅ Safe | kaizen_engine.py --apply |
| Skill structure | ❌ Review | Manual after prompt-audit |
| Cross-links | ❌ Review | Manual after bootstrap_skills.py --validate |

## Layer 5: Validation (BIGGEST GAP)

**Current state: NO feedback loop.** Improvements are applied but never measured.

**Implementation path:**
1. Record pre-change metric (e.g., phantom claim rate)
2. Apply improvement
3. Wait 5 sessions
4. Record post-change metric
5. IF improvement > 10% → keep; IF degradation > 10% → rollback

## Kaizen Skill Integration

| Skill | Layer | Role |
|:------|:-----|:-----|
| closeout-manager | 1, 5 | Telemetry collection + validation metrics |
| infrastructure-audit | 1, 2 | CF health monitoring + anomaly detection |
| kaizen_engine.py | 2, 3, 4 | Pattern analysis + improvement generation + auto-apply |
| deep-research | 3 | EV-ranked improvement portfolio |
| prompt-audit | 2 | Structural quality gates |
| bootstrap_skills.py | 4 | Safe deployment of changes |
| skill-sync | 5 | Post-deployment verification |

## Best Practices

1. **Never auto-apply structural skill changes.** Only model configs are safe for automation.
2. **Measure before AND after.** Untracked improvements are untestable hypotheses.
3. **Choke nodes first.** Fix the one bottleneck that unlocks everything.
4. **Small batch, high frequency.** One change → 3 sessions → validate → next change.
5. **Data beats intuition.** If error rate goes UP after improvement, the data is right.
