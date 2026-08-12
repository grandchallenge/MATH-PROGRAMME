#!/usr/bin/env python3
# Deterministically render Batch-1 Union-Closed visual-pedagogy SVG candidates.
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "governance" / "visual_pedagogy" / "review_candidates" / "union_closed"

FAMILY = (
    frozenset(),
    frozenset({"a"}),
    frozenset({"b"}),
    frozenset({"a", "b"}),
    frozenset({"a", "c"}),
    frozenset({"a", "b", "c"}),
)
ELEMENTS = ("a", "b", "c")

def fmt_set(s):
    return "∅" if not s else "{" + ",".join(sorted(s)) + "}"

def frequencies():
    return {x: sum(x in s for s in FAMILY) for x in ELEMENTS}

def svg_document(title, desc, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(desc)}</desc>
<style>
text{{font-family:Arial,Helvetica,sans-serif;fill:#111}}
.h1{{font-size:34px;font-weight:700}} .h2{{font-size:22px;font-weight:700}}
.body{{font-size:19px}} .small{{font-size:16px}} .mono{{font-family:monospace;font-size:18px}}
.box{{fill:white;stroke:#222;stroke-width:2}} .soft{{fill:#f4f4f4;stroke:#444;stroke-width:2}}
.line{{stroke:#222;stroke-width:2;fill:none}} .dash{{stroke:#444;stroke-width:2;stroke-dasharray:8 7;fill:none}}
</style>
<rect width="1200" height="900" fill="white"/>
{body}
<text x="40" y="872" class="small">Review candidate · documentary exposition only · visual_is_evidence: false</text>
</svg>
'''

def garden():
    freq = frequencies()
    nodes = {
        frozenset(): (110, 680),
        frozenset({"a"}): (310, 560),
        frozenset({"b"}): (610, 560),
        frozenset({"a","b"}): (440, 390),
        frozenset({"a","c"}): (790, 390),
        frozenset({"a","b","c"}): (610, 210),
    }
    edges = [
        (frozenset(), frozenset({"a"})), (frozenset(), frozenset({"b"})),
        (frozenset({"a"}), frozenset({"a","b"})),
        (frozenset({"b"}), frozenset({"a","b"})),
        (frozenset({"a"}), frozenset({"a","c"})),
        (frozenset({"a","b"}), frozenset({"a","b","c"})),
        (frozenset({"a","c"}), frozenset({"a","b","c"})),
        (frozenset({"b"}), frozenset({"a","b","c"})),
    ]
    edge_svg = "\n".join(
        f'<path d="M{x1+65} {y1} L{x2+65} {y2+38}" class="line"/>'
        for s1,s2 in edges for (x1,y1),(x2,y2) in [(nodes[s1],nodes[s2])]
    )
    node_svg = "\n".join(
        f'<rect x="{x}" y="{y}" width="130" height="58" rx="8" class="box"/>'
        f'<text x="{x+65}" y="{y+36}" text-anchor="middle" class="body">{escape(fmt_set(s))}</text>'
        for s,(x,y) in nodes.items()
    )
    body=f'''
<text x="40" y="55" class="h1">An exact union-closed family</text>
<text x="40" y="92" class="body">F = {{∅, {{a}}, {{b}}, {{a,b}}, {{a,c}}, {{a,b,c}}}}</text>
{edge_svg}
{node_svg}
<rect x="950" y="150" width="210" height="300" rx="12" class="soft"/>
<text x="970" y="190" class="h2">Frequency ledger</text>
<text x="970" y="235" class="body">freq(a) = {freq["a"]}</text>
<text x="970" y="275" class="body">freq(b) = {freq["b"]}</text>
<text x="970" y="315" class="body">freq(c) = {freq["c"]}</text>
<text x="970" y="370" class="body">|F| / 2 = 3</text>
<text x="970" y="410" class="small">a and b meet</text><text x="970" y="435" class="small">the half threshold.</text>
<text x="55" y="785" class="body">{{a}} ∪ {{b}} = {{a,b}};  {{b}} ∪ {{a,c}} = {{a,b,c}}.</text>
<text x="55" y="820" class="small">This exact example illustrates closure; Frankl asks for an abundant element in every finite nonempty union-closed family.</text>
'''
    return svg_document("The Garden That Closes — exact review candidate",
        "A six-set union-closed family is arranged by inclusion, with exact frequencies a equals four, b equals three, c equals two, and the half threshold equal to three.", body)

def frequency():
    rows=[]
    y0=240
    for i,s in enumerate(FAMILY):
        y=y0+i*68
        cells="".join(
            f'<text x="{710+j*95}" y="{y}" text-anchor="middle" class="body">{"●" if x in s else "○"}</text>'
            for j,x in enumerate(ELEMENTS)
        )
        rows.append(f'<text x="535" y="{y}" class="mono">{escape(fmt_set(s))}</text>{cells}<text x="1035" y="{y}" text-anchor="middle" class="body">{len(s)}</text>')
    body=f'''
<text x="40" y="55" class="h1">The half-way balance as exact incidence counting</text>
<text x="40" y="92" class="body">F = {{∅, {{a}}, {{b}}, {{a,b}}, {{a,c}}, {{a,b,c}}}}, so |F| = 6 and |F|/2 = 3.</text>
<text x="55" y="155" class="h2">Frequency bars</text>
<text x="55" y="210" class="body">a</text><rect x="90" y="182" width="232" height="38" class="soft"/><text x="335" y="210" class="body">4 / 6</text>
<text x="55" y="285" class="body">b</text><rect x="90" y="257" width="174" height="38" class="soft"/><text x="277" y="285" class="body">3 / 6</text>
<text x="55" y="360" class="body">c</text><rect x="90" y="332" width="116" height="38" class="soft"/><text x="219" y="360" class="body">2 / 6</text>
<line x1="264" y1="165" x2="264" y2="390" class="dash"/>
<text x="275" y="405" class="small">threshold = 3 occurrences</text>
<text x="55" y="465" class="small">Bar length encodes count; labels retain the meaning without color.</text>
<text x="525" y="155" class="h2">Incidence matrix</text>
<text x="710" y="195" text-anchor="middle" class="h2">a</text><text x="805" y="195" text-anchor="middle" class="h2">b</text><text x="900" y="195" text-anchor="middle" class="h2">c</text><text x="1035" y="195" text-anchor="middle" class="h2">|A|</text>
{''.join(rows)}
<text x="525" y="690" class="body">Column sums: 4 + 3 + 2 = 9</text>
<text x="525" y="730" class="body">Row-size sum: 0 + 1 + 1 + 2 + 2 + 3 = 9</text>
<text x="525" y="775" class="h2">Σₓ freq_F(x) = Σ_A |A|</text>
<text x="55" y="805" class="small">The identity controls an average; by itself it does not prove the universal half-frequency conjecture.</text>
'''
    return svg_document("The Half-Way Balance — exact review candidate",
        "Frequency bars and an incidence matrix show a appears in four of six sets, b in three, c in two; the half threshold is three and both sides of the incidence double-count equal nine.", body)

def lattice():
    pos={"∅":(560,720), "{a}":(300,570), "{b}":(760,570), "{a,b}":(470,405), "{a,c}":(900,405), "{a,b,c}":(650,210)}
    edges=[("∅","{a}"),("∅","{b}"),("{a}","{a,b}"),("{b}","{a,b}"),("{a}","{a,c}"),("{a,b}","{a,b,c}"),("{a,c}","{a,b,c}"),("{b}","{a,b,c}")]
    edge_svg="".join(f'<path d="M{x1+60} {y1} L{x2+60} {y2+45}" class="line"/>' for u,v in edges for (x1,y1),(x2,y2) in [(pos[u],pos[v])])
    irr={"{a}","{b}","{a,c}"}
    node_svg="".join(f'<rect x="{x}" y="{y}" width="120" height="58" rx="8" class="{"soft" if name in irr else "box"}"/><text x="{x+60}" y="{y+36}" text-anchor="middle" class="body">{escape(name)}</text>' for name,(x,y) in pos.items())
    body=f'''
<text x="40" y="55" class="h1">A finite join-semilattice with join = union</text>
<text x="40" y="92" class="body">The same F ordered by inclusion. Every displayed join is an actual union in F.</text>
{edge_svg}{node_svg}
<rect x="40" y="180" width="300" height="260" rx="12" class="soft"/>
<text x="65" y="220" class="h2">Join-irreducibles</text>
<text x="65" y="265" class="body">{{a}}</text><text x="65" y="305" class="body">{{b}}</text><text x="65" y="345" class="body">{{a,c}}</text>
<text x="65" y="400" class="small">Shaded nodes are the non-bottom</text><text x="65" y="425" class="small">join-irreducibles in this example.</text>
<rect x="900" y="650" width="260" height="145" rx="12" class="box"/>
<text x="920" y="682" class="h2">Exact joins</text>
<text x="920" y="722" class="body">{{a}} ∨ {{b}} = {{a,b}}</text>
<text x="920" y="760" class="body">{{b}} ∨ {{a,c}} = {{a,b,c}}</text>
<text x="40" y="815" class="small">This illustrates A ∨ B = A ∪ B; it does not replace the translation theorems connecting lattice and set-family formulations.</text>
'''
    return svg_document("Union-closed family as a join-semilattice — exact review candidate",
        "The six sets are ordered by inclusion with join equal to union. The nodes {a}, {b}, and {a,c} are marked as join-irreducible in this finite example, and two exact joins are written explicitly.", body)

def entropy():
    body=r'''
<text x="40" y="55" class="h1">From a uniform random set to coordinate marginals</text>
<text x="40" y="92" class="body">Let A be uniform on the same six-set family F. Then H(A) = log₂ 6 exactly.</text>
<rect x="55" y="155" width="300" height="250" rx="12" class="box"/>
<text x="80" y="195" class="h2">Membership marginals</text>
<text x="80" y="245" class="body">p(a) = P(a ∈ A) = 4/6 = 2/3</text>
<text x="80" y="290" class="body">p(b) = P(b ∈ A) = 3/6 = 1/2</text>
<text x="80" y="335" class="body">p(c) = P(c ∈ A) = 2/6 = 1/3</text>
<text x="80" y="380" class="small">These are exact for this finite example.</text>
<path d="M370 280 L515 280" class="line"/><text x="392" y="260" class="small">independent A,B</text>
<rect x="530" y="155" width="300" height="250" rx="12" class="soft"/>
<text x="555" y="195" class="h2">Union marginals</text>
<text x="555" y="235" class="small">qᵢ = P(i ∈ A ∪ B)</text>
<text x="555" y="275" class="body">q(a) = 1 − (1/3)² = 8/9</text>
<text x="555" y="320" class="body">q(b) = 1 − (1/2)² = 3/4</text>
<text x="555" y="365" class="body">q(c) = 1 − (2/3)² = 5/9</text>
<path d="M845 280 L1010 280" class="line"/>
<rect x="1025" y="175" width="130" height="210" rx="12" class="box"/>
<text x="1040" y="215" class="h2">Closure</text><text x="1040" y="260" class="small">A ∪ B</text><text x="1040" y="295" class="small">still lies</text><text x="1040" y="330" class="small">in F.</text>
<rect x="55" y="500" width="1100" height="225" rx="12" class="box"/>
<text x="80" y="545" class="h2">Imported entropy/coupling terrain: exact scope matters</text>
<text x="80" y="590" class="body">• Entropy and coupled copies turn closure into inequalities involving coordinate marginals.</text>
<text x="80" y="630" class="body">• Rigorous dimension-free positive lower bounds are known; exact constants and hypotheses are source-specific.</text>
<text x="80" y="670" class="body">• A positive bound below one half, or a bound for one coupling ansatz, is not Frankl’s universal 1/2 theorem.</text>
<text x="80" y="710" class="small">The independent-copy calculation above is an exact illustration, not a claim that every source theorem uses independent copies.</text>
<line x1="80" y1="780" x2="1120" y2="780" class="dash"/>
<text x="80" y="812" class="body">Open target: some element has frequency ≥ 1/2 in every finite nonempty union-closed family.</text>
'''
    return svg_document("The Entropy Bridge — exact illustrative review candidate",
        "A uniform random member of the six-set family has marginals two thirds, one half, and one third. Independent copies produce union marginals eight ninths, three quarters, and five ninths. A guardrail separates this illustration from source-specific entropy theorems and the open one-half conjecture.", body)

def frontier():
    body=r'''
<text x="40" y="55" class="h1">The theorem frontier: status before atmosphere</text>
<text x="40" y="92" class="body">Established progress approaches the open one-half boundary without becoming the universal theorem.</text>
<line x1="170" y1="700" x2="1080" y2="700" class="line"/><line x1="170" y1="165" x2="170" y2="700" class="line"/>
<line x1="170" y1="250" x2="1080" y2="250" class="dash"/>
<text x="185" y="235" class="h2">OPEN UNIVERSAL BOUNDARY: 1/2</text>
<rect x="215" y="505" width="185" height="115" rx="10" class="box"/><text x="235" y="540" class="h2">Elementary</text><text x="235" y="575" class="small">powersets, singleton</text><text x="235" y="600" class="small">injection, top union</text>
<rect x="430" y="455" width="185" height="165" rx="10" class="box"/><text x="450" y="490" class="h2">Exact bounded</text><text x="450" y="525" class="small">n ≤ 4 replay</text><text x="450" y="555" class="small">finite verification</text><text x="450" y="590" class="small">not unbounded proof</text>
<rect x="645" y="405" width="185" height="215" rx="10" class="soft"/><text x="665" y="440" class="h2">Imported</text><text x="665" y="475" class="small">average-size and</text><text x="665" y="505" class="small">dimension-free</text><text x="665" y="535" class="small">positive bounds</text><text x="665" y="575" class="small">constants/hypotheses</text><text x="665" y="600" class="small">source-specific</text>
<rect x="860" y="355" width="185" height="265" rx="10" class="box"/><text x="880" y="390" class="h2">Formal / structural</text><text x="880" y="425" class="small">lattice results,</text><text x="880" y="455" class="small">minimal-</text><text x="880" y="480" class="small">counterexample</text><text x="880" y="505" class="small">restrictions, hybrid</text><text x="880" y="530" class="small">certificate packages</text><text x="880" y="570" class="small">individual records</text><text x="880" y="595" class="small">govern exact scope</text>
<text x="185" y="755" class="body">No admitted result crosses the dashed line to prove the universal half-frequency statement.</text>
<text x="185" y="800" class="small">Public proof claims remain “needs audit” until theorem statements, dependencies, and complete proofs are independently admitted.</text>
'''
    return svg_document("Islands of theorem — explicit status-map review candidate",
        "A status map separates elementary results, bounded exact verification, imported positive bounds, and formal structural results beneath a dashed open universal one-half boundary.", body)

RENDERERS = {
    "plate_garden_successor.svg": garden,
    "plate_frequency_successor.svg": frequency,
    "plate_lattice_successor.svg": lattice,
    "plate_entropy_successor.svg": entropy,
    "plate_frontier_successor.svg": frontier,
}

def render_all():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in RENDERERS.items():
        (OUT / name).write_text(fn(), encoding="utf-8", newline="\n")

if __name__ == "__main__":
    render_all()
