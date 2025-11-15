#!/usr/bin/env python3
"""Demo Twitter/X Scraper - Generates mock data for testing."""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
import click

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.config import Config
from src.html_generator import HTMLGenerator


def generate_mock_tweets(username: str, num_tweets: int = 20, days: int = 7) -> list:
    """Generate mock tweet data for demonstration."""
    tweets = []

    sample_texts = [
        "Excited to announce our latest AI research breakthrough! 🚀",
        "Check out our new blog post on machine learning advancements.",
        "We're hiring! Join our team of amazing engineers.",
        "Just published a new paper on transformer architectures.",
        "Thank you to our amazing community for all the support!",
        "New product feature launching next week. Stay tuned!",
        "Interesting insights from today's conference.",
        "Our open-source project just hit 10k stars on GitHub!",
        "Collaborating with @research_lab on exciting new projects.",
        "Behind the scenes look at our development process.",
        "Important update regarding our API changes.",
        "We're thrilled to share our Q4 results with you.",
        "Join us for our upcoming webinar on AI ethics.",
        "Happy to announce our partnership with @tech_company!",
        "Check out this fascinating research from our team.",
        "New tutorial series starting next Monday!",
        "Celebrating our 5-year anniversary today!",
        "Important security update - please read.",
        "Our CEO's thoughts on the future of technology.",
        "Amazing work by our engineering team this quarter!"
    ]

    hashtags_pool = [
        ['AI', 'MachineLearning'],
        ['Tech', 'Innovation'],
        ['OpenSource', 'Coding'],
        ['DataScience', 'Analytics'],
        ['Research', 'Science'],
        []
    ]

    for i in range(num_tweets):
        # Random date within the last N days
        days_ago = random.randint(0, days)
        hours_ago = random.randint(0, 23)
        tweet_date = datetime.now() - timedelta(days=days_ago, hours=hours_ago)

        # Random engagement metrics
        likes = random.randint(10, 5000)
        retweets = random.randint(5, 1000)
        replies = random.randint(0, 300)
        quotes = random.randint(0, 150)

        # Random text and hashtags
        text = random.choice(sample_texts)
        hashtags = random.choice(hashtags_pool)

        # Random media (30% chance)
        media = []
        if random.random() < 0.3:
            media.append({
                'type': 'image',
                'url': f'https://via.placeholder.com/600x400?text=Sample+Image+{i+1}'
            })

        tweet = {
            'id': str(1000000 + i),
            'author': {
                'name': username.title(),
                'username': username,
                'profile_image': f'https://via.placeholder.com/48x48?text={username[0].upper()}'
            },
            'text': text,
            'date': tweet_date.strftime('%b %d, %Y · %I:%M %p UTC'),
            'timestamp': tweet_date,
            'link': f'https://twitter.com/{username}/status/{1000000 + i}',
            'is_retweet': random.random() < 0.2,
            'is_pinned': i == 0 and random.random() < 0.3,
            'stats': {
                'likes': likes,
                'retweets': retweets,
                'quotes': quotes,
                'replies': replies
            },
            'media': media,
            'hashtags': hashtags,
            'mentions': [],
            'replies_count': replies,
            'replies': []
        }

        tweets.append(tweet)

    # Sort by date (newest first)
    tweets.sort(key=lambda x: x['timestamp'], reverse=True)

    return tweets


@click.command()
@click.argument('username')
@click.option('--days', type=int, default=7, help='Number of days of mock data')
@click.option('--output', default='demo_webpage.html', help='Output HTML file name')
@click.option('--max-tweets', type=int, default=20, help='Number of mock tweets to generate')
def main(username: str, days: int, output: str, max_tweets: int):
    """
    Generate a demo HTML report with mock tweet data.

    USAGE:
        python demo_scraper.py @username --days 7 --max-tweets 30

    EXAMPLES:
        python demo_scraper.py @openai --days 7
        python demo_scraper.py @elonmusk --days 14 --max-tweets 50
    """
    # Clean username
    username = username.lstrip('@')

    click.echo("=" * 60)
    click.echo("Twitter/X Scraper DEMO Mode")
    click.echo("=" * 60)
    click.echo()
    click.echo(f"[*] Generating mock data for @{username}...")
    click.echo(f"[*] Creating {max_tweets} tweets over {days} days...")
    click.echo()

    # Generate mock tweets
    tweets = generate_mock_tweets(username, max_tweets, days)

    click.echo(f"[+] Generated {len(tweets)} mock tweets!")
    click.echo()

    # Determine output path
    if not output.endswith('.html'):
        output += '.html'

    output_path = Config.OUTPUT_DIR / output

    # Build date range string
    date_range = f"Last {days} days (DEMO DATA)"

    # Generate HTML
    click.echo("[*] Generating HTML report...")
    html_generator = HTMLGenerator()
    html_generator.generate_html(
        tweets=tweets,
        username=username,
        output_file=output_path,
        date_range=date_range
    )

    click.echo()
    click.echo("=" * 60)
    click.echo("[+] Demo Report Generated Successfully!")
    click.echo("=" * 60)
    click.echo()
    click.echo(f"[*] Mock tweets: {len(tweets)}")
    click.echo(f"[*] HTML report: {output_path}")
    click.echo()
    click.echo("[!] NOTE: This is DEMO data with randomly generated content.")
    click.echo("[*] To scrape real tweets, use twitter_scraper.py with valid credentials.")
    click.echo()
    click.echo("[*] Open the HTML file in your browser to view the demo report!")
    click.echo()


if __name__ == '__main__':
    main()
