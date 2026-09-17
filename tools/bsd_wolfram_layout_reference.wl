(* BSD documentary exact-object visual layout reference.
   Mathematical fixtures remain governed by bsd_wolfram_semantic_master.wl.
   This file records the Wolfram-native layout language used to review the web delivery derivatives.
   No expression in this file is mathematical evidence. *)

ClearAll["Global`*"];
navy = RGBColor[8/255, 26/255, 46/255];
gold = RGBColor[194/255, 154/255, 72/255];
paper = RGBColor[243/255, 234/255, 213/255];
pale = RGBColor[232/255, 237/255, 240/255];
soft = RGBColor[247/255, 240/255, 223/255];
serif = "Times"; sans = "Helvetica";

wrap[s_, w_, fs_: 19] := Pane[
  Style[s, fs, navy, FontFamily -> serif, LineSpacing -> {1.08, 0}],
  {w, Automatic}, Alignment -> Left
];
panel[title_, body_, w_] := Framed[
  Column[{Style[title, 21, Bold, navy, FontFamily -> sans], body},
    Spacings -> .9, Alignment -> Left],
  Background -> paper, FrameStyle -> Directive[navy, Opacity[.55]],
  RoundingRadius -> 5, FrameMargins -> {{18, 18}, {14, 14}},
  ImageSize -> {w, Automatic}
];
header[roman_, title_, subtitle_] := Column[{
  Style["PLATE " <> roman <> " · " <> title, 34, Bold, navy, FontFamily -> serif],
  Style[subtitle, 16, GrayLevel[.35], FontFamily -> sans]
}, Alignment -> Center, Spacings -> .3];
plateFrame[items_] := Framed[
  Column[items, Spacings -> {Automatic, 1.05}, Alignment -> Center],
  Background -> paper, FrameStyle -> Directive[gold, 1.5],
  FrameMargins -> {{28, 28}, {24, 24}}, ImageSize -> {1450, 930}
];

(* Plate I *)
e5[x_] := x^3 - 25 x;
p5 = {25/4, 75/8};
curve5 = ContourPlot[y^2 == e5[x], {x, -8, 15}, {y, -18, 22},
  ContourStyle -> Directive[navy, Thick], PlotPoints -> 70, Frame -> True,
  Axes -> True, Background -> paper, PlotRangePadding -> Scaled[.03],
  ImageSize -> {760, 470},
  Epilog -> {gold, PointSize[.018], Point[p5], navy,
    Text[Style["P = (25/4, 75/8)", 16, Bold, FontFamily -> serif], p5 + {3.6, 1.6}]}
];
triangle5 = Graphics[{
  FaceForm[pale], EdgeForm[Directive[navy, Thick]], Polygon[{{0, 0}, {3/2, 0}, {0, 20/3}}],
  gold, PointSize[.025], Point[{{0, 0}, {3/2, 0}, {0, 20/3}}], navy,
  Text[Style["3/2", 18, Bold, FontFamily -> serif], {3/4, -.6}],
  Text[Style["20/3", 18, Bold, FontFamily -> serif], {-.55, 10/3}],
  Text[Style["41/6", 18, Bold, FontFamily -> serif], {1.05, 3.5}],
  Text[Style["area = 5", 20, Bold, FontFamily -> sans], {.75, -1.45}]},
  PlotRange -> {{-1.1, 2.15}, {-2, 7.6}}, Frame -> True,
  FrameStyle -> Directive[navy, Opacity[.55]], Background -> paper, ImageSize -> {470, 470}
];
plate1 = plateFrame[{
  header["I", "Rational point to rational triangle", "Exact object correspondence · E5 and the congruent-number triangle"],
  Grid[{{panel["The elliptic curve", curve5, 810], panel["Exact rational right triangle", triangle5, 500]}}, Alignment -> Top, Spacings -> {1.2, 0}],
  Framed[Grid[{{"Elliptic curve", "E5: y^2 = x^3 - 25x", "Rational point", "P = (25/4, 75/8)"},
               {"Triangle", "a = 3/2   b = 20/3   c = 41/6", "Area", "ab/2 = 5"}},
      Alignment -> Left, Spacings -> {1.4, 1.1}], Background -> soft,
      FrameStyle -> Directive[gold, Opacity[.8]], FrameMargins -> {{24, 24}, {18, 18}}],
  Style["Exact arithmetic correspondence. The finite real plot does not determine rank and does not prove BSD.", 15, navy, FontFamily -> serif]
}];

