#!/usr/bin/env python3
import os
import json
import datetime
from openai import OpenAI
from markdown import markdown

# 1. Load your API key
client = OpenAI()

# 2. Define prompts for each category
categories = {
    "trends": "Write a Gen Z-style listicle of the top 5 TikTok trends right now.",
    "styles": "Describe 5 of the hottest fashion styles among teens today.",
    "jokes": "Give me 7 fresh, teen-friendly jokes in bullet form.",
    "tea": "Spill the hottest teen gossip (the “tea”) in a short blog post."
}

today = datetime.date.today().isoformat()
posts_dir = "posts"
os.makedirs(posts_dir, exist_ok=True)

# 3. Generate & save each post
latest = {}
for cat, prompt in categories.items():
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You’re a snappy teen blogger."},
                  {"role":"user","content":prompt}]
    )
    content_md = resp.choices[0].message.content
    filename = f"{posts_dir}/{today}-{cat}.md"
    with open(filename, "w") as f:
        f.write(f"# {cat.title()} — {today}\n\n")
        f.write(content_md)
    latest[cat] = f"{today}-{cat}.md"

# 4. Update the index
with open(f"{posts_dir}/latest.json", "w") as f:
    json.dump(latest, f, indent=2)

print("✅ Generated posts:", latest)
