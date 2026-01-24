# 🔍 Misinformation Debunking Copilot

A Windows 11 compatible tool that helps you scale your fact-checking workflow on Facebook with **human-in-the-loop** controls. This tool automates browsing, collection, and draft generation, but **requires manual approval for all posts**.

## ⚠️ Important Safety Notice

**This tool does NOT auto-post comments.** It is designed to assist, not replace, human judgment:

- ✅ Automates: Browsing, scrolling, screenshot capture, text extraction, scoring
- ✅ Assists: Draft generation, content organization
- ❌ Does NOT: Auto-post, auto-comment, or take any action without your approval
- ✅ Requires: Manual review and posting by you

## 🎯 Features

### Collection
- Automated browsing of Facebook pages, groups, and search results
- Configurable scrolling pace and limits
- Screenshot capture and text extraction
- Persistent browser profile (login once, reuse cookies)

### Analysis
- Heuristic-based misinformation scoring (0-100)
- Optional LLM-enhanced analysis (OpenAI, Anthropic, Ollama)
- Automatic tagging of problematic content patterns
- Fact-check question generation

### Review Dashboard
- Visual post browser with screenshots
- Filtering by score, status, and keywords
- Export to CSV for record-keeping

### Draft Generation
- 3 rebuttal styles per post:
  1. Short & Punchy
  2. Factual & Calm
  3. Snarky but Appropriate
- Copy-to-clipboard functionality
- One-click browser opening of original posts

## 📋 Prerequisites

