"""MkDocs lifecycle for source-locked Erdős reference pages.

Build-only Markdown is removed after rendering so authoritative registry and
authored editorial articles remain the only durable inputs in Git.
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from erdos_compendium import (  # noqa: E402
    build, clean, GENERATED, load_batch_admissions, EDITORIAL, EXPECTED_COUNT
)


def on_pre_build(config, **kwargs):
    result = build()
    if result["problems"] != 1221 or result["pages"] < 1222:
        raise RuntimeError("Erdős site generation incomplete")
    print("ERDOS_COMPENDIUM_BUILD " + str(result))


def on_post_build(config, **kwargs):
    site = Path(config["site_dir"])
    required = [
        site / "erdos/catalogue/index.html",
        site / "erdos/problems/0001/index.html",
        site / "erdos/problems/0002/index.html",
        site / "erdos/problems/0003/index.html",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    clean()
    if missing:
        raise RuntimeError(f"Erdős rendered-site sentinel pages missing: {missing}")


ERDOS_HOME_MARKER = "<!-- GCL_ERDOS_HOME_STATUS -->"
ERDOS_SHOWCASE_MARKER = "<!-- GCL_ERDOS_SHOWCASE_STATUS -->"


def protected_erdos_counts() -> dict[str, int]:
    """Checked public editorial states, not independently certified theorems."""
    admitted = load_batch_admissions()
    written = {int(path.stem) for path in EDITORIAL.glob("[0-9][0-9][0-9][0-9].md")}
    total = EXPECTED_COUNT
    reviewed = len(admitted)
    drafted = len(written - admitted.keys())
    reference_only = total - len(written)
    if (not (0 <= reviewed <= total)
            or not set(admitted) <= written
            or not all(1 <= n <= total for n in written)
            or reviewed + drafted + reference_only != total):
        raise RuntimeError("Erdős homepage count disagrees with protected catalogue")
    return {"registered": total, "reviewed": reviewed,
            "drafts": drafted, "reference_only": reference_only}


def erdos_showcase_status() -> str:
    """Reader-facing snapshot, sourced from the exact protected build head."""
    counts = protected_erdos_counts()
    return (
        '<div class="showcase-declaration" aria-label="Erdős Compendium progress">\n'
        '<span>The collection today</span>\n'
        f'<p>{counts["reviewed"]:,} reviewed articles among '
        f'{counts["registered"]:,} listed problems</p>\n</div>\n'
        f'<p>Another {counts["drafts"]:,} articles have been written '
        f'but are awaiting review. The remaining '
        f'{counts["reference_only"]:,} problems have catalogue entries '
        'without a full article yet. '
        'These figures are updated whenever the site is rebuilt, using the '
        '<a href="https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/'
        'governance/erdos_compendium/EDITORIAL_ADMISSIONS.json">'
        'record of reviewed articles</a> and the manuscripts themselves. '
        'They measure the progress of the collection, not how many '
        'mathematical questions have been solved.</p>'
    )


def erdos_home_status() -> str:
    """Build the public homepage from current protected admission authority.

    Draft Markdown presence must never count as an editorial admission. A
    separate normalized source digest gate runs in load_batch_admissions().
    """
    counts = protected_erdos_counts()
    total = counts["registered"]
    reviewed = counts["reviewed"]
    drafted = counts["drafts"]
    reference_only = counts["reference_only"]
    cards = (
        (f"{total:,}", "registered problems", "All entries navigable"),
        (f"{reviewed:,}", "reviewed explainers", "Source-bound editorial admission"),
        (f"{drafted:,}", "unadmitted drafts", "Written; no editorial acceptance"),
        (f"{reference_only:,}", "reference-only entries", "Full manuscript not yet present"),
    )
    rendered_cards = "\n".join(
        f'<div class="home-erdos-stat"><strong>{number}</strong>'
        f'<span class="home-erdos-stat__label">{label}</span>'
        f'<span class="home-erdos-stat__description">{description}</span></div>'
        for number, label, description in cards
    )
    return (
        '<div class="home-erdos-status" aria-label="Erdős Compendium publication state">\n'
        '<div class="home-erdos-status__stats">\n' + rendered_cards + '\n</div>\n'
        '<p class="home-erdos-status__provenance">'
        'Counts are recalculated at site build from the protected '
        '<a href="https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/'
        'governance/erdos_compendium/EDITORIAL_ADMISSIONS.json">'
        'editorial admissions ledger</a> and checked manuscripts. '
        'Editorial review confirms a documented explanatory article, '
        '<strong>not an independently certified theorem or proof</strong>.'
        '</p>\n'
        '<p class="home-erdos-status__maintenance">'
        '<strong>Rendering repairs completed:</strong> '
        '<a href="https://github.com/grandchallenge/MATH-PROGRAMME/issues/2690">'
        '25 legacy articles</a> and '
        '<a href="https://github.com/grandchallenge/MATH-PROGRAMME/issues/2698">'
        'four additional articles</a> were corrected through protected '
        'source-hash amendments, then checked in deployed browsers. '
        'The remaining Compendium editorial work is still open.'
        '</p>\n</div>'
    )


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    """Inject source-validated admission counts into public landing surfaces."""
    uri = page.file.src_uri
    if uri == "index.md":
        if markdown.count(ERDOS_HOME_MARKER) != 1:
            raise RuntimeError("Erdős homepage requires exactly one status marker")
        return markdown.replace(ERDOS_HOME_MARKER, erdos_home_status())
    if uri == "SHOWCASE.md":
        if markdown.count(ERDOS_SHOWCASE_MARKER) != 1:
            raise RuntimeError("Erdős Showcase requires exactly one status marker")
        return markdown.replace(ERDOS_SHOWCASE_MARKER, erdos_showcase_status())
    return markdown
