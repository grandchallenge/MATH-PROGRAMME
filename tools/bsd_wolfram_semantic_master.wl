(* BSD-001 exact-object-first documentary semantic master.
   Wolfram Language is used to verify the mathematics and to provide a
   reproducible reference rendering. Static web SVGs are publication
   derivatives; no visualization is proof evidence. *)

ClearAll["Global`*"];

navy = RGBColor[8/255, 26/255, 46/255];
gold = RGBColor[194/255, 154/255, 72/255];
paper = RGBColor[243/255, 234/255, 213/255];
pale = RGBColor[232/255, 237/255, 240/255];

assert[name_, test_] := If[TrueQ[test], Null, Print["FAILED: " <> name]; Abort[]];

(* Plate I: congruent-number-five exact object. *)
e5[x_] := x^3 - 25 x;
p5 = {25/4, 75/8};
triangle5 = {3/2, 20/3, 41/6};
assert["P5 lies on E5", p5[[2]]^2 == e5[p5[[1]]]];
assert["triangle is right", triangle5[[1]]^2 + triangle5[[2]]^2 == triangle5[[3]]^2];
assert["triangle area is five", triangle5[[1]] triangle5[[2]]/2 == 5];

curve5 = ContourPlot[
  y^2 == e5[x], {x, -8, 15}, {y, -18, 22},
  ContourStyle -> Directive[navy, Thick], PlotPoints -> 70,
  Frame -> True, Axes -> True, FrameLabel -> {"x", "y"},
  Background -> paper,
  Epilog -> {gold, PointSize[.018], Point[p5], navy,
    Text[Style["P = (25/4, 75/8)", 14], p5 + {3.2, 1.5}]}
];
triangleGraphic = Graphics[
  {FaceForm[pale], EdgeForm[{navy, Thick}],
   Polygon[{{0, 0}, {3/2, 0}, {0, 20/3}}], gold, PointSize[.025],
   Point[{{0, 0}, {3/2, 0}, {0, 20/3}}], navy,
   Text[Style["3/2", 14], {3/4, -1/2}],
   Text[Style["20/3", 14], {-1/2, 10/3}],
   Text[Style["41/6", 14], {1, 4}],
   Text[Style["area = 5", 15], {3/4, -1.2}]},
  PlotRange -> {{-1, 2}, {-1.8, 7.4}}, Frame -> True, Background -> paper
];

(* Plate II: exact chord-tangent example. *)
e2[x_] := x^3 - x + 1;
p2 = {0, 1}; q2 = {1, 1}; r2 = {-1, 1}; sum2 = {-1, -1};
Scan[assert["group-law point lies on E", #[[2]]^2 == e2[#[[1]]]] &, {p2, q2, r2, sum2}];
assert["third intersection is R", Expand[e2[x] - 1] == Expand[(x + 1) x (x - 1)]];
assert["reflection gives P+Q", sum2 == {r2[[1]], -r2[[2]]}];

groupPlot = ContourPlot[
  y^2 == e2[x], {x, -2.4, 2.4}, {y, -3.2, 3.4},
  ContourStyle -> Directive[navy, Thick], PlotPoints -> 70,
  Frame -> True, Axes -> True, Background -> paper,
  Epilog -> {Directive[gold, Dashed, Thick], Line[{{-2.4, 1}, {2.4, 1}}],
    gold, PointSize[.018], Point[{p2, q2, r2, sum2}], navy,
    Text["R=(-1,1)", r2 + {-0.65, .2}], Text["P=(0,1)", p2 + {.4, .2}],
    Text["Q=(1,1)", q2 + {.45, .2}], Text["P+Q=(-1,-1)", sum2 + {0, -.35}],
    gold, Arrow[{r2, sum2}]}
];

(* Plate III: exact finite-field count and sample traces. *)
pointsMod[p_] := Select[Tuples[Range[0, p - 1], 2], Mod[#[[2]]^2 - e5[#[[1]]], p] == 0 &];
pointCount[p_] := 1 + Length[pointsMod[p]];
ap[p_] := p + 1 - pointCount[p];
pts13 = pointsMod[13];
assert["19 affine F13 points", Length[pts13] == 19];
assert["20 projective F13 points", pointCount[13] == 20];
assert["a13 = -6", ap[13] == -6];
samplePrimes = {3, 7, 11, 13, 17, 19, 23, 29, 31};
sampleAP = Association@Table[p -> ap[p], {p, samplePrimes}];
assert["sample a_p fixture", Values[sampleAP] == {0, 0, 0, -6, -2, 0, 0, -10, 0}];
finiteFieldPlot = ListPlot[pts13, PlotStyle -> Directive[gold, PointSize[.018]],
  Frame -> True, FrameLabel -> {"x mod 13", "y mod 13"},
  PlotRange -> {{-.5, 12.5}, {-.5, 12.5}}, GridLines -> {Range[0, 12], Range[0, 12]},
  AspectRatio -> 1, Background -> paper];
tracePlot = BarChart[Values[sampleAP], ChartLabels -> Keys[sampleAP],
  AxesLabel -> {"p", "a_p"}, ChartStyle -> gold, Background -> paper];

(* Plates IV-V: quantified structures. *)
strongBSD = HoldForm[L^(r)[E, 1]/r! == (Omega[E] Reg[E/Q] ShaOrder[E/Q] Product[c[p], p])/TorsionOrder[E/Q]^2];
obligations = {
  "rank E(Q) = ord_(s=1) L(E,s)",
  "#Sha(E/Q) is finite",
  "normalized leading term equals the arithmetic factor ledger"
};
frontier = {
  {"Mordell-Weil finite generation", "all E/Q", "ESTABLISHED"},
  {"Modularity", "all E/Q", "ESTABLISHED"},
  {"rank equality + finite Sha", "analytic rank 0 or 1", "ESTABLISHED"},
  {"rank E(Q) = ord at s = 1", "all E/Q", "OPEN"},
  {"Sha(E/Q) finite", "all E/Q", "OPEN"},
  {"complete normalized leading term", "all E/Q", "OPEN"}
};

semanticFixture = <|
  "plate_01" -> <|"curve" -> "y^2=x^3-25x", "point" -> p5, "triangle" -> triangle5, "area" -> 5|>,
  "plate_02" -> <|"curve" -> "y^2=x^3-x+1", "P" -> p2, "Q" -> q2, "R" -> r2, "PplusQ" -> sum2|>,
  "plate_03" -> <|"p" -> 13, "affine_points" -> pts13, "projective_count" -> pointCount[13], "a13" -> ap[13], "sample_ap" -> sampleAP|>,
  "plate_04" -> <|"formula" -> ToString[strongBSD, InputForm], "obligations" -> obligations|>,
  "plate_05" -> frontier
|>;

Print[ExportString[semanticFixture, "RawJSON", "Compact" -> False]];
