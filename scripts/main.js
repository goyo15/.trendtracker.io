// scripts/main.js
// This script fetches up to 15 AI-generated posts per category and injects them into .posts as styled cards with images

document.addEventListener('DOMContentLoaded', async () => {
  const container = document.querySelector('.posts');
  if (!container) return;

  // Determine category from filename (fallback to 'trends')
  const page = window.location.pathname
    .split('/')
    .pop()
    .replace('.html', '') || 'trends';

  try {
    // Load mapping of categories to today's markdown filenames
    const latestRes = await fetch('/posts/latest.json');
    if (!latestRes.ok) throw new Error('Failed to load latest.json');
    const latest = await latestRes.json();

    const files = latest[page] || [];
    if (!files.length) {
      container.innerHTML = '<p class="error">No posts available for today.</p>';
      return;
    }

    // Fetch each markdown file and build card HTML
    const cardHtmlArray = await Promise.all(
      files.map(async (fname) => {
        const mdRes = await fetch(`/posts/${fname}`);
        if (!mdRes.ok) return '';
        const mdText = await mdRes.text();

        // Extract topic from the first line of markdown ("# topic — date")
        const firstLine = mdText.split('\n')[0] || '';
        const topicMatch = firstLine.match(/^#\s*(.*?)\s+—/);
        const topic = topicMatch ? topicMatch[1] : page;

        // Generate an image URL from Unsplash based on the topic
        const query = encodeURIComponent(topic);
        const imageUrl = `https://source.unsplash.com/featured/400x200/?${query}`;

        // Convert markdown to HTML
        const contentHtml = marked.parse(mdText);

        // Return card structure
        return `
<div class="post-card">
  <img class="post-card-image" src="${imageUrl}" alt="${topic}" />
  <div class="post-card-content">
    <h2 class="post-card-title">${topic}</h2>
    ${contentHtml}
  </div>
</div>
        `.trim();
      })
    );

    // Render cards in a grid
    container.innerHTML = cardHtmlArray.filter(Boolean).join('\n');
  } catch (err) {
    console.error(err);
    container.innerHTML = '<p class="error">Sorry, unable to load posts.</p>';
  }
});
