# Installation Guide

## Important: Python Version Compatibility

**This tool works best with Python 3.9 - 3.11**

If you're using Python 3.13 (like you are), snscrape has compatibility issues. Here are your options:

### Option 1: Use Python 3.11 (Recommended)

1. **Install Python 3.11** from https://www.python.org/downloads/
2. **Create a virtual environment with Python 3.11**:
   ```bash
   py -3.11 -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Option 2: Use Alternative Scraping Methods

The tool is designed with fallback methods. If snscrape doesn't work:

#### Method A: Use Twitter API (Best Quality)
1. Get Twitter API credentials from https://developer.twitter.com
2. Add to `.env` file:
   ```
   TWITTER_BEARER_TOKEN=your_token_here
   TWITTER_API_KEY=your_key_here
   TWITTER_API_SECRET=your_secret_here
   ```
3. Install tweepy:
   ```bash
   pip install tweepy
   ```

#### Method B: Manual Installation of Compatible snscrape

Try installing an older, compatible version:
```bash
pip uninstall snscrape
pip install snscrape==0.6.2.20230320
```

### Option 3: Quick Test with Mock Data

For testing purposes, you can create a demo version with mock data:

```bash
python demo_scraper.py @username --days 7 --output demo.html
```

## Full Installation Steps (Python 3.11)

1. **Navigate to project directory**:
   ```bash
   cd twitter_scraper
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

6. **Test installation**:
   ```bash
   python twitter_scraper.py --help
   ```

## Troubleshooting

### Issue: "FileFinder object has no attribute 'find_module'"

**Cause**: Python 3.13 compatibility issue with snscraper

**Solution**: Use Python 3.9-3.11 OR install tweepy for API-based scraping:
```bash
pip install tweepy
```

### Issue: "Cannot choose from an empty sequence" (ntscraper)

**Cause**: Nitter instances are unavailable

**Solution**: Use snscrape or Twitter API instead

### Issue: Emojis not displaying in console

**Cause**: Windows console encoding

**Solution**: Already fixed in latest version - uses ASCII symbols instead

## Recommended Setup

For the best experience:

1. **Python Version**: 3.11
2. **Scraping Method**: snscrape (automatic fallback)
3. **Optional**: Twitter API credentials for unlimited access

## Quick Start After Installation

```bash
# Test with a small scrape
python twitter_scraper.py @openai --days 1 --max-tweets 10

# Full scrape
python twitter_scraper.py @username --days 7 --output report.html
```

## Need Help?

Check:
1. `scraper.log` for detailed error messages
2. README.md for full documentation
3. EXAMPLE_USAGE.md for usage examples
