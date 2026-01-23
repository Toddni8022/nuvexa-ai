# NUVEXA AI

**Your Living AI Assistant with Execution Power**

## What is NUVEXA?

NUVEXA is not another chatbot. It's a living AI assistant that completes tasks for you, including AI-native shopping and checkout.

## Features

- 🤖 **Assistant Mode**: General help, planning, and research
- 🛒 **Shopping Mode**: Search products and complete purchases
- 💭 **Therapist Mode**: Emotional support and active listening
- 🏗️ **Builder Mode**: Project planning and visual simulation

## Quick Start

### Windows
1. Run **SETUP.bat** to install dependencies
2. Edit **.env** file and add your OpenAI API key
3. Run **RUN_NUVEXA.bat** to start
4. NUVEXA opens in your browser!

### macOS/Linux (for iOS Access)
1. Open Terminal and navigate to the `nuvexa_ai` folder
2. Run `chmod +x SETUP_IOS.sh RUN_IOS.sh` to make scripts executable
3. Run `./SETUP_IOS.sh` to install dependencies
4. Edit **.env** file and add your OpenAI API key
5. Run `./RUN_IOS.sh` to start the server
6. **On your iOS device**: Open Safari and go to the URL shown in the terminal
7. Add to Home Screen for app-like experience!

### iOS Features
- ✨ **Mobile-optimized interface** with touch-friendly controls
- 📱 **Responsive design** that adapts to iPhone and iPad screens
- 🔄 **Add to Home Screen** for native app-like experience
- 🎨 **iOS-specific styling** with proper safe areas and gestures
- ⚡ **Fast and smooth** scrolling on iOS devices

## Requirements

- **Windows 10/11** (for Windows)
- **macOS 10.14+** or **Linux** (for iOS compatibility via network access)
- **iOS 12+** with Safari (for mobile access)
- Python 3.8 or higher
- OpenAI API key (free at: https://platform.openai.com/api-keys)

## The NUVEXA Vision

Traditional AI tools give you answers but leave you to execute manually. NUVEXA completes the follow-through - turning intention into action.

## iOS Setup Guide

### Prerequisites
- A Mac or Linux computer on the same WiFi network as your iOS device
- An iOS device (iPhone or iPad) with iOS 12 or later

### Step-by-Step Setup

1. **On Your Computer (Mac/Linux)**
   ```bash
   cd nuvexa_ai
   chmod +x SETUP_IOS.sh RUN_IOS.sh
   ./SETUP_IOS.sh
   ```

2. **Configure Your API Key**
   - Open the `.env` file in a text editor
   - Add your OpenAI API key: `OPENAI_API_KEY=your-key-here`
   - Get a free API key at: https://platform.openai.com/api-keys

3. **Start the Server**
   ```bash
   ./RUN_IOS.sh
   ```
   - The script will display the URL to access from your iOS device
   - Example: `http://192.168.1.100:8501`

4. **On Your iOS Device**
   - Make sure you're connected to the same WiFi network
   - Open **Safari** (recommended for best compatibility)
   - Enter the URL shown in the terminal
   - NUVEXA will load in your browser!

5. **Optional: Add to Home Screen**
   - In Safari, tap the Share button
   - Scroll down and tap "Add to Home Screen"
   - Name it "NUVEXA" and tap "Add"
   - Now you can launch NUVEXA like a native app!

### Troubleshooting iOS

- **Can't connect?** Make sure both devices are on the same WiFi network
- **Firewall blocking?** On macOS, allow the connection when prompted
- **Keyboard issues?** The app uses 16px font to prevent auto-zoom on iOS
- **Scrolling issues?** Try enabling "Request Desktop Website" in Safari

### iOS Browser Compatibility

- **Safari (Recommended)**: Full support with PWA features
- **Chrome iOS**: Supported but limited PWA functionality
- **Firefox iOS**: Supported but limited PWA functionality

Built with ❤️ to solve the AI execution gap.
