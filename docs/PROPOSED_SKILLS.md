# Proposed Claude Skills for DNR Newsletter Automation

Based on a thorough codebase review, here are proposed skills designed following the 4 Core Truths:

1. **Expertise Transfer, Not Instructions** - Make Claude think like an editor, not follow steps
2. **Flow, Not Friction** - Produce output directly, not intermediate documents
3. **Voice Matches Domain** - Sound like a newsletter editor, not documentation
4. **Focused Beats Comprehensive** - Every section earns its place

---

## Skill 1: Story Deduplication & Grouping

### Problem Identified
Same story covered by multiple outlets appears 3-5 times in newsletter. Currently only URL-based deduplication exists. `main.py:136` has a TODO: "Implement smarter grouping of related stories."

### What This Skill Does
Identifies when multiple stories cover the same event and groups them into a single entry with multiple source citations. This is what experienced editors do manually - recognize "Governor Murphy announces transit funding" from NJ.com, NJ Spotlight, and NJ Monitor as one story.

### Trigger Phrases
- "Group duplicate stories"
- "Find stories covering the same event"
- "Consolidate multi-outlet coverage"
- "Which stories should be merged?"

### Expert Thinking Pattern
When seeing two headlines:
- "Murphy signs $2B transit bill" (NJ.com)
- "Governor approves major transit funding package" (NJ Spotlight)

An editor thinks: Same event, different framing. Keep NJ.com headline (more specific), cite both sources. This signals importance - multi-outlet = consider for top_stories.

### Output Format
```
GROUPED STORIES FOUND:

[1] Transit funding announcement (3 sources)
    Recommended headline: "Murphy signs $2B transit bill"
    Sources: NJ.com, NJ Spotlight News, NJ Monitor
    → Move to: top_stories (multi-outlet coverage)

[2] Montclair council meeting (2 sources)
    Recommended headline: "Montclair council approves downtown rezoning"
    Sources: Montclair Local, Baristanet
    → Keep in: housing
```

---

## Skill 2: RSS Feed Health Monitor

### Problem Identified
7 RSS feeds return `null`, TAPinto and USA Today network feeds often return 0 articles. No monitoring or alerting. Silent failures mean missing stories from major outlets.

### What This Skill Does
Diagnoses RSS feed health, identifies broken/underperforming feeds, suggests alternatives or fixes. Like a newsroom's tech person checking "why aren't we getting AP wire stories?"

### Trigger Phrases
- "Check RSS feed health"
- "Why is [outlet] returning no stories?"
- "Diagnose feed issues"
- "Which feeds are broken?"

### Expert Thinking Pattern
When a feed returns 0 articles:
1. Is the URL accessible? (network issue vs. dead feed)
2. Has the feed format changed? (RSS 2.0 vs Atom vs JSON Feed)
3. Is there a rate limit or paywall blocking us?
4. Is there an alternative feed URL?

### Output Format
```
FEED HEALTH REPORT:

BROKEN (0 stories, 7+ days):
- NJ Advance Media: Feed URL returns 404
  → Action: Check if they moved to njadvancemedia.com/rss

- TAPinto Montclair: Feed exists but empty
  → Action: Use Playwright scraper instead (already configured)

UNDERPERFORMING (<5 stories/week):
- Press of AC: Only returning 2 stories vs. usual 15
  → Possible: Paywall blocking, try adding ?outputType=amp

HEALTHY: 62/75 feeds returning expected story counts
```

---

## Skill 3: Editorial Feedback Processor

### Problem Identified
Current feedback loop (`workflow.py:278-388`) only searches first 15 stories per section, uses simple substring matching. User says "remove all crime stories" but system can only handle one at a time.

### What This Skill Does
Processes natural language editing instructions with full semantic understanding. Handles bulk operations, fuzzy matching, and editorial judgment calls.

### Trigger Phrases
- "Move the [topic] story to [section]"
- "Remove all [type] stories from [section]"
- "This doesn't belong in top stories"
- "Swap the order of..."

### Expert Thinking Pattern
When editor says "remove crime stories from top stories":
1. What counts as crime? (not just "murder" - also "arrested", "charged", "indicted")
2. Exception: Policy implications (AG investigation of systemic issue = keep)
3. Where do removed stories go? (skip vs. lastly vs. appropriate section)

### Output Format
```
PROCESSING: "Remove crime stories from top stories"

IDENTIFIED FOR REMOVAL (5 stories):
✓ "Man charged in Newark carjacking" → moved to skip
✓ "Three arrested in drug bust" → moved to skip
✓ "Fatal crash closes Route 80" → moved to skip
? "AG announces crackdown on wage theft" → KEPT (policy/enforcement story)
? "Police union contract dispute" → KEPT (labor/politics story)

KEPT 2 stories that mention police/crime but are policy-focused.
Want me to remove those too? (y/n)
```

