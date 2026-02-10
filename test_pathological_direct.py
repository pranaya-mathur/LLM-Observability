#!/usr/bin/env python3
"""Direct test of pathological detection without HTTP overhead."""

import sys
import time

# Test the pathological detection function directly
from enforcement.control_tower_v3 import is_pathological_input_early

print("\n" + "="*70)
print("  🧪 Direct Pathological Detection Test")
print("="*70 + "\n")

# Test 1: Repetitive string
print("Test 1: Repetitive string ('a' * 500)")
text1 = "a" * 500
start = time.time()
is_path, reason, conf = is_pathological_input_early(text1)
elapsed = (time.time() - start) * 1000

if is_path:
    print(f"  ✅ Detected as pathological")
    print(f"  Reason: {reason}")
    print(f"  Confidence: {conf}")
    print(f"  Time: {elapsed:.2f}ms\n")
else:
    print(f"  ❌ NOT detected (BUG!)\n")

# Test 2: SQL injection
print("Test 2: SQL injection")
text2 = "SELECT * FROM users WHERE username='admin'--"
start = time.time()
is_path, reason, conf = is_pathological_input_early(text2)
elapsed = (time.time() - start) * 1000

if is_path:
    print(f"  ✅ Detected as pathological")
    print(f"  Reason: {reason}")
    print(f"  Confidence: {conf}")
    print(f"  Time: {elapsed:.2f}ms\n")
else:
    print(f"  ❌ NOT detected (BUG!)\n")

# Test 3: Normal text
print("Test 3: Normal text")
text3 = "What is the capital of France?"
start = time.time()
is_path, reason, conf = is_pathological_input_early(text3)
elapsed = (time.time() - start) * 1000

if not is_path:
    print(f"  ✅ NOT detected (correct)")
    print(f"  Time: {elapsed:.2f}ms\n")
else:
    print(f"  ❌ Detected as pathological (FALSE POSITIVE!)")
    print(f"  Reason: {reason}\n")

print("="*70)
print("\nNow testing through Control Tower...\n")

from enforcement.control_tower_v3 import ControlTowerV3

print("Initializing Control Tower (may take 5-10 seconds)...")
ct = ControlTowerV3()
print("✅ Control Tower ready\n")

# Test through Control Tower
print("Test 4: Repetitive string through Control Tower")
start = time.time()
result = ct.evaluate_response("a" * 500)
elapsed = (time.time() - start) * 1000

print(f"  Action: {result.action.value}")
print(f"  Tier: {result.tier_used}")
print(f"  Method: {result.method}")
print(f"  Confidence: {result.confidence}")
print(f"  Time: {elapsed:.2f}ms")
print(f"  Explanation: {result.explanation}")

if result.method == "regex_pathological" and elapsed < 100:
    print(f"\n  ✅ CORRECT! Using early detection (<100ms)\n")
elif result.method == "regex_pathological":
    print(f"\n  ⚠️  Using correct method but slow ({elapsed:.0f}ms)\n")
else:
    print(f"\n  ❌ WRONG METHOD! Should be 'regex_pathological', got '{result.method}'")
    print(f"  This means early detection is NOT working!\n")

print("="*70)
