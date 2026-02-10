#!/usr/bin/env python3
"""Force restart backend with cache clearing.

This script helps when uvicorn --reload doesn't pick up changes
due to @lru_cache decorators or module-level caching.
"""

import sys
import subprocess
import time
import os

print("\n" + "="*70)
print("  🔄 Backend Restart Helper")
print("="*70 + "\n")

print("This will help you restart the backend with a fresh cache.\n")

print("Step 1: Make sure you've STOPPED the current backend (Ctrl+C)")
print("        Check that port 8000 is free.\n")

input("Press Enter when backend is stopped... ")

print("\n✅ Good! Now clearing Python cache...\n")

# Clear __pycache__ directories
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        pycache_path = os.path.join(root, '__pycache__')
        print(f"  Clearing {pycache_path}")
        try:
            import shutil
            shutil.rmtree(pycache_path)
        except Exception as e:
            print(f"  ⚠️  Could not clear {pycache_path}: {e}")

print("\n✅ Cache cleared!\n")
print("Step 2: Now start the backend with this command:\n")
print("  python -m uvicorn api.app_complete:app --reload --port 8000\n")
print("IMPORTANT: Start it in a FRESH terminal window/tab for best results.\n")
print("Step 3: After backend starts (shows 'Control Tower initialized'),")
print("        run: python verify_fixes.py\n")
print("Expected result: <10ms processing times! 🚀\n")