---

## Skill 4: Classification Edge Case Handler

### Problem Identified
105 hardcoded exclusion keywords miss variants. "Hit by car" vs "struck by vehicle" vs "pedestrian killed" - all same concept, inconsistent filtering. Crime vs policy distinction is murky (corruption investigation = both).

### What This Skill Does
Handles classification edge cases where simple keywords fail. Applies editorial judgment about what really belongs in top_stories vs what's "if it bleeds, it leads."

### Trigger Phrases
- "Should this be in top stories?"
- "Is this crime or policy?"
- "Why was this classified as [section]?"
- "This feels miscategorized"

### Expert Thinking Pattern
For "AG charges 5 officials with corruption in public contract scheme":
- Contains: "charges" (crime keyword) + "officials" + "corruption" + "public contract"
- Crime angle: Yes, people are being charged
- Policy angle: Yes, systemic issue with public contracting
- Decision: TOP STORIES - this is accountability journalism, not crime blotter

For "Man shot during argument over parking spot":
- Contains: "shot" (crime keyword)
- Crime angle: Yes, violent crime
- Policy angle: None - isolated incident
- Decision: SKIP - this is crime blotter, not policy news

### Output Format
```
CLASSIFICATION ANALYSIS: "AG charges 5 officials with corruption"

Why it was classified as: top_stories (confidence: 0.8)

CRIME INDICATORS:
- "charges" - typically triggers crime filter
- "corruption" - criminal activity mentioned

POLICY INDICATORS:
- "officials" - government actors involved
- "public contract" - systemic/structural issue
- Multi-outlet coverage (3 sources)

RECOMMENDATION: KEEP in top_stories
This is accountability journalism about systemic government failure,
not a crime blotter item about individual criminal behavior.

The distinction: Crime blotter = "what happened to whom"
Policy news = "what this reveals about systems/institutions"
```

---

## Skill 5: Source Management

### Problem Identified
49 outlets in domain_map (`html_formatter.py`), but new outlets require code changes. Stories without recognized sources are silently dropped. No validation that source names match outlets.

### What This Skill Does
Manages source attribution: adds new outlets, validates source names, handles edge cases like source name variations.

### Trigger Phrases
- "Add [outlet] as a source"
- "Stories from [domain] aren't showing the right name"
- "Why is this story missing a source?"
- "Update source name for [outlet]"

### Expert Thinking Pattern
When adding a new source:
1. What's the canonical name? (The Record vs Bergen Record vs NorthJersey.com)
2. What domain(s) do they use? (app.com for Asbury Park Press)
3. Do they have RSS? Priority level?
4. Do they require Playwright scraping?

### Output Format
```
ADDING NEW SOURCE: Hudson County View

Domain detected: hudsoncountyview.com
Suggested display name: "Hudson County View"
RSS feed found: https://hudsoncountyview.com/feed/
Coverage area: Hudson County hyperlocal

CHANGES NEEDED:
1. Add to config/rss_feeds.json:
   {
     "name": "Hudson County View",
     "domain": "hudsoncountyview.com",
     "rss_url": "https://hudsoncountyview.com/feed/",
     "priority": 2
   }

2. Add to html_formatter.py domain_map:
   "hudsoncountyview.com": "Hudson County View"

Apply these changes? (y/n)
```

---

## Skill 6: Newsletter Quality Audit

### Problem Identified
No automated checking of newsletter balance, section distribution, or coverage gaps. Editor has to manually review everything.

### What This Skill Does
Audits a generated newsletter for quality issues: section imbalance, missing coverage areas, duplicate topics, stale stories.

### Trigger Phrases
- "Audit this newsletter"
- "Check newsletter quality"
- "Is this edition balanced?"
- "What's missing from today's newsletter?"

### Expert Thinking Pattern
A good newsletter has:
- Balance: No section overwhelming others (unless major news day)
- Coverage: Major ongoing stories represented
- Freshness: Nothing older than 36 hours (or 76 hours on Monday)
- Variety: Not 5 stories about same topic
- Sources: Mix of statewide and regional/local

### Output Format
```
NEWSLETTER QUALITY AUDIT - Dec 25, 2025

SECTION BALANCE:
top_stories: 5 ✓
politics: 12 ✓
housing: 3 ⚠️ (below typical 5-10)
education: 8 ✓
health: 4 ✓
environment: 2 ⚠️ (below typical 3-10)
lastly: 15 ✓

COVERAGE GAPS:
- No NJ Transit stories (usually 1-2/day)
- No offshore wind coverage (major ongoing story)
- Heavy on Essex County, light on South Jersey

POTENTIAL ISSUES:
- 3 stories about same Murphy announcement (consider grouping)
- 1 story from Oct 2025 (stale - check date parsing)

SOURCE DIVERSITY:
- 60% from statewide outlets ✓
- 25% from regional dailies ✓
- 15% from hyperlocal ⚠️ (usually 20-25%)

RECOMMENDATION: Add environment stories, check for South Jersey coverage
```

