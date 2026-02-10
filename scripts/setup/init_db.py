#!/usr/bin/env python
"""Database initialization script."""

import sys
import os

# Add parent directory to path (now two levels up)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from persistence.database import init_db


if __name__ == "__main__":
    print("Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)
