(() => {
  const reader = document.querySelector('[data-gcl-reader="bsd"]');
  if (!reader) return;

  const plateActivations = {
    '../../assets/documentaries/bsd/plate_curve.svg': {
      src: '../../assets/visual_pedagogy/bsd_exact/plate_01_rational_point_triangle.svg',
      alt: 'Exact finite-window plot of E5, y squared equals x cubed minus 25x, with P equals 25 over 4 comma 75 over 8, paired with the exact rational right triangle of sides 3 over 2, 20 over 3, and 41 over 6 and area five.',
      title: 'Rational Point to Rational Triangle',
      note: 'Exact arithmetic correspondence. The finite real plot does not determine rank and does not prove BSD.'
    },
    '../../assets/documentaries/bsd/plate_harmony.svg': {
      src: '../../assets/visual_pedagogy/bsd_exact/plate_02_group_law.svg',
      alt: 'Exact chord-tangent addition example on y squared equals x cubed minus x plus one, with P equals zero comma one, Q equals one comma one, third intersection R equals minus one comma one, and reflected sum P plus Q equals minus one comma minus one.',
      title: 'The Chord–Tangent Group Law',
      note: 'Exact rational addition example. It illustrates the operation; it is not a picture of the full Mordell–Weil group.'
    },
    '../../assets/documentaries/bsd/plate_bridge.svg': {
      src: '../../assets/visual_pedagogy/bsd_exact/plate_03_good_prime.svg',
      alt: 'Exact finite-field point set for E5 modulo 13 with 19 affine solutions, total point count 20, a13 equal to minus 6, the resulting local Euler factor, and an exact finite sample of a p values at selected good primes.',
      title: 'Counting at a Good Prime',
      note: 'Each displayed point and trace value is exact. No single prime, and no finite sample of primes, determines rank.'
    },
    '../../assets/documentaries/bsd/plate_overture.svg': {
      src: '../../assets/visual_pedagogy/bsd_exact/plate_04_strong_bsd_ledger.svg',
      alt: 'Strong BSD leading-term formula with separate labelled inputs for the real period, regulator, Tate-Shafarevich order, local Tamagawa factors, rational torsion denominator, and a three-row list separating rank equality, Sha finiteness, and the leading-term identity.',
      title: 'The Strong BSD Leading-Term Ledger',
      note: 'The dependency structure is explicit. It does not convert the conjectural identity or its finiteness hypothesis into established facts.'
    },
    '../../assets/documentaries/bsd/plate_frontier.svg': {
      src: '../../assets/visual_pedagogy/bsd_exact/plate_05_theorem_frontier.svg',
      alt: 'Six-row theorem-status matrix separating Mordell-Weil finite generation, modularity, and analytic-rank-zero-or-one results from the universally open rank equality, Sha finiteness, and complete normalized leading-term formula.',
      title: 'The Exact BSD Theorem Frontier',
      note: 'Scope is part of theorem status. Established special cases do not remove the universal quantifier.'
    }
  };

  reader.querySelectorAll('.monograph-plate img').forEach((image) => {
    const original = image.getAttribute('src');
    const activation = plateActivations[original];
    if (!activation) return;
    image.src = activation.src;
    image.alt = activation.alt;
    image.dataset.visualPedagogyActivation = 'bsd-exact-object';
    const figure = image.closest('[data-plate]');
    const title = figure?.querySelector('figcaption strong');
    const note = figure?.querySelector('figcaption small');
    if (title) title.textContent = activation.title;
    if (note) note.textContent = activation.note;
  });
})();
