#!/bin/bash

# NUVEXA iOS Run Script
# This script starts NUVEXA server accessible from iOS devices on your network

echo "========================================="
echo "  🤖 Starting NUVEXA for iOS"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
    echo "✓ Virtual environment activated"
    echo ""
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please run SETUP_IOS.sh first."
    exit 1
fi

# Get local IP address for display
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "localhost")
else
    LOCAL_IP="localhost"
fi

echo "========================================="
echo "  📱 Access NUVEXA from iOS"
echo "========================================="
echo ""
echo "On your iOS device:"
echo "1. Open Safari"
echo "2. Go to: http://$LOCAL_IP:8501"
echo ""
echo "On this computer:"
echo "   Go to: http://localhost:8501"
echo ""
echo "========================================="
echo ""
echo "🚀 Starting NUVEXA server..."
echo "   (Press Ctrl+C to stop)"
echo ""

# Start Streamlit with network access enabled
streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true

# Note: If you get a firewall prompt on macOS, allow the connection
# to enable access from iOS devices on your network
