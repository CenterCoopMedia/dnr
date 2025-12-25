---
name: dnr-source-management
description: Manage news source configuration for the DNR newsletter. Add new outlets, update domain mappings for source attribution, validate source names, and handle source-related issues like missing attribution.
allowed-tools: Read, Edit, Grep, Glob
---

# Source Management

You manage the news sources that feed into the DNR newsletter. This includes adding new outlets, mapping domains to display names, and ensuring proper source attribution.

## Source Configuration Locations

**RSS Feeds:** `config/rss_feeds.json`
- 75+ NJ news sources
- Organized by category (statewide, regional, hyperlocal)
- Fields: name, domain, rss_url, priority, coverage notes

**Domain Mapping:** `src/html_formatter.py` (domain_map dict)
- Maps URL domains to display names
- Used when source isn't provided in RSS
- ~49 outlets currently mapped

**Playwright Sources:** `src/playwright_fetcher.py`
- Sites requiring browser scraping
- USA Today network, TAPinto network

## Adding a New RSS Source

### Step 1: Gather Information
- Full outlet name
- Domain (e.g., hudsoncountyview.com)
- RSS feed URL (check /feed, /rss, /atom.xml)
- Coverage area (statewide, regional, hyperlocal)
- Priority (1=critical, 2=standard, 3=lower)

### Step 2: Add to rss_feeds.json
```json
{
  "name": "Hudson County View",
  "domain": "hudsoncountyview.com",
  "rss_url": "https://hudsoncountyview.com/feed/",
  "priority": 2,
  "notes": "Hudson County hyperlocal"
}
```

### Step 3: Add to domain_map
In `src/html_formatter.py`:
```python
domain_map = {
    ...
    "hudsoncountyview.com": "Hudson County View",
    ...
}
```

## Source Name Conventions

**Use canonical names:**
- "NJ.com" not "NJ Advance Media" or "nj.com"
- "NJ Spotlight News" not "NJ Spotlight" or "NJSN"
- "NorthJersey.com" not "Bergen Record" or "North Jersey"

**Handle variations:**
- www.nj.com → NJ.com
- mobile.nj.com → NJ.com
- amp.nj.com → NJ.com

**TAPinto network:**
- Use "TAPinto [Town]" format
- e.g., "TAPinto Montclair", "TAPinto Newark"

## Current Source Categories

### Primary Statewide (Priority 1)
- NJ.com, NJ Spotlight News, NJ Monitor, NJ Globe
- NJBIZ, ROI-NJ

### Regional Dailies (Priority 1-2)
- NorthJersey.com (Bergen Record)
- Asbury Park Press (APP)
- Press of Atlantic City
- Trentonian

### Hyperlocal (Priority 2)
- Montclair Local, Village Green, Baristanet
- Hudson Reporter, Jersey Digs
- Morristown Green, MercerMe
- TAPinto network (multiple towns)

### Specialty (Priority 2-3)
- NJ Arts, NJ Education Report
- InsiderNJ (politics)
- Echo News TV

### Public Media (Priority 2)
- WHYY, WNYC/Gothamist

## Output Format for Source Operations

```
SOURCE OPERATION: [Add / Update / Validate]

OUTLET: [Name]
Domain: [domain.com]
RSS Feed: [URL or "Not found"]
Current in config: [Yes/No]
Current in domain_map: [Yes/No]

CHANGES NEEDED:
1. [specific file and change]
2. [specific file and change]

VALIDATION:
- RSS feed accessible: [Yes/No]
- Returns stories: [N stories found]
- Domain resolves: [Yes/No]

Ready to apply? (y/n)
```

## Handling Missing Source Attribution

When stories appear without sources:

1. **Check RSS feed** - Does it include source in item?
2. **Check domain_map** - Is the domain mapped?
3. **Check URL format** - Subdomain or unusual path?

Stories without sources are **silently dropped** from the newsletter. This is intentional quality control but can hide issues.

## Source Validation

To validate a source:

```bash
# Check if RSS works
curl -s "RSS_URL" | head -20

# Check if domain maps correctly
grep "DOMAIN" src/html_formatter.py
```

## Common Source Issues

**Source shows as wrong name:**
- Check domain_map for typos
- Check if multiple domains for same outlet
- Update mapping

**Source missing from newsletter:**
- Check if domain is in domain_map
- Check if URL pattern is unusual
- Add domain mapping

**RSS returns no stories:**
- Feed may be broken
- Feed URL may have changed
- May need Playwright instead

## Priority Guidelines

**Priority 1 (Always fetch):**
- Major statewide outlets
- Breaking news sources
- High-volume, reliable feeds

**Priority 2 (Standard):**
- Regional dailies
- Established hyperlocals
- Specialty/beat outlets

**Priority 3 (Lower):**
- Newer outlets
- Inconsistent publishers
- Niche coverage areas
