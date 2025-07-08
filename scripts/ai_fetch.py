#!/usr/bin/env python3
import os
import json
import datetime
from openai import OpenAI
from markdown import markdown
from slugify import slugify

# Instantiate OpenAI client (reads OPENAI_API_KEY from env)
client = OpenAI()

# Step 1: Seed prompts that return a ranked list of 15 items
seed_prompts = {
    "trends": "List the top 15 current TikTok trends, ranked by relevance, news coverage, and popularity among Gen Z. Return as a numbered list.",
    "styles": "List the top 15 hottest teen fashion styles right now, ranked by relevance, media buzz, and popularity. Return as a numbered list.",
    "jokes":  "List the top 15 fresh, teen-friendly joke topics right now, ranked by relevancy and virality. Return as a numbered list.",
    "tea":    "List the top 15 pieces of teen gossip (the “tea”), ranked by recency, social media buzz, and popularity. Return as a numbered list."
}

# Prepare output folder and date
today = datetime.date.today().isoformat()
posts_dir = "posts"
os.makedirs(posts_dir, exist_ok=True)

latest = {}

for cat, seed in seed_prompts.items():
    # 1) Generate the ranked list of topics
    resp1 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You’re a data-driven trend analyst."},
            {"role": "user",   "content": seed}
        ]
    )
    topics_text = resp1.choices[0].message.content

    # Parse out numbered list into a Python list
    topics = []
    for line in topics_text.splitlines():
        line = line.strip()
        if line and line[0].isdigit() and "." in line:
            _, rest = line.split(".", 1)
            topics.append(rest.strip())
    topics = topics[:15]  # enforce a hard cap at 15

    # 2) For each topic, generate a post
    filenames = []
    for idx, topic in enumerate(topics, start=1):
        prompt = f"Write a snappy teen-blog post (~150 words) about “{topic}”."
        resp2 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You’re a snappy teen blogger."},
                {"role": "user",   "content": prompt}
            ]
        )
        content_md = resp2.choices[0].message.content

        # Slugify the topic for filenames
        slug = slugify(topic)[:40]
        fname = f"{today}-{cat}-{idx:02d}-{slug}.md"
        path = os.path.join(posts_dir, fname)

        # Write out the markdown file
        with open(path, "w") as f:
            f.write(f"# {topic} — {today}\n\n")
            f.write(content_md)

        filenames.append(fname)

    # Record all filenames for this category
    latest[cat] = filenames

# 3) Save latest.json mapping each category to its list of today’s files
with open(os.path.join(posts_dir, "latest.json"), "w") as f:
    json.dump(latest, f, indent=2)

print("✅ Generated posts:", latest)