- **Windows 11** (or Windows 10)
- **Python 3.11+**
- **Git** (for cloning the repository)
- **Facebook account** (you'll log in manually once)

## 🚀 Setup Instructions

### 1. Clone or Download

```bash
cd misinformation_copilot
```

### 2. Create Virtual Environment

```bash
# Windows Command Prompt
python -m venv venv
venv\Scripts\activate

# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# If you get an error about execution policy in PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

This downloads the Chromium browser that Playwright will use.

### 5. Configure Environment

```bash
# Copy the example .env file
copy .env.example .env

# Edit .env with your preferred text editor
notepad .env
```

**Basic configuration (works without API keys):**
```env
LLM_PROVIDER=mock
BROWSER_HEADLESS=false
```

**Advanced configuration (with LLM):**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

Supported LLM providers:
- `mock` - No API key required, uses heuristics only
- `openai` - Requires OpenAI API key
- `anthropic` - Requires Anthropic API key
- `ollama` - Requires local Ollama installation

### 6. Configure Targets

Edit `data/targets.json` to add Facebook pages, groups, or searches you want to monitor:

```json
{
  "targets": [
    {
      "name": "Climate Denial Page",
      "url": "https://www.facebook.com/some-page",
      "type": "page"
    },
    {
      "name": "Vaccine Misinformation Search",
      "url": "https://www.facebook.com/search/posts?q=vaccine%20hoax",
      "type": "search"
    }
  ]
}
```

**How to get URLs:**
- **Pages**: Visit the page, copy URL from address bar
- **Groups**: Visit the group, copy URL from address bar
- **Searches**: Search on Facebook, copy URL from address bar

## 🎮 Usage

### Method 1: Streamlit Dashboard (Recommended)

**Start the dashboard:**

```bash
streamlit run app/ui.py
```

The dashboard will open in your browser at `http://localhost:8501`

**First time setup:**
1. Go to the **Collection** tab
2. Click **Start Collection** (browser will open)
3. **Manually log in to Facebook** in the browser window
4. Close the browser when collection completes
5. Your session is saved - no need to log in again!

**Dashboard workflow:**
1. **Collection Tab**: Configure and run collection
2. **Dashboard Tab**: Review posts, see scores
3. Click on any post to expand details
4. **Generate Drafts** button creates 3 rebuttal options
5. **Copy Draft** buttons copy to clipboard
6. **Open Post** opens in your default browser
7. **Manually paste and post** the rebuttal on Facebook
8. Mark as **Done**, **Skip**, or **Needs Research**

### Method 2: Command Line Collector

```bash
python scripts/run_collector.py --max-posts 20 --scroll-passes 3
```

**Options:**
- `--max-posts N` - Maximum posts per target (default: 20)
- `--max-targets N` - Maximum targets to process (default: 5)
- `--scroll-passes N` - Number of scroll passes (default: 3)
- `--scroll-delay N` - Delay between scrolls in seconds (default: 2.0)
- `--headless` - Run browser in background

After collection, use the Streamlit dashboard to review posts.

## 📁 Project Structure

```
misinformation_copilot/
├── app/
│   ├── config.py          # Configuration management
│   ├── storage.py         # SQLite database operations
│   ├── collector.py       # Playwright-based collector
│   ├── scoring.py         # Misinformation scoring
│   ├── drafting.py        # Rebuttal generation
│   └── ui.py             # Streamlit dashboard
├── data/
│   ├── targets.json       # Your target list
│   ├── posts.db          # SQLite database (auto-created)
│   ├── screenshots/       # Captured screenshots
│   └── browser_profile/   # Persistent browser session
├── scripts/
│   └── run_collector.py   # Standalone collector script
├── requirements.txt       # Python dependencies
├── .env.example          # Example configuration
└── README.md             # This file
```

## 🔧 Configuration Options

### Collection Settings

Adjust in the Streamlit dashboard or via command-line arguments:

- **Scroll Passes**: Higher = more posts collected, slower
- **Scroll Delay**: Higher = more reliable, slower (respect rate limits!)
- **Max Posts per Target**: Limit collection size
- **Headless Mode**: Run browser in background (can't see login screen!)

### LLM Providers

**Mock Mode (Default)**
- No API key required
- Uses heuristics only
- Good for testing and basic scoring

**OpenAI**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
```

**Anthropic**
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**Ollama (Local)**
```env
LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

## 📊 How It Works

### 1. Collection Phase
- Opens browser with your saved login session
- Visits each target URL
- Scrolls page to load posts
- Extracts text content and metadata
- Takes screenshots
- Stores everything in local database

### 2. Scoring Phase
- Analyzes text for misinformation indicators:
  - ALL CAPS and excessive punctuation
  - Sensational language ("They don't want you to know!")
  - Vague sources ("Someone said...")
  - Conspiracy markers
  - Emotional manipulation
- Assigns 0-100 score
- Optionally uses LLM for nuanced analysis

### 3. Review Phase (You!)
- Browse collected posts in dashboard
- Filter by score, status, keywords
- Review screenshots and extracted text
- Generate rebuttal drafts

### 4. Draft Generation
- Creates 3 rebuttal styles:
  - **Short Punchy**: Quick, direct response
  - **Factual Calm**: Evidence-based, educational
  - **Snarky**: Personality + facts, no hate speech
- Copy to clipboard

### 5. Manual Posting (You!)
- Open post in browser
- Paste your selected draft
- Edit as needed
- **YOU** click Post
- Mark as Done in dashboard

## ⚖️ Limitations & Best Practices

### Technical Limitations
- **Facebook changes**: Selectors may break when Facebook updates
- **Login walls**: Some content requires login to view
- **Rate limiting**: Facebook may throttle or block excessive requests
- **Dynamic content**: Some posts load asynchronously and may be missed

### Ethical & Legal Considerations

✅ **DO:**
- Use on public content
- Verify facts before posting rebuttals
- Respect platform terms of service
- Use reasonable delays between actions
- Maintain a respectful tone
- Disclose if using AI-assisted drafts (if required by platform)

❌ **DON'T:**
- Auto-post without review
- Harass individuals
- Coordinate mass reporting/commenting
- Violate Facebook's automation policies
- Evade detection mechanisms
- Use for commercial spam
- Impersonate others

### Staying Within Normal User Workflows

**This tool is designed for human assistance, not automation:**

1. **Use realistic pacing**: Don't collect thousands of posts in minutes
2. **Manual posting only**: Review and post each comment yourself
3. **One account**: Don't create multiple accounts for amplification
4. **Natural patterns**: Spread activity over time, don't post 50 comments in a row
5. **Quality over quantity**: Focus on substantive fact-checking, not volume

**If Facebook detects automation:**
- You may be temporarily blocked from commenting
- Your account could be restricted
- Solution: Use longer delays, manual posting only

## 🐛 Troubleshooting

### "Playwright not installed"
```bash
playwright install chromium
```

### "Login required" or "Can't access posts"
- Run collection with `BROWSER_HEADLESS=false`
- Manually log in when browser opens
- Your session will be saved in `data/browser_profile/`

### "No posts collected"
- Check target URLs are correct
- Increase scroll passes
- Increase scroll delay
- Check Facebook didn't show login/consent dialogs

### "Copy to clipboard failed"
- Install `pyperclip`: `pip install pyperclip`
- On Linux: May need `xclip` or `xsel`
- Fallback: Manually copy draft text

### LLM errors
- Check API key in `.env`
- Verify model name is correct
- Check API rate limits
- Try `LLM_PROVIDER=mock` as fallback

### Database locked
- Close other instances of the app
- Delete `data/posts.db.lock` if it exists

## 🔄 Updates & Maintenance

**Updating Facebook selectors:**

If Facebook changes and posts aren't collecting:
1. Open `app/collector.py`
2. Find `post_selectors` list
3. Use browser DevTools to find new selectors
4. Add to the list

**Backing up your data:**

```bash
# Backup database and screenshots
copy data\posts.db posts_backup.db
xcopy /E /I data\screenshots screenshots_backup
```

## 📝 Example Workflow

1. **Morning**: Run collector for 10 minutes
   ```bash
   streamlit run app/ui.py
   # Go to Collection, click Start Collection
   ```

2. **Review**: Filter to high-score posts
   - Dashboard → Status: "Queued"
   - Score Range: "High (70+)"

3. **Generate drafts**: Click "Generate Drafts" on interesting posts

4. **Select & edit**: Choose your favorite draft, edit if needed

5. **Post**: Copy draft, open post, paste, review, post manually

6. **Mark done**: Click "Done" to track progress

7. **Export**: At end of week, export to CSV for records

## 🆘 Support

For issues:
1. Check this README
2. Review error messages carefully
3. Check `.env` configuration
4. Try with `LLM_PROVIDER=mock` to isolate LLM issues
5. Check `data/targets.json` syntax

## ⚖️ License & Disclaimer

**License**: MIT (or specify your license)

**Disclaimer**: This tool is provided for educational and fact-checking purposes. Users are responsible for:
- Complying with Facebook's Terms of Service
- Verifying factual accuracy of rebuttals
- Ethical use of automation-assisted workflows
- Legal compliance in their jurisdiction

The authors are not responsible for misuse, account bans, or legal issues arising from use of this tool.

**Use responsibly. Fact-check carefully. Post manually.**

---

## 🎯 Quick Start Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] `pip install -r requirements.txt` completed
- [ ] `playwright install chromium` completed
- [ ] `.env` file created and configured
- [ ] `data/targets.json` configured with your targets
- [ ] Streamlit dashboard running: `streamlit run app/ui.py`
- [ ] Logged in to Facebook in the browser
- [ ] First collection test completed
- [ ] Reviewed posts in dashboard
- [ ] Generated and copied a draft
- [ ] Manually posted a fact-check

**You're ready to scale your fact-checking workflow!** 🚀
