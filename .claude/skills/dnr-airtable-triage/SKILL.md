---
name: dnr-airtable-triage
description: Pre-triage Airtable user submissions for the DNR newsletter. Auto-detect sources from URLs, suggest sections based on headlines, flag potential duplicates with RSS stories, and identify submissions that need manual review.
allowed-tools: Read, Grep, Bash
---

# Airtable Submission Triage

## When to Activate

Activate this skill when:
- User mentions "Airtable submissions" or "user submissions"
- Workflow Step 4 (review Airtable submissions) is reached
- User asks to "triage" or "pre-process" submissions
- Many submissions need review and user wants to speed up process
- Checking if submitted stories duplicate RSS content

## Core Concepts

**Approval Trigger**: In Airtable, when BOTH `Source` AND `Section` fields are populated, an automation sends email to submitter: "Your story was approved for the next edition." Only approve stories that will actually appear.

**Auto-Detection Hierarchy**:
1. **Source**: Extract from URL domain (most reliable)
2. **Section**: Infer from headline keywords (moderate reliability)
3. **Duplicates**: Compare against today's RSS stories

**Triage Categories**:
| Category | Criteria | Action |
|----------|----------|--------|
| Auto-approve | Source + section confident | Apply both fields |
| Needs review | Source OR section unclear | Present for decision |
| Duplicate | Same story in RSS | Skip or merge sources |
| Reject | Not NJ news, broken URL | Don't approve |

## Practical Guidance

### Source Detection

Map URL domains to display names:
```
nj.com → NJ.com
njspotlightnews.org → NJ Spotlight News
newjerseymonitor.com → NJ Monitor
northjersey.com → NorthJersey.com
montclairlocal.news → Montclair Local
tapinto.net → TAPinto [+ town from URL path]
```

Full mapping in `src/html_formatter.py:extract_source_from_url()`

### Section Detection

Keyword signals for sections:

**politics**: legislature, senator, assembly, governor, Murphy, election, vote, bill, mayor, council
**housing**: housing, affordable, rent, zoning, development, apartment, tenant, Blue Acres
**education**: school, student, teacher, Rutgers, university, curriculum, board of ed
**health**: hospital, healthcare, medical, nurse, COVID, vaccine, mental health
**environment**: offshore wind, solar, climate, PFAS, pollution, DEP, flood
**lastly**: restaurant, arts, music, sports, Devils, Giants, festival, museum

### Duplicate Detection

Compare submission URL against:
- Today's RSS feed URLs (exact match)
- Similar headlines from same source (likely duplicate)
- Same event from different source (grouping opportunity)

## Examples

**Input**: 7 Airtable submissions to review

**Output**:
```
AIRTABLE TRIAGE - 7 submissions

AUTO-APPROVED (3):
✓ "Montclair council approves downtown rezoning"
  Source: Montclair Local (from URL)
  Section: housing (keywords: council, approves, rezoning)

✓ "Rutgers announces new engineering dean"
  Source: Rutgers Today (from URL)
  Section: education (keywords: Rutgers, announces)

✓ "Murphy signs offshore wind expansion bill"
  Source: NJ Spotlight News (from URL)
  Section: environment (keywords: offshore wind, bill)

NEEDS REVIEW (2):
? "Big news from Trenton"
  Issue: Vague headline, can't determine section
  Source: InsiderNJ (detected)

? "Check out this important story"
  Issue: No real headline provided
  URL: [needs verification]

DUPLICATE (1):
! "NJ Transit announces fare hikes"
  Already in RSS from NJ.com
  Action: Skip (duplicate) or add source?

REJECTED (1):
✗ "Best pizza spots in Brooklyn"
  Reason: Not NJ news (NYC focus)

SUMMARY: 3 auto-approve, 2 review, 1 duplicate, 1 reject
```

## Guidelines

1. Only auto-approve when BOTH source and section are confident
2. When in doubt, categorize as "needs review"
3. Flag duplicates for merge decision, don't auto-skip
4. Check URL accessibility before approving
5. Preserve submitter attribution in notes

## Integration

- **dnr-story-grouping**: Duplicates may be grouping opportunities
- **dnr-source-management**: Unknown domains may need adding
- **dnr-classification**: Section suggestions use same logic

## File References

- Airtable fetcher: `src/airtable_fetcher.py`
- Section mapping: `SECTION_MAP` and `NEWSLETTER_TO_AIRTABLE` dicts
- Review workflow: `src/workflow.py:review_airtable_submissions()`
