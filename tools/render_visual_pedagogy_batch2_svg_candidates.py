#!/usr/bin/env python3
# Deterministically render Batch-2 BSD/Hodge visual-pedagogy SVG review candidates.
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
BSD_OUT = ROOT / "governance" / "visual_pedagogy" / "review_candidates" / "bsd"
HODGE_OUT = ROOT / "governance" / "visual_pedagogy" / "review_candidates" / "hodge"

def svg_document(title, desc, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(desc)}</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#222"/></marker>
</defs>
<style>
text{{font-family:Arial,Helvetica,sans-serif;fill:#111}}
.h1{{font-size:34px;font-weight:700}} .h2{{font-size:22px;font-weight:700}}
.body{{font-size:19px}} .small{{font-size:16px}} .tiny{{font-size:14px}}
.mono{{font-family:"DejaVu Sans Mono",monospace;font-size:17px}}
.box{{fill:white;stroke:#222;stroke-width:2}} .soft{{fill:#f2f2f2;stroke:#444;stroke-width:2}}
.open{{fill:white;stroke:#222;stroke-width:2;stroke-dasharray:9 7}}
.line{{stroke:#222;stroke-width:2;fill:none}} .arrow{{stroke:#222;stroke-width:2.5;fill:none;marker-end:url(#arrow)}}
.sep{{stroke:#777;stroke-width:1.5}} .label{{font-size:15px;font-weight:700;letter-spacing:1px}}
</style>
<rect width="1200" height="900" fill="white"/>
{body}
<text x="40" y="872" class="small">Review candidate · documentary exposition only · visual_is_evidence: false</text>
</svg>
'''

def bsd_bridge():
    body = r'''
<text x="40" y="55" class="h1">From local point counts to the central point</text>
<text x="40" y="92" class="body">The analytic ledger is assembled prime by prime; no single local factor determines the Mordell-Weil rank.</text>

<rect x="45" y="145" width="335" height="255" rx="12" class="box"/>
<text x="70" y="185" class="h2">At a good prime p</text>
<text x="70" y="230" class="mono">a_p = p + 1 - #E(F_p)</text>
<text x="70" y="278" class="mono">L_p(E,s)^(-1)</text>
<text x="70" y="308" class="mono">= 1 - a_p p^(-s) + p^(1-2s)</text>
<text x="70" y="355" class="small">Bad primes use their separately defined</text>
<text x="70" y="378" class="small">local factors; they are not omitted.</text>

<path d="M395 270 L520 270" class="arrow"/>
<text x="420" y="245" class="small">assemble all</text>
<text x="430" y="265" class="small">local factors</text>

<rect x="535" y="145" width="280" height="255" rx="12" class="soft"/>
<text x="560" y="185" class="h2">Global L-function</text>
<text x="560" y="240" class="mono">L(E,s) = product_p L_p(E,s)</text>
<text x="560" y="292" class="small">Initially an Euler product in its</text>
<text x="560" y="315" class="small">half-plane of convergence.</text>
<text x="560" y="355" class="small">Modularity supplies analytic continuation</text>
<text x="560" y="378" class="small">and a functional equation centered at s=1.</text>

<path d="M830 270 L945 270" class="arrow"/>
<text x="850" y="245" class="small">continue, then</text>
<text x="865" y="265" class="small">inspect s=1</text>

<rect x="960" y="145" width="195" height="255" rx="12" class="box"/>
<text x="985" y="185" class="h2">Central order</text>
<text x="985" y="240" class="mono">r_an = ord_(s=1)</text>
<text x="985" y="270" class="mono">       L(E,s)</text>
<text x="985" y="320" class="small">Count how many</text>
<text x="985" y="343" class="small">Taylor terms vanish</text>
<text x="985" y="366" class="small">before the first</text>
<text x="985" y="389" class="small">nonzero coefficient.</text>

<rect x="45" y="485" width="1110" height="275" rx="12" class="box"/>
<text x="70" y="530" class="h2">Claim boundary</text>
<text x="70" y="575" class="body">1. Local point counts determine local coefficients; they do not individually reveal rank.</text>
<text x="70" y="615" class="body">2. The Euler product and its continuation define the analytic side of BSD.</text>
<text x="70" y="655" class="body">3. BSD conjectures r_alg = r_an; this plate does not assert that equality.</text>
<text x="70" y="705" class="small">The displayed formulas are structural. No numerical point-count dataset or curve-specific rank is inferred here.</text>
'''
    return svg_document(
        "From prime counts to the central point — Batch-2 review candidate",
        "A literal pipeline maps a good-prime point count to a local Euler factor, then to the global elliptic-curve L-function, and finally to its order of vanishing at s equals one. The claim boundary states that no single prime determines rank and BSD equality remains conjectural.",
        body,
    )

def bsd_harmony():
    body = r'''
<text x="40" y="55" class="h1">One elliptic curve, two mathematically distinct ledgers</text>
<text x="40" y="92" class="body">BSD compares invariants built by different constructions; the visual bridge is a conjecture, not an identity by definition.</text>

<rect x="55" y="150" width="470" height="470" rx="14" class="box"/>
<text x="85" y="195" class="label">ARITHMETIC LEDGER</text>
<text x="85" y="245" class="mono">E(Q) ~= Z^r_alg + torsion</text>
<line x1="85" y1="270" x2="495" y2="270" class="sep"/>
<text x="85" y="315" class="body">Mordell-Weil: finite generation</text>
<text x="85" y="365" class="body">r_alg = number of free generators</text>
<text x="85" y="415" class="body">canonical heights -> regulator</text>
<text x="85" y="465" class="body">torsion subgroup is finite</text>
<text x="85" y="530" class="small">These are arithmetic constructions on</text>
<text x="85" y="553" class="small">rational points and their group law.</text>

<rect x="675" y="150" width="470" height="470" rx="14" class="soft"/>
<text x="705" y="195" class="label">ANALYTIC LEDGER</text>
<text x="705" y="245" class="mono">L(E,s) = product_p L_p(E,s)</text>
<line x1="705" y1="270" x2="1115" y2="270" class="sep"/>
<text x="705" y="315" class="body">prime point counts -> Euler factors</text>
<text x="705" y="365" class="body">modularity -> continuation + equation</text>
<text x="705" y="415" class="body">r_an = ord_(s=1) L(E,s)</text>
<text x="705" y="465" class="body">first nonzero Taylor term at s=1</text>
<text x="705" y="530" class="small">These are analytic constructions assembled</text>
<text x="705" y="553" class="small">from local data over all primes.</text>

<path d="M540 320 L660 320" class="line"/>
<path d="M540 450 L660 450" class="line"/>
<rect x="535" y="345" width="130" height="82" rx="12" class="open"/>
<text x="600" y="377" text-anchor="middle" class="label">BSD</text>
<text x="600" y="405" text-anchor="middle" class="mono">r_alg ?= r_an</text>

<rect x="55" y="690" width="1090" height="105" rx="12" class="box"/>
<text x="80" y="728" class="h2">Do not collapse the ledgers</text>
<text x="80" y="762" class="body">Agreement is the conjectural bridge. Neither side is defined by the other, and numerical agreement is not a proof.</text>
'''
    return svg_document(
        "Two ledgers in the same hand — Batch-2 review candidate",
        "Two side-by-side ledgers distinguish the Mordell-Weil arithmetic rank from the analytic order of vanishing of the L-function. A dashed BSD box between them marks the equality as conjectural rather than definitional.",
        body,
    )

def bsd_frontier():
    rows = [
        ("Mordell-Weil finite generation", "ESTABLISHED", "all elliptic curves over Q"),
        ("Modularity / analytic continuation", "ESTABLISHED", "all elliptic curves over Q"),
        ("analytic rank 0 or 1 terrain", "ESTABLISHED", "rank equality + finite Sha"),
        ("universal rank equality", "OPEN", "all analytic ranks"),
        ("universal finiteness of Sha", "OPEN", "general case"),
        ("complete complex leading-term formula", "OPEN", "general case + conventions"),
    ]
    y = 230
    out = []
    for claim, status, scope in rows:
        cls = "soft" if status == "ESTABLISHED" else "open"
        out.append(f'<rect x="55" y="{y-34}" width="1090" height="62" rx="8" class="{cls}"/>')
        out.append(f'<text x="80" y="{y}" class="body">{escape(claim)}</text>')
        out.append(f'<text x="665" y="{y}" class="label">{status}</text>')
        out.append(f'<text x="820" y="{y}" class="small">{escape(scope)}</text>')
        y += 78
    body = f'''
<text x="40" y="55" class="h1">BSD theorem frontier: exact scope, not coastline metaphor</text>
<text x="40" y="92" class="body">Each row states whether the mathematical terrain is established or still open, with its quantifier or hypothesis visible.</text>
<text x="80" y="160" class="label">CLAIM</text>
<text x="665" y="160" class="label">STATUS</text>
<text x="820" y="160" class="label">SCOPE / QUALIFIER</text>
{''.join(out)}
<text x="55" y="735" class="small">"Analytic rank 0 or 1" is deliberately bounded; it is not silently extrapolated to higher rank.</text>
<text x="55" y="770" class="small">Database evidence, parity, Selmer bounds, family averages, and p-adic results do not by themselves settle the universal complex statement.</text>
'''
    return svg_document(
        "BSD theorem frontier — Batch-2 review candidate",
        "A six-row status matrix labels Mordell-Weil finite generation, modularity, and analytic-rank-zero-or-one terrain as established, while universal rank equality, universal finiteness of Tate-Shafarevich, and the complete complex leading-term formula are labelled open.",
        body,
    )

def bsd_overture():
    body = r'''
<text x="40" y="55" class="h1">Strong BSD is a ledger of distinct arithmetic factors</text>
<text x="40" y="92" class="body">After fixing standard conventions, the conjectural leading term combines period, regulator, Sha, Tamagawa factors, and torsion.</text>

<rect x="65" y="145" width="1070" height="175" rx="14" class="soft"/>
<text x="90" y="185" class="label">CONJECTURAL LEADING-TERM IDENTITY</text>
<text x="600" y="245" text-anchor="middle" class="mono">L^(r)(E,1) / r! = Omega_E * Reg * #Sha * product_p c_p / (#E(Q)_tors)^2</text>
<text x="600" y="285" text-anchor="middle" class="small">Normalization conventions matter; the compact typography is mnemonic, not a substitute for definitions.</text>

<rect x="65" y="385" width="195" height="155" rx="12" class="box"/>
<text x="162" y="425" text-anchor="middle" class="h2">Omega_E</text>
<text x="162" y="465" text-anchor="middle" class="body">real period</text>
<text x="162" y="505" text-anchor="middle" class="small">geometry / measure</text>

<rect x="285" y="385" width="195" height="155" rx="12" class="box"/>
<text x="382" y="425" text-anchor="middle" class="h2">Reg</text>
<text x="382" y="465" text-anchor="middle" class="body">regulator</text>
<text x="382" y="505" text-anchor="middle" class="small">height determinant</text>

<rect x="505" y="385" width="195" height="155" rx="12" class="box"/>
<text x="602" y="425" text-anchor="middle" class="h2">#Sha</text>
<text x="602" y="465" text-anchor="middle" class="body">Tate-Shafarevich</text>
<text x="602" y="505" text-anchor="middle" class="small">finiteness is open generally</text>

<rect x="725" y="385" width="195" height="155" rx="12" class="box"/>
<text x="822" y="425" text-anchor="middle" class="h2">product c_p</text>
<text x="822" y="465" text-anchor="middle" class="body">Tamagawa factors</text>
<text x="822" y="505" text-anchor="middle" class="small">bad-prime components</text>

<rect x="945" y="385" width="190" height="155" rx="12" class="box"/>
<text x="1040" y="425" text-anchor="middle" class="h2">torsion^2</text>
<text x="1040" y="465" text-anchor="middle" class="body">denominator</text>
<text x="1040" y="505" text-anchor="middle" class="small">finite subgroup</text>

<rect x="65" y="615" width="1070" height="170" rx="12" class="open"/>
<text x="90" y="655" class="h2">Three obligations remain logically distinct</text>
<text x="90" y="700" class="body">1. algebraic rank = analytic order of vanishing</text>
<text x="90" y="735" class="body">2. finiteness of Sha</text>
<text x="650" y="700" class="body">3. normalized leading-term identity</text>
<text x="650" y="735" class="small">Success on one obligation does not silently establish the others.</text>
'''
    return svg_document(
        "The strong BSD ledger — Batch-2 review candidate",
        "The conjectural strong BSD leading-term formula is shown above five labelled factor boxes for the period, regulator, Tate-Shafarevich order, Tamagawa factors, and torsion denominator. A lower box separates rank equality, Sha finiteness, and the leading-term identity as three distinct obligations.",
        body,
    )

def hodge_cycles():
    body = r'''
<text x="40" y="55" class="h1">The cycle-class map: necessary direction versus open converse</text>
<text x="40" y="92" class="body">For smooth projective X over C, algebraic cycles yield Hodge classes; rational surjectivity is the conjectural step.</text>

<rect x="55" y="160" width="300" height="270" rx="14" class="box"/>
<text x="80" y="205" class="h2">Algebraic cycles</text>
<text x="80" y="255" class="mono">Z^p(X)</text>
<text x="80" y="305" class="body">formal sums of codimension-p</text>
<text x="80" y="335" class="body">irreducible subvarieties</text>
<text x="80" y="385" class="small">Different cycles can have the same</text>
<text x="80" y="408" class="small">cohomology class.</text>

<path d="M375 295 L525 295" class="arrow"/>
<text x="405" y="267" class="mono">cl^p</text>

<rect x="545" y="160" width="600" height="270" rx="14" class="soft"/>
<text x="570" y="205" class="h2">Integral cycle classes land in type (p,p)</text>
<text x="570" y="255" class="mono">cl^p : Z^p(X) -> H^(2p)(X,Z)</text>
<text x="570" y="295" class="mono">with complexification in H^(p,p)(X)</text>
<text x="570" y="345" class="body">This direction is established: algebraic => Hodge type.</text>
<text x="570" y="395" class="small">The map is not injective; homologically trivial cycles map to zero.</text>

<rect x="55" y="520" width="1090" height="235" rx="14" class="open"/>
<text x="80" y="565" class="h2">Rational Hodge conjecture — open general converse</text>
<text x="80" y="615" class="mono">Im(cl^p tensor Q) ?= H^(2p)(X,Q) of Hodge type (p,p)</text>
<text x="80" y="665" class="body">Question: does every rational (p,p) class come from a rational linear combination of algebraic cycles?</text>
<text x="80" y="710" class="small">The integral analogue and unrestricted compact Kahler analogue are false in general; projectivity and rational coefficients are structural.</text>
'''
    return svg_document(
        "From algebraic cycles to Hodge classes — Batch-2 review candidate",
        "A left-to-right cycle-class map shows algebraic codimension-p cycles mapping to degree-2p cohomology classes of Hodge type p,p as the established necessary direction. A separate dashed box asks whether the rationalized image equals all rational p,p classes and labels that converse as open in general.",
        body,
    )

def hodge_diamond():
    body = r'''
<text x="40" y="55" class="h1">Hodge decomposition: type, conjugation, and the diagonal</text>
<text x="40" y="92" class="body">The diagram is schematic in bidegree: it does not invent Hodge numbers for a particular variety.</text>

<rect x="55" y="150" width="1090" height="120" rx="12" class="soft"/>
<text x="80" y="195" class="mono">H^k(X,C) = direct sum over p+q=k of H^(p,q)(X)</text>
<text x="80" y="235" class="mono">complex conjugation: H^(p,q) &lt;-&gt; H^(q,p)</text>

<path d="M600 330 L400 470 L600 610 L800 470 Z" class="line"/>
<path d="M600 370 L470 470 L600 570 L730 470 Z" class="line"/>
<line x1="400" y1="470" x2="800" y2="470" class="sep"/>
<line x1="600" y1="330" x2="600" y2="610" class="sep"/>

<rect x="520" y="440" width="160" height="62" rx="10" class="box"/>
<text x="600" y="478" text-anchor="middle" class="mono">H^(p,p)</text>

<rect x="265" y="420" width="150" height="62" rx="10" class="soft"/>
<text x="340" y="458" text-anchor="middle" class="mono">H^(p,q)</text>
<rect x="785" y="420" width="150" height="62" rx="10" class="soft"/>
<text x="860" y="458" text-anchor="middle" class="mono">H^(q,p)</text>
<path d="M425 405 C500 345 700 345 775 405" class="line"/>
<text x="600" y="350" text-anchor="middle" class="small">conjugate pair when p != q</text>

<rect x="55" y="680" width="1090" height="115" rx="12" class="open"/>
<text x="80" y="720" class="h2">Where algebraic-cycle classes can live</text>
<text x="80" y="758" class="body">Algebraic cycle classes have type (p,p). Being a rational (p,p) class is necessary, but the general converse is the Hodge conjecture.</text>
'''
    return svg_document(
        "The Hodge decomposition — Batch-2 review candidate",
        "A schematic bidegree diamond explains the direct-sum Hodge decomposition, complex-conjugation symmetry between p,q and q,p components, and the diagonal p,p component. It explicitly says the picture does not assign Hodge numbers and that p,p type is necessary but not generally known sufficient for rational algebraicity.",
        body,
    )

OUTPUTS = {
    BSD_OUT / "plate_bridge_successor.svg": bsd_bridge(),
    BSD_OUT / "plate_harmony_successor.svg": bsd_harmony(),
    BSD_OUT / "plate_frontier_successor.svg": bsd_frontier(),
    BSD_OUT / "plate_overture_successor.svg": bsd_overture(),
    HODGE_OUT / "cycles_successor.svg": hodge_cycles(),
    HODGE_OUT / "diamond_successor.svg": hodge_diamond(),
}

def main():
    for path, content in OUTPUTS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(path.relative_to(ROOT))

if __name__ == "__main__":
    main()
