#!/usr/bin/env python3
"""Comprehensive diagnostic to trace the 2-second delay through every component."""

import time
import sys
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

print("\n" + "="*80)
print("  🔬 COMPREHENSIVE DIAGNOSTIC - TRACING THE 2-SECOND DELAY")
print("="*80 + "\n")

print("This will test every single component in isolation to find the culprit.\n")

# ============================================================================
# TEST 1: Python HTTP Request Baseline
# ============================================================================
print("-" * 80)
print("TEST 1: Python HTTP Request Baseline (requests library)")
print("-" * 80)

import requests

print("Testing basic HTTP request to Google...")
start = time.time()
try:
    response = requests.get("https://www.google.com", timeout=5)
    elapsed = (time.time() - start) * 1000
    print(f"  ✅ Google responded in {elapsed:.1f}ms")
    if elapsed > 500:
        print(f"  ⚠️  Your network/DNS is slow!")
except Exception as e:
    print(f"  ❌ Failed: {e}")

print()

# ============================================================================
# TEST 2: Localhost Connection Speed
# ============================================================================
print("-" * 80)
print("TEST 2: Localhost Connection Speed")
print("-" * 80)

print("Testing connection to localhost:8000...")
start = time.time()
try:
    response = requests.get("http://localhost:8000/", timeout=5)
    elapsed = (time.time() - start) * 1000
    print(f"  ✅ Backend responded in {elapsed:.1f}ms")
    if elapsed > 2000:
        print(f"  ❌ FOUND IT! Backend root endpoint is slow!")
    elif elapsed > 500:
        print(f"  ⚠️  Backend root endpoint is slower than expected")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    print("  Make sure backend is running!")
    sys.exit(1)

print()

# ============================================================================
# TEST 3: 127.0.0.1 vs localhost
# ============================================================================
print("-" * 80)
print("TEST 3: 127.0.0.1 vs localhost (DNS issue check)")
print("-" * 80)

print("Testing with localhost...")
start = time.time()
try:
    response = requests.get("http://localhost:8000/", timeout=5)
    localhost_time = (time.time() - start) * 1000
    print(f"  localhost: {localhost_time:.1f}ms")
except Exception as e:
    print(f"  ❌ localhost failed: {e}")
    localhost_time = 9999

print("Testing with 127.0.0.1...")
start = time.time()
try:
    response = requests.get("http://127.0.0.1:8000/", timeout=5)
    ip_time = (time.time() - start) * 1000
    print(f"  127.0.0.1: {ip_time:.1f}ms")
except Exception as e:
    print(f"  ❌ 127.0.0.1 failed: {e}")
    ip_time = 9999

if abs(localhost_time - ip_time) > 1000:
    print(f"\n  ❌ FOUND IT! DNS resolution issue! Difference: {abs(localhost_time - ip_time):.1f}ms")
    print(f"  Use 127.0.0.1 instead of localhost!")
else:
    print(f"\n  ✅ No DNS issue (difference: {abs(localhost_time - ip_time):.1f}ms)")

print()

# ============================================================================
# TEST 4: Authentication Timing Breakdown
# ============================================================================
print("-" * 80)
print("TEST 4: Authentication Flow Timing")
print("-" * 80)

