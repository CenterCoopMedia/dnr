# Project log: Daily News Roundup (DNR) automation

## Project overview

Automation system for the Daily News Roundup Mailchimp newsletter produced by the Center for Cooperative Media at Montclair State University. The newsletter aggregates and curates local journalism news from across the NJ news ecosystem for distribution to the NJ News Commons network.

**Schedule:** Monday through Thursday mornings
**Distribution:** Mailchimp campaign to NJ News Commons subscribers
**Goal:** Automate story collection, classification, and draft creation so Joe only needs to review and click send.

## Session history

### 2025-12-16 - Project initialization and data analysis

**Setup completed:**
- Created project directory at `C:\Users\Joe Amditis\Desktop\Crimes\sandbox\dnr`
- Initialized git repository
- Created GitHub repo: https://github.com/CenterCoopMedia/dnr (public, under CenterCoopMedia org)
- Set up project structure (src/, config/, tests/, history/)

**Historical data analyzed:**
- 7 CSV files containing ~33,000 lines of historical newsletter data
- 1 HTML Mailchimp template
- Data spans from March 2022 onward

---

## Data analysis findings

### Newsletter structure (from HTML template)

The newsletter has 7 content sections, each color-coded:

| Section | Emoji | CSS Class | Accent Color |
|---------|-------|-----------|--------------|
| Top stories | 📰 | section-top-stories | #4A90E2 (blue) |
| Government + politics | 🏛️ | section-politics | #6a1b9a (purple) |
| Housing + development | 🏘️ | section-housing | #00897b (teal) |
| Work + education | 🏫 | section-education | #3949ab (indigo) |
| Health + safety | 🦠 | section-health | #d32f2f (red) |
| Climate + environment | 🌳 | section-environment | #43a047 (green) |
| Before you go | ☝️ | section-lastly | #fb8c00 (orange) |

**Template features:**
- Two CTA blocks: "Submit story" form and "Subscribe" button
- Mailchimp merge tags for date: `*|DATE:l, F j, Y|*`
- Campaign archive link
- MSU footer with logo
- Responsive design (mobile-friendly)

### Story HTML format

Each story follows this exact format:
```html
<li>Headline text (<a href="URL">Source Name</a>)
```

Stories are wrapped in `<ul>` tags within each section. Link colors inherit from section CSS class.

### CSV data format

| Column | Description |
|--------|-------------|
| Date | Timestamp (mixed formats: DD/MM/YYYY HH:MM:SS or YYYY-MM-DD HH:MM:SS) |
| OUTPUT | Pre-formatted HTML `<li>` element |

**Separator rows:** Lines containing `,-` mark boundaries between different newsletter editions.

---

## Source domains identified

### Primary NJ news sources (high frequency)

| Source Name | Domain | Type |
|-------------|--------|------|
| NJ.com | nj.com | Major metro daily |
| NJ Spotlight News | njspotlightnews.org | Nonprofit news |
| NJ Monitor | newjerseymonitor.com | Nonprofit news |
| NJ Globe | newjerseyglobe.com | Political news |
| NorthJersey.com | northjersey.com | Bergen Record / USA Today |
| Press of Atlantic City | pressofatlanticcity.com | Daily newspaper |
| Asbury Park Press | app.com | Daily newspaper |
| TAPinto | tapinto.net | Hyperlocal network |
| ROI-NJ | roi-nj.com | Business news |
| WHYY | whyy.org | Public media (Philly/NJ) |

### Regional/hyperlocal sources

| Source Name | Domain | Coverage |
|-------------|--------|----------|
| 70and73.com | 70and73.com | South Jersey (Burlington/Camden) |
| Morristown Green | morristowngreen.com | Morris County |
| Princeton Perspectives | princetonperspectives.com | Princeton area |
| NJ Pen | njpen.com | Camden County |
| Jersey Digs | jerseydigs.com | Real estate/development |
| MercerMe | mercerme.com | Mercer County |
| NJ Biz | njbiz.com | Business |
| New Jersey Monthly | njmonthly.com | Statewide magazine |
| Jersey Shore Online | jerseyshoreonline.com | Shore communities |
| MyCentralJersey | mycentraljersey.com | Central Jersey |
| Route 40 | rtforty.com | Atlantic County |
| NJ Arts | njarts.net | Arts/culture |
| NJ Indy | njindy.com | News |
| Patch | patch.com | Hyperlocal network |

### National/regional outlets (occasional)

- The Inquirer (Philadelphia)
- New York Times
- Washington Post
- Wall Street Journal
- NBC New York
- Gothamist
- The Guardian
- Associated Press
- WNYC
- HuffPost
- New York Post
- Fox 5
- News12

---

## Topic/category patterns

### Top stories
- Breaking statewide news
- Major policy announcements
- High-profile investigations
- Cannabis legalization updates
- Public safety incidents

### Government + politics
- State legislature activity
- Elections and campaigns
- Political corruption/ethics
- Municipal government
- Courts and judiciary
- Voter registration
- Budget/spending

### Housing + development
- Affordable housing projects
- Real estate market trends
- Zoning decisions
- Rent control
- Homelessness
- Construction/development
- Utility issues

### Work + education
- K-12 schools
- Higher education
- School board elections
- Curriculum controversies
- Teacher issues
- Workforce development

### Health + safety
- COVID-19 updates (historically)
- Public health policy
- Healthcare access
- Mental health
- Crime/safety
- Veterans issues

### Climate + environment
- Offshore wind energy
- Clean energy policy
- Weather events
- Environmental regulations
- Warehouse development
- Bag ban/plastic reduction
- Pollution/Superfund sites

### Before you go (Lastly)
- Human interest stories
- Arts and culture
- Sports
- Community events
- Lighter news
- Recalls/consumer info
- Local achievements

---

## Current status

- ✅ Completed: Project setup and GitHub repo
- ✅ Completed: Historical data analysis
- ✅ Completed: Source domain identification
- ✅ Completed: Category/topic pattern analysis
- ✅ Completed: HTML format documentation
- ⏳ In progress: Awaiting workflow clarification from Joe
- 📋 Planned: Build RSS aggregation system
- 📋 Planned: Build story classification system
- 📋 Planned: Build Mailchimp API integration
- 📋 Planned: Build automation scheduler

## Key files

| File | Purpose |
|------|---------|
| `PROJECT_LOG.md` | Development log and documentation |
| `README.md` | Project overview and usage |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |
| `history/*.csv` | Historical newsletter data (7 category files) |
| `history/dnr-template.html` | Mailchimp HTML template |

## Dependencies

**Confirmed:**
- Mailchimp Marketing API (for campaign creation)
- feedparser (RSS parsing)
- beautifulsoup4 (HTML parsing)
- pandas (data analysis)
- requests (HTTP requests)
- python-dotenv (environment management)
- schedule (optional, for automated runs)

**Potential additions:**
- Anthropic API or local LLM for story classification
- Google News API or similar for discovery
- Playwright (if scraping needed beyond RSS)

## Architecture decisions

**Pending clarification from Joe:**
1. Source of raw story candidates (RSS feeds? Manual? Aggregator?)
2. Classification approach (rules-based? AI-assisted?)
3. Mailchimp API credentials and template setup
4. Desired automation level (draft only vs. scheduled send)
5. Hard rules for story inclusion/exclusion

## Future enhancements

- Automated daily runs via Windows Task Scheduler or cron
- Story deduplication across sources
- Priority scoring for story placement
- Analytics on open rates by category
- Source diversity tracking
- Slack/email notifications when draft is ready
