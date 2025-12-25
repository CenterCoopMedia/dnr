---
name: dnr-filter-rules
description: Manage content filtering rules for the DNR newsletter. Add or update exclusion keywords, test if headlines would be filtered, identify false positives/negatives, and understand current filter behavior.
allowed-tools: Read, Grep, Edit
---

# Filter Rule Management

## When to Activate

Activate this skill when:
- User wants to add/modify filter keywords
- Story slipped through that should have been filtered
- Story was incorrectly filtered (false positive)
- User asks "why was this filtered?" or "would this be filtered?"
- Reviewing filter effectiveness

## Core Concepts

**Filter Architecture**: Two-stage filtering
1. **Pre-classification** (rss_fetcher.py): Generic broadcasts skipped entirely
2. **Post-classification** (classifier.py): Crime/crash removed from top_stories only

**Keyword Categories** (105 total in TOP_STORIES_EXCLUSION_KEYWORDS):
| Category | Count | Examples |
|----------|-------|----------|
| Crime | ~35 | murder, carjacking, robbery, assault |
| Crashes | ~22 | fatal crash, pedestrian struck, pileup |
| Sports | ~22 | varsity, state championship, player of week |
| Shopping | ~13 | gift guide, black friday, deals |
| Lottery | ~10 | powerball, winning numbers, jackpot |
| Restaurant | ~16 | best pizza, restaurant review, food critic |
| Homes | ~18 | mansion sold, luxury home, million-dollar |

**Match Behavior**: Case-insensitive substring match
- "crash" matches "crashed", "crashing", "car crash"
- Careful: "fire" matches "fired" (different meaning)

## Practical Guidance

### Testing a Headline

```python
from src.classifier import is_crime_or_crash_headline

headline = "Test headline here"
filtered = is_crime_or_crash_headline(headline)
print(f"Would be filtered: {filtered}")
```

### Adding a Keyword

Consider before adding:
1. **Variants**: Does it have plural/tense forms that need separate entries?
2. **False positives**: Will it incorrectly match other stories?
3. **Category**: Which filter category does it belong to?

Example:
```python
# Adding "vehicle theft" to crime category
TOP_STORIES_EXCLUSION_KEYWORDS = [
    # Crime
    "carjacked", "carjacking", "murder", ...
    "vehicle theft",  # NEW - catches car theft stories
    ...
]
```

### Identifying Gaps

Look for patterns in stories that slip through:
- Different phrasing: "hit by car" vs "pedestrian struck"
- Synonyms: "car theft" vs "carjacking"
- Compound phrases: "multiple fatalities"

## Examples

**Input**: "Would this headline be filtered: 'Two killed in wrong-way crash on Parkway'"

**Output**:
```
FILTER TEST

Headline: "Two killed in wrong-way crash on Parkway"

MATCH FOUND: "wrong-way" → crashes category
MATCH FOUND: "crash" → crashes category
MATCH FOUND: "killed" → crime category

Result: YES, would be filtered from top_stories

Current behavior: Correct - this is a traffic incident,
not policy news. Would be moved to skip section.
```

**Input**: "This crime story slipped through: 'Teen arrested after armed robbery at mall'"

**Output**:
```
FILTER GAP ANALYSIS

Headline: "Teen arrested after armed robbery at mall"

MATCHED KEYWORDS:
- "arrested" → NOT in list (gap!)
- "armed robbery" → IN list ✓
- "robbery" → IN list ✓

Wait - this SHOULD have been caught by "robbery" and "armed robbery".

INVESTIGATION:
Let me check the actual filter...

Possible issues:
1. Case sensitivity problem?
2. Filter not running on this story?
3. Story pre-classified from Airtable (bypasses filter)?

ACTION: Verify story source and classification path
```

**Input**: "Add 'vehicle theft' to the filter"

**Output**:
```
ADDING KEYWORD: "vehicle theft"

Category: Crime (alongside carjacking, robbery, etc.)

IMPACT ANALYSIS:
Would now catch headlines like:
- "Police investigate vehicle theft ring"
- "Vehicle theft up 20% in Newark"

FALSE POSITIVE RISK: Low
- "vehicle" alone is neutral
- "theft" scoped to crime context

RELATED KEYWORDS TO CONSIDER:
- "car theft" - NOT currently in list
- "auto theft" - NOT currently in list
- "stolen vehicle" - NOT currently in list

RECOMMENDATION: Add all four variants:
- "vehicle theft"
- "car theft"
- "auto theft"
- "stolen vehicle"

Add to src/classifier.py TOP_STORIES_EXCLUSION_KEYWORDS
in the Crime section.
```

## Guidelines

1. Always test keyword impact before adding
2. Consider related variants to add together
3. Check for false positive risk with common words
4. Document why keyword was added (future reference)
5. Group keywords by category in the code

## Integration

- **dnr-classification**: Filter runs after classification
- **dnr-editorial-feedback**: Manual removes may suggest filter gaps
- **dnr-quality-audit**: Repeated issues indicate filter problems

## File References

- Exclusion keywords: `src/classifier.py:TOP_STORIES_EXCLUSION_KEYWORDS`
- Filter function: `src/classifier.py:is_crime_or_crash_headline()`
- Broadcast patterns: `src/rss_fetcher.py:SKIP_HEADLINE_PATTERNS`
