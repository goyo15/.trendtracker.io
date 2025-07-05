// Simple loader for the latest posts (for demo, loads from posts/latest.json)
document.addEventListener('DOMContentLoaded', () => {
  const sectionMap = {
    'index.html': 'latest-posts',
    'trends.html': 'trend-posts',
    'styles.html': 'style-posts',
    'jokes.html': 'joke-posts',
    'tea.html': 'tea-posts'
  };

  // Get current page
  const path = window.location.pathname.split('/').pop() || 'index.html';
  const sectionId = sectionMap[path];

  if (!sectionId) return;

  fetch('posts/latest.json')
    .then(res => res.json())
    .then(posts => {
      const postsEl = document.getElementById(sectionId);
      if (!postsEl) return;
      // Filter posts by type if not home
      let filtered = posts;
      if (path !== 'index.html') {
        const type = path.replace('.html', '');
        filtered = posts.filter(post => post.type === type);
      }
      postsEl.innerHTML = filtered.map(post => `
        <div class="post-card">
          <h2>${post.title}</h2>
          <p>${post.summary}</p>
          <a href="posts/${post.file}">Read more</a>
        </div>
      `).join('');
    });
});