---

## Skill 7: Filter Rule Management

### Problem Identified
105 keywords in `TOP_STORIES_EXCLUSION_KEYWORDS` are hardcoded. Adding new patterns requires code changes. No way to test if a keyword would catch a story.

### What This Skill Does
Manages content filtering rules: adds keywords, tests patterns, identifies false positives/negatives.

### Trigger Phrases
- "Add [keyword] to exclusion list"
- "Would this headline be filtered?"
- "Why wasn't this filtered from top stories?"
- "Show me what the filters catch"

### Expert Thinking Pattern
When adding a filter:
1. What variations exist? ("crash" vs "crashed" vs "crashing")
2. Will it cause false positives? ("crash" catches "stock market crash")
3. Is it category-appropriate? (crime, sports, shopping, lottery, etc.)

### Output Format
```
FILTER ANALYSIS: "carjacking"

CURRENT STATUS: ✓ In exclusion list (crime category)

STORIES THIS WOULD CATCH TODAY:
1. "Man arrested in Newark carjacking" - ✓ correct filter
2. "Carjacking suspect leads police on chase" - ✓ correct filter

RELATED KEYWORDS TO CONSIDER:
- "car theft" - NOT in list, would catch 2 stories
- "vehicle theft" - NOT in list
- "auto theft" - NOT in list

RECOMMENDATION: Add "car theft", "vehicle theft", "auto theft" to crime category
These are essentially the same as "carjacking" but without the jacking.
```

---

## Skill 8: Airtable Submission Triage

### Problem Identified
Manual review of each Airtable submission is tedious (`workflow.py` Step 4). Each requires confirming source and selecting section interactively.

### What This Skill Does
Pre-triages Airtable submissions: auto-detects source from URL, suggests section based on headline, flags potential duplicates with RSS stories.

### Trigger Phrases
- "Triage Airtable submissions"
- "Review user submissions"
- "What submissions need attention?"

### Expert Thinking Pattern
For each submission:
1. Can we auto-detect source from URL? (most cases: yes)
2. Does headline suggest obvious section?
3. Is this a duplicate of an RSS story we already have?
4. Is this actually NJ news?

### Output Format
```
AIRTABLE SUBMISSION TRIAGE - 7 submissions

AUTO-APPROVED (high confidence):
✓ "Montclair council approves..."
  Source: Montclair Local (detected from URL)
  Section: housing (keyword: "approves" + "zoning")

✓ "Rutgers announces new dean"
  Source: Rutgers Today (detected)
  Section: education (keyword: "Rutgers")

NEEDS REVIEW (3):
? "Big news from Trenton" - Vague headline, can't auto-classify
? "Check out this story" - No headline, just URL
? URL returns 404 - May be broken link

DUPLICATES DETECTED (1):
! "Murphy signs transit bill" - Already in RSS from NJ.com
  Action: Skip (duplicate) or merge sources?

REJECTED (1):
✗ "Best pizza in NYC" - Not NJ news (NYC focus)
```

---

## Implementation Priority

Based on impact and effort:

| Skill | Impact | Effort | Priority |
|-------|--------|--------|----------|
| Story Deduplication | High | Medium | 1 |
| Newsletter Quality Audit | High | Low | 2 |
| Editorial Feedback Processor | High | Medium | 3 |
| Airtable Submission Triage | Medium | Low | 4 |
| Classification Edge Cases | Medium | Medium | 5 |
| RSS Feed Health Monitor | Medium | Low | 6 |
| Filter Rule Management | Low | Low | 7 |
| Source Management | Low | Low | 8 |

---

## Skill File Structure

Each skill should be created in `.claude/skills/` following this pattern:

```
.claude/skills/
├── dnr-automation/
│   └── SKILL.md (existing)
├── dnr-story-grouping/
│   └── SKILL.md
├── dnr-quality-audit/
│   └── SKILL.md
├── dnr-editorial-feedback/
│   └── SKILL.md
├── dnr-airtable-triage/
│   └── SKILL.md
├── dnr-classification/
│   └── SKILL.md
├── dnr-feed-health/
│   └── SKILL.md
├── dnr-filter-rules/
│   └── SKILL.md
└── dnr-source-management/
    └── SKILL.md
```
