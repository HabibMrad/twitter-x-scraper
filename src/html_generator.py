"""HTML report generation with professional styling."""

import logging
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import base64
import json

logger = logging.getLogger(__name__)


class HTMLGenerator:
    """Generates self-contained HTML reports from tweet data."""

    def __init__(self):
        """Initialize the HTML generator."""
        self.tweets: List[Dict[str, Any]] = []
        self.username: str = ""

    def generate_html(
        self,
        tweets: List[Dict[str, Any]],
        username: str,
        output_file: Path,
        date_range: str = ""
    ) -> None:
        """
        Generate a self-contained HTML file with all tweet data.

        Args:
            tweets: List of tweet dictionaries
            username: Twitter username
            output_file: Path to output HTML file
            date_range: Date range string for display
        """
        self.tweets = tweets
        self.username = username

        logger.info(f"Generating HTML report for {len(tweets)} tweets...")

        # Generate HTML content
        html_content = self._build_html(date_range)

        # Write to file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"HTML report saved to {output_file}")
        except Exception as e:
            logger.error(f"Error writing HTML file: {e}")
            raise

    def _build_html(self, date_range: str) -> str:
        """
        Build complete HTML document.

        Args:
            date_range: Date range string

        Returns:
            Complete HTML string
        """
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@{self.username} - Tweet Analysis Report</title>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    <div class="theme-toggle">
        <button id="themeToggle" onclick="toggleTheme()">
            <span class="dark-icon">🌙</span>
            <span class="light-icon">☀️</span>
        </button>
    </div>

    <div class="container">
        <header class="header">
            <h1>Tweet Analysis Report</h1>
            <div class="header-info">
                <div class="username">@{self.username}</div>
                {f'<div class="date-range">{date_range}</div>' if date_range else ''}
                <div class="tweet-count">{len(self.tweets)} tweets</div>
                <div class="generated-at">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
        </header>

        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search tweets..." onkeyup="filterTweets()">
            </div>
            <div class="filters">
                <label>
                    <input type="checkbox" id="filterRetweets" onchange="filterTweets()">
                    Hide Retweets
                </label>
                <label>
                    <input type="checkbox" id="filterMedia" onchange="filterTweets()">
                    Media Only
                </label>
                <label>
                    <select id="sortOrder" onchange="sortTweets()">
                        <option value="newest">Newest First</option>
                        <option value="oldest">Oldest First</option>
                        <option value="most-liked">Most Liked</option>
                        <option value="most-retweeted">Most Retweeted</option>
                    </select>
                </label>
            </div>
        </div>

        <div class="stats-summary">
            <div class="stat-card">
                <div class="stat-label">Total Tweets</div>
                <div class="stat-value" id="totalTweets">{len(self.tweets)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Likes</div>
                <div class="stat-value" id="totalLikes">{self._calculate_total_likes()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Retweets</div>
                <div class="stat-value" id="totalRetweets">{self._calculate_total_retweets()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Engagement</div>
                <div class="stat-value" id="avgEngagement">{self._calculate_avg_engagement()}</div>
            </div>
        </div>

        <div class="tweets-container" id="tweetsContainer">
            {self._build_tweets_html()}
        </div>
    </div>

    <script>
        {self._get_javascript()}
    </script>
</body>
</html>"""

    def _get_css(self) -> str:
        """Get CSS styles for the HTML document."""
        return """
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-tertiary: #e9ecef;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --border-color: #dee2e6;
            --accent-color: #0066cc;
            --accent-hover: #0052a3;
            --retweet-color: #17bf63;
            --like-color: #e0245e;
            --shadow: rgba(0, 0, 0, 0.1);
        }

        [data-theme="dark"] {
            --bg-primary: #15202b;
            --bg-secondary: #192734;
            --bg-tertiary: #22303c;
            --text-primary: #ffffff;
            --text-secondary: #8899a6;
            --border-color: #38444d;
            --shadow: rgba(255, 255, 255, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }

        #themeToggle {
            background: var(--bg-primary);
            border: 2px solid var(--border-color);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
            box-shadow: 0 2px 8px var(--shadow);
        }

        #themeToggle:hover {
            transform: scale(1.1);
        }

        [data-theme="dark"] .dark-icon {
            display: none;
        }

        [data-theme="light"] .light-icon,
        .light-icon {
            display: none;
        }

        [data-theme="dark"] .light-icon {
            display: inline;
        }

        .header {
            background: var(--bg-primary);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px var(--shadow);
        }

        .header h1 {
            font-size: 32px;
            margin-bottom: 15px;
            color: var(--text-primary);
        }

        .header-info {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            font-size: 14px;
            color: var(--text-secondary);
        }

        .username {
            font-size: 20px;
            font-weight: bold;
            color: var(--accent-color);
        }

        .controls {
            background: var(--bg-primary);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px var(--shadow);
        }

        .search-box {
            margin-bottom: 15px;
        }

        .search-box input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-size: 16px;
            background: var(--bg-secondary);
            color: var(--text-primary);
            transition: border-color 0.3s;
        }

        .search-box input:focus {
            outline: none;
            border-color: var(--accent-color);
        }

        .filters {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            align-items: center;
        }

        .filters label {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            font-size: 14px;
        }

        .filters input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }

        .filters select {
            padding: 8px 12px;
            border: 2px solid var(--border-color);
            border-radius: 6px;
            background: var(--bg-secondary);
            color: var(--text-primary);
            cursor: pointer;
            font-size: 14px;
        }

        .stats-summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: var(--bg-primary);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px var(--shadow);
            text-align: center;
        }

        .stat-label {
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 8px;
        }

        .stat-value {
            font-size: 28px;
            font-weight: bold;
            color: var(--accent-color);
        }

        .tweets-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .tweet {
            background: var(--bg-primary);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px var(--shadow);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .tweet:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px var(--shadow);
        }

        .tweet-header {
            display: flex;
            align-items: flex-start;
            margin-bottom: 15px;
        }

        .tweet-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            margin-right: 12px;
            background: var(--bg-tertiary);
        }

        .tweet-author {
            flex: 1;
        }

        .tweet-author-name {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 2px;
        }

        .tweet-author-username {
            color: var(--text-secondary);
            font-size: 14px;
        }

        .tweet-badges {
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }

        .badge {
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
        }

        .badge-retweet {
            background: rgba(23, 191, 99, 0.1);
            color: var(--retweet-color);
        }

        .badge-pinned {
            background: rgba(0, 102, 204, 0.1);
            color: var(--accent-color);
        }

        .tweet-content {
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 15px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .tweet-content a {
            color: var(--accent-color);
            text-decoration: none;
        }

        .tweet-content a:hover {
            text-decoration: underline;
        }

        .tweet-media {
            margin-bottom: 15px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }

        .tweet-media img {
            width: 100%;
            border-radius: 8px;
            cursor: pointer;
            transition: opacity 0.2s;
        }

        .tweet-media img:hover {
            opacity: 0.9;
        }

        .tweet-media video {
            width: 100%;
            border-radius: 8px;
        }

        .tweet-stats {
            display: flex;
            gap: 20px;
            padding-top: 12px;
            border-top: 1px solid var(--border-color);
            font-size: 14px;
            color: var(--text-secondary);
        }

        .tweet-stat {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .tweet-stat-icon {
            font-size: 16px;
        }

        .tweet-date {
            margin-top: 10px;
            font-size: 13px;
            color: var(--text-secondary);
        }

        .tweet-link {
            display: inline-block;
            margin-top: 8px;
            color: var(--accent-color);
            font-size: 13px;
            text-decoration: none;
        }

        .tweet-link:hover {
            text-decoration: underline;
        }

        .no-results {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
            font-size: 18px;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }

            .header h1 {
                font-size: 24px;
            }

            .header-info {
                flex-direction: column;
                gap: 10px;
            }

            .filters {
                flex-direction: column;
                align-items: flex-start;
            }

            .stats-summary {
                grid-template-columns: 1fr;
            }

            .tweet-media {
                grid-template-columns: 1fr;
            }
        }
        """

    def _build_tweets_html(self) -> str:
        """Build HTML for all tweets."""
        if not self.tweets:
            return '<div class="no-results">No tweets found.</div>'

        tweets_html = []
        for tweet in self.tweets:
            tweets_html.append(self._build_tweet_html(tweet))

        return '\n'.join(tweets_html)

    def _build_tweet_html(self, tweet: Dict[str, Any]) -> str:
        """Build HTML for a single tweet."""
        author = tweet.get('author', {})
        stats = tweet.get('stats', {})
        media = tweet.get('media', [])

        # Build badges
        badges = []
        if tweet.get('is_retweet'):
            badges.append('<span class="badge badge-retweet">Retweet</span>')
        if tweet.get('is_pinned'):
            badges.append('<span class="badge badge-pinned">Pinned</span>')

        badges_html = f'<div class="tweet-badges">{"".join(badges)}</div>' if badges else ''

        # Build media HTML
        media_html = ''
        if media:
            media_items = []
            for item in media:
                if item['type'] == 'image':
                    media_items.append(f'<img src="{item["url"]}" alt="Tweet image" loading="lazy">')
                elif item['type'] == 'video':
                    media_items.append(f'<video src="{item["url"]}" controls></video>')

            if media_items:
                media_html = f'<div class="tweet-media">{"".join(media_items)}</div>'

        # Format text with links
        text = self._format_tweet_text(tweet.get('text', ''))

        return f"""
        <div class="tweet"
             data-is-retweet="{str(tweet.get('is_retweet', False)).lower()}"
             data-has-media="{str(bool(media)).lower()}"
             data-likes="{stats.get('likes', 0)}"
             data-retweets="{stats.get('retweets', 0)}"
             data-date="{tweet.get('date', '')}">
            <div class="tweet-header">
                {f'<img class="tweet-avatar" src="{author.get("profile_image", "")}" alt="Profile">' if author.get('profile_image') else '<div class="tweet-avatar"></div>'}
                <div class="tweet-author">
                    <div class="tweet-author-name">{author.get('name', 'Unknown')}</div>
                    <div class="tweet-author-username">@{author.get('username', '')}</div>
                    {badges_html}
                </div>
            </div>
            <div class="tweet-content">{text}</div>
            {media_html}
            <div class="tweet-stats">
                <div class="tweet-stat">
                    <span class="tweet-stat-icon">❤️</span>
                    <span>{self._format_number(stats.get('likes', 0))}</span>
                </div>
                <div class="tweet-stat">
                    <span class="tweet-stat-icon">🔁</span>
                    <span>{self._format_number(stats.get('retweets', 0))}</span>
                </div>
                <div class="tweet-stat">
                    <span class="tweet-stat-icon">💬</span>
                    <span>{self._format_number(stats.get('replies', 0))}</span>
                </div>
                <div class="tweet-stat">
                    <span class="tweet-stat-icon">💭</span>
                    <span>{self._format_number(stats.get('quotes', 0))}</span>
                </div>
            </div>
            <div class="tweet-date">{tweet.get('date', 'Unknown date')}</div>
            {f'<a href="{tweet.get("link", "")}" class="tweet-link" target="_blank">View on Twitter →</a>' if tweet.get('link') else ''}
        </div>
        """

    def _format_tweet_text(self, text: str) -> str:
        """Format tweet text with clickable links, mentions, and hashtags."""
        import re

        # Convert URLs to links
        text = re.sub(
            r'(https?://[^\s]+)',
            r'<a href="\1" target="_blank">\1</a>',
            text
        )

        # Convert mentions to links
        text = re.sub(
            r'@(\w+)',
            r'<a href="https://twitter.com/\1" target="_blank">@\1</a>',
            text
        )

        # Convert hashtags to links
        text = re.sub(
            r'#(\w+)',
            r'<a href="https://twitter.com/hashtag/\1" target="_blank">#\1</a>',
            text
        )

        return text

    def _format_number(self, num: int) -> str:
        """Format large numbers with K/M suffixes."""
        if num >= 1000000:
            return f"{num / 1000000:.1f}M"
        elif num >= 1000:
            return f"{num / 1000:.1f}K"
        else:
            return str(num)

    def _calculate_total_likes(self) -> str:
        """Calculate total likes across all tweets."""
        total = sum(tweet.get('stats', {}).get('likes', 0) for tweet in self.tweets)
        return self._format_number(total)

    def _calculate_total_retweets(self) -> str:
        """Calculate total retweets across all tweets."""
        total = sum(tweet.get('stats', {}).get('retweets', 0) for tweet in self.tweets)
        return self._format_number(total)

    def _calculate_avg_engagement(self) -> str:
        """Calculate average engagement per tweet."""
        if not self.tweets:
            return "0"

        total_engagement = sum(
            tweet.get('stats', {}).get('likes', 0) +
            tweet.get('stats', {}).get('retweets', 0) +
            tweet.get('stats', {}).get('replies', 0)
            for tweet in self.tweets
        )

        avg = total_engagement / len(self.tweets)
        return self._format_number(int(avg))

    def _get_javascript(self) -> str:
        """Get JavaScript for interactive features."""
        return """
        // Theme toggle
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }

        // Load saved theme
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', savedTheme);
        });

        // Search and filter
        function filterTweets() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const hideRetweets = document.getElementById('filterRetweets').checked;
            const mediaOnly = document.getElementById('filterMedia').checked;
            const tweets = document.querySelectorAll('.tweet');
            let visibleCount = 0;

            tweets.forEach(tweet => {
                const text = tweet.querySelector('.tweet-content').textContent.toLowerCase();
                const isRetweet = tweet.getAttribute('data-is-retweet') === 'true';
                const hasMedia = tweet.getAttribute('data-has-media') === 'true';

                let shouldShow = true;

                if (searchTerm && !text.includes(searchTerm)) {
                    shouldShow = false;
                }

                if (hideRetweets && isRetweet) {
                    shouldShow = false;
                }

                if (mediaOnly && !hasMedia) {
                    shouldShow = false;
                }

                tweet.style.display = shouldShow ? 'block' : 'none';
                if (shouldShow) visibleCount++;
            });

            // Show no results message
            const container = document.getElementById('tweetsContainer');
            let noResults = container.querySelector('.no-results');

            if (visibleCount === 0) {
                if (!noResults) {
                    noResults = document.createElement('div');
                    noResults.className = 'no-results';
                    noResults.textContent = 'No tweets match your filters.';
                    container.appendChild(noResults);
                }
            } else if (noResults) {
                noResults.remove();
            }
        }

        // Sort tweets
        function sortTweets() {
            const container = document.getElementById('tweetsContainer');
            const tweets = Array.from(container.querySelectorAll('.tweet'));
            const sortOrder = document.getElementById('sortOrder').value;

            tweets.sort((a, b) => {
                switch (sortOrder) {
                    case 'oldest':
                        return new Date(a.getAttribute('data-date')) - new Date(b.getAttribute('data-date'));
                    case 'newest':
                        return new Date(b.getAttribute('data-date')) - new Date(a.getAttribute('data-date'));
                    case 'most-liked':
                        return parseInt(b.getAttribute('data-likes')) - parseInt(a.getAttribute('data-likes'));
                    case 'most-retweeted':
                        return parseInt(b.getAttribute('data-retweets')) - parseInt(a.getAttribute('data-retweets'));
                    default:
                        return 0;
                }
            });

            tweets.forEach(tweet => container.appendChild(tweet));
        }

        // Image click to enlarge (simple implementation)
        document.addEventListener('click', (e) => {
            if (e.target.tagName === 'IMG' && e.target.closest('.tweet-media')) {
                window.open(e.target.src, '_blank');
            }
        });
        """
