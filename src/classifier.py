"""Story classifier using Claude API to categorize news stories."""

import json
import os
from typing import Optional

import anthropic
from dotenv import load_dotenv

load_dotenv()

# Newsletter sections
SECTIONS = [
    "top_stories",
    "politics",
    "housing",
    "education",
    "health",
    "environment",
    "lastly"
]

SECTION_DESCRIPTIONS = {
    "top_stories": "Major breaking news, high-impact statewide stories, investigations, stories covered by multiple outlets",
    "politics": "Government, legislature, elections, campaigns, courts, police, corruption, budgets, taxes, voting",
    "housing": "Affordable housing, rent, development, zoning, real estate, homelessness, construction, warehouses",
    "education": "Schools (K-12), universities, colleges, school boards, teachers, curriculum, education policy",
    "health": "Healthcare, hospitals, public health, mental health, addiction, insurance, medical issues",
    "environment": "Climate, clean energy, weather, pollution, environmental regulations, offshore wind, PFAS",
    "lastly": "Arts, culture, sports, entertainment, restaurants, community events, human interest, lighter news"
}


def classify_story(
    headline: str,
    url: str,
    summary: Optional[str] = None,
    source: Optional[str] = None
) -> dict:
    """
    Classify a single story into a newsletter section using Claude.

    Args:
        headline: Story headline
        url: Story URL
        summary: Optional story summary
        source: Optional source name

    Returns:
        Dict with section, confidence, and reasoning
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Build context
    story_info = f"Headline: {headline}\nURL: {url}"
    if summary:
        story_info += f"\nSummary: {summary}"
    if source:
        story_info += f"\nSource: {source}"

    section_list = "\n".join([
        f"- {section}: {desc}"
        for section, desc in SECTION_DESCRIPTIONS.items()
    ])

    prompt = f"""You are classifying New Jersey news stories for a daily newsletter.

Given this story:
{story_info}

Classify it into ONE of these sections:
{section_list}

Respond with JSON only:
{{"section": "section_name", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}

Rules:
- If multiple outlets cover the same story, it's likely "top_stories"
- Breaking news and major statewide impact = "top_stories"
- Light/fun stories, arts, sports = "lastly"
- When uncertain between sections, choose the more specific one
- Confidence should reflect how clearly it fits the section"""

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        # Parse JSON from response
        # Handle potential markdown code blocks
        if "```" in response_text:
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()

        result = json.loads(response_text)

        # Validate section
        if result.get("section") not in SECTIONS:
            result["section"] = "lastly"  # Default fallback

        return result

    except Exception as e:
        print(f"Classification error for '{headline[:50]}...': {e}")
        return {
            "section": "lastly",
            "confidence": 0.3,
            "reasoning": f"Classification failed: {str(e)}"
        }


def classify_stories_batch(stories: list[dict], max_per_request: int = 10) -> list[dict]:
    """
    Classify multiple stories efficiently using batch requests.

    Args:
        stories: List of story dicts with headline, url, etc.
        max_per_request: Max stories to classify in one API call

    Returns:
        List of stories with section assignments added
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    results = []

    # Process in batches
    for i in range(0, len(stories), max_per_request):
        batch = stories[i:i + max_per_request]

        # Build batch prompt
        stories_text = "\n\n".join([
            f"[{j+1}] Headline: {s.get('headline', s.get('title', ''))}\n"
            f"    URL: {s.get('url', '')}\n"
            f"    Source: {s.get('source', 'Unknown')}"
            for j, s in enumerate(batch)
        ])

        section_list = "\n".join([
            f"- {section}: {desc}"
            for section, desc in SECTION_DESCRIPTIONS.items()
        ])

        prompt = f"""Classify these New Jersey news stories for a daily newsletter.

Stories:
{stories_text}

Sections:
{section_list}

Respond with JSON array only - one object per story in order:
[{{"story": 1, "section": "section_name", "confidence": 0.0-1.0}}, ...]

Rules:
- Breaking news, major statewide impact, multi-outlet coverage = "top_stories"
- Light/fun stories, arts, sports, human interest = "lastly"
- Choose the most specific applicable section"""

        try:
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # Parse JSON
            if "```" in response_text:
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            classifications = json.loads(response_text)

            # Merge classifications with stories
            for j, story in enumerate(batch):
                story_copy = story.copy()
                if j < len(classifications):
                    cls = classifications[j]
                    story_copy["section"] = cls.get("section", "lastly")
                    story_copy["confidence"] = cls.get("confidence", 0.5)
                else:
                    story_copy["section"] = "lastly"
                    story_copy["confidence"] = 0.3
                results.append(story_copy)

        except Exception as e:
            print(f"Batch classification error: {e}")
            # Fall back to individual classification
            for story in batch:
                result = classify_story(
                    headline=story.get("headline", story.get("title", "")),
                    url=story.get("url", ""),
                    summary=story.get("summary"),
                    source=story.get("source")
                )
                story_copy = story.copy()
                story_copy["section"] = result["section"]
                story_copy["confidence"] = result["confidence"]
                results.append(story_copy)

    return results


def select_best_headline(headlines: list[str]) -> str:
    """
    Given multiple headlines for the same story, select the best one.

    Args:
        headlines: List of headlines from different outlets

    Returns:
        The best headline (clear, accurate, not clickbaity)
    """
    if len(headlines) == 1:
        return headlines[0]

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    headlines_text = "\n".join([f"{i+1}. {h}" for i, h in enumerate(headlines)])

    prompt = f"""Select the best headline from these options covering the same story:

{headlines_text}

Choose the headline that:
- Best captures the essence of the story
- Is clear and informative
- Is NOT clickbaity or hyperbolic
- Uses appropriate tone

Respond with just the number of the best headline."""

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text.strip()
        # Extract number
        num = int("".join(c for c in response if c.isdigit()))
        if 1 <= num <= len(headlines):
            return headlines[num - 1]
    except:
        pass

    # Fallback: return first headline
    return headlines[0]


if __name__ == "__main__":
    import sys

    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    # Test classification
    test_stories = [
        {
            "headline": "Murphy signs bill expanding offshore wind development in New Jersey",
            "url": "https://example.com/1",
            "source": "NJ Spotlight"
        },
        {
            "headline": "Jersey City school board approves $1.2 billion budget",
            "url": "https://example.com/2",
            "source": "NJ.com"
        },
        {
            "headline": "New ramen shop opens in Montclair, draws crowds",
            "url": "https://example.com/3",
            "source": "Montclair Local"
        },
        {
            "headline": "NJ Transit fares to increase 15% starting July 1",
            "url": "https://example.com/4",
            "source": "NorthJersey.com"
        }
    ]

    print("=" * 60)
    print("CLASSIFIER TEST")
    print("=" * 60)

    results = classify_stories_batch(test_stories)

    for story in results:
        print(f"\n{story['source']}: {story['headline'][:50]}...")
        print(f"  → Section: {story['section']} (confidence: {story.get('confidence', 'N/A')})")
