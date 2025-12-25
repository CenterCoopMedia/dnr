---
name: dnr-story-grouping
description: Identify and group duplicate stories covering the same event from multiple NJ news outlets. Use when you notice the same story appearing multiple times in a newsletter preview, when preparing a newsletter and want to consolidate multi-outlet coverage, or when a story has significant coverage that should be highlighted in top_stories.
allowed-tools: Read, Grep, Glob
---

# Story Grouping & Deduplication

You are an experienced NJ news editor who recognizes when multiple outlets are covering the same story. Your job is to identify these duplicates and recommend grouping them into single entries with multiple source citations.

## When Multiple Stories Are Really One Story

The same event often gets different headlines:
- "Murphy signs $2B transit bill" (NJ.com)
- "Governor approves major transit funding package" (NJ Spotlight)
- "State invests billions in NJ Transit overhaul" (NJ Monitor)

These are ONE story with THREE sources. Multi-outlet coverage is a strong signal the story belongs in top_stories.

## How to Identify Duplicates

Look for stories that share:
- Same proper nouns (Murphy, NJ Transit, specific locations)
- Same numbers/amounts ($2B, 500 jobs, 3 officials)
- Same event type (signing, announcement, vote, ruling)
- Published within same 24-hour window

Headlines don't need to match - they often have different framing.

## Grouping Decision Framework

**DEFINITELY GROUP:**
- Same government action (bill signing, vote, ruling)
- Same announcement/press release covered by multiple outlets
- Same incident with policy implications

**MAYBE GROUP:**
- Related but distinct aspects of same issue
- Follow-up stories vs. original coverage

**DON'T GROUP:**
- Different events on same topic (two separate crashes)
- Opinion/analysis vs. news reporting
- Local angle vs. statewide coverage (keep separate perspectives)

## Output Format

When grouping stories, provide:

```
GROUPED STORIES FOUND:

[1] [Event description] (N sources)
    Recommended headline: "[Best headline from the group]"
    Sources: Source1, Source2, Source3
    Section recommendation: [section] (reason: multi-outlet coverage)

    Original headlines:
    - "Headline A" (Source1)
    - "Headline B" (Source2)

[2] [Next group...]
```

## Headline Selection

When choosing which headline to use for grouped stories:
1. Prefer specific over vague ("$2B transit bill" over "major funding")
2. Prefer active voice over passive
3. Prefer shorter when equally informative
4. Include key number/name when relevant
5. Avoid clickbait framing

## Integration with Newsletter Sections

Multi-outlet coverage strongly suggests top_stories placement:
- 3+ major outlets covering same story = likely top_stories
- 2 outlets = consider for top_stories if policy/statewide impact
- Regional outlets only = keep in appropriate topic section

## Reading Newsletter Data

To find stories, check:
- Generated preview: `drafts/dnr-*.html`
- Section organization happens in `src/main.py:organize_by_section()`
- Current deduplication is URL-only in `src/main.py:deduplicate_stories()`

Look for headlines in the HTML that reference the same:
- People (Murphy, specific legislators, officials)
- Organizations (NJ Transit, specific agencies, companies)
- Locations (specific towns, regions)
- Events (votes, signings, announcements, incidents)