print("Step 1: POST to /api/auth/login...")
start = time.time()
try:
    response = requests.post(
        "http://localhost:8000/api/auth/login",
        params={"username": "admin", "password": "admin123"},
        timeout=10
    )
    login_time = (time.time() - start) * 1000
    print(f"  Total time: {login_time:.1f}ms")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"  ✅ Login successful")
        
        if login_time > 2000:
            print(f"  ❌ FOUND IT! Login endpoint is taking {login_time:.1f}ms!")
            print(f"  Issue is in authentication or database operations.")
    else:
        print(f"  ❌ Login failed with status {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"  ❌ Login failed: {e}")
    sys.exit(1)

print()

# ============================================================================
# TEST 5: Detection Endpoint Timing (Authenticated)
# ============================================================================
print("-" * 80)
print("TEST 5: Detection Endpoint Timing Breakdown")
print("-" * 80)

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

test_cases = [
    ("Simple text", "Hello world"),
    ("SQL injection", "SELECT * FROM users"),
    ("Repetitive", "a" * 500),
]

for name, text in test_cases:
    print(f"\nTesting: {name}")
    start = time.time()
    try:
        response = requests.post(
            "http://localhost:8000/api/detect",
            headers=headers,
            json={"text": text},
            timeout=10
        )
        total_time = (time.time() - start) * 1000
        
        if response.status_code == 200:
            result = response.json()
            backend_time = result.get('processing_time_ms', 0)
            overhead = total_time - backend_time
            
            print(f"  Total time:      {total_time:.1f}ms")
            print(f"  Backend time:    {backend_time:.1f}ms")
            print(f"  Overhead:        {overhead:.1f}ms")
            print(f"  Method:          {result.get('method')}")
            print(f"  Tier:            {result.get('tier_used')}")
            
            if overhead > 2000:
                print(f"  ❌ FOUND IT! Overhead is {overhead:.1f}ms!")
        else:
            print(f"  ❌ Request failed with status {response.status_code}")
    except Exception as e:
        print(f"  ❌ Failed: {e}")

print()

# ============================================================================
# TEST 6: Direct Component Testing (No HTTP)
# ============================================================================
print("-" * 80)
print("TEST 6: Direct Component Testing (Bypass HTTP)")
print("-" * 80)

print("\nTesting database operations directly...")
try:
    from persistence.database import get_db, SessionLocal
    from persistence.user_repository import UserRepository
    
    print("Creating database session...")
    start = time.time()
    db = SessionLocal()
    db_session_time = (time.time() - start) * 1000
    print(f"  Session creation: {db_session_time:.1f}ms")
    
    if db_session_time > 1000:
        print(f"  ❌ FOUND IT! Database session creation is taking {db_session_time:.1f}ms!")
    
    print("Querying user...")
    start = time.time()
    user_repo = UserRepository(db)
    user = user_repo.get_by_username("admin")
    query_time = (time.time() - start) * 1000
    print(f"  User query: {query_time:.1f}ms")
    
    if query_time > 1000:
        print(f"  ❌ FOUND IT! User query is taking {query_time:.1f}ms!")
    
    db.close()
    print(f"  ✅ Database operations completed in {db_session_time + query_time:.1f}ms total")
    
except Exception as e:
    print(f"  ❌ Database test failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting Control Tower directly...")
try:
    from enforcement.control_tower_v3 import ControlTowerV3
    
    print("Evaluating response with Control Tower...")
    start = time.time()
    ct = ControlTowerV3()
    init_time = (time.time() - start) * 1000
    print(f"  Control Tower init: {init_time:.1f}ms")
    
    start = time.time()
    result = ct.evaluate_response("SELECT * FROM users")
    eval_time = (time.time() - start) * 1000
    print(f"  Evaluation time: {eval_time:.1f}ms")
    print(f"  Method: {result.method}")
    print(f"  Tier: {result.tier_used}")
    
    if eval_time > 100:
        print(f"  ⚠️  Control Tower is slower than expected")
    else:
        print(f"  ✅ Control Tower is fast")
    
except Exception as e:
    print(f"  ❌ Control Tower test failed: {e}")
    import traceback
    traceback.print_exc()

print()

# ============================================================================
# TEST 7: Rate Limiter Timing
# ============================================================================
print("-" * 80)
print("TEST 7: Rate Limiter Timing")
print("-" * 80)

try:
    from api.middleware.rate_limiter import check_rate_limit
    from persistence.database import SessionLocal
    from persistence.user_repository import UserRepository
    
    print("Testing rate limiter...")
    db = SessionLocal()
    user_repo = UserRepository(db)
    user = user_repo.get_by_username("admin")
    
    start = time.time()
    import asyncio
    result = asyncio.run(check_rate_limit(user, db))
    rate_limit_time = (time.time() - start) * 1000
    print(f"  Rate limit check: {rate_limit_time:.1f}ms")
    
    if rate_limit_time > 1000:
        print(f"  ❌ FOUND IT! Rate limiter is taking {rate_limit_time:.1f}ms!")
    else:
        print(f"  ✅ Rate limiter is fast")
    
    db.close()
    
except Exception as e:
    print(f"  ❌ Rate limiter test failed: {e}")
    import traceback
    traceback.print_exc()

print()

# ============================================================================
# SUMMARY
# ============================================================================
print("="*80)
print("  📊 DIAGNOSTIC SUMMARY")
print("="*80)
print()
print("Review the timings above. The component with >2000ms is the culprit.")
print()
print("Common issues:")
print("  1. DNS resolution (localhost vs 127.0.0.1)")
print("  2. Database session creation (SQLite file locking)")
print("  3. Database queries (missing indexes, slow queries)")
print("  4. Middleware processing (logging, metrics)")
print("  5. Network/firewall (Windows Defender, antivirus)")
print()
print("="*80 + "\n")
