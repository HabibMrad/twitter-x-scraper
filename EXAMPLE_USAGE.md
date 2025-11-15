# Example Usage Guide

## Quick Start Examples

### 1. Test with Help Command

```bash
python twitter_scraper.py --help
```

Expected output:
```
Usage: twitter_scraper.py [OPTIONS] USERNAME

  Scrape Twitter/X account tweets and generate HTML analysis page.

  USAGE: python twitter_scraper.py @username --from 2024-11-12 --to 2024-11-16

  EXAMPLES: python twitter_scraper.py @elonmusk --days 7 python
  twitter_scraper.py @openai --from 2024-11-01 --to 2024-11-15 --exclude-
  retweets python twitter_scraper.py @github --days 30 --output
  github_tweets.html

Options:
  --from TEXT              Start date (YYYY-MM-DD)
  --to TEXT                End date (YYYY-MM-DD)
  --days INTEGER           Alternative to date range - last N days
  --output TEXT            Output HTML file name
  --exclude-retweets       Only fetch original content
  --include-replies        Fetch reply threads
  --max-tweets INTEGER     Maximum tweets to fetch
  --help                   Show this message and exit.
```

### 2. Simple Scrape (Last 7 Days)

```bash
python twitter_scraper.py @openai --days 7
```

This will:
- Scrape tweets from @openai from the last 7 days
- Save HTML report to `output/webpage.html`
- Save raw data to `data/openai_[timestamp].json`

### 3. Date Range Scrape

```bash
python twitter_scraper.py @elonmusk --from 2024-11-01 --to 2024-11-15 --output elon_nov.html
```

This will:
- Scrape tweets from @elonmusk between Nov 1-15, 2024
- Save HTML report to `output/elon_nov.html`

### 4. Advanced: Exclude Retweets, Custom Output

```bash
python twitter_scraper.py @github --days 30 --exclude-retweets --max-tweets 200 --output github_analysis.html
```

This will:
- Scrape last 30 days of original tweets only (no retweets)
- Fetch up to 200 tweets
- Save to `output/github_analysis.html`

## Expected Output

### Console Output

```
============================================================
Twitter/X Scraper CLI Tool
============================================================

🔍 Initializing scraper for @openai...
📥 Fetching tweets... This may take a few minutes.

Processing tweets: 100%|████████████████████| 47/47 [00:23<00:00,  2.01it/s]

✅ Successfully scraped 47 tweets!

📄 Generating HTML report...

============================================================
✨ Success!
============================================================

📊 Tweets scraped: 47
📁 HTML report: C:\...\twitter_scraper\output\webpage.html
💾 Raw data saved in: C:\...\twitter_scraper\data

🌐 Open the HTML file in your browser to view the analysis!
```

### File Structure After Running

```
twitter_scraper/
├── output/
│   └── webpage.html         # Your HTML report - OPEN THIS IN BROWSER
├── data/
│   └── openai_20241115_143022.json  # Raw data backup
├── scraper.log              # Detailed logs
└── ... (rest of project files)
```

## Using the HTML Report

### Features to Try

1. **Dark Mode**: Click the moon/sun button in top-right corner
2. **Search**: Type keywords in the search box (e.g., "AI", "GPT", "Claude")
3. **Filter Retweets**: Check "Hide Retweets" to see only original content
4. **Filter Media**: Check "Media Only" to see tweets with images/videos
5. **Sort**: Use dropdown to sort by:
   - Newest First (default)
   - Oldest First
   - Most Liked
   - Most Retweeted
6. **Click Images**: Click any image to open full-size in new tab
7. **View on Twitter**: Click "View on Twitter →" link on any tweet

### Sample Data Included

The HTML report shows:
- **Header**: Username, date range, total tweets, generation timestamp
- **Statistics**: Total tweets, likes, retweets, average engagement
- **Each Tweet**:
  - Author profile picture and name
  - Tweet text with clickable links, @mentions, #hashtags
  - Images/videos embedded
  - Engagement metrics (likes, retweets, replies, quotes)
  - Timestamp
  - Link to original tweet

## Troubleshooting Examples

### Problem: "No tweets found"

**Solution**: Try a broader date range or check username

```bash
# Instead of:
python twitter_scraper.py @wrongusername --days 7

# Try:
python twitter_scraper.py @openai --days 30 --max-tweets 200
```

### Problem: Rate limiting errors

**Solution**: Add delays between runs, use smaller date ranges

```bash
# Instead of scraping 90 days at once:
python twitter_scraper.py @user --days 90

# Break into smaller chunks:
python twitter_scraper.py @user --from 2024-10-01 --to 2024-10-31 --output oct.html
python twitter_scraper.py @user --from 2024-11-01 --to 2024-11-15 --output nov.html
```

### Problem: Missing images in HTML

**Solution**: Images are linked from Twitter's CDN - you need internet to view them

The HTML file is self-contained for text, but images/videos are linked externally for smaller file size.

## Real-World Use Cases

### 1. Competitive Analysis

```bash
# Scrape competitor's last month of tweets
python twitter_scraper.py @competitor --days 30 --exclude-retweets --output competitor_analysis.html
```

Then analyze in the HTML:
- Search for product mentions
- Sort by most liked to see top content
- Filter media to see their visual content strategy

### 2. Content Archive

```bash
# Archive your own tweets
python twitter_scraper.py @yourusername --from 2024-01-01 --to 2024-12-31 --max-tweets 1000 --output my_2024_tweets.html
```

### 3. Research Project

```bash
# Study an account's communication patterns
python twitter_scraper.py @research_subject --days 90 --include-replies --output research_data.html
```

Then use the raw JSON data in `data/` folder for further analysis.

## Next Steps

1. **Customize the HTML**: Edit `src/html_generator.py` to change styling
2. **Add Features**: Extend `src/scraper.py` with additional metrics
3. **Automate**: Create scheduled tasks to scrape daily/weekly
4. **Integrate**: Use the raw JSON data with other analysis tools

## Tips for Best Results

1. **Start Small**: Test with `--days 7` first
2. **Use Max Tweets**: Set `--max-tweets` appropriate to your needs
3. **Check Logs**: Review `scraper.log` if something goes wrong
4. **Backup Data**: The JSON files in `data/` are your backups
5. **Share Reports**: The HTML files are portable - share via email/cloud
