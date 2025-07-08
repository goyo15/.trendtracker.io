// scripts/main.js
document.addEventListener('DOMContentLoaded', async () => {
  const container = document.querySelector('.posts');
  if (!container) return;  // no .posts section here

  // 1. Figure out our "category" from the filename
  const name = window.location.pathname.split('/').pop() || 'index.html';
  let category = name.replace('.html', '');
  if (category === '' || category === 'index') {
    category = 'trends';    // or whichever you want as your homepage feed
  }

  try {
    // 2. Get the mapping of latest files
    const latestRes = await fetch('/posts/latest.json');
    if (!latestRes.ok) throw new Error('Could not load latest.json');
    const latest = await latestRes.json();

    // 3. Lookup our file for today
    const mdFilename = latest[category];
    if (!mdFilename) throw new Error(`No post for category "${category}"`);

    // 4. Fetch that markdown
    const postRes = await fetch(`/posts/${mdFilename}`);
    if (!postRes.ok) throw new Error(`Could not load ${mdFilename}`);
    const markdownText = await postRes.text();

    // 5. Convert to HTML and inject
    container.innerHTML = marked.parse(markdownText);
  }
  catch (err) {
    console.error(err);
    container.innerHTML = `<p class="error">Sorry, we couldn’t load today’s post. Try again later.</p>`;
  }
});
