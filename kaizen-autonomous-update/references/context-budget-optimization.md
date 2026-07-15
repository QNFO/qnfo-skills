# Context Budget Optimization — Skill Loading Best Practices

> Documents the token cost of skill loading and 7 optimization rules. Load when auditing token efficiency.

---

## The Problem

Every skill loaded via `skill_view()` consumes context window tokens. With 58 skills, blind loading wastes budget:
- System prompt: ~8,000 tokens/turn
- Skill descriptions (58): ~5,000 tokens/turn
- Full skill body (avg): ~2,000 tokens
- qnfo-agent body: ~190,000 tokens (extreme outlier)

### The 70% Compaction Threshold
Per qnfo-agent §0.9.3, when context reaches 70% of capacity, stop ALL new discovery. Loading skills at 70%+ context steals from execution budget.

---

## 7 Optimization Rules

### 1. Never Load More Than 3 Skills Simultaneously
```
✅ skill_view("literature-search") → execute → skill_view("citation-manager")
❌ skill_view("A") + skill_view("B") + skill_view("C") + skill_view("D")
```

### 2. skill_view() Over read() for Triggering
`skill_view()` activates for current loop only — doesn't pin to conversation. `read()` loads permanently.

### 3. Never Load qnfo-agent for Info Retrieval
190K tokens. Use `skill_view` or `grep` instead.

### 4. Reference Files are Pay-Per-View
Don't pre-load all references. Load only when executing that specific stage.

### 5. Network Skills are Cheapest
Skills with no bundled resources cost only SKILL.md body. Skills with large scripts cost more.

### 6. Cross-Links are Not Free
Each `> **Related:**` entry costs ~15-30 tokens/skill per turn. 58 skills × avg 3 related × 25 tokens ≈ 4,350 tokens/turn just for cross-link metadata.

### 7. Autoload Only When Needed
If autoloader loaded 5 skills but only 2 were used, 3 wasted ~6,000 tokens.

---

## Kaizen Auto-Detection Rules

1. **Skill bloat:** Skills with body >15KB never loaded in 30 days → flag for trimming
2. **Stale cross-links:** Related pairs that never co-occur → flag for removal
3. **Overloaded autoloader:** >50% of loaded skills unused → tune thresholds

---

> **Version:** v1.0
