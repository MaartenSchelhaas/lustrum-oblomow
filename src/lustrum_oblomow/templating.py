"""Shared Jinja2 template environment for the page routes."""

import hashlib
from pathlib import Path

from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
ASSETS_DIR = Path(__file__).resolve().parent / "static" / "assets"

# Cache-busting: base.html appends ?v=<hash> to these, so a changed file gets
# a URL no browser or CDN has ever cached before. See security.py for the
# matching long-lived Cache-Control on /assets/css/ and /assets/js/.
_VERSIONED_ASSETS = ("css/style.css", "js/main.js")
_ASSET_VERSIONS = {
    path: hashlib.sha256((ASSETS_DIR / path).read_bytes()).hexdigest()[:10]
    for path in _VERSIONED_ASSETS
}


def asset_version(relative_path: str) -> str:
    return _ASSET_VERSIONS[relative_path]


templates = Jinja2Templates(directory=TEMPLATES_DIR)
templates.env.globals["asset_version"] = asset_version
