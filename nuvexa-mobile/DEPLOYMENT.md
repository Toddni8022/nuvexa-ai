# NUVEXA Mobile - Deployment Guide

Complete guide for deploying to production.

## Overview

We'll deploy:
- **Backend** → Render, Railway, or Fly.io
- **Frontend** → Vercel, Netlify, or Render

Choose your preferred platform below.

---

## Option 1: Render (Recommended - Easiest)

Free tier available, automatic deploys from Git.

### Prerequisites

1. Create account at [render.com](https://render.com)
2. Push your code to GitHub
3. Have your OpenAI API key ready

### Deploy Backend

1. **Create Web Service:**
   - Dashboard → New → Web Service
   - Connect GitHub repository
   - Select your repo

2. **Configure:**
   ```
   Name: nuvexa-api
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

3. **Environment Variables:**
   Click "Advanced" → Add Environment Variables:
   ```
   OPENAI_API_KEY=your-key-here
   OPENAI_MODEL=gpt-4
   CORS_ORIGINS=*
   ```

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-3 minutes for build
   - Copy your backend URL: `https://nuvexa-api.onrender.com`

### Deploy Frontend

1. **Create Static Site:**
   - Dashboard → New → Static Site
   - Connect same GitHub repository

2. **Configure:**
   ```
   Name: nuvexa-frontend
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

3. **Environment Variables:**
   ```
   VITE_API_URL=https://nuvexa-api.onrender.com
   ```
   (Use your actual backend URL from previous step)

4. **Deploy:**
   - Click "Create Static Site"
   - Wait 1-2 minutes
   - Your app is live! 🎉

### Update Backend CORS

After frontend deploys, update backend CORS:

1. Go to backend service on Render
2. Environment → Edit `CORS_ORIGINS`
3. Set to: `https://your-frontend.onrender.com`

---

## Option 2: Railway + Vercel

Fast deployments, generous free tier.

### Deploy Backend on Railway

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Deploy:**
   ```bash
   cd backend
   railway init
   railway up
   ```

4. **Set Environment Variables:**
   ```bash
   railway variables set OPENAI_API_KEY=your-key-here
   railway variables set OPENAI_MODEL=gpt-4
   railway variables set CORS_ORIGINS=*
   ```

5. **Get URL:**
   ```bash
   railway domain
   ```
   Copy the URL (e.g., `https://nuvexa-api.railway.app`)

### Deploy Frontend on Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd frontend
   vercel
   ```

4. **Set Environment Variable:**
   When prompted or in dashboard:
   ```
   VITE_API_URL=https://nuvexa-api.railway.app
   ```

5. **Production Deploy:**
   ```bash
   vercel --prod
   ```

Your app is live! 🚀

---

## Option 3: Fly.io (Advanced)

More control, Docker-based deployments.

### Prerequisites

Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

### Deploy Backend

1. **Login:**
   ```bash
   fly auth login
   ```

2. **Launch:**
   ```bash
   cd backend
   fly launch
   ```

3. **Configure (fly.toml):**
   ```toml
   app = "nuvexa-api"

   [build]
     dockerfile = "Dockerfile"

   [env]
     PORT = "8000"

   [[services]]
     internal_port = 8000
     protocol = "tcp"

     [[services.ports]]
       port = 80
       handlers = ["http"]

     [[services.ports]]
       port = 443
       handlers = ["tls", "http"]
   ```

4. **Set Secrets:**
   ```bash
   fly secrets set OPENAI_API_KEY=your-key-here
   fly secrets set OPENAI_MODEL=gpt-4
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

### Deploy Frontend

Similar process:
```bash
cd frontend
fly launch
fly secrets set VITE_API_URL=https://nuvexa-api.fly.dev
fly deploy
```

---

## Option 4: Docker Compose (Self-Hosted)

Deploy to any server with Docker.

### docker-compose.yml

Create in project root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=gpt-4
      - CORS_ORIGINS=http://localhost:3000
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      args:
        - VITE_API_URL=http://localhost:8000
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Deploy

```bash
# Create .env file
echo "OPENAI_API_KEY=your-key" > .env

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

Access at `http://localhost:3000`

---

## Post-Deployment Checklist

### ✅ Verify Backend

```bash
# Health check
curl https://your-backend-url.com/api/health

# Test chat
curl -X POST https://your-backend-url.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "mode": "assistant"}'
```

### ✅ Test Frontend

1. Open frontend URL in browser
2. Open developer console
3. Check for errors
4. Send a test message
5. Verify shopping mode works

### ✅ Mobile Testing

1. Open on iPhone Safari
2. Test all features
3. Add to home screen
4. Test offline capabilities
5. Check different screen sizes

### ✅ Performance

Use Lighthouse in Chrome DevTools:
- Performance score > 90
- Accessibility score > 95
- Best Practices score > 90
- SEO score > 90

---

## Monitoring & Maintenance

### Set Up Monitoring

**Backend:**
- Add health check endpoint monitoring
- Set up error tracking (Sentry)
- Monitor API response times
- Track API costs (OpenAI usage)

**Frontend:**
- Monitor bundle size
- Track Core Web Vitals
- Set up error tracking
- Monitor user engagement

### Regular Maintenance

**Weekly:**
- Check error logs
- Review API usage/costs
- Monitor uptime

**Monthly:**
- Update dependencies
- Security audit
- Performance review
- Cost optimization

**Quarterly:**
- Major feature updates
- Infrastructure review
- Scaling assessment

---

## Scaling Strategies

### When to Scale

Monitor these metrics:
- Response time > 2s
- Error rate > 1%
- CPU usage > 80%
- Memory usage > 85%

### Horizontal Scaling

**Backend:**
```bash
# Railway: Scale instances
railway scale --replicas 3

# Fly.io: Scale regions
fly scale count 3

# Render: Upgrade plan for auto-scaling
```

**Frontend:**
- Add CDN (Cloudflare, CloudFront)
- Enable caching
- Optimize images

### Database Addition

When conversation history is needed:

1. **Add PostgreSQL:**
   ```bash
   railway add --service postgresql
   ```

2. **Update Backend:**
   - Add SQLAlchemy models
   - Implement conversation storage
   - Add user sessions

3. **Migrate:**
   ```bash
   alembic upgrade head
   ```

---

## Troubleshooting Deployments

### Build Fails

**Python dependencies:**
```bash
# Specify Python version
echo "3.11" > runtime.txt

# Check requirements.txt
pip freeze > requirements.txt
```

**Node build fails:**
```bash
# Clear cache
npm ci --cache .npm

# Specify Node version in package.json
"engines": {
  "node": ">=18.0.0"
}
```

### CORS Errors

Update backend CORS settings:
```python
# app/config.py
cors_origins: list[str] = [
    "https://your-frontend.vercel.app",
    "https://your-frontend.netlify.app"
]
```

### SSL/HTTPS Issues

Most platforms handle SSL automatically. If issues:
- Ensure backend accepts HTTPS
- Check mixed content warnings
- Verify certificates

### High Costs

OpenAI API optimization:
- Reduce max_tokens
- Use GPT-3.5 instead of GPT-4
- Implement caching
- Add rate limiting

---

## Production Best Practices

### Security

✅ Use environment variables for secrets
✅ Enable HTTPS only
✅ Implement rate limiting
✅ Add input validation
✅ Sanitize user inputs
✅ Regular security audits

### Performance

✅ Enable gzip compression
✅ Implement caching
✅ Optimize images
✅ Minimize bundle size
✅ Use CDN for assets
✅ Database indexing

### Reliability

✅ Health checks
✅ Error monitoring
✅ Logging
✅ Backup strategies
✅ Disaster recovery plan
✅ Auto-scaling

---

## Cost Estimates

### Free Tier (Testing)

- **Render:** Free backend + frontend
- **Vercel:** Free frontend hosting
- **Railway:** $5 credit/month free
- **OpenAI:** Pay per use (~$0.002/request)

**Monthly:** ~$5-10 for light usage

### Production (1000 users)

- **Backend:** ~$25-50/month
- **Frontend:** Free - $20/month
- **Database:** ~$15-30/month
- **OpenAI API:** ~$100-500/month

**Total:** $140-600/month depending on usage

### Optimization

Reduce costs by:
- Caching responses
- Using GPT-3.5 Turbo
- Implementing rate limits
- Optimizing prompts
- Batch processing

---

**Need help?** Open an issue on GitHub or check the troubleshooting guide!

Happy deploying! 🚀
