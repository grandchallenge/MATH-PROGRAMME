"""Hardened urllib helpers for authenticated GitHub API downloads."""
from __future__ import annotations

import urllib.parse
import urllib.request


class CrossOriginAuthStrippingRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Keep API auth on same-origin redirects and drop it for signed downloads."""

    def redirect_request(
        self,
        request: urllib.request.Request,
        file_pointer: object,
        code: int,
        message: str,
        headers: object,
        new_url: str,
    ) -> urllib.request.Request | None:
        redirected = super().redirect_request(
            request, file_pointer, code, message, headers, new_url
        )
        if redirected is None:
            return None
        source = urllib.parse.urlsplit(request.full_url)
        destination = urllib.parse.urlsplit(new_url)
        if (source.scheme.lower(), source.netloc.lower()) != (
            destination.scheme.lower(),
            destination.netloc.lower(),
        ):
            redirected.remove_header("Authorization")
        return redirected


def build_github_opener() -> urllib.request.OpenerDirector:
    """Return an opener safe for GitHub API endpoints that redirect to signed URLs."""

    return urllib.request.build_opener(CrossOriginAuthStrippingRedirectHandler())
