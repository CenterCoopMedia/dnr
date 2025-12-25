---
name: dnr-source-management
description: Manage news source configuration for the DNR newsletter. Add new outlets, update domain mappings for source attribution, validate source names, and handle source-related issues like missing attribution.
allowed-tools: Read, Edit, Grep, Glob
---

# Source Management

## When to Activate

Activate this skill when:
- User wants to add a new news outlet
- Stories appear with wrong or missing source names
- Domain mapping needs updating
- New RSS feed discovered
- Source attribution failing for known outlet

## Core Concepts

**Two Configuration Points**:
1. **RSS feeds** (`config/rss_feeds.json`): Where to fetch stories
2. **Domain mapping** (`src/html_formatter.py`): How to display source names

Both must be updated when adding a new source.

**Source Name Conventions**:
- Use canonical names: "NJ.com" not "nj.com" or "NJ Advance Media"
- Be consistent: "NJ Spotlight News" not "NJ Spotlight" or "NJSN"
- Handle subdomains: www.nj.com, mobile.nj.com → all map to "NJ.com"
- TAPinto network: "TAPinto [Town]" format

**Priority Levels**:
| Priority | Description | Examples |
|----------|-------------|----------|
| 1 | Always fetch, critical | NJ.com, NJ Spotlight |
| 2 | Standard, reliable | Regional dailies, hyperlocals |
| 3 | Lower priority | Niche, inconsistent |

## Practical Guidance

### Adding a New Source

**Step 1: Gather Information**
```
Outlet name: [canonical name]
Domain: [primary domain]
RSS URL: [check /feed, /rss, /atom.xml]
Coverage: [statewide/regional/hyperlocal]
Priority: [1/2/3]
```

**Step 2: Add to rss_feeds.json**
```json
{
  "name": "Hudson County View",
  "domain": "hudsoncountyview.com",
  "rss_url": "https://hudsoncountyview.com/feed/",
  "priority": 2,
  "notes": "Hudson County hyperlocal"
}
```

**Step 3: Add to domain_map**
In `src/html_formatter.py`:
```python
domain_map = {
    ...
    "hudsoncountyview.com": "Hudson County View",
    ...
}
```

### Finding RSS Feeds

Common patterns to check:
- `/feed/`
- `/rss/`
- `/atom.xml`
- `/feed/rss/`
- `?feed=rss2`

Test with:
```bash
curl -s "https://outlet.com/feed/" | head -20
```

### Fixing Missing Attribution

If stories appear without sources:
1. Check if domain is in domain_map
2. Check for subdomain/path variations
3. Add mapping if missing

## Examples

**Input**: "Add Hudson County View as a source"

**Output**:
```
ADDING SOURCE: Hudson County View

DISCOVERY:
Domain: hudsoncountyview.com
RSS Feed: https://hudsoncountyview.com/feed/ ✓
Feed test: Returns 15 articles ✓

CONFIGURATION CHANGES:

1. config/rss_feeds.json (add to hyperlocal_hudson):
{
  "name": "Hudson County View",
  "domain": "hudsoncountyview.com",
  "rss_url": "https://hudsoncountyview.com/feed/",
  "priority": 2,
  "notes": "Hudson County hyperlocal"
}

2. src/html_formatter.py (add to domain_map):
"hudsoncountyview.com": "Hudson County View",

Apply changes? (y/n)
```

**Input**: "Stories from jerseydigs.com show as 'Unknown'"

**Output**:
```
SOURCE ATTRIBUTION FIX

Issue: jerseydigs.com not in domain_map

CHECKING:
- RSS config: ✓ Exists as "Jersey Digs"
- Domain map: ✗ MISSING

ROOT CAUSE: Domain mapping not added when RSS was configured

FIX: Add to src/html_formatter.py domain_map:
"jerseydigs.com": "Jersey Digs",

This will make all Jersey Digs stories display proper attribution.
```

## Guidelines

1. Always update BOTH rss_feeds.json AND domain_map
2. Test RSS feed before adding (verify it returns stories)
3. Use canonical outlet names consistently
4. Check for subdomain variations (www, mobile, amp)
5. Document coverage area in notes field

## Integration

- **dnr-feed-health**: New sources need health monitoring
- **dnr-airtable-triage**: Source detection uses domain_map
- **dnr-quality-audit**: Source diversity depends on coverage

## File References

- RSS config: `config/rss_feeds.json`
- Domain mapping: `src/html_formatter.py:extract_source_from_url()`
- Playwright sources: `src/playwright_fetcher.py:PLAYWRIGHT_SOURCES`

## Current Source Count

- RSS feeds configured: 75+
- Domain mappings: 49
- Playwright sources: 10 (USA Today network + TAPinto)
