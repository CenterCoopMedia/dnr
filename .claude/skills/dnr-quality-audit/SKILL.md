---
name: dnr-quality-audit
description: Audit a DNR newsletter for quality issues including section imbalance, coverage gaps, duplicate topics, source diversity, and stale stories. Use before sending a newsletter to catch issues, when a newsletter feels "off", or to understand why certain sections are over/under-populated.
allowed-tools: Read, Grep, Glob, Bash
---

# Newsletter Quality Audit

## When to Activate

Activate this skill when:
- User says "audit", "check quality", or "review newsletter"
- Before sending newsletter to 3,000 subscribers
- Newsletter "feels off" or unbalanced
- Sections are unexpectedly empty or overflowing
- User asks about coverage gaps or missing topics

## Core Concepts

**Quality Dimensions**: A good DNR edition balances five dimensions:
1. **Section Balance** - Appropriate story counts per section
2. **Coverage Breadth** - Major ongoing stories represented
3. **Source Diversity** - Mix of statewide, regional, hyperlocal
4. **Geographic Spread** - North, Central, South Jersey representation
5. **Freshness** - Content within appropriate time window

**Expected Ranges** (based on historical analysis):
| Section | Typical | Warning |
|---------|---------|---------|
| top_stories | 3-6 | >6 or 0 |
| politics | 5-15 | >20 or <3 |
| housing | 3-10 | 0 |
| education | 3-10 | 0 |
| health | 3-10 | 0 |
| environment | 3-10 | 0 |
| lastly | 5-20 | >25 |

**Ongoing Stories**: Topics that should almost always appear:
- NJ Transit (constant newsworthy)
- State legislature (when in session)
- Offshore wind (major multi-year story)
- Housing affordability (persistent issue)

## Practical Guidance

### Audit Checklist

**1. Section Balance**
- Count stories per section
- Flag sections outside typical range
- Check top_stories doesn't exceed 6

**2. Coverage Gaps**
- Compare against ongoing story list
- Note missing major topics
- Check for breaking news that should be included

**3. Source Analysis**
- Calculate outlet distribution
- Flag if >40% from single source
- Verify hyperlocal representation (target: 20-25%)

**4. Duplicate Detection**
- Look for same event covered multiple times
- Identify grouping opportunities
- Check for topic clustering (5 stories on same narrow issue)

**5. Geographic Check**
- Note regional distribution
- Flag if entire region missing
- Check South Jersey representation (often light)

**6. Freshness Validation**
- Verify dates within lookback window
- Monday: 76 hours (Friday 5am - now)
- Tue-Thu: 36 hours

## Examples

**Input**: "Audit today's newsletter"

**Output**:
```
NEWSLETTER QUALITY AUDIT - Dec 25, 2025

SECTION BALANCE:
top_stories: 5 ✓
politics: 12 ✓
housing: 2 ⚠️ (below typical 3-10)
education: 8 ✓
health: 4 ✓
environment: 1 ⚠️ (below typical 3-10)
lastly: 15 ✓

COVERAGE GAPS:
- No NJ Transit stories (usually 1-2/day)
- No offshore wind coverage (major ongoing)

SOURCE DIVERSITY:
- NJ.com: 35% ✓
- NJ Spotlight: 20% ✓
- Hyperlocal: 18% ⚠️ (target 20-25%)

GEOGRAPHIC BALANCE:
- North Jersey: 45%
- Central Jersey: 35%
- South Jersey: 20% ✓

POTENTIAL ISSUES:
- 3 stories about same Murphy announcement (group?)

OVERALL: Ready with minor issues
```

## Guidelines

1. Always complete full checklist before overall assessment
2. Flag issues with specific data, not vague concerns
3. Provide actionable recommendations
4. Note both problems and what's working well
5. Consider news cycle context (slow news day vs major events)

## Integration

- **dnr-story-grouping**: Grouping addresses duplicate topic issues
- **dnr-feed-health**: Feed issues may explain coverage gaps
- **dnr-classification**: Section imbalance may indicate classification drift

## File References

- Preview to audit: `drafts/dnr-YYYY-MM-DD.html`
- Section markers: `<!-- TOP STORIES -->`, `<!-- POLITICS STORIES -->`, etc.
- Template structure: `history/dnr-template.html`
