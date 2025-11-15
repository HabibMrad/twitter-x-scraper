# Quick Start Guide

## Fastest Way to Test (No Setup Required!)

### 1. Generate Demo Report (Recommended for Testing)

```bash
python demo_scraper.py @username --days 7 --max-tweets 30
```

This will:
- Generate a beautiful HTML report with mock data
- No Twitter API credentials needed
- No scraping - instant results
- Perfect for testing the HTML output features

**Example:**
```bash
python demo_scraper.py @marsar0 --days 7 --max-tweets 30 --output demo_report.html
```

Then open `output/demo_report.html` in your browser!

## Demo Features You Can Test

The demo HTML report includes all features:
- ✅ Dark mode toggle (click moon/sun icon)
- ✅ Search functionality
- ✅ Filter by retweets/media
- ✅ Sort options (newest, oldest, most liked, most retweeted)
- ✅ Responsive design
- ✅ Tweet statistics
- ✅ Clickable links, hashtags, mentions
- ✅ Image display
- ✅ Professional styling

## For Real Twitter Scraping

### Option 1: Using the Demo to Test (Recommended First)

Before scraping real data, try the demo:

```bash
# Generate demo for any username
python demo_scraper.py @openai --days 14 --max-tweets 50

# View the output
# Open: output/demo_webpage.html in your browser
```

### Option 2: Real Scraping with Tweepy (Requires API)

1. **Get Twitter API Credentials**:
   - Go to https://developer.twitter.com
   - Create an app
   - Get Bearer Token, API Key, API Secret

2. **Create `.env` file**:
   ```bash
   cp .env.example .env
   # Edit .env and add your credentials
   ```

3. **Run scraper**:
   ```bash
   python twitter_scraper.py @username --days 7
   ```

### Option 3: Use Python 3.9-3.11 for snscrape

If you want to use the free snscraper method (no API needed):

1. Install Python 3.11
2. Create virtual environment with Python 3.11
3. Install dependencies
4. Run scraper

See `INSTALL.md` for detailed instructions.

## What You Get

Both demo and real scraping produce:

### HTML Report (`output/webpage.html`)
- Self-contained, shareable HTML file
- Professional design
- Interactive features (search, filter, sort)
- Dark/light mode
- Mobile-friendly
- All engagement metrics

### Example Output Structure

```
output/
└── webpage.html        # Open this in your browser!

Features:
├── Header (username, date range, stats)
├── Controls (search, filters, sort)
├── Statistics Dashboard
└── Tweet Feed
    ├── Tweet 1 (text, media, metrics)
    ├── Tweet 2
    └── ...
```

## Comparison: Demo vs Real

| Feature | Demo Mode | Real Scraping |
|---------|-----------|---------------|
| Speed | Instant | 1-5 minutes |
| API Required | ❌ No | ✅ Yes (or snscrape) |
| Data | Mock/Random | Real tweets |
| Testing | ✅ Perfect | Production use |
| Cost | Free | Free (with limits) |

## Troubleshooting

### Can't scrape real tweets?

**Use demo mode!**
```bash
python demo_scraper.py @username --days 7
```

### HTML not displaying properly?

- Make sure you opened the file in a web browser (Chrome, Firefox, Edge)
- File is in `output/` directory
- Check browser console for errors (F12)

### Want to customize the HTML?

- Edit `src/html_generator.py`
- Modify CSS styles
- Add custom features

## Next Steps

1. **Try the demo** (2 minutes):
   ```bash
   python demo_scraper.py @marsar0 --days 7 --max-tweets 30
   ```

2. **View the output**:
   - Open `output/demo_webpage.html` in browser
   - Test dark mode, search, filters

3. **For real scraping**:
   - Read `INSTALL.md`
   - Get Twitter API credentials
   - Use `twitter_scraper.py`

## Common Use Cases

### 1. Quick Preview/Demo
```bash
python demo_scraper.py @elonmusk --days 30 --max-tweets 100
```

### 2. Test HTML Styling
```bash
# Generate demo with your username
python demo_scraper.py @yourusername --days 14 --max-tweets 50

# Edit src/html_generator.py to customize
# Re-run to see changes
```

### 3. Share Sample Reports
```bash
# Generate professional-looking demo
python demo_scraper.py @company --days 7 --max-tweets 20

# Share output/demo_webpage.html with team
```

## Tips

- **Start with demo mode** to test features quickly
- **Use small numbers** for testing (--max-tweets 10)
- **The HTML file is self-contained** - share it via email/cloud
- **All features work in demo** - perfect for presentations

## Questions?

- Check `README.md` for full documentation
- See `EXAMPLE_USAGE.md` for more examples
- Read `INSTALL.md` for installation issues

---

**Start with demo mode and explore the features before setting up real scraping!**
