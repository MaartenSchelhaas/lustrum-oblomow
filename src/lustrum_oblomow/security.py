"""Security headers applied to every response.

The site is fully static (no user input is ever reflected back), so the
main XSS defense is simply not doing that. This middleware adds the usual
defense-in-depth headers on top of that.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

_CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self'; "
    "img-src 'self' data:; "
    "font-src 'self'; "
    "base-uri 'none'; "
    "form-action 'self'; "
    "frame-ancestors 'none'"
)

# CSS/JS are requested with a content-hash query string (see templating.py),
# so a changed file is always a new URL: safe to cache for as long as
# possible. Fonts never change under an existing filename either. Images can
# still be replaced under the same filename by a future content edit, so
# they get a modest cache instead of a long/immutable one. Everything else
# (the rendered HTML pages) must never be cached, so a deploy is visible
# immediately.
_LONG_CACHE = "public, max-age=31536000, immutable"
_MODERATE_CACHE = "public, max-age=3600"
_NO_CACHE = "no-cache"


def _cache_control_for(path: str) -> str:
    if path.startswith("/assets/css/") or path.startswith("/assets/js/") or path.startswith("/assets/fonts/"):
        return _LONG_CACHE
    if path.startswith("/assets/"):
        return _MODERATE_CACHE
    return _NO_CACHE


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = _CSP
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Cache-Control"] = _cache_control_for(request.url.path)
        return response
