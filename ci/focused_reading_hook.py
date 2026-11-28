"""Apply native Material reading metadata without changing evidence bytes."""


def on_page_context(context, page, config, nav, **kwargs):
    """Hide only primary navigation on explicitly selected source pages."""
    if page.file.src_uri not in config["extra"].get("focused_reading_pages", []):
        return context
    hidden = list(page.meta.get("hide") or [])
    if "navigation" not in hidden:
        hidden.append("navigation")
    page.meta["hide"] = hidden
    return context
