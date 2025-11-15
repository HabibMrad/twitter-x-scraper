"""Twitter scraping functionality using ntscraper."""

import logging
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path
from ntscraper import Nitter
from tqdm import tqdm

from .config import Config

logger = logging.getLogger(__name__)


class TwitterScraper:
    """Scrapes Twitter/X account tweets using ntscraper."""

    def __init__(self):
        """Initialize the scraper."""
        self.scraper = Nitter(log_level=1)
        self.tweets_data: List[Dict[str, Any]] = []

    def scrape_user_tweets(
        self,
        username: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        days: Optional[int] = None,
        exclude_retweets: bool = False,
        include_replies: bool = False,
        max_tweets: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Scrape tweets from a Twitter user.

        Args:
            username: Twitter username (with or without @)
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            days: Alternative to date range - last N days
            exclude_retweets: Skip retweets
            include_replies: Include reply threads
            max_tweets: Maximum number of tweets to fetch

        Returns:
            List of tweet dictionaries with full data
        """
        # Clean username
        username = username.lstrip('@')

        # Calculate date range
        if days:
            to_date = datetime.now().strftime('%Y-%m-%d')
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        logger.info(f"Scraping tweets from @{username}")
        logger.info(f"Date range: {from_date} to {to_date}")

        try:
            # Fetch tweets using ntscraper
            logger.info("Fetching tweets...")
            tweets = self.scraper.get_tweets(username, mode='user', number=max_tweets)

            if not tweets or 'tweets' not in tweets:
                logger.warning(f"No tweets found for @{username}")
                return []

            all_tweets = []
            raw_tweets = tweets.get('tweets', [])

            logger.info(f"Processing {len(raw_tweets)} tweets...")

            for tweet in tqdm(raw_tweets, desc="Processing tweets"):
                try:
                    # Parse tweet data
                    tweet_data = self._parse_tweet(tweet, username)

                    # Apply filters
                    if from_date or to_date:
                        tweet_date = self._parse_tweet_date(tweet_data.get('date', ''))
                        if tweet_date:
                            if from_date and tweet_date < datetime.strptime(from_date, '%Y-%m-%d'):
                                continue
                            if to_date and tweet_date > datetime.strptime(to_date, '%Y-%m-%d'):
                                continue

                    # Filter retweets
                    if exclude_retweets and tweet_data.get('is_retweet', False):
                        continue

                    all_tweets.append(tweet_data)

                    # Fetch replies if requested
                    if include_replies and tweet_data.get('replies_count', 0) > 0:
                        replies = self._fetch_replies(tweet_data.get('link', ''))
                        tweet_data['replies'] = replies

                    time.sleep(Config.RATE_LIMIT_DELAY)

                except Exception as e:
                    logger.error(f"Error processing tweet: {e}")
                    continue

            self.tweets_data = all_tweets
            logger.info(f"Successfully scraped {len(all_tweets)} tweets")

            # Save raw data
            self._save_raw_data(username, all_tweets)

            return all_tweets

        except Exception as e:
            logger.error(f"Error scraping tweets: {e}")
            raise

    def _parse_tweet(self, tweet: Dict[str, Any], username: str) -> Dict[str, Any]:
        """
        Parse raw tweet data into structured format.

        Args:
            tweet: Raw tweet data from ntscraper
            username: Twitter username

        Returns:
            Structured tweet dictionary
        """
        return {
            'id': tweet.get('tweet-id', ''),
            'author': {
                'name': tweet.get('name', username),
                'username': username,
                'profile_image': tweet.get('profile-image', '')
            },
            'text': tweet.get('text', ''),
            'date': tweet.get('date', ''),
            'timestamp': self._parse_tweet_date(tweet.get('date', '')),
            'link': tweet.get('link', ''),
            'is_retweet': tweet.get('is-retweet', False),
            'is_pinned': tweet.get('is-pinned', False),
            'stats': {
                'likes': self._parse_number(tweet.get('likes', '0')),
                'retweets': self._parse_number(tweet.get('retweets', '0')),
                'quotes': self._parse_number(tweet.get('quotes', '0')),
                'replies': self._parse_number(tweet.get('comments', '0'))
            },
            'media': self._parse_media(tweet),
            'hashtags': tweet.get('hashtags', []),
            'mentions': tweet.get('mentions', []),
            'replies_count': self._parse_number(tweet.get('comments', '0')),
            'replies': []
        }

    def _parse_media(self, tweet: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Extract media (images/videos) from tweet.

        Args:
            tweet: Raw tweet data

        Returns:
            List of media items
        """
        media = []

        # Images
        if 'photos' in tweet and tweet['photos']:
            for photo_url in tweet['photos']:
                media.append({
                    'type': 'image',
                    'url': photo_url
                })

        # Videos
        if 'videos' in tweet and tweet['videos']:
            for video_url in tweet['videos']:
                media.append({
                    'type': 'video',
                    'url': video_url
                })

        return media

    def _parse_tweet_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse tweet date string to datetime object.

        Args:
            date_str: Date string from tweet

        Returns:
            Datetime object or None
        """
        if not date_str:
            return None

        try:
            # Try multiple date formats
            formats = [
                '%b %d, %Y · %I:%M %p %Z',
                '%b %d, %Y',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d'
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue

            return None
        except Exception as e:
            logger.debug(f"Could not parse date '{date_str}': {e}")
            return None

    def _parse_number(self, num_str: str) -> int:
        """
        Parse number string (handles K, M suffixes).

        Args:
            num_str: Number string (e.g., '1.2K', '5M')

        Returns:
            Integer value
        """
        if not num_str or num_str == '0':
            return 0

        try:
            num_str = str(num_str).strip().upper()

            if 'K' in num_str:
                return int(float(num_str.replace('K', '')) * 1000)
            elif 'M' in num_str:
                return int(float(num_str.replace('M', '')) * 1000000)
            else:
                return int(num_str)
        except (ValueError, AttributeError):
            return 0

    def _fetch_replies(self, tweet_url: str) -> List[Dict[str, Any]]:
        """
        Fetch replies to a tweet (recursive thread fetching).

        Args:
            tweet_url: URL of the tweet

        Returns:
            List of reply tweet dictionaries
        """
        # Note: ntscraper has limited reply fetching
        # This is a placeholder for future enhancement
        replies = []

        try:
            # This would require additional implementation
            # For now, return empty list
            logger.debug(f"Reply fetching not fully implemented for {tweet_url}")
        except Exception as e:
            logger.error(f"Error fetching replies: {e}")

        return replies

    def _save_raw_data(self, username: str, tweets: List[Dict[str, Any]]) -> None:
        """
        Save raw tweet data to JSON file.

        Args:
            username: Twitter username
            tweets: List of tweet dictionaries
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = Config.DATA_DIR / f"{username}_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'username': username,
                    'scraped_at': datetime.now().isoformat(),
                    'tweet_count': len(tweets),
                    'tweets': tweets
                }, f, indent=2, ensure_ascii=False)

            logger.info(f"Raw data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving raw data: {e}")
