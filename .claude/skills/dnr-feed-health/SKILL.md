---
name: dnr-feed-health
description: Diagnose RSS feed health issues, identify broken or underperforming feeds, and suggest fixes or alternatives. Use when feeds return no stories, when major outlets seem missing from newsletters, or for periodic feed audits.
allowed-tools: Bash, Read, Grep, Glob
---

# RSS Feed Health Monitor

## When to Activate

Activate this skill when:
- User asks about feed health or broken feeds
- Major outlet missing from newsletter
- Feed returns 0 stories unexpectedly
- Coverage gaps suggest feed issues
- Periodic audit requested

## Core Concepts

**Feed Categories**:
| Status | Definition | Action |
|--------|------------|--------|
| Healthy | Returns expected story count | Monitor |
| Underperforming | Returns < expected | Investigate |
| Broken | Returns 0 consistently | Fix urgently |
| Unconfigured | Has null RSS URL | Use Playwright or find feed |

**Priority Feeds** (must always work):
1. NJ.com - primary statewide
2. NJ Spotlight News - policy focus
3. NJ Monitor - statewide
4. NorthJersey.com - North Jersey regional
5. Press of Atlantic City - South Jersey

**Known Problem Patterns**:
- USA Today Network (NorthJersey, APP, Press of AC): Often blocked, use Playwright
- TAPinto Network: RSS unreliable, use Playwright
- NJ.com: Add `?outputType=amp` to bypass paywall

## Practical Guidance

### Diagnostic Commands

**Test single feed**:
```bash
curl -s "FEED_URL" | head -20
```

**Test all feeds**:
```bash
cd /home/user/dnr
venv/Scripts/python.exe src/rss_fetcher.py --test
```

**Check feed format**:
```python
import feedparser
feed = feedparser.parse('FEED_URL')
print(f'Entries: {len(feed.entries)}')
print(f'Status: {feed.status}')
```

### Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Feed URL changed | 404 error | Find new URL, update config |
| Rate limited | Intermittent failures | Add delay or use Playwright |
| Paywall blocking | Empty feed | Add Playwright source |
| Format changed | Parse errors | Check RSS vs Atom format |
| Site redesign | Selectors fail (Playwright) | Update CSS selectors |

### Feed Configuration

Located in `config/rss_feeds.json`:
```json
{
  "name": "Outlet Name",
  "domain": "outlet.com",
  "rss_url": "https://outlet.com/feed/",
  "priority": 2,
  "notes": "Optional notes"
}
```

## Examples

**Input**: "Why are we missing NorthJersey stories?"

**Output**:
```
FEED DIAGNOSIS: NorthJersey.com

Status: BLOCKED (0 stories returned)
URL: https://www.northjersey.com/arcio/rss/

Test result:
- HTTP Status: 403 Forbidden
- User-Agent blocking detected

ROOT CAUSE: USA Today Network blocks automated requests

SOLUTION:
NorthJersey.com is already configured in Playwright sources.
Verify Playwright is enabled: run with --playwright flag

Alternative: Check if they have public RSS at /feeds or /rss
```

**Input**: "Run feed health check"

**Output**:
```
FEED HEALTH REPORT - Dec 25, 2025

BROKEN (0 stories, need attention):
- TAPinto Montclair: Feed empty
  → Use Playwright scraper (already configured)

- NJ Advance Media: Feed URL 404
  → Check for new feed location

UNDERPERFORMING (<5 stories when expect 10+):
- Press of AC: Only 2 stories
  → May be rate limited, verify with manual test

UNCONFIGURED (null RSS URL):
- Newark News Today
- Jersey City Times
- NJ PBS
→ These rely on Playwright or need RSS discovery

HEALTHY: 62/75 feeds returning normal counts

TOP PERFORMERS:
- NJ.com: 45 stories
- NJ Spotlight: 28 stories
- NJ Monitor: 22 stories

RECOMMENDATION: Run with --playwright for full coverage
```

## Guidelines

1. Test systematically before concluding feed is broken
2. Distinguish network errors from feed format issues
3. Check if Playwright backup exists before panicking
4. Document fixes in feed config notes
5. Priority 1 feeds need immediate attention

## Integration

- **dnr-quality-audit**: Coverage gaps may indicate feed issues
- **dnr-source-management**: Broken feeds may need config updates
- **dnr-automation**: Feed health affects pipeline reliability

## File References

- Feed config: `config/rss_feeds.json`
- RSS fetcher: `src/rss_fetcher.py`
- Playwright sources: `src/playwright_fetcher.py`
- Test utility: `rss_fetcher.py --test`
