#!/bin/bash

echo "🛑 Stopping NUVEXA Mobile..."

# Kill backend
if [ -f /tmp/nuvexa-backend.pid ]; then
    BACKEND_PID=$(cat /tmp/nuvexa-backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo "   ✅ Backend stopped"
    fi
    rm /tmp/nuvexa-backend.pid
fi

# Kill frontend
if [ -f /tmp/nuvexa-frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/nuvexa-frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo "   ✅ Frontend stopped"
    fi
    rm /tmp/nuvexa-frontend.pid
fi

# Cleanup any remaining processes
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo "✅ All servers stopped!"
