#!/bin/bash

echo "================================================"
echo "  🚀 Starting NUVEXA Mobile"
echo "================================================"
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from nuvexa-mobile directory"
    echo "   cd /home/user/nuvexa-ai/nuvexa-mobile"
    exit 1
fi

# Start backend in background
echo "📡 Starting backend..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and start
source venv/bin/activate
pip install -q -r requirements.txt > /dev/null 2>&1

# Check for API key
if ! grep -q "sk-" .env 2>/dev/null; then
    echo ""
    echo "⚠️  WARNING: OpenAI API key not found!"
    echo "   Please edit backend/.env and add your API key"
    echo "   Get one at: https://platform.openai.com/api-keys"
    echo ""
fi

# Start backend in background
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/nuvexa-backend.log 2>&1 &
BACKEND_PID=$!
echo "   ✅ Backend started (PID: $BACKEND_PID)"

cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend in background
echo "📱 Starting frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   Installing dependencies..."
    npm install > /dev/null 2>&1
fi

npm run dev > /tmp/nuvexa-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   ✅ Frontend started (PID: $FRONTEND_PID)"

cd ..

# Wait for servers to be ready
echo ""
echo "⏳ Waiting for servers to start..."
sleep 3

# Get IP address
IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")

echo ""
echo "================================================"
echo "  ✅ NUVEXA Mobile is running!"
echo "================================================"
echo ""
echo "📍 Access URLs:"
echo ""
echo "   On this computer:"
echo "   🌐 http://localhost:5173"
echo ""
echo "   On your iPhone (same WiFi):"
echo "   📱 http://$IP:5173"
echo ""
echo "   Backend API:"
echo "   🔧 http://localhost:8000"
echo "   📚 http://localhost:8000/docs"
echo ""
echo "================================================"
echo ""
echo "💡 Tips:"
echo "   - Add to iPhone home screen for app experience"
echo "   - View logs: tail -f /tmp/nuvexa-*.log"
echo "   - Stop servers: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "🛑 To stop, press Ctrl+C or run:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Save PIDs for easy stopping
echo "$BACKEND_PID" > /tmp/nuvexa-backend.pid
echo "$FRONTEND_PID" > /tmp/nuvexa-frontend.pid

# Keep script running
wait
