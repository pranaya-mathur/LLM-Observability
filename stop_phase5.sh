#!/bin/bash
# Phase 5 Shutdown Script
# Stops API and Dashboard

set -e

echo "============================================================"
echo "          LLM Observability - Phase 5 Shutdown             "
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to stop process
stop_process() {
    local name=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "${YELLOW}🛑 Stopping $name (PID: $PID)...${NC}"
            kill $PID 2>/dev/null || true
            sleep 2
            
            # Force kill if still running
            if ps -p $PID > /dev/null 2>&1; then
                kill -9 $PID 2>/dev/null || true
            fi
            
            echo -e "${GREEN}✅ $name stopped${NC}"
        else
            echo -e "${YELLOW}⚠️  $name not running (PID: $PID)${NC}"
        fi
        rm "$pid_file"
    else
        echo -e "${YELLOW}⚠️  $name PID file not found${NC}"
    fi
}

# Stop API
stop_process "API Server" "logs/api.pid"

# Stop Dashboard
stop_process "Dashboard" "logs/dashboard.pid"

# Also kill by port in case PID files are missing
echo ""
echo -e "${YELLOW}🛠️  Cleaning up any remaining processes...${NC}"

# Kill processes on port 8000 (API)
API_PIDS=$(lsof -ti:8000 2>/dev/null || true)
if [ ! -z "$API_PIDS" ]; then
    echo -e "${YELLOW}Killing processes on port 8000: $API_PIDS${NC}"
    kill -9 $API_PIDS 2>/dev/null || true
fi

# Kill processes on port 8501 (Dashboard)
DASH_PIDS=$(lsof -ti:8501 2>/dev/null || true)
if [ ! -z "$DASH_PIDS" ]; then
    echo -e "${YELLOW}Killing processes on port 8501: $DASH_PIDS${NC}"
    kill -9 $DASH_PIDS 2>/dev/null || true
fi

echo ""
echo "============================================================"
echo -e "${GREEN}✅ Phase 5 has been stopped${NC}"
echo "============================================================"
echo ""
echo "Logs are available at:"
echo "  - logs/api.log"
echo "  - logs/dashboard.log"
echo ""
echo "To restart:"
echo "  ./start_phase5.sh"
echo ""
