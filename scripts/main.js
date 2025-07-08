// scripts/main.js
// This script fetches up to 15 AI-generated posts per category and injects them into .posts

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

    // Fetch each markdown file, convert to HTML, and collect
    const htmlParts = await Promise.all(
      files.map(async (fname) => {
        const mdRes = await fetch(`/posts/${fname}`);
        if (!mdRes.ok) return '';
        const mdText = await mdRes.text();
        return marked.parse(mdText);
      })
    );

    // Inject all posts separated by an <hr/>
    container.innerHTML = htmlParts.filter(Boolean).join('\n<hr/>\n');
  } catch (err) {
    console.error(err);
    container.innerHTML = '<p class="error">Sorry, unable to load posts.</p>';
  }
});
