"""Configuration management for Twitter scraper."""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration settings."""

    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    OUTPUT_DIR = BASE_DIR / "output"

    # Twitter API credentials (optional)
    TWITTER_BEARER_TOKEN: Optional[str] = os.getenv("TWITTER_BEARER_TOKEN")
    TWITTER_API_KEY: Optional[str] = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = os.getenv("TWITTER_API_SECRET")

    # Scraping configuration
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RATE_LIMIT_DELAY: int = int(os.getenv("RATE_LIMIT_DELAY", "2"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # User agent
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)

    @classmethod
    def setup_logging(cls) -> None:
        """Configure logging for the application."""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cls.BASE_DIR / 'scraper.log'),
                logging.StreamHandler()
            ]
        )


# Initialize configuration
Config.ensure_directories()
Config.setup_logging()
