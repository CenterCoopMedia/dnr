---
name: dnr-editorial-feedback
description: Process natural language editing instructions for the DNR newsletter with full semantic understanding. Handles bulk operations like "remove all crime stories", fuzzy headline matching, and editorial judgment calls about where stories belong.
allowed-tools: Read, Grep, Edit
---

# Editorial Feedback Processor

## When to Activate

Activate this skill when:
- User gives editing instructions in natural language
- User wants to move, remove, or reorder stories
- Bulk operations needed ("remove all X from Y")
- User says "this doesn't belong" or similar
- Refining newsletter after preview review

## Core Concepts

**Editor Shorthand**: Editors speak efficiently. Map their intent:

| They Say | They Mean |
|----------|-----------|
| "the transit story" | Find headline mentioning NJ Transit, transit, train, etc. |
| "crime stories" | Headlines with crime/violence indicators |
| "move to politics" | Change section assignment |
| "doesn't belong" | Remove from newsletter (→ skip) |
| "this is top stories" | Elevate to top_stories section |

**Crime vs Policy Distinction** (critical judgment call):
- **Crime blotter** = "What happened to whom" → Remove from top_stories
- **Policy news** = "What this reveals about systems" → May belong in top_stories

Example: "AG charges 5 officials with corruption" = POLICY (systemic issue)
Example: "Man arrested for carjacking" = CRIME (isolated incident)

**Current Limitation**: Existing feedback loop (`workflow.py:278-388`) only searches first 15 stories per section. This skill provides full semantic search.

## Practical Guidance

### Processing Steps

1. **Parse Intent**: Identify action (move/remove/reorder) and target
2. **Find Matches**: Search all sections using semantic matching
3. **Apply Editorial Judgment**: Flag edge cases for confirmation
4. **Generate Actions**: Produce specific, reversible changes

### Matching Strategies

**For specific stories**: Match proper nouns, numbers, unique phrases
```
"the Murphy announcement" → Headlines containing "Murphy" + announcement-type verbs
```

**For categories**: Match semantic indicators
```
"crime stories" → murder, shooting, stabbing, robbery, carjacking, assault, arrested, charged, etc.
```

**For bulk operations**: Iterate all matches, present for confirmation
```
"remove all crime from top stories" → List all matches before applying
```

### Edge Case Handling

When a story could go either way:
1. Present the ambiguity
2. Explain reasoning for both interpretations
3. Let user decide

## Examples

**Input**: "Remove all crime stories from top stories"

**Output**:
```
IDENTIFIED FOR REMOVAL (4 stories):
✓ "Man charged in Newark carjacking" → skip
✓ "Three arrested in drug bust" → skip
✓ "Fatal crash closes Route 80" → skip
? "AG announces crackdown on wage theft" → KEPT (policy/enforcement)

Note: Kept 1 story - mentions enforcement but is policy-focused.
Remove it too? (y/n)
```

**Input**: "Move the transit story to politics"

**Output**:
```
FOUND: "NJ Transit announces fare increases for 2026"
Current section: top_stories
Action: Move to politics

Apply? (y/n)
```

**Input**: "This doesn't belong" (after viewing specific story)

**Output**:
```
Which story should be removed?
[Awaiting clarification or assuming context from recent discussion]
```

## Guidelines

1. Always confirm bulk operations before applying
2. Flag policy/crime edge cases rather than auto-deciding
3. Provide reasoning for kept stories in bulk removes
4. Actions should be reversible (log what was changed)
5. When ambiguous, ask for clarification

## Integration

- **dnr-classification**: Uses same crime/policy distinction logic
- **dnr-story-grouping**: "Combine these" triggers grouping skill
- **dnr-quality-audit**: Post-edit audit catches remaining issues

## Section Reference

| Section | Content Type |
|---------|--------------|
| top_stories | Major policy, statewide impact, multi-outlet |
| politics | Government, elections, courts |
| housing | Development, zoning, affordability |
| education | Schools, universities |
| health | Healthcare, public health |
| environment | Climate, energy, DEP |
| lastly | Arts, sports, lighter news |
| skip | Non-NJ, filtered content |
