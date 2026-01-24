# ⚠️ Limitations and Best Practices

## Technical Limitations

### Facebook Platform Changes

**Issue**: Facebook frequently updates its HTML structure and CSS classes.

**Impact**: Post selectors in `collector.py` may break, causing no posts to be collected.

**Mitigation**:
- Check `app/collector.py` for `post_selectors` list
- Use browser DevTools to inspect current Facebook structure
- Update selectors as needed
- The tool tries multiple selector strategies for robustness

### Dynamic Content Loading

**Issue**: Facebook uses infinite scroll and lazy loading.

**Impact**: Some posts may not be visible when collector runs.

**Mitigation**:
- Increase scroll passes (3-10)
- Increase scroll delay (2-5 seconds)
- Posts load as you scroll, so more passes = more posts
- Trade-off: Speed vs. completeness

### Login & Authentication Walls

**Issue**: Facebook may require login for certain content.

**Impact**: Can't collect posts from private groups or when logged out.

**Mitigation**:
- Use persistent browser profile (saves your login)
- First run: Manually log in when browser opens
- Subsequent runs: Automatically reuses session
- For private groups: You must be a member

### Rate Limiting & Detection

**Issue**: Facebook monitors for automated activity.

**Impact**: Account may be temporarily restricted if detected.

**Mitigation**:
- Use realistic scroll delays (2+ seconds)
- Limit collection volume (20-50 posts at a time)
- **NEVER** auto-post comments (this tool doesn't, by design)
- Spread collection over time (collect once per day, not every minute)
- Manual posting only maintains plausible deniability

### Screenshot Quality

**Issue**: Screenshots may not capture full post context (images, videos).

**Impact**: You see partial information in dashboard.

**Mitigation**:
- Always click "Open Post" to view full context
- Screenshots are for reference, not complete record
- Use "Needs Research" status for posts requiring deeper investigation

### Text Extraction Accuracy

**Issue**: Complex posts (images with text, videos) may have incomplete extraction.

**Impact**: Scoring may be inaccurate, drafts may miss context.

**Mitigation**:
- Review screenshots alongside text
- Edit generated drafts before posting
- Use "Needs Research" for unclear posts
- OCR is not implemented by default (can be added if needed)

## Scoring Limitations

### Heuristic-Based Scoring

**Issue**: Rule-based scoring can have false positives/negatives.

**Examples**:
- Satire posts may score high (lots of caps, sensational language)
- Subtle misinformation may score low (calm tone, appears factual)
- Context matters: "BREAKING NEWS" in journalism vs. conspiracy posts

**Mitigation**:
- Use score as triage tool, not final judgment
- Review all posts manually before responding
- LLM mode provides more nuanced analysis (if configured)
- Adjust thresholds based on your domain

### LLM Scoring (When Enabled)

**Issue**: LLMs can hallucinate or misinterpret context.

**Examples**:
- May flag legitimate news as misinformation
- May miss cultural or regional context
- Cost: API calls add up with high volume

**Mitigation**:
- Always fact-check LLM analysis
- Use mock mode for initial testing (free)
- Review "fact-check questions" for verification leads
- LLM is assistant, not oracle

### Score Calibration

**Issue**: Scores are relative, not absolute.

**Impact**: 70/100 in one domain ≠ 70/100 in another.

**Mitigation**:
- Calibrate based on your targets
- Track false positive/negative rates
- Adjust filters in dashboard over time
- Focus on high-confidence cases initially

## Workflow Limitations

### No Auto-Posting (By Design!)

**Limitation**: You must manually copy, paste, and post each rebuttal.

**Why**:
- Prevents accidental or unreviewed posts
- Maintains human judgment in the loop
- Reduces automation detection risk
- Ethical responsibility

**Not a bug, it's a feature!**

### Draft Generation Quality

**Issue**: Generated drafts may need editing.

**Examples**:
- May not match your exact voice
- May miss specific domain knowledge
- May be too harsh or too soft for context
- Template mode (mock) is generic

**Mitigation**:
- Always read and edit drafts before posting
- Use as starting point, not final product
- Develop personal templates for common cases
- LLM mode learns from prompt tuning (edit `drafting.py`)

### Fact-Checking Burden

**Issue**: Tool doesn't verify facts for you.

**Impact**: You must independently verify claims before rebutting.

**Mitigation**:
- Use "fact-check questions" as research starting points
- Consult fact-checking sites (Snopes, PolitiFact, etc.)
- Mark "Needs Research" and circle back
- Only post rebuttals you can personally defend

## Ethical & Legal Limitations

### Platform Terms of Service

**Issue**: Facebook prohibits automated posting.

**Impact**: Violating TOS can result in account ban.

**Compliance Strategy**:
- ✅ This tool does NOT auto-post
- ✅ Collection uses normal browser automation (gray area)
- ✅ All posting is manual (compliant)
- ⚠️ High-volume collection may still be flagged
- **Use conservative pacing and delays**

### Harassment & Coordinated Behavior

**Issue**: Platform policies prohibit harassment and coordinated inauthentic behavior.

**Impact**: Even manual posting can violate policies if done in coordination or targeting individuals.

**Boundaries**:
- ✅ Fact-checking public misinformation
- ✅ Correcting false claims with sources
- ✅ Educational responses
- ❌ Targeting individuals repeatedly
- ❌ Coordinating with others to mass-comment
- ❌ Personal attacks or doxxing

### Legal Considerations

**Varies by jurisdiction:**
- Libel/defamation: Be factually correct
- Impersonation: Don't pretend to be someone else
- Copyright: Don't copy-paste entire articles
- Privacy: Don't share personal information

**This tool is for educational fact-checking, not legal action.**

## Staying Within Normal User Workflows

### Realistic Pacing

**Normal User**:
- Visits 5-10 pages per hour
- Scrolls for 1-2 minutes per page
- Posts 1-5 comments per day

**This Tool (Safe Configuration)**:
- Collect from 5 targets max per run
- 3-5 scroll passes (simulates manual scrolling)
- 2-5 second delays between scrolls
- Post 5-10 comments per day (manually)

**Suspicious Configuration** (Avoid!):
- Collecting from 50 targets in 10 minutes
- 0.1 second scroll delays
- 100 posts collected per minute
- Posting 50 comments in an hour

### Detection Indicators

Facebook may flag you if:
- Too fast: Impossible human speed
- Too regular: Exact timing patterns (e.g., every 2.000 seconds)
- Too much: Volume exceeds human capacity
- Too perfect: No typos, instant responses

**How to stay under the radar**:
- Add randomness: Vary scroll delays (2-4 seconds, not exactly 2.0)
- Take breaks: Don't collect 24/7
- Manual posting: Adds natural variance
- Quality over quantity: 10 good rebuttals > 100 spam comments

### Multi-Account Coordination (Don't!)

**Prohibited**: Creating multiple accounts to amplify messages.

**Allowed**: Using one personal account for fact-checking.

**This tool assumes single-account, single-user operation.**

## Performance & Scalability

### Database Size

**Issue**: SQLite database grows with posts.

**Impact**: Performance degrades with 10,000+ posts.

**Mitigation**:
- Archive old posts (export to CSV, delete from DB)
- Run `VACUUM` on SQLite database periodically
- Focus on active monitoring, not long-term storage

### Screenshot Storage

**Issue**: Screenshots consume disk space.

**Impact**: 1000 posts × 500KB = 500MB.

**Mitigation**:
- Periodically delete old screenshots
- Use lower resolution if needed (edit `collector.py`)
- Mark posts "Done" and batch-delete with screenshots

### Browser Memory

**Issue**: Playwright browsers use RAM.

**Impact**: May slow down on low-end machines.

**Mitigation**:
- Close browser between runs
- Use headless mode (less RAM)
- Process fewer targets per run

## Future Considerations

### Potential Improvements

**Not currently implemented** (could be added):
- OCR for text in images
- Video content analysis
- Multi-platform support (Twitter, Reddit)
- Automated fact-checking API integration
- Machine learning for custom scoring
- Collaborative fact-checking (multi-user)

**Trade-offs**:
- More features = more complexity
- More automation = more detection risk
- More accuracy = more API costs

### Maintenance Requirements

**Expect to maintain**:
- Selectors when Facebook updates (monthly?)
- LLM prompts for better drafts (as needed)
- Target list (add/remove as interests change)
- Dependencies (update Python packages quarterly)

## Summary

**This tool is designed for:**
- ✅ Individual fact-checkers scaling their workflow
- ✅ Educational and research purposes
- ✅ Human-supervised automation
- ✅ Transparent, ethical use

**This tool is NOT designed for:**
- ❌ Mass automation campaigns
- ❌ Bypassing platform protections
- ❌ Harassment or coordinated attacks
- ❌ Replacing human judgment

**Use responsibly. Verify facts. Post manually. Respect platform rules.**

---

*Last Updated: 2024*
