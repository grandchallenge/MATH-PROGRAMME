# SERIES STYLE CONTRACT

## Physical and typographic identity

- Trim: 7 × 10 inches.
- Main text: Libertinus Serif.
- Sans: Libertinus Sans.
- Mathematics: Libertinus Math.
- Monospace: DejaVu Sans Mono or metrically compatible fallback.
- Restrained warm-paper / dark-ink / muted semantic accents.
- GCL color names remain stable: `GCLInk`, `GCLWarm`, `GCLPale`, `GCLBlue`, `GCLGreen`.
- Color is reinforcement, never the only carrier of meaning.
- Running heads identify chapter/section rather than merely the series title.
- Strong widow/orphan control and microtypography are required for RC builds.

## Voice

Technical, rigorous, economical. Prefer exact ordinary language before specialized terminology. Avoid ceremonial claims. A sentence such as “this is the same structure” must mean an explicit correspondence; otherwise write “this is a useful reading/analogy.”

The governing pedagogical maxim is:

> Formal notation should arrive after the problem it solves is visible.

## Chapter rhythm

Default chapter architecture:

1. motivating problem or communicative/computational tension;
2. conceptual picture;
3. informal explanation;
4. formal interlude;
5. worked example;
6. executable laboratory;
7. “Do not confuse” failure boundary;
8. exercises in all six modes;
9. short bridge to the next chapter.

Do not force section headings merely to satisfy the template; preserve the rhythm even when sections merge.

## Boxes

Series-stable semantic boxes:

- `Intuition`
- `Formal Interlude`
- `Checkpoint`
- `Do not confuse`
- `Computational Laboratory`
- `Governing Principle`
- `Worked Example`
- `Proof Workshop`
- `Design Clinic`

A future volume may add a box only if the distinction recurs often enough to justify a new visual grammar.

## Plate grammar

Every plate uses the shared `gclplate` TikZ style. Labels use opaque or near-opaque local backgrounds (`gcllabel`) as a safety layer, but routing remains the primary solution to collisions.

Connector priorities:

1. direct noncrossing line;
2. curved route with explicit out/in angles;
3. orthogonal route / waypoint;
4. local pointer or stub;
5. move the label;
6. only then change scale.

Never shrink text solely to accommodate an arrow.

Plate caption format:

`Plate N. <descriptive title>. <pedagogical claim>. <limit of analogy / scope statement where needed>.`

## Series front matter

Every volume includes:

- collection / series title;
- volume title/subtitle;
- scope/publication page;
- preface explaining why this volume is necessary;
- series orientation locating the current volume;
- explicit statement that “grand unified theory” is a research thesis.

## Back matter

Every volume includes:

- formal reference / notation guide;
- glossary where needed;
- bibliography;
- generated index;
- illustration register or production appendix;
- course/self-study roadmap where pedagogically useful;
- transition to next volume.