# 📋 Project Summary

## Overview

**Misinformation Debunking Copilot** is a Windows 11 compatible Python application that assists fact-checkers in scaling their workflow on Facebook. It automates the tedious parts (browsing, collecting, drafting) while maintaining human control over the final posting decision.

**Core Principle**: Assist, don't automate. Human in the loop for all final actions.

## Architecture

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.11+ | Core application |
| **Browser Automation** | Playwright (Chromium) | Facebook browsing |
| **UI Framework** | Streamlit | Interactive dashboard |
| **Database** | SQLite3 | Post storage |
| **LLM Integration** | OpenAI / Anthropic / Ollama | Optional enhanced scoring |
| **Environment** | python-dotenv | Configuration management |
| **Utilities** | pyperclip | Clipboard operations |

### System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER CONFIGURATION                       │
│  • data/targets.json (Facebook URLs to monitor)             │
│  • .env (LLM provider, API keys)                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    COLLECTION PHASE                          │
│  collector.py:                                              │
│  • Playwright opens browser (persistent session)            │
│  • Visits each target URL                                   │
│  • Scrolls page to load posts                               │
│  • Extracts text, author, timestamp                         │
│  • Takes screenshots                                         │
│  • Stores in SQLite database                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     SCORING PHASE                            │
│  scoring.py:                                                │
│  • Heuristic analysis (caps, punctuation, phrases)          │
│  • Optional LLM analysis (nuanced scoring)                  │
│  • Assigns 0-100 misinformation score                       │
│  • Tags problematic patterns                                │
│  • Generates fact-check questions                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    REVIEW PHASE (UI)                         │
│  ui.py (Streamlit Dashboard):                              │
│  • Display posts with scores                               │
│  • Filter by status, score, keywords                        │
│  • Show screenshots + extracted text                        │
│  • User reviews and selects posts to respond to            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DRAFTING PHASE                            │
│  drafting.py:                                               │
│  • Generate 3 rebuttal styles:                              │
│    1. Short & Punchy                                        │
│    2. Factual & Calm                                        │
│    3. Snarky but Appropriate                                │
│  • User selects preferred draft                             │
│  • Copy to clipboard                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   MANUAL POSTING (USER)                      │
│  • User clicks "Open Post" (opens in browser)               │
│  • User pastes draft                                        │
│  • User reviews and edits                                   │
│  • USER clicks Post button                                  │
│  • User marks post as Done in dashboard                     │
└─────────────────────────────────────────────────────────────┘
```

## Module Breakdown

### `app/config.py`

**Purpose**: Centralized configuration management

**Key Features**:
- Environment variable loading via `.env`
- Path management (database, screenshots, browser profile)
- LLM provider configuration
- Default settings for collection
- Targets JSON loading/saving

**Key Classes**:
- `Config`: Static configuration class

**Exports**:
- `Config`, `DB_PATH`, `SCREENSHOTS_DIR`, `BROWSER_PROFILE_DIR`, `TARGETS_PATH`

---

### `app/storage.py`

**Purpose**: SQLite database operations and file management

**Key Features**:
- Database initialization with schema
- CRUD operations for posts
- Filtering and sorting
- Export to CSV
- Screenshot file management
- Statistics generation

**Database Schema**:
```sql
posts (
    id INTEGER PRIMARY KEY,
    target_name TEXT,
    url TEXT,
    author TEXT,
    post_timestamp TEXT,
    text_content TEXT,
    screenshot_path TEXT,
    collected_at DATETIME,
    status TEXT,  -- queued, done, skip, needs_research
    misinfo_score INTEGER,
    tags TEXT,  -- JSON array
    rationale TEXT,
    fact_check_questions TEXT,  -- JSON array
    drafts TEXT  -- JSON array
)
```

**Key Classes**:
- `PostStorage`: Main database interface

**Key Functions**:
- `get_storage()`: Singleton accessor

---

### `app/collector.py`

**Purpose**: Playwright-based Facebook post collection

**Key Features**:
- Persistent browser context (saves login session)
- Configurable scrolling and pacing
- Multiple post selector strategies (robustness)
- Screenshot capture
- Text extraction
- Automatic scoring integration
- Progress callbacks for UI

**Key Classes**:
- `FacebookCollector`: Main collector

**Key Functions**:
- `collect_posts()`: Convenience function

**Safety Features**:
- No auto-posting
- Respects scroll delays
- Uses normal browser profile

---

### `app/scoring.py`

**Purpose**: Misinformation likelihood scoring

**Key Features**:
- Heuristic-based scoring (no API required)
- Optional LLM integration (OpenAI, Anthropic, Ollama)
- Pattern detection for sensational language
- Conspiracy theory markers
- Fact-check question generation

**Heuristic Patterns**:
- ALL CAPS excessive usage
- Excessive punctuation (!!!)
- Sensational phrases ("they don't want you to know")
- Vague sources ("someone said")
- Conspiracy markers ("wake up sheeple")

**Key Classes**:
- `MisinfoScorer`: Main scoring engine

**LLM Integration**:
- Blends heuristic (40%) + LLM (60%) scores
- Fallback to heuristics if LLM fails
- JSON response parsing

---

### `app/drafting.py`

**Purpose**: Rebuttal draft generation

**Key Features**:
- 3 distinct writing styles
- Template-based fallback (no LLM required)
- LLM-enhanced drafts (when available)
- Context-aware generation

**Draft Styles**:
1. **Short Punchy**: 2-3 sentences, direct, cuts through nonsense
2. **Factual Calm**: Evidence-based, "what we know / don't know"
3. **Snarky**: Personality + facts, no hate speech

**Key Classes**:
- `RebuttalDrafter`: Main drafting engine

**Key Functions**:
- `generate_drafts()`: Convenience function

---

### `app/ui.py`

**Purpose**: Streamlit web dashboard

**Key Features**:
- Multi-page interface (Dashboard, Collection, Statistics, Configuration)
- Real-time filtering and sorting
- Post card display with screenshots
- Draft generation and clipboard copy
- Status management
- Export functionality
- Configuration editor

**Pages**:
1. **Dashboard**: Review and respond to posts
2. **Collection**: Run collector with settings
3. **Statistics**: View analytics
4. **Configuration**: Manage targets and settings

**User Actions**:
- Generate Drafts
- Copy to Clipboard
- Open Post in Browser
- Mark Done/Skip/Needs Research
- Export to CSV

---

### `scripts/run_collector.py`

**Purpose**: Command-line interface for collection

**Key Features**:
- Argument parsing
- Progress display
- Interactive confirmation
- Error handling
- Statistics reporting

**Usage**:
```bash
python scripts/run_collector.py \
    --max-posts 20 \
    --scroll-passes 3 \
    --scroll-delay 2.0 \
    --headless
