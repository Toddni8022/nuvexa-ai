# NUVEXA Mobile

A lightning-fast, mobile-first AI assistant with shopping capabilities. Built with React + Vite frontend and FastAPI backend.

## ✨ Features

- 🤖 **AI Assistant Mode** - Get help, advice, and answers
- 🛒 **Shopping Mode** - Find and compare products
- 📱 **Mobile-First** - Optimized for iPhone and all devices
- ⚡ **Lightning Fast** - Sub-3s load times
- 🎨 **Beautiful UI** - Modern, clean interface
- 🔄 **PWA Ready** - Add to home screen for app-like experience
- 🌐 **Universal** - Works on iOS, Android, and desktop

## 🏗️ Architecture

```
Frontend (React + Vite)
     ↓ REST API
Backend (FastAPI)
     ↓
OpenAI GPT-4
```

### Tech Stack

**Frontend:**
- React 18
- Vite (fast builds)
- Context API (state management)
- CSS Modules
- PWA with service worker

**Backend:**
- Python 3.11+
- FastAPI
- OpenAI API
- Pydantic v2
- Uvicorn

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 1. Clone and Setup

```bash
git clone <your-repo>
cd nuvexa-mobile
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env and add your OPENAI_API_KEY

# Run backend
python -m uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.template .env
# Edit .env if needed (default points to localhost:8000)

# Run frontend
npm run dev
```

Frontend runs at: `http://localhost:5173`

### 4. Open on Your Phone

1. Find your computer's IP address:
   - **Mac/Linux**: `ifconfig | grep inet`
   - **Windows**: `ipconfig`

2. On your phone (same WiFi network):
   - Open browser and go to: `http://YOUR_IP:5173`

3. **Add to Home Screen** (iOS):
   - Tap Share → "Add to Home Screen"
   - Launch like a native app!

## 📱 iOS Testing

### Test on iPhone Simulator (Mac)

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Run iOS Simulator
open -a Simulator

# In simulator, open Safari and go to:
http://localhost:5173
```

### Test on Real iPhone

1. Connect iPhone and Mac to same WiFi
2. Get your Mac's IP: `ipconfig getifaddr en0`
3. On iPhone Safari: `http://YOUR_IP:5173`

## 🚢 Deployment

### Option 1: Render (Easiest)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy Backend**
   - Go to [render.com](https://render.com)
   - New → Web Service
   - Connect your repo
   - Select `backend` folder
   - Add environment variable: `OPENAI_API_KEY`
   - Deploy!

3. **Deploy Frontend**
   - New → Static Site
   - Connect your repo
   - Select `frontend` folder
   - Add build command: `npm install && npm run build`
   - Add environment variable: `VITE_API_URL=https://your-backend.onrender.com`
   - Deploy!

### Option 2: Railway (Backend) + Vercel (Frontend)

**Backend on Railway:**
```bash
cd backend
railway login
railway init
railway up
railway variables set OPENAI_API_KEY=your-key
```

**Frontend on Vercel:**
```bash
cd frontend
vercel login
vercel
# Follow prompts, add VITE_API_URL env variable
```

### Option 3: Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy backend
cd backend
fly launch
fly secrets set OPENAI_API_KEY=your-key
fly deploy

# Deploy frontend
cd ../frontend
fly launch
fly secrets set VITE_API_URL=https://your-backend.fly.dev
fly deploy
```

## 🧪 Testing Locally

### Test Backend API

```bash
# Health check
curl http://localhost:8000/api/health

# Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "mode": "assistant"}'

# Test shop
curl -X POST http://localhost:8000/api/shop \
  -H "Content-Type: application/json" \
  -d '{"query": "laptop"}'
```

### Test Frontend

1. Open browser dev tools (F12)
2. Toggle device toolbar (mobile view)
3. Select iPhone or other device
4. Test touch interactions

## 📁 Project Structure

```
nuvexa-mobile/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Settings
│   │   ├── services/
│   │   │   ├── openai_service.py    # OpenAI integration
│   │   │   └── shopping_service.py  # Product search
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   └── middleware/
│   │       └── error_handler.py # Error handling
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.template
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── contexts/            # State management
│   │   ├── services/            # API client
│   │   ├── styles/              # CSS
│   │   ├── App.jsx              # Main component
│   │   └── main.jsx             # Entry point
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.template
│
├── render.yaml                  # Render deployment
├── railway.json                 # Railway deployment
└── README.md
```

## 🔧 Configuration

### Backend Environment Variables

```bash
OPENAI_API_KEY=your-key-here       # Required
OPENAI_MODEL=gpt-4                 # Optional (default: gpt-4)
OPENAI_MAX_TOKENS=1000             # Optional (default: 1000)
HOST=0.0.0.0                       # Optional (default: 0.0.0.0)
PORT=8000                          # Optional (default: 8000)
CORS_ORIGINS=*                     # Optional (default: localhost origins)
```

### Frontend Environment Variables

```bash
VITE_API_URL=http://localhost:8000  # Backend URL
```

## 🎨 Customization

### Add New Modes

1. Add mode in `backend/app/services/openai_service.py`:
   ```python
   prompts = {
       "assistant": "...",
       "shopping": "...",
       "your_mode": "Your custom prompt"
   }
   ```

2. Add mode endpoint in `backend/app/main.py`:
   ```python
   @app.get("/api/modes")
   async def get_modes():
       return {
           "modes": [
               ...,
               {"id": "your_mode", "name": "Your Mode", "icon": "🎯"}
           ]
       }
   ```

### Customize Styling

Edit `frontend/src/styles/App.css`:
- Change `:root` variables for colors
- Modify component styles
- Adjust responsive breakpoints

### Add Real Shopping API

Replace mock data in `backend/app/services/shopping_service.py`:
```python
def search_products(self, query: str):
    # Call real API (Amazon, eBay, etc.)
    response = requests.get(f"https://api.example.com/search?q={query}")
    return response.json()
```

## 📈 Scaling & Improvements

### Performance

- **Add Redis caching** for frequent queries
- **Implement rate limiting** to prevent abuse
- **Use CDN** for frontend assets
- **Add database** for conversation history
- **Implement streaming** for real-time AI responses

### Features

- **User authentication** with JWT
- **Conversation persistence** with database
- **Voice input** for mobile
- **Push notifications** for updates
- **Analytics** to track usage
- **A/B testing** for UX improvements

### Infrastructure

- **Kubernetes** for container orchestration
- **Load balancing** for high traffic
- **Monitoring** with Prometheus/Grafana
- **Logging** with ELK stack
- **CI/CD** with GitHub Actions

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.11+

# Check OpenAI key
echo $OPENAI_API_KEY

# Check port availability
lsof -i :8000
```

### Frontend won't connect to backend

1. Check backend is running: `curl http://localhost:8000/api/health`
2. Check CORS settings in backend
3. Verify `VITE_API_URL` in frontend `.env`
4. Check browser console for errors

### iOS zoom on input

Already fixed! Inputs use 16px font size to prevent zoom.

### Can't access from phone

1. Check same WiFi network
2. Check firewall settings
3. Try `0.0.0.0` instead of `localhost`
4. Check IP address is correct

## 📝 License

MIT License - feel free to use for any project!

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 💬 Support

Questions? Issues? Open a GitHub issue or reach out!

---

Built with ❤️ for the mobile-first future
