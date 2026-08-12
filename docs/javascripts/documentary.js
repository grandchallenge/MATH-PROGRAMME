(() => {
  const reader = document.querySelector('[data-gcl-reader]');
  if (!reader) return;

  const plateActivations = {
    union_closed: {
      '../../assets/documentaries/union_closed/plate_garden.svg': {
        src: '../../assets/visual_pedagogy/batch1/union_closed/plate_garden_r2.svg',
        alt: 'Exact six-set union-closed family shown as a strict Hasse-style cover diagram, with frequencies a in four sets, b in three, c in two, and half threshold three.',
        title: 'The Garden That Closes',
        note: 'Exact cover relations, selected unions, and frequencies expose this example without claiming the general Frankl conjecture.'
      },
      '../../assets/documentaries/union_closed/plate_frequency.svg': {
        src: '../../assets/visual_pedagogy/batch1/union_closed/plate_frequency.svg',
        alt: 'Frequency bars and a six-row incidence matrix show counts four, three, and two against a half threshold of three; column and row-size sums both equal nine.',
        title: 'The Half-Way Balance',
        note: 'Exact incidence counts expose the half threshold and the double-count identity.'
      },
      '../../assets/documentaries/union_closed/plate_lattice.svg': {
        src: '../../assets/visual_pedagogy/batch1/union_closed/plate_lattice.svg',
        alt: 'Six-set join-semilattice under inclusion with join equal to union; {a}, {b}, and {a,c} are marked join-irreducible and two exact joins are written.',
        title: 'The Lattice Mirror',
        note: 'Join is union in one exact finite example; general translation theorems retain their hypotheses.'
      },
      '../../assets/documentaries/union_closed/plate_entropy.svg': {
        src: '../../assets/visual_pedagogy/batch1/union_closed/plate_entropy.svg',
        alt: 'Uniform random set from the six-set family has marginals two thirds, one half, and one third; independent copies have union marginals eight ninths, three quarters, and five ninths, with a guardrail separating the example from source-specific entropy theorems.',
        title: 'The Entropy Bridge',
        note: 'An exact independent-copy calculation illustrates the entropy terrain without claiming the universal one-half theorem.'
      },
      '../../assets/documentaries/union_closed/plate_frontier.svg': {
        src: '../../assets/visual_pedagogy/batch1/union_closed/plate_frontier.svg',
        alt: 'Status map places elementary, bounded exact, imported positive-bound, and formal structural results below a dashed line labeled open universal boundary one half.',
        title: 'Islands of Theorem',
        note: 'Established partial terrain remains visibly below the open universal one-half boundary.'
      }
    },
    bsd: {
      '../../assets/documentaries/bsd/plate_curve.svg': {
        src: '../../assets/visual_pedagogy/batch1/bsd/plate_curve.png',
        alt: 'An exact real plot of E5, y squared equals x cubed minus 25x, marks P equals 25 over 4 comma 75 over 8 and is paired with a right triangle whose exact rational sides give area five.',
        title: 'A Rational Point Opens a Door',
        note: 'The point and area-five triangle are exact; the finite plot is not a rank computation or a proof of BSD.'
      }
    }
  };

  const activateReviewedPlates = () => {
    const mapping = plateActivations[reader.dataset.gclReader];
    if (!mapping) return;
    reader.querySelectorAll('.monograph-plate img').forEach((image) => {
      const original = image.getAttribute('src');
      const activation = mapping[original];
      if (!activation) return;
      image.src = activation.src;
      image.alt = activation.alt;
      image.dataset.visualPedagogyActivation = 'batch1';
      const figure = image.closest('[data-plate]');
      const title = figure?.querySelector('figcaption strong');
      const note = figure?.querySelector('figcaption small');
      if (title) title.textContent = activation.title;
      if (note) note.textContent = activation.note;
    });
  };

  activateReviewedPlates();

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