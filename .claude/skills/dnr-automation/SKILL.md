---
name: dnr-automation
description: Automate the Daily News Roundup (DNR) newsletter pipeline for the Center for Cooperative Media. Run the DNR script with different modes (--preview generates HTML preview only, --dry-run shows story counts without generating files, full pipeline creates Mailchimp draft). Use this skill when working on DNR newsletter automation, running the pipeline, previewing newsletters, testing story collection and classification, or troubleshooting the NJ News Commons newsletter workflow.
allowed-tools: Bash, Read, Glob, Grep
---

# DNR automation skill

Automate the Daily News Roundup newsletter pipeline for the Center for Cooperative Media. This skill provides guidance on running the DNR automation system with various execution modes.

## What is DNR?

The Daily News Roundup is a Mailchimp newsletter produced by the Center for Cooperative Media that aggregates and curates local journalism news for distribution to the NJ News Commons network. The pipeline collects stories from RSS feeds and Airtable submissions, classifies them by topic using Claude API, deduplicates them across sources, and generates an HTML-formatted draft campaign in Mailchimp.

**Production schedule:** Monday through Thursday mornings
**Audience:** NJ News Commons subscribers (~2,000)
**Distribution method:** Mailchimp

## Quick start

The DNR pipeline supports three execution modes:

```bash
# Navigate to DNR project
cd C:\Users\Joe Amditis\Desktop\Crimes\sandbox\dnr

# Full pipeline: collect stories, classify, format HTML, create Mailchimp draft
venv\Scripts\python.exe src/main.py

# Preview mode: generate HTML only (no Mailchimp API calls)
venv\Scripts\python.exe src/main.py --preview

# Dry-run mode: show story counts without generating output
venv\Scripts\python.exe src/main.py --dry-run

# Custom lookback: search RSS feeds for stories from the past N hours
venv\Scripts\python.exe src/main.py --hours 48
```

## Pipeline workflow

The DNR pipeline executes these steps in order:

1. **Story collection** - Polls 75+ RSS feeds from NJ news outlets, retrieves user submissions from Airtable, combines all sources
2. **Classification** - Uses Claude API (Haiku) to classify stories into newsletter sections
3. **Deduplication** - Removes duplicate URLs, groups stories covering the same event
4. **Organization** - Distributes stories across 7 newsletter sections with limits enforced
5. **HTML formatting** - Generates Mailchimp-compatible HTML using the DNR template
6. **Mailchimp integration** - Creates draft campaign ready for review (full pipeline only)

## Execution modes

### Full pipeline (production)
```bash
venv\Scripts\python.exe src/main.py
```
- Runs complete pipeline including Mailchimp draft creation
- Use when ready to create a newsletter for review and publication
- Output: Mailchimp draft campaign + HTML preview file

### Preview mode
```bash
venv\Scripts\python.exe src/main.py --preview
```
- Runs pipeline without Mailchimp API calls
- Generates HTML output for review
- Use for testing pipeline, reviewing HTML formatting, checking classification
- Output: HTML preview file at `drafts/dnr-YYYY-MM-DD.html`

### Dry-run mode
```bash
venv\Scripts\python.exe src/main.py --dry-run
```
- Shows story counts by source only
- No classification, HTML generation, or API calls
- Use for quick availability check
- Output: Story count summary

### Custom hours lookback
```bash
venv\Scripts\python.exe src/main.py --hours N --preview
```
- Collects stories from past N hours (default: 24)
- Can combine with --preview or --dry-run

## Newsletter sections

| Section | Description | Typical count |
|---------|-------------|---------------|
| Top stories | Breaking news, high-impact statewide stories | 3-6 max |
| Politics | Government, legislature, elections, courts | 5-15 |
| Housing | Affordable housing, development, zoning | 3-10 |
| Education | Schools, universities, education policy | 3-10 |
| Health | Healthcare, hospitals, public health | 3-10 |
| Environment | Climate, energy, pollution, offshore wind | 3-10 |
| Lastly | Arts, culture, sports, lighter news | 5-20 |

## Primary story sources

**Statewide:** NJ.com, NJ Spotlight News, NJ Monitor, NJ Globe, NJ Biz, ROI-NJ
**Regional:** NorthJersey.com, Press of Atlantic City, Trentonian, NJ Herald
**Hyperlocal:** Montclair Local, Village Green, Baristanet, Jersey Digs, Hudson Reporter
**Public media:** WHYY, WNYC/Gothamist
**User submissions:** Airtable form (linked in each newsletter)

## Editorial rules

- Multi-outlet coverage typically = Top Stories
- Stories in Top Stories excluded from topic sections
- Choose headlines that capture story essence, avoid clickbait
- Use sentence case for headlines (not Title Case)
- Source order: Order discovered or headline source first

## Environment setup

```bash
cd C:\Users\Joe Amditis\Desktop\Crimes\sandbox\dnr
python -m venv venv
venv\Scripts\pip.exe install -r requirements.txt
```

Required environment variables in `.env`:
- ANTHROPIC_API_KEY (for story classification)
- MAILCHIMP_API_KEY, MAILCHIMP_SERVER_PREFIX, MAILCHIMP_LIST_ID
- AIRTABLE_PAT, AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID

## Troubleshooting

**Pipeline fails with API errors:**
- Check .env file has all required credentials
- Verify API keys are valid and not expired
- Test connections: `venv\Scripts\python.exe src/test_connections.py`

**Low story count:**
- Check RSS feed connectivity
- Try `--hours 48` for broader time window
- Verify Airtable submissions exist

**Classification seems off:**
- Review story headlines in output
- Check classifier prompt in `src/classifier.py`
- Consider manual section overrides in Airtable submissions

## Common tasks

```bash
# Create today's newsletter
venv\Scripts\python.exe src/main.py

# Preview without Mailchimp
venv\Scripts\python.exe src/main.py --preview

# Quick story count check
venv\Scripts\python.exe src/main.py --dry-run

# Test with smaller time window
venv\Scripts\python.exe src/main.py --hours 12 --preview

# Test API connections
venv\Scripts\python.exe src/test_connections.py
```

## Project files

- `src/main.py` - Main pipeline orchestrator
- `src/rss_fetcher.py` - RSS feed collection
- `src/airtable_fetcher.py` - Airtable submissions
- `src/classifier.py` - Claude API story classification
- `src/html_formatter.py` - HTML newsletter generation
- `config/rss_feeds.json` - RSS feed configuration (75+ sources)
- `history/dnr-template.html` - Mailchimp HTML template
- `drafts/` - Generated HTML previews

## Support

Contact: Joe Amditis (amditisj@montclair.edu)
Project: Center for Cooperative Media, Montclair State University
Repository: https://github.com/CenterCoopMedia/dnr
