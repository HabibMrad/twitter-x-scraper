"""Twitter scraping functionality using multiple methods."""

import logging
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path
from tqdm import tqdm

from .config import Config

logger = logging.getLogger(__name__)


class TwitterScraper:
    """Scrapes Twitter/X account tweets using multiple fallback methods."""

    def __init__(self):
        """Initialize the scraper."""
        self.tweets_data: List[Dict[str, Any]] = []
        self.scraper_method = None
        self._initialize_scraper()

    def _initialize_scraper(self):
        """Try to initialize available scraping methods."""
        # Try snscrape first (most reliable)
        try:
            import snscrape.modules.twitter as sntwitter
            self.scraper_method = 'snscrape'
            logger.info("Using snscrape for scraping")
            return
        except ImportError:
            logger.debug("snscrape not available")

        # Try ntscraper as fallback
        try:
            from ntscraper import Nitter
            self.scraper = Nitter(log_level=1)
            self.scraper_method = 'ntscraper'
            logger.info("Using ntscraper for scraping")
            return
        except Exception as e:
            logger.debug(f"ntscraper not available: {e}")

        # If nothing works, raise error
        logger.error("No scraping method available. Please install snscrape or ntscraper")

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

        # Use appropriate scraping method
        if self.scraper_method == 'snscrape':
            return self._scrape_with_snscrape(
                username, from_date, to_date, exclude_retweets, max_tweets
            )
        elif self.scraper_method == 'ntscraper':
            return self._scrape_with_ntscraper(
                username, from_date, to_date, exclude_retweets, max_tweets
            )
        else:
            raise Exception("No scraping method available. Please install snscrape or ntscraper")

    def _scrape_with_snscrape(
        self,
        username: str,
        from_date: str,
        to_date: str,
        exclude_retweets: bool,
        max_tweets: int
    ) -> List[Dict[str, Any]]:
        """Scrape using snscrape."""
        import snscrape.modules.twitter as sntwitter

        logger.info("Fetching tweets with snscrape...")

        # Build query
        query = f"from:{username}"
        if from_date:
            query += f" since:{from_date}"
        if to_date:
            query += f" until:{to_date}"
        if exclude_retweets:
            query += " -filter:retweets"

        all_tweets = []

        try:
            # Scrape tweets
            scraper = sntwitter.TwitterSearchScraper(query)

            for i, tweet in enumerate(tqdm(scraper.get_items(), desc="Processing tweets", total=max_tweets)):
                if i >= max_tweets:
                    break

                # Parse tweet data
                tweet_data = self._parse_snscrape_tweet(tweet, username)
                all_tweets.append(tweet_data)

                time.sleep(Config.RATE_LIMIT_DELAY)

            self.tweets_data = all_tweets
            logger.info(f"Successfully scraped {len(all_tweets)} tweets")

            # Save raw data
            self._save_raw_data(username, all_tweets)

            return all_tweets

        except Exception as e:
            logger.error(f"Error scraping with snscrape: {e}")
            raise

    def _parse_snscrape_tweet(self, tweet: Any, username: str) -> Dict[str, Any]:
        """Parse snscrape tweet data."""
        media = []

        # Extract media
        if hasattr(tweet, 'media') and tweet.media:
            for item in tweet.media:
                if hasattr(item, 'thumbnailUrl'):
                    media.append({
                        'type': 'image',
                        'url': item.thumbnailUrl or item.fullUrl or ''
                    })
                elif hasattr(item, 'variants'):
                    # Video
                    video_url = item.variants[0].url if item.variants else ''
                    media.append({
                        'type': 'video',
                        'url': video_url
                    })

        return {
            'id': str(tweet.id),
            'author': {
                'name': tweet.user.displayname if hasattr(tweet, 'user') else username,
                'username': tweet.user.username if hasattr(tweet, 'user') else username,
                'profile_image': tweet.user.profileImageUrl if hasattr(tweet, 'user') else ''
            },
            'text': tweet.rawContent if hasattr(tweet, 'rawContent') else tweet.content,
            'date': tweet.date.strftime('%b %d, %Y · %I:%M %p UTC') if hasattr(tweet, 'date') else '',
            'timestamp': tweet.date if hasattr(tweet, 'date') else None,
            'link': tweet.url if hasattr(tweet, 'url') else '',
            'is_retweet': hasattr(tweet, 'retweetedTweet') and tweet.retweetedTweet is not None,
            'is_pinned': False,
            'stats': {
                'likes': tweet.likeCount if hasattr(tweet, 'likeCount') else 0,
                'retweets': tweet.retweetCount if hasattr(tweet, 'retweetCount') else 0,
                'quotes': tweet.quoteCount if hasattr(tweet, 'quoteCount') else 0,
                'replies': tweet.replyCount if hasattr(tweet, 'replyCount') else 0
            },
            'media': media,
            'hashtags': [tag for tag in tweet.hashtags] if hasattr(tweet, 'hashtags') and tweet.hashtags else [],
            'mentions': [mention.username for mention in tweet.mentionedUsers] if hasattr(tweet, 'mentionedUsers') and tweet.mentionedUsers else [],
            'replies_count': tweet.replyCount if hasattr(tweet, 'replyCount') else 0,
            'replies': []
        }

    def _scrape_with_ntscraper(
        self,
        username: str,
        from_date: str,
        to_date: str,
        exclude_retweets: bool,
        max_tweets: int
    ) -> List[Dict[str, Any]]:
        """Scrape using ntscraper (fallback method)."""
        logger.info("Fetching tweets with ntscraper...")

        try:
            # Fetch tweets using ntscraper
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
                    tweet_data = self._parse_ntscraper_tweet(tweet, username)

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
            logger.error(f"Error scraping with ntscraper: {e}")
            raise

    def _parse_ntscraper_tweet(self, tweet: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Parse ntscraper tweet data into structured format."""
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
            'media': media,
            'hashtags': tweet.get('hashtags', []),
            'mentions': tweet.get('mentions', []),
            'replies_count': self._parse_number(tweet.get('comments', '0')),
            'replies': []
        }

    def _parse_tweet_date(self, date_str: str) -> Optional[datetime]:
        """Parse tweet date string to datetime object."""
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
        """Parse number string (handles K, M suffixes)."""
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

    def _save_raw_data(self, username: str, tweets: List[Dict[str, Any]]) -> None:
        """Save raw tweet data to JSON file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = Config.DATA_DIR / f"{username}_{timestamp}.json"

        try:
            # Convert datetime objects to strings for JSON serialization
            tweets_serializable = []
            for tweet in tweets:
                tweet_copy = tweet.copy()
                if tweet_copy.get('timestamp') and isinstance(tweet_copy['timestamp'], datetime):
                    tweet_copy['timestamp'] = tweet_copy['timestamp'].isoformat()
                tweets_serializable.append(tweet_copy)

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'username': username,
                    'scraped_at': datetime.now().isoformat(),
                    'tweet_count': len(tweets),
                    'tweets': tweets_serializable
                }, f, indent=2, ensure_ascii=False)

            logger.info(f"Raw data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving raw data: {e}")
