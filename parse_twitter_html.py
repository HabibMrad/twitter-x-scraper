#!/usr/bin/env python3
"""Parse Twitter/X HTML and generate beautiful report."""

import sys
import re
import json
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import click

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.config import Config
from src.html_generator import HTMLGenerator


def parse_twitter_html(html_file: Path) -> list:
    """
    Parse Twitter HTML file and extract tweet data.

    Args:
        html_file: Path to saved Twitter HTML file

    Returns:
        List of parsed tweet dictionaries
    """
    print(f"[*] Reading HTML file: {html_file}")

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    print(f"[*] File size: {len(html_content):,} characters")

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Try to extract from script tags (Twitter embeds data in JSON)
    tweets = []

    # Method 1: Look for JSON in script tags
    script_tags = soup.find_all('script')
    print(f"[*] Found {len(script_tags)} script tags")

    for script in script_tags:
        if script.string and 'tweet' in script.string.lower():
            try:
                # Try to find JSON data
                json_match = re.search(r'\{.*"tweet".*\}', script.string, re.DOTALL)
                if json_match:
                    print("[+] Found potential tweet data in script tag")
                    # Note: This is complex and may need adjustment based on actual HTML structure
            except:
                pass

    # Method 2: Parse visible tweet elements (fallback)
    print("[*] Looking for tweet articles...")
    articles = soup.find_all('article', attrs={'data-testid': 'tweet'})

    if not articles:
        # Try alternative selectors
        articles = soup.find_all('article')

    print(f"[*] Found {len(articles)} tweet articles")

    for idx, article in enumerate(articles):
        try:
            tweet_data = parse_tweet_article(article, idx)
            if tweet_data:
                tweets.append(tweet_data)
                print(f"[+] Parsed tweet {idx + 1}/{len(articles)}")
        except Exception as e:
            print(f"[!] Error parsing tweet {idx}: {e}")
            continue

    print(f"[+] Successfully parsed {len(tweets)} tweets")
    return tweets


