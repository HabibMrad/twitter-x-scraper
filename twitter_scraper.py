#!/usr/bin/env python3
"""Twitter/X Scraper CLI Tool - Main entry point."""

import sys
import logging
from pathlib import Path
from datetime import datetime
import click

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.config import Config
from src.scraper import TwitterScraper
from src.html_generator import HTMLGenerator

logger = logging.getLogger(__name__)


@click.command()
@click.argument('username')
@click.option('--from', 'from_date', help='Start date (YYYY-MM-DD)')
@click.option('--to', 'to_date', help='End date (YYYY-MM-DD)')
@click.option('--days', type=int, help='Alternative to date range - last N days')
@click.option('--output', default='webpage.html', help='Output HTML file name')
@click.option('--exclude-retweets', is_flag=True, help='Only fetch original content')
@click.option('--include-replies', is_flag=True, help='Fetch reply threads')
@click.option('--max-tweets', type=int, default=100, help='Maximum tweets to fetch')
def main(
    username: str,
    from_date: str,
    to_date: str,
    days: int,
    output: str,
    exclude_retweets: bool,
    include_replies: bool,
    max_tweets: int
):
    """
    Scrape Twitter/X account tweets and generate HTML analysis page.

    USAGE:
        python twitter_scraper.py @username --from 2024-11-12 --to 2024-11-16

    EXAMPLES:
        python twitter_scraper.py @elonmusk --days 7
        python twitter_scraper.py @openai --from 2024-11-01 --to 2024-11-15 --exclude-retweets
        python twitter_scraper.py @github --days 30 --output github_tweets.html
    """
    try:
        # Display banner
        click.echo("=" * 60)
        click.echo("Twitter/X Scraper CLI Tool")
        click.echo("=" * 60)
        click.echo()

        # Validate inputs
        if not from_date and not to_date and not days:
            click.echo("⚠️  No date range specified. Using last 7 days as default.")
            days = 7

        if (from_date or to_date) and days:
            click.echo("❌ Error: Cannot use both --from/--to and --days options together.")
            sys.exit(1)

        # Initialize scraper
        click.echo(f"🔍 Initializing scraper for @{username.lstrip('@')}...")
        scraper = TwitterScraper()

        # Scrape tweets
        click.echo("📥 Fetching tweets... This may take a few minutes.")
        click.echo()

        tweets = scraper.scrape_user_tweets(
            username=username,
            from_date=from_date,
            to_date=to_date,
            days=days,
            exclude_retweets=exclude_retweets,
            include_replies=include_replies,
            max_tweets=max_tweets
        )

        if not tweets:
            click.echo("❌ No tweets found for the specified criteria.")
            sys.exit(0)

        click.echo()
        click.echo(f"✅ Successfully scraped {len(tweets)} tweets!")
        click.echo()

        # Generate HTML report
        click.echo("📄 Generating HTML report...")

        # Determine output path
        if not output.endswith('.html'):
            output += '.html'

        output_path = Config.OUTPUT_DIR / output

        # Build date range string
        date_range = ""
        if days:
            date_range = f"Last {days} days"
        elif from_date and to_date:
            date_range = f"{from_date} to {to_date}"
        elif from_date:
            date_range = f"From {from_date}"
        elif to_date:
            date_range = f"Until {to_date}"

        # Generate HTML
        html_generator = HTMLGenerator()
        html_generator.generate_html(
            tweets=tweets,
            username=username.lstrip('@'),
            output_file=output_path,
            date_range=date_range
        )

        click.echo()
        click.echo("=" * 60)
        click.echo("✨ Success!")
        click.echo("=" * 60)
        click.echo()
        click.echo(f"📊 Tweets scraped: {len(tweets)}")
        click.echo(f"📁 HTML report: {output_path}")
        click.echo(f"💾 Raw data saved in: {Config.DATA_DIR}")
        click.echo()
        click.echo("🌐 Open the HTML file in your browser to view the analysis!")
        click.echo()

    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Scraping interrupted by user.")
        sys.exit(1)

    except Exception as e:
        logger.exception("Fatal error occurred")
        click.echo(f"\n❌ Error: {str(e)}")
        click.echo("\n💡 Troubleshooting tips:")
        click.echo("   1. Check if the username is correct")
        click.echo("   2. Verify your internet connection")
        click.echo("   3. Check the log file: scraper.log")
        click.echo("   4. Try with a smaller date range")
        sys.exit(1)


if __name__ == '__main__':
    main()
