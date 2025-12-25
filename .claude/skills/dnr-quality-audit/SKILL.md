---
name: dnr-quality-audit
description: Audit a DNR newsletter for quality issues including section imbalance, coverage gaps, duplicate topics, source diversity, and stale stories. Use before sending a newsletter to catch issues, when a newsletter feels "off", or to understand why certain sections are over/under-populated.
allowed-tools: Read, Grep, Glob, Bash
---

# Newsletter Quality Audit

You are an experienced newsletter editor checking today's edition before it goes out to 3,000 subscribers. Your job is to catch issues that would make the NJ News Commons look bad or fail to serve readers.

## What Makes a Good DNR Edition

**Section Balance:**
- top_stories: 3-6 stories (never more than 6)
- politics: 5-15 stories (often the largest section)
- housing: 3-10 stories
- education: 3-10 stories
- health: 3-10 stories
- environment: 3-10 stories
- lastly: 5-20 stories (catch-all for lighter news)

**Coverage Diversity:**
- Mix of statewide outlets (NJ.com, NJ Spotlight, NJ Monitor)
- Regional representation (North, Central, South Jersey)
- Hyperlocal perspectives when relevant
- Not dominated by any single outlet

**Freshness:**
- Monday: Stories from Friday 5am onwards (76 hours)
- Tue-Thu: Stories from past 36 hours
- Nothing older than lookback window

**Topic Variety:**
- Not 5 stories about the same narrow topic
- Major ongoing stories represented (NJ Transit, offshore wind, etc.)
- Breaking news included if significant

## Quality Checks to Perform

### 1. Section Balance Check
Read the HTML preview and count stories per section. Flag:
- Any section with 0 stories
- Sections significantly below typical range
- Sections exceeding maximum (especially top_stories > 6)

### 2. Coverage Gap Check
Look for missing coverage of:
- NJ Transit (almost always newsworthy)
- State legislature (if in session)
- Offshore wind (major ongoing story)
- Housing/affordability (constant issue)
- Major breaking news you're aware of

### 3. Source Diversity Check
Count stories per outlet. Flag:
- More than 40% from any single outlet
- Zero hyperlocal stories
- Missing major outlets (NJ.com, NJ Spotlight should usually appear)

### 4. Duplicate Topic Check
Look for multiple stories on same narrow topic that should be grouped:
- Same announcement covered multiple times
- Same incident without policy angle repeated
- Same topic dominating a section

### 5. Geographic Balance Check
Note the geographic distribution:
- Heavy North Jersey, light South Jersey (common issue)
- Missing county regions entirely
- All statewide, no local perspectives

### 6. Freshness Check
If visible, check publication dates:
- Stories older than lookback window
- Evergreen content mixed with breaking news

## Output Format

```
NEWSLETTER QUALITY AUDIT - [Date]

SECTION BALANCE:
top_stories: N [check/warning]
politics: N [check/warning]
housing: N [check/warning]
education: N [check/warning]
health: N [check/warning]
environment: N [check/warning]
lastly: N [check/warning]

COVERAGE GAPS:
- [Missing topic/area 1]
- [Missing topic/area 2]

POTENTIAL ISSUES:
- [Issue description]
- [Issue description]

SOURCE DIVERSITY:
- Top sources: [Outlet] (N%), [Outlet] (N%)
- Hyperlocal representation: [percentage]
- [Any concerns]

GEOGRAPHIC BALANCE:
- [Assessment]

RECOMMENDATIONS:
1. [Specific actionable recommendation]
2. [Specific actionable recommendation]

OVERALL ASSESSMENT: [Ready to send / Needs attention / Major issues]
```

## Reading Newsletter Data

Check these files:
- `drafts/dnr-YYYY-MM-DD.html` - Generated preview
- `history/dnr-template.html` - Template structure

Count stories by looking for `<li>` tags within each section's content area.

Section markers in HTML:
- `<!-- TOP STORIES -->`
- `<!-- POLITICS STORIES -->`
- `<!-- HOUSING STORIES -->`
- etc.
