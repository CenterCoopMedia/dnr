# DNR Newsletter Claude Skills

Skills for the Daily News Roundup newsletter automation system, designed following context engineering principles from the [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) repository.

## Design Principles

### The 4 Core Truths

1. **Expertise Transfer, Not Instructions** - Skills make Claude think like a newsletter editor, not follow steps
2. **Flow, Not Friction** - Produce actionable output directly, not intermediate analysis
3. **Voice Matches Domain** - Sound like a practitioner making editorial decisions
4. **Focused Beats Comprehensive** - Each section earns its place; keep skills under 500 lines

### Context Engineering Insights Applied

- **Progressive Disclosure**: Skills load only when activated by specific triggers
- **Tool Consolidation**: Related functionality grouped into cohesive skills
- **Integration Notes**: Each skill documents how it connects to others
- **Practical Examples**: Input/output demonstrations show correct usage

---

## Skill Catalog

### 1. dnr-automation (Primary Skill)
**Purpose**: Run the DNR newsletter pipeline

**When to Activate**: User wants to run, preview, or test the newsletter

**Key Capabilities**:
- Execute 7-step workflow (fetch → classify → preview → publish)
- Handle different modes (--preview, --dry-run, --playwright)
- Date-aware fetching (76h Monday, 36h Tue-Thu)
- Troubleshoot API and connectivity issues

---

### 2. dnr-story-grouping
**Purpose**: Identify and consolidate multi-outlet coverage

**When to Activate**: Same story appears multiple times from different outlets

**Key Capabilities**:
- Semantic matching beyond URL deduplication
- Headline selection criteria (specific > vague, active voice)
- Multi-outlet → top_stories signal recognition
- Source citation consolidation

**Addresses**: TODO at `main.py:136` for smarter story grouping

---

### 3. dnr-quality-audit
**Purpose**: Audit newsletter before sending to 3,000 subscribers

**When to Activate**: Before publish, when newsletter "feels off"

**Key Capabilities**:
- Section balance checking (expected vs actual counts)
- Coverage gap detection (ongoing stories, breaking news)
- Source diversity analysis (outlet distribution)
- Geographic balance (North/Central/South Jersey)
- Freshness validation (within lookback window)

---

### 4. dnr-editorial-feedback
**Purpose**: Process natural language editing instructions

**When to Activate**: User gives editing commands during refinement

**Key Capabilities**:
- Bulk operations ("remove all crime from top stories")
- Semantic story matching (find "the transit story")
- Crime vs policy distinction (editorial judgment)
- Edge case flagging for human decision

**Improves**: Existing feedback loop that only searches first 15 stories

---

### 5. dnr-airtable-triage
**Purpose**: Pre-process user submissions for faster review

**When to Activate**: Multiple Airtable submissions need review (Step 4)

**Key Capabilities**:
- Auto-detect source from URL domain
- Suggest section from headline keywords
- Identify RSS duplicates (merge opportunity)
- Flag submissions needing manual review
- Reject non-NJ or broken submissions

---

### 6. dnr-classification
**Purpose**: Handle classification edge cases

**When to Activate**: Story seems miscategorized, crime/policy unclear

**Key Capabilities**:
- Crime blotter vs policy news distinction
- Confidence calibration (0.8+ auto, 0.3-0.5 review)
- Decision tree for ambiguous stories
- Reasoning explanation for verdicts

---

### 7. dnr-feed-health
**Purpose**: Diagnose RSS feed issues

**When to Activate**: Major outlet missing, coverage gaps suggest feed problems

**Key Capabilities**:
- Feed status categorization (healthy/underperforming/broken)
- Diagnostic commands (curl, feedparser tests)
- Common issue identification (paywall, rate limit, format change)
- Playwright fallback recommendations

---

### 8. dnr-filter-rules
**Purpose**: Manage content exclusion keywords

**When to Activate**: Story slipped through or was incorrectly filtered

