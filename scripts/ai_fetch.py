#!/usr/bin/env python3
import os, json, datetime
from openai import OpenAI
from markdown import markdown
from slugify import slugify

client = OpenAI()

# Prompts per category
seed_prompts = {
    "trends": "List the top 15 current TikTok trends, ranked by relevance, news coverage, and popularity among Gen Z. Return as a numbered list.",
    "styles": "List the top 15 hottest teen fashion styles right now, ranked by relevance, media buzz, and popularity. Return as a numbered list.",
    "jokes":  "List the top 15 fresh, teen-friendly joke topics right now, ranked by relevancy and virality. Return as a numbered list.",
    "tea":    "List the top 15 pieces of teen gossip (the “tea”), ranked by recency, social media buzz, and popularity. Return as a numbered list."
}

today = datetime.date.today().isoformat()
posts_dir = "posts"
os.makedirs(posts_dir, exist_ok=True)

latest = {}

for cat, seed in seed_prompts.items():
    # 1) get the 15 sub-topics
    resp1 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You’re a data-driven trend analyst."},
            {"role": "user",   "content": seed}
        ]
    )
    topics_text = resp1.choices[0].message.content
    # parse numbered list into Python list
    topics = []
    for line in topics_text.splitlines():
        # e.g. "1. Dancing in grocery aisles"
        if line.strip() and line.strip()[0].isdigit():
            topic = line.split('.', 1)[1].strip()
            topics.append(topic)
    topics = topics[:15]  # enforce hard limit just in case

    # 2) generate one post per sub-topic
    filenames = []
    for i, topic in enumerate(topics, start=1):
        prompt = f"Write a snappy teen-blog post (~150 words) about “{topic}”."
        resp2 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You’re a snappy teen blogger."},
                {"role": "user",   "content": prompt}
            ]
        )
        content_md = resp2.choices[0].message.content
        slug = slugify(topic)[:40]  # limit filename length
        fname = f"{today}-{cat}-{i:02d}-{slug}.md"
        path = os.path.join(posts_dir, fname)
        with open(path, "w") as f:
            f.write(f"# {topic} — {today}\n\n{content_md}")
        filenames.append(fname)

    latest[cat] = filenames

# write our index
with open(f"{posts_dir}/latest.json", "w") as f:
    json.dump(latest, f, indent=2)

print("✅ Generated posts:", latest)