```

---

## Data Storage

### Database

**Location**: `data/posts.db`

**Type**: SQLite3

**Size Considerations**:
- ~1KB per post (text only)
- Grows linearly with collection
- Recommend archiving after 10,000+ posts

### Screenshots

**Location**: `data/screenshots/`

**Format**: PNG

**Naming**: `{target_name}_{timestamp}.png`

**Size Considerations**:
- ~500KB per screenshot
- Can accumulate quickly
- Recommend periodic cleanup of old screenshots

### Browser Profile

**Location**: `data/browser_profile/`

**Purpose**: Persistent browser session (saves login)

**Contents**:
- Cookies
- Local storage
- Session data

**Privacy Note**: Contains your Facebook session. Keep secure.

---

## Configuration Files

### `.env`

**Purpose**: Environment variables for sensitive data

**Key Settings**:
```env
LLM_PROVIDER=mock|openai|anthropic|ollama
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
BROWSER_HEADLESS=true|false
```

**Security**: Never commit to git (in `.gitignore`)

### `data/targets.json`

**Purpose**: List of Facebook URLs to monitor

**Schema**:
```json
{
  "targets": [
    {
      "name": "Human-readable name",
      "url": "https://www.facebook.com/...",
      "type": "page|group|search"
    }
  ]
}
```

**Editing**: Via UI Configuration page or text editor

---

## Security Considerations

### API Keys

- Stored in `.env` (not committed to git)
- Never logged or displayed
- Used only for LLM API calls

### Browser Session

- Stored in `data/browser_profile/`
- Contains your Facebook login session
- Keep directory secure
- Delete to log out

### Database

- No sensitive data stored (public posts only)
- Screenshots may contain personal info from posts
- Export with caution

### No Auto-Posting

- Hardcoded safety: No automatic comment submission
- All posting requires manual action
- Clipboard copy only

---

## Extension Points

### Adding New LLM Providers

**Location**: `app/scoring.py` and `app/drafting.py`

**Steps**:
1. Add provider to `Config.get_llm_config()`
2. Implement `_score_with_{provider}()` method
3. Implement `_draft_with_{provider}()` method
4. Update `.env.example`

### Customizing Heuristics

**Location**: `app/scoring.py`

**Modify**:
- `SENSATIONAL_PHRASES`
- `LACK_OF_SOURCES`
- `CONSPIRACY_MARKERS`
- `_heuristic_score()` method

### Updating Facebook Selectors

**Location**: `app/collector.py`

**Modify**:
- `post_selectors` list in `_extract_posts()`
- Use browser DevTools to find new selectors

### Custom Draft Styles

**Location**: `app/drafting.py`

**Modify**:
- `_build_drafting_prompt()` for LLM mode
- `_generate_with_templates()` for mock mode

---

## Dependencies

### Core

- `streamlit` - Web UI framework
- `playwright` - Browser automation
- `python-dotenv` - Environment config

### Optional LLMs

- `openai` - OpenAI API client
- `anthropic` - Anthropic API client
- `requests` - For Ollama HTTP API

### Utilities

- `pyperclip` - Clipboard operations
- `Pillow` - Image handling (for screenshots)

### Built-in

- `sqlite3` - Database (Python standard library)
- `json`, `re`, `datetime`, `pathlib` - Standard library

---

## Testing Strategy

### Unit Testing (Not Implemented)

**Could add**:
- `tests/test_scoring.py` - Heuristic scoring tests
- `tests/test_drafting.py` - Template generation tests
- `tests/test_storage.py` - Database operations tests

### Integration Testing

**Manual**:
1. Run `test_setup.py` - Verify imports and structure
2. Test with mock LLM provider
3. Test collection with sample HTML file
4. Test UI navigation

### Production Testing

1. Start with 1-2 targets
2. Collect 5-10 posts
3. Review scoring accuracy
4. Generate drafts, review quality
5. Scale up gradually

---

## Deployment

### Windows

**Method 1**: Batch scripts (recommended)
- `SETUP.bat` - One-time setup
- `START_DASHBOARD.bat` - Launch UI

**Method 2**: Manual
- Create venv
- Install dependencies
- Run streamlit

### Other Platforms

**Linux / macOS**:
- Same Python code works
- Use shell scripts instead of `.bat`
- May need different pyperclip backend

**Docker** (could be added):
- Would need X11 forwarding for non-headless mode
- Browser profile persistence

---

## Maintenance

### Regular

- Update `data/targets.json` as interests change
- Archive old posts (export + delete)
- Update Python packages quarterly

### As Needed

- Fix Facebook selectors when they break
- Tune heuristics for your domain
- Adjust LLM prompts for better drafts

### Upgrades

- Python 3.12+ compatible (should work)
- Streamlit updates (test before upgrading)
- Playwright updates (minor version safe)

---

## License & Legal

**License**: MIT (or specify)

**Disclaimer**: Educational purposes only. Users responsible for:
- Platform TOS compliance
- Legal compliance in jurisdiction
- Ethical use
- Fact verification

**Not Liable For**:
- Account bans
- Legal issues
- Misuse of tool
- Factual errors in generated drafts

---

## Support & Community

**Documentation**:
- `README.md` - Setup and usage
- `QUICK_START.md` - Fast track guide
- `LIMITATIONS.md` - Known issues and best practices
- `PROJECT_SUMMARY.md` - This file

**Troubleshooting**:
- Run `test_setup.py`
- Check `.env` configuration
- Verify targets.json syntax
- Review error messages

**Contributing** (if open source):
- Submit issues for bugs
- Pull requests for improvements
- Share custom heuristics
- Report Facebook selector changes

---

## Future Roadmap

### Potential Features

**Not promised, just ideas**:
- [ ] Multi-platform support (Twitter, Reddit)
- [ ] OCR for image text
- [ ] Video transcript analysis
- [ ] Collaborative fact-checking (multi-user)
- [ ] Browser extension integration
- [ ] Mobile app version
- [ ] Automated fact-checking API integration
- [ ] Machine learning for personalized scoring

**Design Philosophy**:
- Keep it simple
- Maintain human-in-loop
- Prioritize ethics over features
- Stay under platform radar

---

**Built with care for responsible fact-checking. Use wisely.** 🔍
