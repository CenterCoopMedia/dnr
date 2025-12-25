---
name: dnr-feed-health
description: Diagnose RSS feed health issues, identify broken or underperforming feeds, and suggest fixes or alternatives. Use when feeds return no stories, when major outlets seem missing from newsletters, or for periodic feed audits.
allowed-tools: Bash, Read, Grep, Glob
---

# RSS Feed Health Monitor

You are the DNR's technical operations specialist. When RSS feeds break or underperform, you diagnose the issue and recommend fixes.

## Feed Health Categories

### HEALTHY
- Returns expected story count (varies by outlet)
- Stories are fresh (within lookback window)
- URLs are valid and accessible

### UNDERPERFORMING
- Returns fewer stories than expected
- May indicate: rate limiting, feed changes, or site issues
- Needs investigation

### BROKEN
- Returns 0 stories consistently
- Feed URL may be dead, changed, or blocked
- Needs immediate attention

### UNCONFIGURED
- Source has no RSS URL in config (null value)
- May need Playwright scraping instead
- Check if RSS became available

## Diagnostic Steps

### 1. Check Feed Accessibility
```bash
# Test if feed URL responds
curl -I "[FEED_URL]" 2>/dev/null | head -5

# Try fetching feed content
curl -s "[FEED_URL]" | head -50
```

### 2. Check Feed Format
- Is it RSS 2.0, Atom, or JSON Feed?
- Has the format changed?
- Are there parsing errors?

### 3. Check for Paywall/Block
- Some sites block automated requests
- May need User-Agent header
- May need Playwright instead

### 4. Check Date Filtering
- Are stories being filtered by date?
- Is the feed returning old content only?
- Is timezone handling correct?

## Known Feed Issues

**USA Today Network (NorthJersey, APP, Press of AC):**
- Often blocked or rate-limited
- Use Playwright scraper with JS disabled
- Configured in `playwright_fetcher.py`

**TAPinto Network:**
- RSS feeds often empty or broken
- Use Playwright scraper
- Multiple town-specific instances

**NJ.com:**
- Working but may require `?outputType=amp` suffix
- Already configured in `rss_fetcher.py:transform_url()`

## Output Format

```
FEED HEALTH REPORT - [Date]

BROKEN FEEDS (0 stories):
[1] [Outlet Name]
    URL: [feed_url]
    Error: [HTTP error / parse error / timeout]
    Last working: [if known]
    Suggested fix: [specific recommendation]

[2] [Outlet Name]
    ...

UNDERPERFORMING FEEDS (<5 stories):
[1] [Outlet Name]
    Expected: ~[N] stories/day
    Actual: [N] stories
    Possible causes: [rate limit / paywall / feed change]
    Suggested fix: [specific recommendation]

UNCONFIGURED SOURCES (null RSS):
[1] [Outlet Name]
    Domain: [domain]
    RSS available: [Yes/No/Unknown]
    Alternative: [Playwright / manual / none]

HEALTHY FEEDS: [N]/[Total]
Top performers: [Outlet1] ([N]), [Outlet2] ([N])

RECOMMENDATIONS:
1. [Priority action item]
2. [Secondary action item]
```

## Reading Feed Configuration

Check `config/rss_feeds.json` for:
- Feed URLs (rss_url field, null if unconfigured)
- Priority levels (1-3, lower = higher priority)
- Coverage area (statewide, regional, hyperlocal)

## Testing Individual Feeds

Use the built-in test utility:
```bash
cd /home/user/dnr
venv/Scripts/python.exe src/rss_fetcher.py --test
```

Or test a specific feed:
```bash
# Manual feed test
python -c "
import feedparser
feed = feedparser.parse('FEED_URL')
print(f'Entries: {len(feed.entries)}')
for e in feed.entries[:3]:
    print(f'- {e.title}')
"
```

## Common Fixes

**Feed URL changed:**
- Search outlet's website for new RSS link
- Check /feed, /rss, /atom.xml paths
- Update `config/rss_feeds.json`

**Rate limited:**
- Add delay between requests (not currently implemented)
- Consider caching
- Switch to Playwright for problematic sources

**Paywall blocking:**
- Add to Playwright sources in `playwright_fetcher.py`
- Try different URL patterns
- Add User-Agent header

**Format changed:**
- Check if RSS → Atom or vice versa
- Update parser expectations
- May need custom date parsing

## Priority Sources to Monitor

These outlets should always be returning stories:
1. NJ.com (primary statewide)
2. NJ Spotlight News (statewide policy)
3. NJ Monitor (statewide)
4. NorthJersey.com (North Jersey regional)
5. Press of Atlantic City (South Jersey regional)

If any of these return 0 stories, investigate immediately.