def parse_tweet_article(article, index: int) -> dict:
    """Parse a single tweet article element."""

    # Extract text content
    text_elements = article.find_all('div', attrs={'data-testid': 'tweetText'})
    if not text_elements:
        text_elements = article.find_all('div', lang=True)

    text = ""
    if text_elements:
        text = text_elements[0].get_text(strip=True)

    # Extract author info
    author_name = "Unknown"
    author_username = "unknown"

    # Look for username links
    links = article.find_all('a', href=True)
    for link in links:
        href = link.get('href', '')
        if href.startswith('/') and not any(x in href for x in ['status', 'photo', 'video']):
            username_match = re.match(r'/([^/]+)$', href)
            if username_match:
                author_username = username_match.group(1)
                author_name = link.get_text(strip=True) or author_username
                break

    # Extract timestamp
    time_elements = article.find_all('time')
    date_str = "Unknown"
    timestamp = None

    if time_elements:
        time_elem = time_elements[0]
        date_str = time_elem.get('datetime', time_elem.get_text(strip=True))
        try:
            if 'T' in date_str:  # ISO format
                timestamp = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                date_str = timestamp.strftime('%b %d, %Y · %I:%M %p UTC')
        except:
            pass

    # Extract engagement metrics
    likes = 0
    retweets = 0
    replies = 0
    quotes = 0
    views = 0

    # Look for buttons with aria-label
    buttons = article.find_all('button')
    for button in buttons:
        aria_label = button.get('aria-label', '').lower()

        # Extract numbers from aria labels like "123 Likes"
        if 'like' in aria_label and 'unlike' not in aria_label:
            match = re.search(r'([\d,]+)', aria_label)
            if match:
                likes = int(match.group(1).replace(',', ''))

        if 'retweet' in aria_label or 'repost' in aria_label:
            match = re.search(r'([\d,]+)', aria_label)
            if match:
                retweets = int(match.group(1).replace(',', ''))

        if 'repl' in aria_label:
            match = re.search(r'([\d,]+)', aria_label)
            if match:
                replies = int(match.group(1).replace(',', ''))

        if 'quote' in aria_label:
            match = re.search(r'([\d,]+)', aria_label)
            if match:
                quotes = int(match.group(1).replace(',', ''))

    # Look for view count
    view_elements = article.find_all(attrs={'data-testid': 'app-text-transition-container'})
    for elem in view_elements:
        text = elem.get_text()
        if 'view' in text.lower() or 'K' in text or 'M' in text:
            match = re.search(r'([\d.]+)([KM])?', text)
            if match:
                num = float(match.group(1))
                suffix = match.group(2)
                if suffix == 'K':
                    views = int(num * 1000)
                elif suffix == 'M':
                    views = int(num * 1000000)
                else:
                    views = int(num)

    # Also check for visible text with numbers (backup method)
    all_text = article.get_text()

    # Extract images and videos
    media = []

    # Extract images
    images = article.find_all('img', src=True)
    for img in images:
        src = img.get('src', '')
        if 'media' in src or 'pbs.twimg.com' in src:
            # Skip profile images and emoji
            if 'profile' not in src.lower() and 'emoji' not in src.lower():
                media.append({
                    'type': 'image',
                    'url': src
                })

    # Extract videos
    videos = article.find_all('video')
    for video in videos:
        # Try to get video source
        poster = video.get('poster', '')
        if poster:
            media.append({
                'type': 'video',
                'url': poster  # Use poster as placeholder
            })

        # Look for source tags
        sources = video.find_all('source')
        for source in sources:
            src = source.get('src', '')
            if src:
                media[-1]['url'] = src  # Replace poster with actual video URL
                break

    # Extract profile image
    profile_image = ""
    for img in images:
        src = img.get('src', '')
        if 'profile' in src.lower() or 'profile_images' in src:
            profile_image = src
            break

    # Extract tweet link
    tweet_link = ""
    for link in links:
        href = link.get('href', '')
        if '/status/' in href:
            tweet_link = f"https://twitter.com{href}" if not href.startswith('http') else href
            break

    # Extract tweet ID from link
    tweet_id = str(index + 1000000)
    if tweet_link:
        id_match = re.search(r'/status/(\d+)', tweet_link)
        if id_match:
            tweet_id = id_match.group(1)

    # Detect retweets and quote tweets
    is_retweet = False
    is_quote = False

    # Look for retweet indicators
    all_article_text = article.get_text()
    if 'retweeted' in all_article_text.lower() or 'reposted' in all_article_text.lower():
        is_retweet = True

    # Look for quoted tweet (embedded article)
    quoted_articles = article.find_all('article')
    if len(quoted_articles) > 1:
        is_quote = True

    # Check for retweet icon or text
    retweet_elements = article.find_all(attrs={'data-testid': 'socialContext'})
    if retweet_elements:
        for elem in retweet_elements:
            elem_text = elem.get_text().lower()
            if 'retweet' in elem_text or 'repost' in elem_text:
                is_retweet = True
                break

    # Detect pinned tweet
    is_pinned = False
    if 'pinned' in all_article_text.lower():
        is_pinned = True

    return {
        'id': tweet_id,
        'author': {
            'name': author_name,
            'username': author_username,
            'profile_image': profile_image
        },
        'text': text,
        'date': date_str,
        'timestamp': timestamp or datetime.now(),
        'link': tweet_link,
        'is_retweet': is_retweet,
        'is_pinned': is_pinned,
        'stats': {
            'likes': likes,
            'retweets': retweets,
            'quotes': quotes,
            'replies': replies,
            'views': views
        },
        'media': media,
        'hashtags': re.findall(r'#(\w+)', text),
        'mentions': re.findall(r'@(\w+)', text),
        'replies_count': replies,
        'replies': []
    }


@click.command()
@click.argument('html_file', type=click.Path(exists=True))
@click.option('--output', default='parsed_tweets.html', help='Output HTML file name')
@click.option('--username', default='omarsar0', help='Twitter username')
def main(html_file: str, output: str, username: str):
    """
    Parse Twitter HTML file and generate beautiful report.

    USAGE:
        python parse_twitter_html.py twitter_omarsar0.html --output omarsar0_real.html

    EXAMPLES:
        python parse_twitter_html.py saved_page.html
        python parse_twitter_html.py twitter.html --output report.html --username elonmusk
    """
    print("=" * 60)
    print("Twitter HTML Parser")
    print("=" * 60)
    print()

    html_path = Path(html_file)

    # Parse the HTML
    tweets = parse_twitter_html(html_path)

    if not tweets:
        print("[X] No tweets found in HTML file!")
        print("[*] Tips:")
        print("   1. Make sure you scrolled down to load tweets")
        print("   2. Verify you copied the full HTML (right-click <html> tag)")
        print("   3. Save the file with .html extension")
        sys.exit(1)

    print()
    print(f"[+] Found {len(tweets)} tweets!")
    print()

    # Determine output path
    if not output.endswith('.html'):
        output += '.html'

    output_path = Config.OUTPUT_DIR / output

    # Generate HTML report
    print("[*] Generating HTML report...")
    html_generator = HTMLGenerator()
    html_generator.generate_html(
        tweets=tweets,
        username=username,
        output_file=output_path,
        date_range="Parsed from Twitter HTML"
    )

    print()
    print("=" * 60)
    print("[+] Success!")
    print("=" * 60)
    print()
    print(f"[*] Tweets parsed: {len(tweets)}")
    print(f"[*] HTML report: {output_path}")
    print()
    print("[*] Open the HTML file in your browser to view!")
    print()


if __name__ == '__main__':
    main()
