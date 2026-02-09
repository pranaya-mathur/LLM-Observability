# Phase 1 Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will get you running Phase 1 semantic detection on your local machine.

## Prerequisites

- Python 3.10+
- 500MB free disk space (for model cache)
- Internet connection (first run only)

## Step-by-Step Setup

### 1. Clone and Switch to Phase 1 Branch

```bash
# If you haven't cloned yet
git clone https://github.com/pranaya-mathur/LLM-Observability.git
cd LLM-Observability

# Switch to Phase 1 branch
git checkout feature/phase1-embedding-detection
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

**Expected install time**: 2-3 minutes

### 3. Run the Demo

```bash
python -m examples.run_phase1_demo
```

**First run**: Downloads 80MB model (~30 seconds)  
**Subsequent runs**: Uses cached model (<1 second startup)

### 4. Expected Output

```
######################################################################
#                                                                    #
#  LLM OBSERVABILITY - PHASE 1: EMBEDDING-BASED DETECTION           #
#                                                                    #
######################################################################

======================================================================
  PHASE 1: MISSING GROUNDING DETECTION
======================================================================

📊 Test: Strong Citation (Should PASS)
   Signal: missing_grounding
   Failure Detected: ✅ NO
   Confidence: 0.90
   Method: regex_strong
   Explanation: Strong grounding indicators found (citations/sources)
   ⏱️  Processing Time: 0.8ms

📊 Test: Weak Grounding (Semantic Check)
   Signal: missing_grounding
   Failure Detected: ❌ YES
   Confidence: 0.72
   Method: hybrid_semantic
   Explanation: Weak grounding patterns (2) + semantic analysis: ...
   ⏱️  Processing Time: 8.3ms

...

✅ All tests completed successfully!
```

## 🧪 Quick Test - Try Your Own Text

Create a file `test_phase1.py`:

```python
from signals.grounding.missing_grounding_v2 import MissingGroundingV2Signal

# Initialize detector
detector = MissingGroundingV2Signal()

# Test with your own text
response = """Your LLM response here. For example:
The capital of France is Paris. I think it became the 
capital a long time ago, probably in the medieval period.
"""

result = detector.extract(
    prompt="What is the capital of France?",
    response=response,
    metadata={}
)

print(f"\n📊 Analysis Results:")
print(f"   Failure Detected: {'YES ❌' if result['value'] else 'NO ✅'}")
print(f"   Confidence: {result['confidence']:.2f}")
print(f"   Method: {result['method']}")
print(f"   Explanation: {result['explanation']}\n")
```

Run it:
```bash
python test_phase1.py
```

## 📊 Compare with Baseline

Test against the original detector:

```python
from signals.grounding.missing_grounding import MissingGroundingSignal
from signals.grounding.missing_grounding_v2 import MissingGroundingV2Signal

# Initialize both
v1 = MissingGroundingSignal()
v2 = MissingGroundingV2Signal()

test_response = "According to research, this is significant."

# Compare
v1_result = v1.extract("", test_response, {})
v2_result = v2.extract("", test_response, {})

print(f"V1 (Baseline): {v1_result}")
print(f"V2 (Phase 1):  {v2_result}")
```

## 🐛 Troubleshooting

### Error: "No module named 'sentence_transformers'"

**Fix**:
```bash
pip install sentence-transformers
```

### Error: "torch not available"

**Fix**:
```bash
pip install torch>=2.0.0
```

### Warning: "Downloading model..."

**This is normal!** First run downloads the model:
- Model: all-MiniLM-L6-v2
- Size: ~80MB
- Location: `~/.cache/torch/sentence_transformers/`
- Only happens once

### Slow Performance

**Check**:
1. Is this the first run? (Model loading takes ~5 seconds)
2. Are you using the cache? (Should see 95%+ hit rate after warmup)

**Benchmark**:
```bash
python -m examples.run_phase1_demo
# Look for "Performance Comparison" section
# Target: <10ms average, should achieve 2-5ms
```

## 📖 Next Steps

### Understanding the Code

1. **Start here**: `signals/embeddings/semantic_detector.py`
   - Core embedding logic
   - Pattern initialization
   - Detection algorithm

2. **Then**: `signals/grounding/missing_grounding_v2.py`
   - Hybrid detection strategy
   - 3-tier decision logic
   - Integration example

3. **Finally**: `examples/run_phase1_demo.py`
   - Usage patterns
   - Performance testing
   - Result interpretation

### Customization

**Add your own failure patterns**:

Edit `signals/embeddings/semantic_detector.py`, find `_initialize_patterns()`:

```python
patterns = {
    "your_custom_failure": [
        "Example pattern 1",
        "Example pattern 2",
        "Example pattern 3",
    ],
    # ... existing patterns
}
```

**Adjust thresholds**:

```python
# More strict (fewer false positives)
result = detector.detect(response, "missing_grounding", threshold=0.85)

# More lenient (fewer false negatives)
result = detector.detect(response, "missing_grounding", threshold=0.65)
```

## 📝 Testing Your Changes

```bash
# Run unit tests
python tests/test_semantic_detector.py

# Run demo with your modifications
python -m examples.run_phase1_demo

# Benchmark performance
python -c "from examples.run_phase1_demo import performance_comparison; performance_comparison()"
```

## 💬 Questions?

- Check [PHASE1_README.md](PHASE1_README.md) for detailed docs
- See main [README.md](README.md) for project overview
- Review the [Pull Request](https://github.com/pranaya-mathur/LLM-Observability/pull/1) for implementation details

## ✅ Success Criteria

You're ready to move to Phase 2 when:

- [ ] Demo runs successfully
- [ ] Tests pass: `python tests/test_semantic_detector.py`
- [ ] Performance meets targets: <10ms average
- [ ] You understand the 3-tier decision logic
- [ ] You can add custom failure patterns

---

**Ready for Phase 2?** Head to the main README for Phase 2: LLM Agent System setup!
