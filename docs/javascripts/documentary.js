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
        src: '../../assets/visual_pedagogy/bsd_exact/plate_01_rational_point_triangle.svg',
        alt: 'Exact finite-window plot of E5, y squared equals x cubed minus 25x, with P equals 25 over 4 comma 75 over 8, paired with the exact rational right triangle of sides 3 over 2, 20 over 3, and 41 over 6 and area five.',
        title: 'Rational Point to Rational Triangle',
        note: 'Exact arithmetic correspondence. The finite real plot does not determine rank and does not prove BSD.'
      },
      '../../assets/documentaries/bsd/plate_bridge.svg': {
        src: '../../assets/visual_pedagogy/bsd_exact/plate_03_good_prime.svg',
        alt: 'Exact finite-field point set for E5 modulo 13 with 19 affine solutions, total point count 20, a13 equal to minus 6, the resulting local Euler factor, and an exact finite sample of a p values at selected good primes.',
        title: 'Counting at a Good Prime',
        note: 'Each displayed point and trace value is exact. No single prime, and no finite sample of primes, determines rank.'
      },
      '../../assets/documentaries/bsd/plate_harmony.svg': {
        src: '../../assets/visual_pedagogy/bsd_exact/plate_02_group_law.svg',
        alt: 'Exact chord-tangent addition example on y squared equals x cubed minus x plus one, with P equals zero comma one, Q equals one comma one, third intersection R equals minus one comma one, and reflected sum P plus Q equals minus one comma minus one.',
        title: 'The Chord–Tangent Group Law',
        note: 'Exact rational addition example. It illustrates the operation; it is not a picture of the full Mordell–Weil group.'
      },
      '../../assets/documentaries/bsd/plate_frontier.svg': {
        src: '../../assets/visual_pedagogy/bsd_exact/plate_05_theorem_frontier.svg',
        alt: 'Six-row theorem-status matrix separating Mordell-Weil finite generation, modularity, and analytic-rank-zero-or-one results from the universally open rank equality, Sha finiteness, and complete normalized leading-term formula.',
        title: 'The Exact BSD Theorem Frontier',
        note: 'Scope is part of theorem status. Established special cases do not remove the universal quantifier.'
      },
      '../../assets/documentaries/bsd/plate_overture.svg': {
        src: '../../assets/visual_pedagogy/bsd_exact/plate_04_strong_bsd_ledger.svg',
        alt: 'Strong BSD leading-term formula with separate labelled inputs for the real period, regulator, Tate-Shafarevich order, local Tamagawa factors, rational torsion denominator, and a three-row list separating rank equality, Sha finiteness, and the leading-term identity.',
        title: 'The Strong BSD Leading-Term Ledger',
        note: 'The dependency structure is explicit. It does not convert the conjectural identity or its finiteness hypothesis into established facts.'
      }
    },
    hodge: {
      '../../assets/documentaries/hodge/cycles.svg': {
        src: '../../assets/visual_pedagogy/batch2/hodge/cycles.png',
        alt: 'A rendered geometric variety with highlighted cycle ribbons maps by cl superscript p into a layered cohomology chamber for rational Hodge classes; established direction and open converse are separated below.',
        title: 'From Subvarieties to Classes',
        note: 'The cycle-class direction is established; general rational surjectivity is the open converse, and injectivity is not claimed.'
      },
      '../../assets/documentaries/hodge/diamond.svg': {
        src: '../../assets/visual_pedagogy/batch2/hodge/diamond.svg',
        alt: 'A schematic Hodge bidegree diamond shows the direct-sum decomposition, conjugation between p,q and q,p, and a labelled p,p diagonal box, without assigning numerical Hodge numbers.',
        title: 'Hodge Decomposition: Type and Symmetry',
        note: 'Algebraic-cycle classes have p,p type; rational p,p type is necessary but does not prove algebraicity in general.'
      }
    },
    navier_stokes: {
      '../../assets/documentaries/navier_stokes/field.svg': {
        src: '../../assets/visual_pedagogy/batch3/navier_stokes/field.svg',
        alt: 'A schematic velocity-vector field is paired with the incompressible Navier-Stokes equation, with transport, pressure, viscosity, and divergence-free constraint labeled separately.',
        title: 'A Fluid Has a Velocity Everywhere',
        note: 'The field is schematic rather than simulation output; the PDE roles are separated, and no global-regularity or singularity claim is made.'
      },
      '../../assets/documentaries/navier_stokes/frontier.svg': {
        src: '../../assets/visual_pedagogy/batch3/navier_stokes/frontier.svg',
        alt: 'A status ladder separates the scaling-critical line, continuation criteria, partial regularity, and the open universal three-dimensional Navier-Stokes problem.',
        title: 'The Critical Regularity Frontier',
        note: 'Critical scaling, continuation criteria, partial regularity, and the open universal problem remain distinct; conditional results do not settle the Clay problem.'
      }
    },
    poincare: {
      '../../assets/documentaries/poincare/plate_extinction.svg': {
        src: '../../assets/visual_pedagogy/batch3/poincare/plate_extinction.svg',
        alt: 'A four-stage event graph shows an initial closed three-manifold, Ricci flow with surgery, finite extinction under theorem hypotheses, and reverse topological bookkeeping.',
        title: 'Finite Extinction and Reverse Bookkeeping',
        note: 'The event graph separates geometric evolution from reverse topological bookkeeping; schematic extinction is not itself proof.'
      }
    },
    riemann: {
      '../../assets/documentaries/riemann/euler.svg': {
        src: '../../assets/visual_pedagogy/batch3/riemann/euler.svg',
        alt: 'Prime-indexed Euler factors for p equals 2, 3, 5, and all primes assemble into the zeta Euler product, with Re(s) greater than 1 marked as the absolute-convergence domain.',
        title: 'The Euler Product and Its Convergence Boundary',
        note: 'The Euler product is shown with its Re(s) greater than 1 absolute-convergence domain; termwise critical-strip use and RH are not claimed.'
      },
      '../../assets/documentaries/riemann/evidence.svg': {
        src: '../../assets/visual_pedagogy/batch3/riemann/evidence.svg',
        alt: 'Four panels distinguish finite zero verification, partial critical-line results, heuristic evidence, and the universal Riemann hypothesis, which remains open.',
        title: 'Evidence Does Not Remove the Infinite Quantifier',
        note: 'Finite, partial, heuristic, and universal statements remain logically distinct; bounded evidence does not become a proof of RH.'
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
      image.dataset.visualPedagogyActivation = reader.dataset.gclReader === 'bsd' ? 'bsd-exact-object' : 'batch1';
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
