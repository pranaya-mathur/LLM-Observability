#!/bin/bash

# Production startup script for LLM Observability API

set -e

echo "🚀 Starting LLM Observability API in production mode..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Using defaults."
    echo "   Copy .env.example to .env and configure as needed."
fi

# Initialize database
echo "📊 Initializing database..."
python scripts/setup/init_db.py

# Run database migrations (if using Alembic)
# echo "🔄 Running database migrations..."
# alembic upgrade head

# Start the API with Uvicorn
echo "✅ Starting API server..."
uvicorn api.main_v2:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --access-log \
    --proxy-headers \
    --forwarded-allow-ips='*'
