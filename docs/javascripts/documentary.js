(() => {
  const reader = document.querySelector('[data-gcl-reader]');
  if (!reader) return;

  const storageKey = `gcl-documentary:${reader.dataset.gclReader}:scroll`;
  const focusKey = `gcl-documentary:${reader.dataset.gclReader}:focus`;
  const progressOutput = reader.querySelector('[data-reader-progress]');
  const progressBar = reader.querySelector('[data-reader-progress-bar]');
  const focusButton = reader.querySelector('[data-reader-focus]');
  const printButton = reader.querySelector('[data-reader-print]');
  const resetButton = reader.querySelector('[data-reader-reset]');
  const sections = [...reader.querySelectorAll('[data-reader-section]')];
  const tocLinks = [...reader.querySelectorAll('.monograph-contents a[href^="#"]')];
  let saveTimer = null;

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

  const updateProgress = () => {
    const start = reader.querySelector('#monograph-start')?.offsetTop ?? 0;
    const end = reader.offsetTop + reader.offsetHeight - window.innerHeight;
    const ratio = end > start ? clamp((window.scrollY - start) / (end - start), 0, 1) : 0;
    const percent = Math.round(ratio * 100);
    if (progressOutput) progressOutput.value = `${percent}% read`;
    if (progressBar) progressBar.style.width = `${percent}%`;

    clearTimeout(saveTimer);
    saveTimer = window.setTimeout(() => {
      try { localStorage.setItem(storageKey, String(window.scrollY)); } catch (_) {}
    }, 180);
  };

  const setCurrentSection = (id) => {
    tocLinks.forEach((link) => {
      const active = link.getAttribute('href') === `#${id}`;
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };

  if ('IntersectionObserver' in window && sections.length) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible[0]) setCurrentSection(visible[0].target.id);
    }, { rootMargin: '-18% 0px -70% 0px', threshold: [0, 0.1, 0.5] });
    sections.forEach((section) => observer.observe(section));
  }

  const setFocus = (enabled) => {
    reader.classList.toggle('is-focus', enabled);
    focusButton?.setAttribute('aria-pressed', String(enabled));
    if (focusButton) focusButton.textContent = enabled ? 'Exit focus' : 'Focus mode';
    try { localStorage.setItem(focusKey, enabled ? '1' : '0'); } catch (_) {}
  };

  focusButton?.addEventListener('click', () => setFocus(!reader.classList.contains('is-focus')));
  printButton?.addEventListener('click', () => window.print());
  resetButton?.addEventListener('click', () => {
    try {
      localStorage.removeItem(storageKey);
      localStorage.removeItem(focusKey);
    } catch (_) {}
    setFocus(false);
    reader.querySelector('#monograph-start')?.scrollIntoView({ behavior: 'smooth' });
  });

  const dialog = reader.querySelector('[data-plate-dialog]');
  const dialogImage = dialog?.querySelector('[data-plate-dialog-image]');
  const dialogCaption = dialog?.querySelector('[data-plate-dialog-caption]');

  reader.querySelectorAll('[data-plate-open]').forEach((button) => {
    button.addEventListener('click', () => {
      const figure = button.closest('[data-plate]');
      const image = button.querySelector('img');
      const caption = figure?.querySelector('figcaption strong')?.textContent?.trim() || 'Illustrated plate';
      if (!dialog || !dialogImage || !image) return;
      dialogImage.src = image.currentSrc || image.src;
      dialogImage.alt = image.alt;
      if (dialogCaption) dialogCaption.textContent = caption;
      if (typeof dialog.showModal === 'function') dialog.showModal();
    });
  });

  dialog?.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });

  window.addEventListener('scroll', updateProgress, { passive: true });
  window.addEventListener('resize', updateProgress, { passive: true });

  try {
    setFocus(localStorage.getItem(focusKey) === '1');
    if (!location.hash) {
      const saved = Number(localStorage.getItem(storageKey));
      if (Number.isFinite(saved) && saved > 0) {
        window.requestAnimationFrame(() => window.scrollTo({ top: saved, behavior: 'auto' }));
      }
    }
  } catch (_) {}

  updateProgress();
})();
