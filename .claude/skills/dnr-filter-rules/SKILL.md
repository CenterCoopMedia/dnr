---
name: dnr-filter-rules
description: Manage content filtering rules for the DNR newsletter. Add or update exclusion keywords, test if headlines would be filtered, identify false positives/negatives, and understand current filter behavior.
allowed-tools: Read, Grep, Edit
---

# Filter Rule Management

You manage the content filtering rules that keep crime blotter, sports scores, lottery results, and other non-policy content out of top_stories.

## Current Filter Architecture

**Location:** `src/classifier.py`

**Keyword Lists:**
- `TOP_STORIES_EXCLUSION_KEYWORDS` - 105 keywords across categories
- `SKIP_HEADLINE_PATTERNS` (in rss_fetcher.py) - Generic broadcast patterns
- `NJ_KEYWORDS` - Positive NJ relevance signals
- `SKIP_KEYWORDS` - Non-NJ signals (NYC boroughs, other states)

## Filter Categories

### Crime (20+ keywords)
Filters out crime blotter items:
- carjacked, carjacking, murder, murdered, homicide
- stabbing, stabbed, shooting, shot, assault
- robbery, armed robbery, burglary, theft
- drug bust, drug arrest, overdose

### Crashes/Accidents (20+ keywords)
Filters out traffic incidents:
- crash, fatal crash, deadly crash
- pedestrian struck, pedestrian killed
- wrong-way driver, multi-vehicle, pileup

### High School Sports (20+ keywords)
Filters out prep sports:
- high school football/basketball/soccer/etc.
- varsity, state championship
- player of the week, athlete of the week

### Shopping/Deals (10+ keywords)
Filters out gift guides and deals:
- gift guide, gift ideas, holiday gifts
- black friday, cyber monday, deals, discount

### Lottery (8+ keywords)
Filters out lottery coverage:
- lottery, powerball, mega millions
- winning numbers, jackpot winner

### Restaurant/Food (15+ keywords)
Filters out food reviews:
- restaurant review, best pizza, best bagels
- food critic, we tried, taste test

### Expensive Homes (10+ keywords)
Filters out real estate porn:
- mansion sold, million-dollar home
- most expensive, luxury home

## Testing Filter Behavior

To test if a headline would be filtered:

```python
from src.classifier import is_crime_or_crash_headline

headline = "Man arrested in Newark carjacking"
would_filter = is_crime_or_crash_headline(headline)
print(f"Would filter: {would_filter}")
```

## Output Format for Filter Analysis

```
FILTER ANALYSIS: "[keyword or headline]"

CURRENT STATUS: [In list / Not in list]
Category: [crime / crashes / sports / shopping / lottery / restaurant / homes]

MATCHES IN RECENT STORIES:
[1] "[Headline that would match]" - [correct/false positive]
[2] "[Headline that would match]" - [correct/false positive]

RELATED KEYWORDS TO CONSIDER:
- [variant1] - [in list / not in list]
- [variant2] - [in list / not in list]

FALSE POSITIVE RISK:
[Low/Medium/High] - [Explanation]
Example false positive: "[headline that would incorrectly match]"

RECOMMENDATION: [Add / Don't add / Remove / Modify]
```

## Adding New Keywords

When adding a keyword, consider:

1. **Variants**: Does it have plural/past tense forms?
   - "crash" catches "crashed", "crashing" (substring match)
   - But "fire" doesn't catch "fired" (different meaning)

2. **False positives**: Will it catch things it shouldn't?
   - "shot" catches "gunshot" but also "screenshot"
   - "fire" catches "house fire" but also "Murphy fires back"

3. **Coverage**: Are there related terms missing?
   - If adding "carjacking", also consider "car theft", "vehicle theft"

4. **Category**: Which filter category does it belong to?
   - Crime, crashes, sports, shopping, lottery, restaurant, homes

## Modifying Filter Rules

To add a keyword, edit `src/classifier.py`:

```python
TOP_STORIES_EXCLUSION_KEYWORDS = [
    # Crime
    "carjacked", "carjacking", "murder", ...
    "NEW_KEYWORD_HERE",  # Add to appropriate category
    ...
]
```

## Current Keyword Count by Category

As of last analysis:
- Crime: ~35 keywords
- Crashes/Accidents: ~22 keywords
- Sports: ~22 keywords
- Shopping/Deals: ~13 keywords
- Lottery: ~10 keywords
- Restaurant/Food: ~16 keywords
- Expensive Homes: ~18 keywords

**Total: ~105 keywords**

## Known Gaps

Based on stories that slip through:

1. **Vehicle theft variants**: "car theft", "vehicle stolen" - not in list
2. **Violence variants**: "hit by car", "struck by vehicle" - only "pedestrian struck"
3. **Sports variants**: "final score", "box score" - may be missing
4. **Food variants**: "best [food item]" patterns incomplete

## Generic Broadcast Patterns

Separate from keyword filters, these patterns skip entire stories at RSS level:

Located in `src/rss_fetcher.py` as `SKIP_HEADLINE_PATTERNS`:
- "newscast for"
- "morning edition", "evening edition"
- "news roundup for"
- "weather forecast for"
- "podcast:", "listen:", "watch:"
- "nj spotlight news:", "whyy news:"

These are substring matches applied to headlines before classification.
