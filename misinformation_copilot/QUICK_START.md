# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## For Windows Users

### 1. First-Time Setup (5 minutes)

1. **Double-click** `SETUP.bat`
2. Wait for installation to complete
3. Edit `data\targets.json` with your Facebook targets
4. (Optional) Edit `.env` to configure LLM provider

### 2. Launch Dashboard

**Double-click** `START_DASHBOARD.bat`

The dashboard will open in your browser at `http://localhost:8501`

### 3. First Collection

1. Click **Collection** tab in sidebar
2. Adjust settings if needed:
   - Scroll Passes: 3
   - Max Posts per Target: 20
   - Scroll Delay: 2 seconds
3. Click **Start Collection**
4. **Log in to Facebook** when browser opens (first time only)
5. Wait for collection to complete
6. Browser will close automatically

### 4. Review & Respond

1. Click **Dashboard** tab
2. Browse collected posts
3. Click on a high-score post to expand
4. Click **Generate Drafts**
5. Review the 3 draft rebuttals
6. Click **Copy Draft 1/2/3** to copy your favorite
7. Click **Open Post** to open in browser
8. **Paste and manually post** your rebuttal
9. Return to dashboard, click **Done**

## Command Line (Alternative)

```bash
# Activate virtual environment
venv\Scripts\activate

# Run collector
python scripts\run_collector.py --max-posts 20

# Start dashboard
streamlit run app\ui.py
```

## Tips

- Start with 1-2 targets to test
- Use "mock" LLM mode initially (no API key needed)
- Review generated drafts carefully before posting
- Mark posts as "Needs Research" when unsure
- Export to CSV weekly for record-keeping

## Troubleshooting

**"Python not found"**
- Install Python 3.11+ from python.org
- Check "Add to PATH" during installation

**"Can't collect posts"**
- Make sure you're logged in to Facebook
- Check target URLs are correct
- Increase scroll delay for slower connections

**"Clipboard copy failed"**
- Manually select and copy the draft text

## Need Help?

See full `README.md` for detailed documentation.

---

**Remember: This tool assists but does not auto-post. You maintain full control!**
