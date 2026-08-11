(* OZ-RT-BZ-T3-009: exact RISC-free Q-row replay.
   Requires a Wolfram Language kernel and network access to the exact pinned GitHub blob.
   No HolonomicFunctions/RISC package is loaded. *)

Clear[n,k,l,e];
url = "https://raw.githubusercontent.com/rain-1/-odd-zeta-values-moremath/968477ed7e406df6542f8da6fbe1cd6ca7273c47/work/lb5/Qrow_rhosigma.m";
expectedBlob = "61f12f412726887f506e1d423b7ee183a22116e5";

bytes = Import[url, "Byte"];
prefix = ToCharacterCode["blob " <> ToString[Length[bytes]] <> FromCharacterCode[0]];
blob = IntegerString[Hash[ByteArray[Join[prefix, bytes]], "SHA1"], 16, 40];
If[blob =!= expectedBlob, Print["QROW_BLOB_MISMATCH: ", blob]; Abort[]];

{rho, sigma} = ToExpression[FromCharacterCode[bytes]];
If[{LeafCount[rho], LeafCount[sigma]} =!= {10553, 1819}, Print["QROW_LEAFCOUNT_DRIFT"]; Abort[]];

(* Independent kernel ratios from the Gamma-product definition of T. *)
rn[j_Integer?NonNegative] := Together[
  Product[(n+k+i) (n+l+i) (n+k+l+i) (n+i) /
          ((n-k+i)^2 (n-l+i)^2), {i,1,j}]];
rk = Together[(n-k)^2 (n+k+1) (n+k+l+1) / ((k+1)^3 (k+l+1))];
rl = Together[(n-l)^2 (n+l+1) (n+k+l+1) / ((l+1)^3 (k+l+1))];

a0[x_] := 41218 x^3 + 198849 x^2 + 320790 x + 173057;
b8[x_] := 3874492 x^8 + 59373972 x^7 + 394148190 x^6 + 1481084196 x^5 +
          3447878810 x^4 + 5095855458 x^3 + 4673546679 x^2 + 2433871008 x + 551502039;
b9[x_] := 48802112 x^9 + 967468896 x^8 + 8488000862 x^7 + 43246197636 x^6 +
          140983768422 x^5 + 304912330849 x^4 + 437406946975 x^3 + 401272692378 x^2 +
          213593890911 x + 50257929339;
cc = {(n+1)^5 (n+2) a0[n+1], -2 (n+2) b8[n], -2 b9[n],
      2 (n+3)^5 (2 n+5) a0[n]};

(* Delta_k F = F(k+1)-F(k), and analogously for l. *)
z = Together[
  Sum[cc[[j+1]] rn[j], {j,0,3}] -
  ((rho /. k -> k+1) rk - rho + (sigma /. l -> l+1) rl - sigma)];
identityZero = TrueQ[Expand[Numerator[z]] === 0];
If[!identityZero, Print["QROW_CLEARED_NUMERATOR_NONZERO"]; Abort[]];

lowerBoundary = {
  TrueQ[Together[rho /. k -> 0] === 0],
  TrueQ[Together[sigma /. l -> 0] === 0]
};
If[!And @@ lowerBoundary, Print["QROW_LOWER_BOUNDARY_FAILURE"]; Abort[]];

(* Candidate poles at n+1,n+2,n+3 are exactly order <=2.  Multiplying by
   (coordinate-(n+r))^2 gives a finite rational function at each shell. *)
rhoShells = Table[
  Quiet[Check[
    With[{v = Together[((k-(n+r))^2 rho) /. k -> n+r]},
      FreeQ[v, Indeterminate | ComplexInfinity | DirectedInfinity]], False]],
  {r,1,3}];
sigmaShells = Table[
  Quiet[Check[
    With[{v = Together[((l-(n+r))^2 sigma) /. l -> n+r]},
      FreeQ[v, Indeterminate | ComplexInfinity | DirectedInfinity]], False]],
  {r,1,3}];
If[!(And @@ rhoShells && And @@ sigmaShells), Print["QROW_SHELL_POLE_ORDER_FAILURE"]; Abort[]];

(* T contains 1/Gamma[n-k+1]^2 and 1/Gamma[n-l+1]^2.  At offsets r=1,2,3
   these are double zeros with the exact leading coefficients below. *)
gammaZeroCoefficients = Table[
  Coefficient[Normal[Series[1/Gamma[1-r-e]^2, {e,0,2}]], e, 2],
  {r,1,3}];
If[gammaZeroCoefficients =!= {1,1,4}, Print["QROW_KERNEL_ZERO_ORDER_FAILURE"]; Abort[]];

result = <|
  "blob" -> blob,
  "bytes" -> Length[bytes],
  "leafCounts" -> {LeafCount[rho], LeafCount[sigma]},
  "identity" -> identityZero,
  "lowerBoundary" -> lowerBoundary,
  "rhoShells" -> rhoShells,
  "sigmaShells" -> sigmaShells,
  "gammaZeroCoefficients" -> gammaZeroCoefficients,
  "success" -> And[identityZero, And @@ lowerBoundary, And @@ rhoShells,
                    And @@ sigmaShells, gammaZeroCoefficients === {1,1,4}]
|>;
Print[ExportString[result, "RawJSON", "Compact" -> True]];
If[!TrueQ[result["success"]], Abort[]];
