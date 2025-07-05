import openai
import datetime
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_trending_topics():
    # Placeholder: integrate with APIs like Twitter/X, TikTok or Reddit for real data
    return ["Cargo pants comeback", "Viral TikTok dance", "Summer memes 2025"]

def generate_post_content(topics):
    prompt = (
        f"Create a fun, engaging blog post for teens (15-20) about today's top trends: {', '.join(topics)}. "
        "Include a quick style inspo, a trending joke, and a pop culture 'tea' tidbit. Keep it short and vibey. "
        "Format result as:\n"
        "Title: <title>\n"
        "Summary: <summary>\n"
        "Type: <trends/styles/jokes/tea>\n"
        "Content: <markdown content>\n"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def save_post(data, date_str):
    # Parse AI output
    lines = data.splitlines()
    title = lines[0].replace('Title:', '').strip()
    summary = lines[1].replace('Summary:', '').strip()
    post_type = lines[2].replace('Type:', '').strip()
    content = "\n".join(lines[3:]).replace('Content:', '').strip()
    file_name = f"{date_str}-daily.md"
    # Save markdown post
    with open(f"../posts/{file_name}", "w") as f:
        f.write(f"# {title}\n\n{content}")
    # Update latest.json
    latest_path = "../posts/latest.json"
    latest = []
    if os.path.exists(latest_path):
        with open(latest_path, "r") as f:
            latest = json.load(f)
    post_entry = {
        "title": title,
        "summary": summary,
        "type": post_type,
        "file": file_name,
        "date": date_str
    }
    latest.insert(0, post_entry)
    latest = latest[:10]  # Keep only latest 10
    with open(latest_path, "w") as f:
        json.dump(latest, f, indent=2)

if __name__ == "__main__":
    today = datetime.date.today().isoformat()
    topics = fetch_trending_topics()
    ai_result = generate_post_content(topics)
    save_post(ai_result, today)