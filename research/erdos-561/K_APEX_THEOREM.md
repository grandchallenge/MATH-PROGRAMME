# The independent-apex star-forest edge-colouring lemma

**Claim tier:** proof candidate; ordinary mathematical proof, not Lean-checked or independently certified. [MATH-PROGRAMME #3490](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3490).

## Theorem

Let `G` be a finite **simple** graph of maximum degree `D`. Let `U` be an independent set of `k>=1` vertices, **all of degree `D`**. If `G-U` is a star forest (isolated vertices allowed) and `D>=3k`, then the edge chromatic number of `G` is exactly `D`.

## Proof

Let `B` consist of all edges meeting `U`. As `U` is independent, `B` is bipartite with shore `U`, and has maximum degree at most `D`. **König's line-colouring theorem** gives a proper edge-colouring of `B` using colours `P={1,...,D}`. Equivalently, this colouring can be constructed using two-colour alternating-path recolourings, implemented in `k_apex_colouring.py`.

Fix any nontrivial star component `S` of `G-U` with centre `c` and `h` leaves. Let `P_c` be the colours not appearing on the `B`-edges at `c`. Since `c` meets at most `k` apices, `|P_c|>=D-k`. The original graph has degree at most `D`, so `h<=|P_c|`.

For each leaf `x` of `S`, let `L_x⊆P_c` be the colours that do not appear on its incident `B`-edges. Each leaf has at most `k` such edges, so `|L_x|>=D-2k>=k`.

Moreover, **each colour is absent from at most `k` leaf lists**. Indeed, among apex edges, a fixed colour occurs at most once at each of the `k` apices; at most `k` distinct leaf endpoints can therefore forbid it.

Now verify Hall's criterion for any nonempty subset `X` of the leaves:

- If `|X|<=k`, some `L_x` has at least `k>=|X|` colours, so `|∪_{x∈X} L_x|>=|X|`.
- If `|X|>k`, no colour in `P_c` can be missing from every list in `X`, hence `∪_{x∈X}L_x=P_c`; therefore `|∪ L_x|=|P_c|>=h>=|X|`.

Hall gives `h` pairwise distinct permitted colours for the `h` star edges. Colour different components independently. This extends the colouring of `B` to a proper `D`-edge-colouring of `G`. Since the apices have degree `D`, fewer than `D` colours are impossible. Thus `χ'(G)=D`. □

## Scope / caution

The threshold `D>=3k` is **sufficient**, not claimed sharp. Independence of the apices, their degree `D`, simplicity, and the star-forest residual are all essential **hypotheses of this proof**; the theorem does not classify all Ramsey extremizers. No historical priority claim.

## Constructive replay

`python3 k_apex_colouring.py` uses an edge-recolouring algorithm for the bipartite portion and augmenting-path systems of distinct representatives for star edges. Its deterministic seed 561 tests `k=1..4`, `D=3k,3k+1,3k+3` (3,000 cases in total). The finite tests corroborate, but do not replace, the general proof.
