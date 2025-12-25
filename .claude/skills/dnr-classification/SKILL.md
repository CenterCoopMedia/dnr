---
name: dnr-classification
description: Handle classification edge cases where simple keywords fail. Apply editorial judgment about what belongs in top_stories vs other sections, distinguish between crime blotter and policy news, and explain why stories were classified a certain way.
allowed-tools: Read, Grep
---

# Classification Edge Case Handler

## When to Activate

Activate this skill when:
- User questions why a story was classified a certain way
- Story seems miscategorized
- Crime vs policy distinction is unclear
- User asks "should this be in top stories?"
- Classification confidence is low (< 0.5)

## Core Concepts

**The Fundamental Distinction**:
- **Crime Blotter** = "What happened to whom" → Isolated incident, no systemic implications
- **Policy News** = "What this reveals about systems/institutions" → Accountability, reform, patterns

This distinction is the #1 judgment call in DNR classification.

**Top Stories Criteria** (must meet at least one):
- Multi-outlet coverage (3+ major outlets)
- Major court ruling with statewide impact
- Governor/legislative action on significant policy
- Budget/fiscal news affecting many NJ residents
- Major investigation revealing systemic issues

**Never Top Stories**:
- Individual crime incidents (unless policy angle)
- Local government routine business
- Sports, entertainment, lifestyle
- Lottery, weather, traffic reports

## Practical Guidance

### Decision Tree for Ambiguous Stories

```
Does headline mention crime/violence keywords?
├── NO → Use standard section matching
└── YES → Ask: Is there a policy/systemic angle?
    ├── YES (pattern, investigation, reform) → May be appropriate section
    └── NO (isolated incident) → Skip from top_stories
```

### Examples by Pattern

**Corruption/Scandal**:
- "Officials charged with bid-rigging" → POLICY (systemic, accountability)
- "Councilman arrested for DUI" → CRIME (individual misconduct)

**Police/Law Enforcement**:
- "AG report documents pattern of misconduct" → POLICY (systemic)
- "Officer-involved shooting in Newark" → Depends on policy response angle
- "Police union contract negotiations" → POLITICS (labor issue)

**Transportation**:
- "NJ Transit fare increases" → POLITICS or TOP_STORIES (policy)
- "Train delays due to signal problems" → LASTLY (operational)
- "Federal infrastructure grant for NJ Transit" → TOP_STORIES (major funding)

**Development**:
- "Affordable housing project approved" → HOUSING
- "Stadium financing debate" → POLITICS (public funding)
- "New restaurant opening" → LASTLY

## Examples

**Input**: "AG charges 5 officials with corruption in contract scheme"

**Output**:
```
CLASSIFICATION ANALYSIS

Headline: "AG charges 5 officials with corruption in contract scheme"

CRIME INDICATORS:
- "charges" - criminal action
- "corruption" - criminal activity

POLICY INDICATORS:
- "officials" - government actors
- "contract scheme" - systemic issue
- AG involvement suggests accountability journalism

VERDICT: KEEP in top_stories

Reasoning: This is accountability journalism about systemic
government failure, not crime blotter. The focus is on
institutional corruption, not individual criminal acts.

The key question: Does this story inform citizens about
how their government/institutions function?
Answer: YES → Policy news
```

**Input**: "Man shot during argument over parking spot"

**Output**:
```
CLASSIFICATION ANALYSIS

Headline: "Man shot during argument over parking spot"

CRIME INDICATORS:
- "shot" - violent crime
- Individual victim

POLICY INDICATORS:
- None identified

VERDICT: SKIP from top_stories

Reasoning: This is crime blotter - an isolated violent
incident with no systemic or policy implications.
```

## Guidelines

1. Always explain reasoning, not just verdict
2. Look for institutional/systemic angle in crime stories
3. Multi-outlet coverage elevates importance regardless of topic
4. When genuinely ambiguous, lean toward inclusion (editor can remove)
5. Consider: "Does this inform citizens about how institutions work?"

## Integration

- **dnr-editorial-feedback**: Uses same crime/policy logic
- **dnr-filter-rules**: Keywords trigger this skill for edge cases
- **dnr-quality-audit**: Classification issues show in section imbalance

## Confidence Calibration

| Confidence | Meaning | Action |
|------------|---------|--------|
| 0.8-1.0 | Clear match | Auto-assign |
| 0.5-0.8 | Probable match | Assign but note |
| 0.3-0.5 | Uncertain | Flag for review |
| < 0.3 | Low confidence | Needs human decision |

## File References

- Classification logic: `src/classifier.py`
- Section descriptions: `SECTION_DESCRIPTIONS` dict
- Exclusion keywords: `TOP_STORIES_EXCLUSION_KEYWORDS`
- Filter function: `filter_top_stories()`
