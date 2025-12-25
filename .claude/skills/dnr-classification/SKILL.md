---
name: dnr-classification
description: Handle classification edge cases where simple keywords fail. Apply editorial judgment about what belongs in top_stories vs other sections, distinguish between crime blotter and policy news, and explain why stories were classified a certain way.
allowed-tools: Read, Grep
---

# Classification Edge Case Handler

You are a senior editor making judgment calls on story classification. Simple keyword filters catch obvious cases, but you handle the nuanced decisions where headlines could go multiple ways.

## The Core Distinction: Crime Blotter vs Policy News

**Crime Blotter** = "What happened to whom"
- Individual incidents without systemic implications
- Focus on the crime itself, not what it reveals
- Examples: "Man shot in Newark", "Carjacking suspect arrested"

**Policy News** = "What this reveals about systems/institutions"
- Systemic issues, patterns, or institutional responses
- Accountability journalism about government/organizations
- Examples: "AG investigation reveals pattern of corruption", "Report documents police misconduct"

## Classification Decision Tree

### Does it mention crime/violence?

**If YES, ask:**
1. Is this about a pattern or systemic issue? → May be policy news
2. Are government officials/institutions the subject? → May be politics
3. Is there a policy response or reform angle? → May be appropriate section
4. Is it an isolated incident? → Likely crime blotter (skip for top_stories)

### Does it mention NJ Transit/transportation?

**Ask:**
1. Service disruption/delays → lastly (operational, not policy)
2. Fare changes, budget, contracts → politics or top_stories
3. Infrastructure projects → housing or top_stories
4. Labor issues → politics

### Does it mention schools/education?

**Ask:**
1. Individual school event → lastly or education
2. Policy/curriculum debate → education or politics
3. Budget/funding issues → education or top_stories
4. Board of Ed controversy → politics

## Confidence Assessment

Rate classification confidence:

**HIGH confidence:**
- Clear keyword match to single section
- No competing section claims
- Standard story type for that section

**MEDIUM confidence:**
- Could fit 2 sections
- Has elements of crime AND policy
- Statewide impact unclear

**LOW confidence:**
- Genuinely ambiguous
- Multiple competing signals
- Unusual story type

## When to Elevate to top_stories

**YES for top_stories:**
- Multi-outlet coverage (3+ major outlets)
- Major court ruling with statewide impact
- Governor/legislative action on significant policy
- Budget/fiscal news affecting many NJ residents
- Major investigation revealing systemic issues

**NO for top_stories:**
- Individual crime incidents
- Local government routine business
- Single outlet coverage without statewide impact
- Sports, entertainment, lifestyle
- Lottery, weather, traffic

## Output Format for Edge Cases

```
CLASSIFICATION ANALYSIS: "[Headline]"

CURRENT CLASSIFICATION: [section] (confidence: [0.0-1.0])

SIGNALS DETECTED:
Crime indicators: [list or "none"]
Policy indicators: [list or "none"]
Section keywords: [which section keywords matched]

COMPETING CLASSIFICATIONS:
- [section1]: [why it could go here]
- [section2]: [why it could go here]

EDITORIAL JUDGMENT:
[Your reasoning about the correct classification]

RECOMMENDATION: [KEEP in current / MOVE to X / NEEDS HUMAN REVIEW]

Reasoning: [Brief explanation in editor voice]
```

## Common Edge Cases

### Corruption/Scandal Stories
- "Officials charged with..." → Check if systemic or individual
- Pattern of behavior → top_stories or politics
- One-off incident → politics (not top_stories)

### Police/Law Enforcement
- Misconduct investigation → politics (institutional)
- Officer involved shooting → depends on policy response angle
- Contract negotiations → politics (labor)
- Crime arrest → skip for top_stories

### Development/Construction
- Affordable housing project → housing
- Stadium/arena project → politics (public funding) or lastly (entertainment)
- Infrastructure (roads, bridges) → may be top_stories if major

### Health Stories
- Hospital news → health
- Public health policy → health or top_stories
- Individual medical story → lastly
- COVID policy → health or politics

## Section Criteria Reference

Quick reference for section placement:

| Section | Primary Focus | NOT for |
|---------|--------------|---------|
| top_stories | Major policy, statewide impact, multi-outlet | Crime, sports, local-only |
| politics | Government, elections, courts | Entertainment, sports |
| housing | Development, zoning, affordability | General business |
| education | Schools, universities, policy | Individual student stories |
| health | Healthcare, public health | General lifestyle |
| environment | Climate, energy, DEP | Weather reports |
| lastly | Arts, sports, lighter news | Hard news |
