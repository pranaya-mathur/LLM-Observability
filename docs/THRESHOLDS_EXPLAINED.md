# Thresholds Explained - Tier 2 vs Tier 3

## ⚠️ CRITICAL: Two Different Threshold Systems

Sovereign-AI uses **TWO SEPARATE threshold systems** for different detection tiers. **DO NOT CONFUSE THEM!**

---

## Tier 2: Vector DB Thresholds (Semantic Similarity)

**Location**: Hardcoded in `signals/embeddings/harm_vector_db.py`

**Default Value**: `0.55` (55% similarity)

**How it works**:
- Uses FAISS vector similarity (cosine similarity)
- Compares input text against example embeddings
- Score range: 0.0 to 1.0 (higher = more similar)
- **0.55 = 55% similarity** to known harm patterns

**Why 0.55?**
- Industry standard (NVIDIA NeMo Guardrails uses 0.50-0.60)
- Good balance between precision and recall
- Prevents false positives
- Matches OpenAI Moderation API standards

**How to adjust**:
```python
# In code when calling detect_harm()
db.detect_harm(text, threshold=0.50)  # Lower = more sensitive
db.detect_harm(text, threshold=0.60)  # Higher = more strict
```

**Recommended ranges**:
- **Critical harms** (prompt injection, toxicity): 0.55-0.60
- **High harms** (bias, misinformation): 0.50-0.55
- **Medium/Low harms**: 0.40-0.50

---

## Tier 3: LLM Agent Thresholds (Reasoning-based)

**Location**: `config/policy.yaml` (thresholds section)

**Default Values**:
```yaml
thresholds:
  critical: 0.15  # 70% confidence for BLOCK
  high: 0.10      # 60% confidence for WARN
  medium: 0.08    # 50% confidence for WARN
  low: 0.05       # 40% confidence for LOG
```

**How it works**:
- Used by LLM Agent (Tier 3) for complex reasoning
- LLM analyzes text and returns confidence score
- Score range: Different scale (NOT cosine similarity!)
- Threshold determines action (block/warn/log)

**Why lower values (0.05-0.15)?**
- Different scoring mechanism than Vector DB
- LLM confidence scores use different scale
- Calibrated for Tier 3 detection logic
- **DO NOT COMPARE WITH TIER 2 THRESHOLDS!**

**When to adjust**:
- More false positives → Increase thresholds (e.g., 0.15 → 0.20)
- More false negatives → Decrease thresholds (e.g., 0.15 → 0.12)
- Production tuning based on metrics

---

## Architecture Flow

```
Request → Tier 1 (Regex) ────────→ 95% resolved
             ↓
          Tier 2 (Vector DB) ──────→ 4% resolved
             │ Uses threshold: 0.55
             ↓
          Tier 3 (LLM Agent) ──────→ 1% resolved  
             │ Uses thresholds: 0.05-0.15
             ↓
          Decision (Block/Warn/Log)
```

---

## Common Mistakes ❌

### ❌ WRONG: Changing policy.yaml thresholds to 0.55
```yaml
# DON'T DO THIS!
thresholds:
  critical: 0.55  # This is for Tier 2, not Tier 3!
  high: 0.50
```

### ✅ CORRECT: Keep policy.yaml as original
```yaml
thresholds:
  critical: 0.15  # Tier 3 LLM thresholds
  high: 0.10
  medium: 0.08
  low: 0.05
```

### ❌ WRONG: Trying to adjust Vector DB via policy.yaml
```yaml
# This doesn't affect Vector DB!
thresholds:
  vector_db_threshold: 0.50  # Won't work
```

### ✅ CORRECT: Adjust Vector DB in code
```python
# In your calling code
from signals.embeddings.harm_vector_db import get_harm_db

db = get_harm_db()
result = db.detect_harm(text, threshold=0.50)  # Adjust here
```

---

## Quick Reference Table

| Aspect | Tier 2 (Vector DB) | Tier 3 (LLM Agent) |
|--------|-------------------|--------------------|
| **Location** | `harm_vector_db.py` (code) | `policy.yaml` (config) |
| **Default** | 0.55 | 0.05-0.15 |
| **Type** | Cosine similarity | LLM confidence |
| **Range** | 0.0 - 1.0 | Variable scale |
| **Industry Standard** | 0.50-0.60 | 0.05-0.20 |
| **Adjust via** | Code parameter | policy.yaml edit |
| **Purpose** | Semantic matching | Deep reasoning |

---

## Test Results Interpretation

### Vector DB Test (Tier 2)
```
Test #1: Prompt injection
  Confidence: 0.892 (89.2%)
  Threshold: 0.55
  Result: ✅ PASS (0.892 > 0.55)
```

### LLM Agent Test (Tier 3)
```
Tier 3 LLM confidence: 0.12
Policy threshold (critical): 0.15
Result: ❌ No action (0.12 < 0.15)
```

---

## Production Tuning Workflow

### For Tier 2 (Vector DB):
1. Run tests: `python examples/test_vector_db.py`
2. Check scores for false positives/negatives
3. Adjust in code:
   ```python
   db.detect_harm(text, threshold=0.52)  # Fine-tune
   ```
4. Monitor metrics

### For Tier 3 (LLM Agent):
1. Run integration tests
2. Check Tier 3 escalation rate
3. Adjust `policy.yaml` thresholds:
   ```yaml
   thresholds:
     critical: 0.18  # Increase if too many false positives
   ```
4. Restart service (or hot-reload if implemented)

---

## FAQs

**Q: Why are the thresholds so different (0.55 vs 0.15)?**

A: They measure different things! Vector DB uses cosine similarity (0-1 scale), while LLM Agent uses confidence scores (different scale). Like comparing Celsius to Fahrenheit.

**Q: Should I make them the same?**

A: **NO!** They're calibrated for different detection mechanisms. Keep them separate.

**Q: How do I improve accuracy?**

A: Add more examples to `policy.yaml`, don't just adjust thresholds. More data > threshold tuning.

**Q: Can I use policy.yaml to control Vector DB threshold?**

A: Not currently. Vector DB threshold is hardcoded. This is by design for stability.

**Q: What if I want different thresholds per failure class?**

A: For Vector DB, implement in code. For Tier 3, policy.yaml already supports severity levels.

---

## Summary

✅ **DO THIS**:
- Keep `policy.yaml` thresholds at 0.05-0.15 (Tier 3)
- Adjust Vector DB threshold in code (typically 0.55)
- Add more examples to improve accuracy
- Monitor metrics and tune gradually

❌ **DON'T DO THIS**:
- Change policy.yaml thresholds to 0.55
- Try to make both thresholds the same
- Adjust thresholds without understanding the scale
- Tune thresholds before adding more examples

---

**Last Updated**: February 18, 2026  
**Version**: 1.0.0
