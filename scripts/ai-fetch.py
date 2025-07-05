import openai
import requests
import datetime
import json

openai.api_key = "YOUR_OPENAI_API_KEY"

def fetch_trending_topics():
    # Example: Fetch from Reddit or Twitter/X APIs
    # Here we just return a static example for demo
    return ["Cargo pants comeback", "Viral TikTok dance", "Summer memes 2025"]

def generate_post(topics):
    prompt = (
        f"Write a fun, engaging blog post summary for teens (15-20) about today's top trends: {', '.join(topics)}. "
        "Include some style inspo, a trending joke, and a pop culture 'tea' tidbit. Make it short and vibe-y."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    topics = fetch_trending_topics()
    post = generate_post(topics)
    today = datetime.date.today().isoformat()
    with open(f"../posts/{today}-daily.md", "w") as f:
        f.write(post)