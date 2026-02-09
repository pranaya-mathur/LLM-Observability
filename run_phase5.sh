#!/bin/bash
# Phase 5 Quick Start Script
# Run with: bash run_phase5.sh

echo "🚀 Starting LLM Observability - Phase 5"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -r requirements-phase5.txt --quiet

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Default Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🌐 Starting services..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo "\n🛑 Shutting down services..."
    kill $API_PID $DASHBOARD_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start API server in background
echo "🔧 Starting API server on http://localhost:8000..."
python -m uvicorn api.app_complete:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Wait for API to start
sleep 3

# Start dashboard in background
echo "🎨 Starting dashboard on http://localhost:8501..."
streamlit run dashboard/admin_dashboard.py --server.port 8501 --server.headless true &
DASHBOARD_PID=$!

echo ""
echo "✅ All services running!"
echo ""
echo "📚 Access points:"
echo "   • API Docs:  http://localhost:8000/docs"
echo "   • Dashboard: http://localhost:8501"
echo ""
echo "💡 To stop: Press Ctrl+C"
echo ""

# Wait for processes
wait
