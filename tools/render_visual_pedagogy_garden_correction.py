#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "governance" / "visual_pedagogy" / "review_candidates" / "union_closed" / "plate_garden_successor_r2.svg"

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" role="img" aria-labelledby="title desc">
<title id="title">The Garden That Closes — corrected exact candidate R2</title>
<desc id="desc">A six-set union-closed family is shown as a strict Hasse-style cover diagram, with exact frequencies a equals four, b equals three, c equals two, and half threshold three.</desc>
<style>
text{font-family:"DejaVu Sans","Segoe UI Symbol",Arial,sans-serif;fill:#111}
.h1{font-size:34px;font-weight:700}.h2{font-size:22px;font-weight:700}
.body{font-size:19px}.small{font-size:16px}.math{font-family:"DejaVu Sans","Segoe UI Symbol",sans-serif}
.box{fill:white;stroke:#222;stroke-width:2}.soft{fill:#f4f4f4;stroke:#444;stroke-width:2}
.line{stroke:#222;stroke-width:2;fill:none}
</style>
<rect width="1200" height="900" fill="white"/>
<text x="40" y="55" class="h1">An exact union-closed family</text>
<text x="40" y="92" class="body math">F = {∅, {a}, {b}, {a,b}, {a,c}, {a,b,c}}</text>
<text x="40" y="126" class="small">Edges show cover relations only (strict Hasse-style inclusion diagram).</text>
<text x="950" y="126" class="small">visual_is_evidence: false</text>

<!-- strict cover relations only -->
<path d="M565 680 L385 618" class="line"/>
<path d="M565 680 L665 618" class="line"/>
<path d="M385 560 L515 448" class="line"/>
<path d="M665 560 L515 448" class="line"/>
<path d="M665 560 L825 448" class="line"/>
<path d="M515 390 L665 268" class="line"/>
<path d="M825 390 L665 268" class="line"/>

<rect x="500" y="680" width="130" height="58" rx="8" class="box"/>
<g aria-label="empty set">
  <circle cx="565" cy="709" r="12" fill="none" stroke="#111" stroke-width="2"/>
  <line x1="553" y1="721" x2="577" y2="697" stroke="#111" stroke-width="2"/>
</g>
<rect x="320" y="560" width="130" height="58" rx="8" class="box"/><text x="385" y="596" text-anchor="middle" class="body">{b}</text>
<rect x="600" y="560" width="130" height="58" rx="8" class="box"/><text x="665" y="596" text-anchor="middle" class="body">{a}</text>
<rect x="450" y="390" width="130" height="58" rx="8" class="box"/><text x="515" y="426" text-anchor="middle" class="body">{a,b}</text>
<rect x="760" y="390" width="130" height="58" rx="8" class="box"/><text x="825" y="426" text-anchor="middle" class="body">{a,c}</text>
<rect x="600" y="210" width="130" height="58" rx="8" class="box"/><text x="665" y="246" text-anchor="middle" class="body">{a,b,c}</text>

<rect x="950" y="150" width="210" height="300" rx="12" class="soft"/>
<text x="970" y="190" class="h2">Frequency ledger</text>
<text x="970" y="235" class="body">freq(a) = 4</text>
<text x="970" y="275" class="body">freq(b) = 3</text>
<text x="970" y="315" class="body">freq(c) = 2</text>
<text x="970" y="370" class="body">|F| / 2 = 3</text>
<text x="970" y="410" class="small">a exceeds and b meets</text>
<text x="970" y="435" class="small">the half threshold.</text>

<text x="55" y="775" class="h2">Selected unions</text>
<text x="55" y="810" class="body">{a} union {b} = {a,b};  {b} union {a,c} = {a,b,c}.</text>
<text x="55" y="842" class="small">These examples illustrate closure; the full six-set family is checked separately as union-closed.</text>
<text x="55" y="874" class="small">Frankl: every finite union-closed family with at least one nonempty member is conjectured to contain an element in at least half its sets.</text>
</svg>
'''

def main():
    OUT.write_text(SVG, encoding="utf-8", newline="\n")
    print(OUT.relative_to(ROOT))

if __name__ == "__main__":
    main()
