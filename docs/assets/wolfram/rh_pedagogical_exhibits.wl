(* Riemann Hypothesis announcement: Wolfram pedagogical exhibits
   Public, executable companion to the Chaidez-style exposition.
   Scope: elementary exact algebra and finite numerical illustrations.
   NOT: a check of the submitted Lean source or a proof of RH/Dirichlet GRH.
   Wolfram Language functions: ZetaZero, MangoldtLambda, EulerGamma.
*)

Module[{s, t, z, p, psi, sourceWeighted, heights, onLine, rows, results},
  p[z_] := ((z - 1/3)^2 + 4) ((z - 2/3)^2 + 4);

  (* The first five *known* critical-line zero heights; not an exhaustive
     search for zeros away from the line. *)
  heights = Table[N[Im[N[ZetaZero[k], 35]], 12], {k, 1, 5}];

  (* Exact obstruction: a real-coefficient polynomial with the same
     reflection and conjugation symmetries but four off-line zeros. *)
  onLine = Expand[ComplexExpand[p[1/2 + I t]]];

  (* Prime-power weights and the smoothed sum cited in the announcement.
     The + subscript is unnecessary here because 1 <= k <= n. *)
  psi[n_Integer?Positive] := Sum[MangoldtLambda[k], {k, 1, n}];
  sourceWeighted[n_Integer?Positive] :=
    Sum[MangoldtLambda[k] (n/k - 1), {k, 1, n}]
      - n Log[n] + (1 + EulerGamma) n;

  rows = Table[
    {n, N[psi[n], 12], N[sourceWeighted[n], 12]},
    {n, {10, 20, 50, 100}}
  ];

  results = <|
    "knownZeroHeights" -> heights,
    "exactReflectionSymmetry" -> TrueQ[FullSimplify[p[s] == p[1 - s]]],
    "offLineRoot" -> p[1/3 + 2 I],
    "criticalLineSquareIdentity" ->
      TrueQ[FullSimplify[onLine == (145/36 - t^2)^2 + t^2/9]],
    "noZerosOfCountermodelOnCriticalLine" ->
      TrueQ[Resolve[ForAll[t, Element[t, Reals], onLine > 0], Reals]],
    "rowsX_Psi_Weighted" -> rows
  |>;

  If[!TrueQ[results["exactReflectionSymmetry"]] ||
     !TrueQ[results["offLineRoot"] == 0] ||
     !TrueQ[results["criticalLineSquareIdentity"]] ||
     !TrueQ[results["noZerosOfCountermodelOnCriticalLine"]],
    Print["Exact algebra self-check failed."];
    Abort[]
  ];

  Print[results];
  results
]

(* Optional notebook visualization of the first 30 known critical-line zeros:
   ListPlot[
     Table[{Re[N[ZetaZero[k], 20]], Im[N[ZetaZero[k], 20]]},
       {k, 1, 30}],
     Frame -> True, FrameLabel -> {"Re(s)", "Im(s)"},
     PlotRange -> {{0, 1}, All},
     PlotMarkers -> Automatic
   ]
   The picture samples known zeros; it does not survey the whole strip.
*)