(* Plate II *)
e2[x_] := x^3 - x + 1; p = {0, 1}; q = {1, 1}; r = {-1, 1}; sum = {-1, -1};
groupPlot = ContourPlot[y^2 == e2[x], {x, -2.4, 2.4}, {y, -3.2, 3.4},
  ContourStyle -> Directive[navy, Thick], PlotPoints -> 70, Frame -> True, Axes -> True,
  Background -> paper, PlotRangePadding -> Scaled[.03], ImageSize -> {790, 515},
  Epilog -> {Directive[gold, Dashed, Thick], Line[{{-2.4, 1}, {2.4, 1}}], gold,
    PointSize[.018], Point[{p, q, r, sum}], Arrow[{r, sum}]}
];
steps = Grid[MapIndexed[{Framed[Style[First@#2, 16, Bold, navy, FontFamily -> sans],
        Background -> pale, FrameStyle -> None, RoundingRadius -> 20, FrameMargins -> 8], wrap[#1, 390, 19]} &,
    {"P = (0,1), Q = (1,1)", "Their chord is y = 1", "The third intersection is R = (-1,1)",
     "Reflect R across the x-axis", "P + Q = -R = (-1,-1)"}], Alignment -> {Left, Center}, Spacings -> {1.3, 1.5}];
plate2 = plateFrame[{
  header["II", "The chord–tangent group law", "Exact rational addition on E: y^2 = x^3 - x + 1"],
  Grid[{{panel["The elliptic curve and the chord y = 1", groupPlot, 830], panel["Construction", steps, 470]}}, Alignment -> Top, Spacings -> {1.2, 0}],
  Framed[wrap["The displayed rational points satisfy the exact group-law construction; the plate illustrates the operation, not the full Mordell–Weil group.", 1260, 18],
    Background -> soft, FrameStyle -> Directive[gold, Opacity[.8]], FrameMargins -> {{24, 24}, {16, 16}}],
  Style["Exact rational example of geometric addition. The construction illustrates the operation, not the global group structure.", 15, navy, FontFamily -> serif]
}];

(* Plate III *)
pointsMod[prime_] := Select[Tuples[Range[0, prime - 1], 2], Mod[#[[2]]^2 - e5[#[[1]]], prime] == 0 &];
pointCount[prime_] := 1 + Length[pointsMod[prime]]; ap[prime_] := prime + 1 - pointCount[prime];
pts13 = pointsMod[13]; primes = {3, 7, 11, 13, 17, 19, 23, 29, 31}; vals = ap /@ primes;
finitePlot = ListPlot[pts13, PlotStyle -> Directive[gold, PointSize[.02]], Frame -> True,
  PlotRange -> {{-.5, 12.5}, {-.5, 12.5}}, GridLines -> {Range[0, 12], Range[0, 12]},
  GridLinesStyle -> Directive[GrayLevel[.8], Thin], AspectRatio -> 1, Background -> paper, ImageSize -> {610, 390}];
tracePlot = BarChart[vals, ChartLabels -> Placed[primes, Below], ChartStyle -> gold,
  Background -> paper, ImageSize -> {1160, 170}, PlotRangePadding -> Scaled[.05]];
facts = Column[{Grid[{{"Affine solutions", 19}, {"#E5(F_13)", 20}, {"a_13 = 13 + 1 - #E5(F_13)", -6}}, Alignment -> Left],
  Framed[Column[{Style["Local Euler factor", 15, Bold, navy, FontFamily -> sans],
    wrap["(1 + 6·13^(-s) + 13^(1-2s))^(-1)", 390, 20]}], Background -> soft,
    FrameStyle -> Directive[gold, Opacity[.75]], FrameMargins -> {{16, 16}, {11, 11}}]}];
plate3 = plateFrame[{
  header["III", "Counting at a good prime", "Exact finite computation for E5 modulo 13"],
  Grid[{{panel["Finite-field point set", finitePlot, 720], panel["Exact local data at p = 13", facts, 500]}}, Alignment -> Top, Spacings -> {1.15, 0}],
  panel["Exact finite sample of a_p at selected good primes", tracePlot, 1240],
  Style["Each good prime contributes a local Euler factor. No single prime, and no finite sample, determines rank.", 14, navy, FontFamily -> serif]
}];

(* Plate IV *)
leadingLHS = Row[{Superscript[Subscript["L", "E"], "(r)"], "(1) / r!"}];
leadingRHS = Row[{"= ", Subscript["Ω", "E"], " · Reg(E/ℚ) · #Sha(E/ℚ) · ",
                  Subscript["∏", "p"], " ", Subscript["c", "p"], " / ",
                  Superscript[Subscript["#E(ℚ)", "tors"], 2]}];
ledger = Grid[{{"Real period", Subscript["Ω", "E"]}, {"Regulator", "Reg(E/ℚ)"}, {"Tate–Shafarevich", "#Sha(E/ℚ)"},
               {"Local components", Row[{Subscript["∏", "p"], " ", Subscript["c", "p"]}]},
               {"Torsion denominator", Superscript[Subscript["#E(ℚ)", "tors"], 2]}}, Alignment -> Left];
obligations = Grid[{{1, "Rank equality", Row[{"rank E(ℚ) = ", Subscript["ord", "s=1"], " L(E,s)"}]},
                    {2, "Sha finiteness", "#Sha(E/ℚ) is finite"},
                    {3, "Leading term", "the normalized leading coefficient equals the complete arithmetic factor ledger"}}, Alignment -> Left];
plate4 = plateFrame[{
  header["IV", "The strong BSD leading-term ledger", "Quantified dependency structure · three logically distinct obligations"],
  Framed[Column[{Style["The leading-term identity", 21, Bold, navy, FontFamily -> sans],
    Style[leadingLHS, 28, Bold, navy, FontFamily -> serif],
    Style[leadingRHS, 23, navy, FontFamily -> serif]}, Alignment -> Center],
    Background -> soft, FrameStyle -> Directive[gold, Opacity[.8]], FrameMargins -> {{24, 24}, {18, 18}}],
  panel["Arithmetic factor ledger", ledger, 1270], panel["Three obligations, not one slogan", obligations, 1120],
  Style["Rank equality, Sha finiteness, and the normalized leading-term identity are separate obligations.", 14, navy, FontFamily -> serif]
}];

(* Plate V *)
frontierRows = {{"Mordell–Weil finite generation", "all E/ℚ", "ESTABLISHED"}, {"Modularity", "all E/ℚ", "ESTABLISHED"},
  {"rank equality + finite Sha", "analytic rank 0 or 1", "ESTABLISHED"}, {"rank E(ℚ) = ord at s = 1", "all E/ℚ", "OPEN"},
  {"Sha(E/ℚ) finite", "all E/ℚ", "OPEN"}, {"complete normalized leading term", "all E/ℚ", "OPEN"}};
frontier = Grid[Prepend[frontierRows, {"Statement", "Scope", "Status"}], Frame -> All,
  FrameStyle -> Directive[navy, Opacity[.5]], Alignment -> {Left, Center}, Spacings -> {1.2, 1.0}];
plate5 = plateFrame[{
  header["V", "The exact BSD theorem frontier", "Scope is part of theorem status"],
  Column[{Style["Established terrain and universal open frontier", 20, Bold, navy, FontFamily -> sans], frontier}],
  Framed[Column[{Style["Quantifier guardrail", 19, Bold, navy, FontFamily -> sans],
    wrap["Finite computation, parity, Selmer bounds, family averages, p-adic formulas, and one-prime results do not remove the universal quantifier.", 1240, 18]}],
    Background -> soft, FrameStyle -> Directive[gold, Opacity[.8]], FrameMargins -> {{20, 20}, {14, 14}}],
  Style["Established special cases do not erase the universal conjecture.", 14, navy, FontFamily -> serif]
}];

bsdDocumentaryLayoutReference = <|
  "plate_01_rational_point_triangle" -> plate1,
  "plate_02_group_law" -> plate2,
  "plate_03_good_prime" -> plate3,
  "plate_04_strong_bsd_ledger" -> plate4,
  "plate_05_theorem_frontier" -> plate5
|>;

(* Review rendering: Rasterize[#, "Image", RasterSize -> {1536,1024}] & /@ bsdDocumentaryLayoutReference *)
