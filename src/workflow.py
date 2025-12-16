"""Interactive DNR workflow - preview, review, approve, publish.

This script provides a guided workflow for creating the Daily News Roundup:
1. Fetch and classify stories
2. Generate HTML preview
3. Open preview in browser for review
4. Prompt for approval
5. Create Mailchimp draft if approved

Usage:
    python src/workflow.py              # Standard workflow
    python src/workflow.py --playwright # Include paywalled sites
    python src/workflow.py --enrich     # Include URL enrichment
"""

import argparse
import os
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from dotenv import load_dotenv
load_dotenv()

# Import pipeline components
from main import run_pipeline, fetch_all_stories, classify_all_stories, deduplicate_stories, organize_by_section, create_mailchimp_draft
from html_formatter import build_newsletter, count_stories


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the workflow header."""
    clear_screen()
    print("=" * 60)
    print("  DAILY NEWS ROUNDUP - WORKFLOW")
    print("=" * 60)
    print(f"  Date: {datetime.now().strftime('%A, %B %d, %Y')}")
    print("=" * 60)
    print()


def print_step(step_num: int, total: int, description: str):
    """Print a step indicator."""
    print(f"\n[Step {step_num}/{total}] {description}")
    print("-" * 40)


def prompt_yes_no(question: str, default: bool = True) -> bool:
    """Prompt user for yes/no response."""
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        response = input(question + suffix).strip().lower()
        if not response:
            return default
        if response in ('y', 'yes'):
            return True
        if response in ('n', 'no'):
            return False
        print("Please enter 'y' or 'n'")


def prompt_continue():
    """Prompt user to continue."""
    input("\nPress Enter to continue...")


def run_workflow(
    include_playwright: bool = False,
    enrich_stories: bool = False,
    hours_back: int = 24
):
    """
    Run the interactive DNR workflow.

    Args:
        include_playwright: Include Playwright sources
        enrich_stories: Enable URL enrichment
        hours_back: Hours to look back for stories
    """
    print_header()

    # Show configuration
    print("Configuration:")
    print(f"  - Hours back: {hours_back}")
    print(f"  - Playwright sources: {'Yes' if include_playwright else 'No'}")
    print(f"  - URL enrichment: {'Yes' if enrich_stories else 'No'}")

    if not prompt_yes_no("\nReady to start?"):
        print("\nWorkflow cancelled.")
        return

    total_steps = 6

    # Step 1: Fetch stories
    print_step(1, total_steps, "Fetching stories from all sources")

    try:
        # Import optional modules
        if include_playwright:
            try:
                from playwright_fetcher import fetch_all_playwright_sources
                playwright_available = True
            except ImportError:
                print("  Warning: Playwright not available")
                playwright_available = False
                include_playwright = False

        if enrich_stories:
            try:
                from url_enricher import enrich_stories_batch
                enrichment_available = True
            except ImportError:
                print("  Warning: URL enrichment not available")
                enrichment_available = False
                enrich_stories = False

        stories = fetch_all_stories(hours_back=hours_back, include_playwright=include_playwright)

        if not stories:
            print("\nNo stories found! Check your RSS feeds and Airtable connection.")
            return

        print(f"\nTotal stories fetched: {len(stories)}")

    except Exception as e:
        print(f"\nError fetching stories: {e}")
        return

    # Step 2: Optional enrichment
    if enrich_stories and enrichment_available:
        print_step(2, total_steps, "Enriching stories with URL context")
        stories = enrich_stories_batch(stories, max_stories=20)
    else:
        print_step(2, total_steps, "Skipping URL enrichment")

    # Step 3: Classify stories
    print_step(3, total_steps, "Classifying stories into sections")

    try:
        classified = classify_all_stories(stories)
        unique = deduplicate_stories(classified)
        sections = organize_by_section(unique)

        # Show counts
        counts = count_stories(sections)
        print("\nStories by section:")
        total = 0
        section_emojis = {
            "top_stories": "📰", "politics": "🏛️", "housing": "🏘️",
            "education": "🏫", "health": "🦠", "environment": "🌳", "lastly": "☝️"
        }
        for section, count in counts.items():
            emoji = section_emojis.get(section, "•")
            print(f"  {emoji} {section}: {count}")
            total += count
        print(f"  Total: {total}")

    except Exception as e:
        print(f"\nError classifying stories: {e}")
        return

    # Step 4: Generate HTML
    print_step(4, total_steps, "Generating HTML preview")

    try:
        html = build_newsletter(sections)

        # Save preview
        output_dir = Path(__file__).parent.parent / "drafts"
        output_dir.mkdir(exist_ok=True)
        preview_path = output_dir / f"dnr-{datetime.now().strftime('%Y-%m-%d')}.html"

        with open(preview_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  Generated {len(html):,} characters")
        print(f"  Saved to: {preview_path}")

    except Exception as e:
        print(f"\nError generating HTML: {e}")
        return

    # Step 5: Review
    print_step(5, total_steps, "Review preview")

    print("\nOpening preview in your browser...")
    webbrowser.open(f"file://{preview_path.absolute()}")

    print("\nPlease review the newsletter in your browser.")
    print("Check for:")
    print("  - Story selection and placement")
    print("  - Headline accuracy")
    print("  - No duplicate stories across sections")
    print("  - Top stories don't appear in other sections")

    prompt_continue()

    # Step 6: Approval and publish
    print_step(6, total_steps, "Create Mailchimp draft")

    print("\nReady to create Mailchimp draft campaign?")
    print("This will create a DRAFT - you still need to review and send in Mailchimp.")

    if prompt_yes_no("\nCreate Mailchimp draft?"):
        print("\nCreating Mailchimp draft...")

        try:
            campaign_id = create_mailchimp_draft(html)

            if campaign_id:
                print("\n" + "=" * 60)
                print("  SUCCESS!")
                print("=" * 60)
                print(f"\n  Campaign ID: {campaign_id}")
                print(f"\n  Next steps:")
                print("  1. Open Mailchimp and find the draft")
                print("  2. Review the email preview")
                print("  3. Send a test email to yourself")
                print("  4. Schedule or send when ready")
            else:
                print("\nFailed to create Mailchimp draft. Check the error above.")

        except Exception as e:
            print(f"\nError creating Mailchimp draft: {e}")
    else:
        print("\nMailchimp draft NOT created.")
        print(f"HTML preview saved at: {preview_path}")
        print("\nYou can manually copy/paste the HTML into Mailchimp later.")

    print("\n" + "=" * 60)
    print("  WORKFLOW COMPLETE")
    print("=" * 60)
    print()


def main():
    parser = argparse.ArgumentParser(description="Interactive DNR Workflow")
    parser.add_argument("--playwright", action="store_true",
                        help="Include Playwright sources (paywalled sites)")
    parser.add_argument("--enrich", action="store_true",
                        help="Enable URL enrichment with Gemini")
    parser.add_argument("--hours", type=int, default=24,
                        help="Hours back to look for stories (default: 24)")

    args = parser.parse_args()

    try:
        run_workflow(
            include_playwright=args.playwright,
            enrich_stories=args.enrich,
            hours_back=args.hours
        )
    except KeyboardInterrupt:
        print("\n\nWorkflow cancelled by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