**Key Capabilities**:
- Test if headline would be filtered
- Add keywords with variant analysis
- False positive risk assessment
- Gap identification in filter coverage

---

### 9. dnr-source-management
**Purpose**: Configure news source feeds and attribution

**When to Activate**: Add new outlet, fix missing attribution

**Key Capabilities**:
- RSS feed discovery and testing
- Domain mapping for source names
- Two-config synchronization (feeds + display names)
- Priority level guidance

---

## Skill Integration Map

```
                    dnr-automation
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
   dnr-feed-health  dnr-airtable-  dnr-classification
         │          triage              │
         │               │               │
         └───────┬───────┴───────┬───────┘
                 │               │
                 ▼               ▼
         dnr-quality-audit  dnr-editorial-feedback
                 │               │
                 └───────┬───────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
   dnr-story-    dnr-filter-     dnr-source-
   grouping      rules           management
```

**Integration Patterns**:
- `dnr-quality-audit` calls `dnr-story-grouping` for duplicate detection
- `dnr-editorial-feedback` uses `dnr-classification` logic for crime/policy
- `dnr-feed-health` informs `dnr-source-management` about broken feeds
- `dnr-airtable-triage` uses source detection from `dnr-source-management`

---

## Skill Structure Standard

Each skill follows this structure (adapted from Agent-Skills template):

```markdown
---
name: skill-name
description: One-line description for discovery
allowed-tools: Bash, Read, Grep, Edit
---

# Skill Title

## When to Activate
- Bullet list of trigger conditions

## Core Concepts
- Key mental models and principles
- Tables for reference data

## Practical Guidance
- Step-by-step approaches
- Decision trees where applicable

## Examples
- Input/Output demonstrations

## Guidelines
- Numbered, verifiable rules

## Integration
- Links to related skills

## File References
- Relevant source files
```

**Constraints**:
- Keep under 500 lines for optimal performance
- Use third-person in descriptions (discovery-friendly)
- Include specific file references with line numbers where helpful
- Provide concrete examples, not abstract instructions

---

## Implementation Status

| Skill | Status | Lines |
|-------|--------|-------|
| dnr-automation | ✅ Updated | 156 |
| dnr-story-grouping | ✅ Updated | 105 |
| dnr-quality-audit | ✅ Updated | 134 |
| dnr-editorial-feedback | ✅ Updated | 133 |
| dnr-airtable-triage | ✅ Updated | 130 |
| dnr-classification | ✅ Updated | 152 |
| dnr-feed-health | ✅ Updated | 163 |
| dnr-filter-rules | ✅ Updated | 173 |
| dnr-source-management | ✅ Updated | 169 |

All skills under 500 lines as recommended.

---

## Context Engineering Lessons Applied

From the Agent-Skills-for-Context-Engineering repository:

### 1. Tool Consolidation
Instead of 9 narrow skills, we grouped related capabilities:
- Source management includes both RSS config and domain mapping
- Quality audit combines balance, diversity, and freshness checks
- Editorial feedback handles both single and bulk operations

### 2. File System as State Machine
DNR already uses this pattern:
- `drafts/dnr-YYYY-MM-DD.html` tracks preview state
- Workflow steps are sequential with clear handoffs
- Airtable approval triggers automation (state change)

### 3. Observation Masking
Skills reference file locations rather than embedding large content:
- "See `src/classifier.py:TOP_STORIES_EXCLUSION_KEYWORDS`"
- "Check `config/rss_feeds.json`"
- Keeps skill files focused on expertise, not data

### 4. Progressive Disclosure
Skills load only when activated:
- General conversation doesn't need filter rules knowledge
- Feed health details only relevant when diagnosing issues
- Classification edge cases only when stories are ambiguous

### 5. Evaluation Integration
Quality audit skill provides built-in evaluation:
- Section balance against expected ranges
- Source diversity targets (20-25% hyperlocal)
- Geographic coverage checks
