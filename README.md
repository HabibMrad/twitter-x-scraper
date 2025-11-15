# Twitter/X Scraper CLI Tool

A powerful Python CLI tool to scrape Twitter/X account tweets and generate beautiful, self-contained HTML analysis pages.

## Features

- **Flexible Scraping**: Fetch tweets by date range or last N days
- **Comprehensive Data**: Captures tweets, retweets, quotes, replies, media, and engagement metrics
- **Beautiful HTML Output**: Professional, responsive design with dark mode
- **Interactive Features**: Search, filter, sort, and analyze tweets in the browser
- **No API Required**: Uses fallback scraping methods (ntscraper)
- **Data Archival**: Saves raw data to JSON for backup
- **Progress Tracking**: Real-time progress indicators during scraping
- **Error Handling**: Robust handling of rate limits, deleted tweets, and private accounts

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download this project**

2. **Navigate to the project directory**
   ```bash
   cd twitter_scraper
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Install Playwright browsers (required for ntscraper)**
   ```bash
   playwright install
   ```

7. **Configure environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

## Usage

### Basic Command Structure

```bash
python twitter_scraper.py @username [OPTIONS]
```

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `@username` | Twitter username (required) | `@elonmusk` |
| `--from DATE` | Start date (YYYY-MM-DD) | `--from 2024-11-12` |
| `--to DATE` | End date (YYYY-MM-DD) | `--to 2024-11-16` |
| `--days N` | Last N days (alternative to date range) | `--days 7` |
| `--output FILE` | Output HTML file name | `--output report.html` |
| `--exclude-retweets` | Only fetch original content | `--exclude-retweets` |
| `--include-replies` | Fetch reply threads | `--include-replies` |
| `--max-tweets N` | Maximum tweets to fetch (default: 100) | `--max-tweets 500` |

### Examples

1. **Scrape last 7 days of tweets**
   ```bash
   python twitter_scraper.py @openai --days 7
   ```

2. **Scrape specific date range**
   ```bash
   python twitter_scraper.py @elonmusk --from 2024-11-01 --to 2024-11-15
   ```

3. **Exclude retweets and save to custom file**
   ```bash
   python twitter_scraper.py @github --days 30 --exclude-retweets --output github_analysis.html
   ```

4. **Scrape with replies included**
   ```bash
   python twitter_scraper.py @anthropicai --days 14 --include-replies
   ```

5. **Large scrape with more tweets**
   ```bash
   python twitter_scraper.py @tesla --days 60 --max-tweets 1000
   ```

## Output

### HTML Report Features

The generated HTML report includes:

- **Dark Mode Toggle**: Switch between light and dark themes
- **Search Functionality**: Search tweets by content
- **Filters**: Hide retweets, show only media tweets
- **Sorting**: Sort by date, likes, or retweets
- **Statistics**: Total tweets, likes, retweets, and average engagement
- **Tweet Display**: Full text, images, videos, engagement metrics
- **Responsive Design**: Works on mobile and desktop
- **Self-Contained**: Single HTML file with all content embedded

### File Locations

- **HTML Reports**: `output/` directory
- **Raw JSON Data**: `data/` directory (for archival and backup)
- **Log Files**: `scraper.log` in project root

## Project Structure

```
twitter_scraper/
├── twitter_scraper.py      # Main CLI entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
├── scraper.log             # Log file (generated)
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── scraper.py          # Twitter scraping logic
│   └── html_generator.py   # HTML report generation
├── data/                   # Raw JSON backups (generated)
└── output/                 # HTML reports (generated)
```

## Troubleshooting

### Common Issues

1. **"No tweets found"**
   - Verify the username is correct (with or without @)
   - Check if the account is public
   - Try a different date range
   - Increase `--max-tweets` value

2. **"Connection error" or timeout**
   - Check your internet connection
   - Twitter may be blocking requests (try again later)
   - Reduce scraping frequency with smaller date ranges

3. **Missing images/videos in HTML**
   - Media is linked directly from Twitter's CDN
   - Ensure internet connection when viewing HTML
   - Some media may be deleted or unavailable

4. **Playwright installation issues**
   - Run: `playwright install --force`
   - Ensure you have sufficient disk space
   - Check firewall/proxy settings

5. **Rate limiting errors**
   - Reduce scraping frequency
   - Try smaller date ranges
   - Wait a few minutes between runs

### Debug Mode

To enable detailed logging:

1. Edit `.env` file:
   ```
   LOG_LEVEL=DEBUG
   ```

2. Check `scraper.log` for detailed error messages

## API Setup (Optional)

While this tool works without API credentials, you can optionally use the official Twitter API v2 for more reliable scraping:

1. Create a Twitter Developer account at https://developer.twitter.com
2. Create a new project and app
3. Generate API credentials (Bearer Token, API Key, API Secret)
4. Add credentials to `.env` file:
   ```
   TWITTER_BEARER_TOKEN=your_token_here
   TWITTER_API_KEY=your_key_here
   TWITTER_API_SECRET=your_secret_here
   ```

**Note**: API implementation is a future enhancement. Current version uses ntscraper.

## Technical Details

### Dependencies

- **ntscraper**: Twitter scraping without authentication
- **playwright**: Browser automation for scraping
- **click**: CLI interface and argument parsing
- **tqdm**: Progress bars
- **python-dotenv**: Environment variable management
- **Jinja2**: Template engine (for future enhancements)

### Rate Limiting

- Default delay between requests: 2 seconds
- Configurable via `RATE_LIMIT_DELAY` in `.env`
- Automatic retry on failures (max 3 attempts)

### Data Privacy

- All data is stored locally
- No data is sent to external servers (except Twitter for scraping)
- HTML files are self-contained and can be shared safely

## Contributing

Found a bug or want to contribute? Feel free to:

1. Report issues
2. Submit feature requests
3. Create pull requests

## License

This project is provided as-is for educational and research purposes.

**Important**: Respect Twitter's Terms of Service and rate limits. Use responsibly.

## Credits

Built with:
- Python 3
- ntscraper library
- Modern web standards (HTML5, CSS3, JavaScript)

---

**Happy Scraping! 🐦**
