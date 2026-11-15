// Theme toggle. Light is the default; the inline <head> script applies a saved
// dark choice before paint. Nothing is stored until the reader allows it in the
// consent bar, and a refusal lasts only for the browsing session.
(function () {
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');
  if (!toggle) return;

  const THEME = 'theme';
  const CONSENT = 'theme-consent';
  let allowed = localStorage.getItem(CONSENT) === 'granted';

  function isDark() { return root.classList.contains('dark'); }

  function syncUi() { toggle.setAttribute('aria-pressed', String(isDark())); }

  function remember() {
    if (allowed) localStorage.setItem(THEME, isDark() ? 'dark' : 'light');
  }

  syncUi();

  toggle.addEventListener('click', function () {
    root.classList.toggle('dark');
    remember();
    syncUi();
  });

  // Already answered, or already declined this session: no bar.
  if (allowed || sessionStorage.getItem(CONSENT) === 'denied') return;

  const bar = document.createElement('aside');
  bar.className = 'theme-consent';
  bar.setAttribute('aria-label', 'Theme preference');

  const text = document.createElement('p');
  text.textContent = 'Save your light or dark choice in this browser? It stays on your device and is never sent anywhere.';

  const actions = document.createElement('div');
  actions.className = 'theme-consent-actions';

  function addButton(label, onClick) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.addEventListener('click', onClick);
    actions.appendChild(button);
  }

  addButton('Allow', function () {
    localStorage.setItem(CONSENT, 'granted');
    allowed = true;
    remember();
    close();
  });

  addButton('No thanks', function () {
    sessionStorage.setItem(CONSENT, 'denied');
    localStorage.removeItem(THEME);
    close();
  });

  function close() {
    bar.remove();
    document.body.style.paddingBottom = '';
  }

  // Reserve the bar's real height (it wraps to two rows on narrow screens).
  function fit() {
    if (bar.isConnected) document.body.style.paddingBottom = bar.offsetHeight + 'px';
  }

  bar.append(text, actions);
  document.body.appendChild(bar);
  fit();
  addEventListener('resize', fit);
})();

// Homepage feed filter. The input is hidden in the markup and revealed here,
// so it never shows up as a dead control when JavaScript is off.
(function () {
  const search = document.getElementById('post-search');
  const feed = document.getElementById('post-feed');
  const status = document.getElementById('feed-status');
  if (!search || !feed || !status) return;

  const idleText = status.textContent;
  const items = Array.from(feed.querySelectorAll('li'));
  status.hidden = items.length > 0;
  // No point offering a search box on an empty feed.
  document.querySelector('[data-search]').hidden = items.length === 0;

  search.addEventListener('input', function () {
    const q = search.value.trim().toLowerCase();
    let shown = 0;

    items.forEach(function (li) {
      const hit = !q || li.textContent.toLowerCase().includes(q);
      li.hidden = !hit;
      if (hit) shown += 1;
    });

    if (items.length === 0) {
      status.hidden = false;
      status.textContent = idleText;
    } else if (shown === 0) {
      status.hidden = false;
      status.textContent = 'No posts match.';
    } else {
      status.hidden = true;
    }
  });
})();

// Code blocks: name the language and add a copy button, built from the existing markup.
(function () {
  const names = {
    bash: 'Bash', sh: 'Shell', shell: 'Shell',
    js: 'JavaScript', javascript: 'JavaScript', ts: 'TypeScript', typescript: 'TypeScript',
    json: 'JSON', html: 'HTML', css: 'CSS', python: 'Python', py: 'Python',
    rust: 'Rust', go: 'Go', sql: 'SQL', yaml: 'YAML', text: 'Text'
  };

  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(() => true, () => legacyCopy(text));
    }
    return Promise.resolve(legacyCopy(text));
  }

  // file:// and plain http have no clipboard API, so fall back to a hidden textarea.
  function legacyCopy(text) {
    const area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    area.remove();
    return ok;
  }

  document.querySelectorAll('pre').forEach(function (pre) {
    const code = pre.querySelector('code');
    if (!code) return;

    const lang = (code.className.match(/language-([\w-]+)/) || [])[1];
    const wrap = document.createElement('div');
    wrap.className = 'code-block';

    const bar = document.createElement('div');
    bar.className = 'code-bar';
    const label = document.createElement('span');
    label.textContent = names[lang] || (lang ? lang.toUpperCase() : 'Code');
    bar.appendChild(label);

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'code-copy';
    button.textContent = 'Copy';
    button.addEventListener('click', function () {
      copy(code.textContent).then(function (ok) {
        button.textContent = ok ? 'Copied' : 'Copy failed';
        setTimeout(function () { button.textContent = 'Copy'; }, 1600);
      });
    });
    bar.appendChild(button);

    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(bar);
    wrap.appendChild(pre);

    // Colours come from highlight.js when its CDN is reachable; plain text otherwise.
    if (window.hljs) hljs.highlightElement(code);
  });
})();
