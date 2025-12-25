---
name: dnr-story-grouping
description: Identify and group duplicate stories covering the same event from multiple NJ news outlets. Use when you notice the same story appearing multiple times in a newsletter preview, when preparing a newsletter and want to consolidate multi-outlet coverage, or when a story has significant coverage that should be highlighted in top_stories.
allowed-tools: Read, Grep, Glob
---

# Story Grouping & Multi-Outlet Consolidation

## When to Activate

Activate this skill when:
- User mentions "duplicate stories" or "same story multiple times"
- Preparing newsletter and want to check for consolidation opportunities
- Story appears from 3+ outlets (strong top_stories signal)
- User asks about multi-outlet coverage or grouping
- Reviewing newsletter quality and notice repetition

## Core Concepts

**The Multi-Outlet Signal**: When 3+ major outlets cover the same event, it's a strong indicator the story belongs in top_stories. This is editorial judgment encoded as a heuristic.

**Headline Variance**: Same event gets different framing:
- "Murphy signs $2B transit bill" (NJ.com) - specific, number-focused
- "Governor approves major transit funding" (NJ Spotlight) - role-focused
- "State invests billions in NJ Transit" (NJ Monitor) - impact-focused

These are ONE story. Recognize by shared: proper nouns, numbers, event type, timeframe.

**Current Limitation**: DNR only deduplicates by URL (`main.py:136` has TODO for smarter grouping). This skill fills that gap with semantic grouping.

## Practical Guidance

### Identification Signals

**Strong Match (definitely same story)**:
- Identical proper nouns (Murphy, NJ Transit, specific town)
- Same numbers ($2B, 500 jobs, 3 officials)
- Same event type (signing, vote, ruling, arrest)
- Published within 24 hours

**Possible Match (verify content)**:
- Related topic but different angle
- Same subject, different event
- Follow-up vs original coverage

**Not a Match**:
- Same topic, different events (two separate crashes)
- Opinion vs news on same subject
- Different time periods

### Headline Selection Criteria

When consolidating, choose headline that:
1. Contains specific numbers/names over vague language
2. Uses active voice
3. Is shorter when equally informative
4. Avoids clickbait framing

### Section Placement Logic

| Outlet Count | Recommendation |
|--------------|----------------|
| 3+ major outlets | top_stories |
| 2 outlets | Consider top_stories if statewide impact |
| Regional only | Keep in topic section, combine sources |

## Examples

**Input**: Newsletter preview shows:
- "Murphy signs $2B transit funding bill" (NJ.com)
- "Governor approves major NJ Transit investment" (NJ Spotlight News)
- "State commits billions to transit overhaul" (NJ Monitor)

**Output**:
```
GROUPED: Transit funding bill (3 sources)
Headline: "Murphy signs $2B transit funding bill"
Sources: NJ.com, NJ Spotlight News, NJ Monitor
Section: top_stories (multi-outlet coverage)
```

**Input**: Stories about different council meetings in different towns

**Output**: NOT grouped - different events, keep separate in appropriate sections

## Guidelines

1. Only group stories about the SAME event, not same topic
2. Preserve all source citations in grouped entry
3. Choose most specific headline
4. Multi-outlet coverage = strong top_stories signal
5. When uncertain, keep separate (avoid false grouping)

## Integration

- **dnr-quality-audit**: Audit checks for ungrouped duplicates
- **dnr-editorial-feedback**: "Combine these stories" triggers grouping
- **dnr-classification**: Grouped stories may need section reassignment

## File References

- Deduplication logic: `src/main.py:deduplicate_stories()`
- HTML formatting: `src/html_formatter.py:format_grouped_story()`
- Preview output: `drafts/dnr-YYYY-MM-DD.html`
