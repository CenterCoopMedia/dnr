# Daily News Roundup (DNR) automation

Automated newsletter production system for the Daily News Roundup, a Mailchimp newsletter produced by the [Center for Cooperative Media](https://centerforcooperativemedia.org) at Montclair State University.

## Overview

This project automates the creation of the Daily News Roundup newsletter, which aggregates and curates local journalism news for distribution to the NJ News Commons network.

## Features

- Automated news aggregation from curated source domains
- Topic classification and categorization
- HTML formatting for Mailchimp campaigns
- Draft campaign creation via Mailchimp API
- Scheduled execution (Mon-Thurs mornings)

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API credentials
```

## Configuration

Create a `.env` file with the following:

```
MAILCHIMP_API_KEY=your_api_key
MAILCHIMP_LIST_ID=your_audience_id
MAILCHIMP_TEMPLATE_ID=your_template_id
```

## Usage

```bash
# Run newsletter generation (creates draft in Mailchimp)
python src/main.py

# Run with preview (no Mailchimp API calls)
python src/main.py --preview
```

## Project structure

```
dnr/
├── history/          # Historical CSVs and templates for analysis
├── src/              # Source code
├── config/           # Configuration files
├── tests/            # Test files
├── PROJECT_LOG.md    # Development log
├── README.md         # This file
└── requirements.txt  # Python dependencies
```

## License

Internal use only - Center for Cooperative Media

## Contact

Joe Amditis - amditisj@montclair.edu
