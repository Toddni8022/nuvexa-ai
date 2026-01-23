#!/bin/bash

# NUVEXA iOS Setup Script
# This script sets up NUVEXA to run on iOS/macOS and be accessible from mobile devices

echo "========================================="
echo "  🤖 NUVEXA iOS Setup"
echo "========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    echo ""
    echo "For macOS: brew install python3"
    echo "For iOS: Install Pythonista or a-Shell from the App Store"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed."
    echo "Please install pip3."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Create virtual environment (optional but recommended)
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip3 install -r requirements.txt
echo ""
echo "✓ All dependencies installed!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.template .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit the .env file and add your OpenAI API key!"
    echo "   Get your API key at: https://platform.openai.com/api-keys"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Get local IP address
echo "========================================="
echo "  📱 Mobile Access Information"
echo "========================================="
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "Unable to detect")
    echo "Your Mac's IP address: $LOCAL_IP"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "Unable to detect")
    echo "Your computer's IP address: $LOCAL_IP"
fi

echo ""
echo "To access NUVEXA from your iOS device:"
echo "1. Make sure your iOS device is on the same WiFi network"
echo "2. Run ./RUN_IOS.sh to start the server"
echo "3. Open Safari on your iOS device"
echo "4. Go to: http://$LOCAL_IP:8501"
echo ""
echo "========================================="
echo "  ✨ Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run: ./RUN_IOS.sh"
echo ""
