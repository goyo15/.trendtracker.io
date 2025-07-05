# Teen Trend Tracker

A sleek, AI-powered, daily-updated blog for teens, featuring the latest trends, styles, jokes, and tea.

## Structure

- `index.html`, `trends.html`, `styles.html`, `jokes.html`, `tea.html`, `about.html`, `contact.html`: Main site pages
- `styles/main.css`: Core styles
- `scripts/main.js`: JS to render posts
- `scripts/ai_fetch.py`: Python script to generate new posts via OpenAI
- `posts/`: Contains Markdown posts and a `latest.json` index

## How to Use

1. **Set your OpenAI API key as `OPENAI_API_KEY` in your environment.**
2. **Run `python scripts/ai_fetch.py` to generate a new daily post.**
3. The script will update `posts/latest.json` and create a new Markdown file.
4. The site will display the new post automatically.

## Automation

You can set up a daily cron job or GitHub Action to run the Python script for automatic updates.

## Deployment

Host the folder on Netlify, Vercel, or Namecheap. Make sure `posts/` is writable for automation, or automate post generation via CI/CD.
