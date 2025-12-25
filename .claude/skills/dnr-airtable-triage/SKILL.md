---
name: dnr-airtable-triage
description: Pre-triage Airtable user submissions for the DNR newsletter. Auto-detect sources from URLs, suggest sections based on headlines, flag potential duplicates with RSS stories, and identify submissions that need manual review.
allowed-tools: Read, Grep, Bash
---

# Airtable Submission Triage

You are pre-processing user submissions from the Airtable form before the editor reviews them. Your job is to auto-categorize what you can, flag duplicates, and identify submissions needing human attention.

## Submission Fields

Each Airtable submission contains:
- **Headline**: User-provided story title
- **URL**: Link to the article
- **Source**: Sometimes provided, often needs detection
- **Section**: Sometimes pre-selected by user
- **Name**: Submitter name
- **Email**: Submitter email
- **Date added**: When submitted

## Auto-Detection Logic

### Source Detection from URL

Extract source from URL domain. Common mappings:

```
nj.com → NJ.com
njspotlightnews.org → NJ Spotlight News
newjerseymonitor.com → NJ Monitor
newjerseyglobe.com → NJ Globe
northjersey.com → NorthJersey.com
app.com → Asbury Park Press
pressofatlanticcity.com → Press of Atlantic City
montclairlocal.news → Montclair Local
villagegreennj.com → Village Green
tapinto.net → TAPinto [+ town name if in URL]
hudsonreporter.com → Hudson Reporter
jerseydigs.com → Jersey Digs
njbiz.com → NJBIZ
roi-nj.com → ROI-NJ
whyy.org → WHYY
gothamist.com → Gothamist
```

### Section Detection from Headline

Use keyword matching to suggest sections:

**politics**: legislature, senator, assembly, governor, Murphy, election, vote, bill, law, court, ruling, judge, mayor, council, commissioner

**housing**: housing, affordable, rent, zoning, development, apartment, condo, real estate, eviction, tenant, landlord, Blue Acres

**education**: school, student, teacher, Rutgers, Montclair State, university, college, education, curriculum, board of ed

**health**: hospital, healthcare, health, medical, nurse, doctor, COVID, vaccine, mental health, Medicaid

**environment**: offshore wind, solar, climate, PFAS, pollution, DEP, environmental, clean energy, flood, storm

**lastly**: restaurant, arts, music, sports, Devils, Giants, Jets, concert, festival, museum, tourism

**top_stories**: Only if multi-outlet coverage detected or major policy announcement

### Duplicate Detection

Check if submission URL or similar headline exists in today's RSS stories:
- Exact URL match → Definite duplicate
- Same headline from same source → Duplicate
- Similar headline from different source → Potential grouping opportunity

## Triage Categories

### AUTO-APPROVED
- Source confidently detected from URL
- Section clearly indicated by headline keywords
- URL is accessible and valid
- Not a duplicate of RSS content

### NEEDS REVIEW
- Source unclear or from unknown domain
- Headline too vague to categorize
- User-provided section seems wrong for content
- URL returns error or paywall

### DUPLICATE
- Same URL already in RSS feed
- Same story from same source

### REJECTED
- Not NJ news (NYC, PA, national without NJ angle)
- Promotional/spam content
- Broken URL (404, domain expired)
- Too old (outside lookback window)

## Output Format

```
AIRTABLE SUBMISSION TRIAGE - [Date]
[N] submissions to review

AUTO-APPROVED ([N]):
[1] "[Headline]"
    Source: [Detected source] (from URL)
    Section: [Suggested section] (keywords: X, Y)
    Submitted by: [Name]

[2] "[Headline]"
    ...

NEEDS REVIEW ([N]):
[1] "[Headline]"
    Issue: [Why it needs review]
    URL: [URL]
    Submitted by: [Name]

DUPLICATES DETECTED ([N]):
[1] "[Headline]"
    Already in: [Source via RSS]
    Action: Skip or merge sources?

REJECTED ([N]):
[1] "[Headline]"
    Reason: [Why rejected]

SUMMARY:
- [N] ready to auto-approve
- [N] need manual review
- [N] duplicates to handle
- [N] rejected
```

## Checking for Duplicates

To compare against RSS stories, read the current day's output or run a quick check:

```bash
# Check if URL exists in today's stories
grep -r "URL_DOMAIN" drafts/dnr-*.html
```

Or search the RSS fetcher output if available.

## When Approval Triggers Automation

In Airtable, when BOTH Source AND Section fields are populated:
- An automation triggers
- Sends email to submitter: "Your story was approved for the next edition"

So only approve (fill both fields) for stories that will actually appear in the newsletter.
