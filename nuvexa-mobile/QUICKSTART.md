# NUVEXA Mobile - Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

✅ Node.js 18+ installed
✅ Python 3.11+ installed
✅ OpenAI API key ([get one free](https://platform.openai.com/api-keys))

## Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd nuvexa-mobile/backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.template .env

# Edit .env and add your OpenAI API key
nano .env  # or use any text editor
```

In `.env`, set:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

```bash
# Start backend
python -m uvicorn app.main:app --reload
```

✅ Backend running at `http://localhost:8000`

## Step 2: Frontend Setup (1 minute)

Open a **new terminal** window:

```bash
# Navigate to frontend
cd nuvexa-mobile/frontend

# Install dependencies
npm install

# Setup environment
cp .env.template .env
# Default settings work fine for local dev

# Start frontend
npm run dev
```

✅ Frontend running at `http://localhost:5173`

## Step 3: Test It! (30 seconds)

1. Open browser to `http://localhost:5173`
2. Type a message: "Hello!"
3. Get AI response!

## Test on iPhone (2 minutes)

### Same WiFi Network Required

1. **Find your computer's IP:**
   ```bash
   # Mac
   ipconfig getifaddr en0

   # Linux
   hostname -I

   # Windows
   ipconfig
   ```

2. **On your iPhone:**
   - Open Safari
   - Go to: `http://YOUR_IP:5173`
   - Chat with NUVEXA!

3. **Add to Home Screen:**
   - Tap Share button
   - Select "Add to Home Screen"
   - Tap "Add"
   - Launch from home screen like a native app!

## Quick Commands Reference

### Backend
```bash
# Start backend
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload

# View API docs
open http://localhost:8000/docs

# Test health
curl http://localhost:8000/api/health
```

### Frontend
```bash
# Start frontend
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Troubleshooting

### "Module not found" error
```bash
# Backend: Make sure venv is activated
source venv/bin/activate

# Frontend: Reinstall dependencies
rm -rf node_modules
npm install
```

### "OpenAI API error"
- Check your API key in `backend/.env`
- Verify key is valid at platform.openai.com
- Ensure you have credits/billing set up

### Can't access from phone
- Both devices must be on same WiFi
- Check firewall isn't blocking port 5173
- Try computer's IP address, not "localhost"

### Backend CORS error
- Check `backend/app/config.py`
- Add your IP to `cors_origins` list

## Next Steps

✅ Local development working
🚀 Ready to deploy? See `README.md` for deployment guides
🎨 Want to customize? See customization section in `README.md`
🐛 Having issues? Check troubleshooting in `README.md`

---

**That's it!** You now have a fully functional mobile-first AI assistant running locally and accessible from your iPhone!
