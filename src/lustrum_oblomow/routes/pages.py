"""Routes that serve the static HTML pages of the site."""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

router = APIRouter(include_in_schema=False)


@router.get("/")
async def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@router.get("/activiteiten")
async def activiteiten() -> FileResponse:
    return FileResponse(STATIC_DIR / "activiteiten.html")


@router.get("/lustrumreis")
async def lustrumreis() -> FileResponse:
    return FileResponse(STATIC_DIR / "lustrumreis.html")


@router.get("/gadgets")
async def gadgets() -> FileResponse:
    return FileResponse(STATIC_DIR / "gadgets.html")


@router.get("/contact")
async def contact() -> FileResponse:
    return FileResponse(STATIC_DIR / "contact.html")


@router.get("/faq")
async def faq() -> FileResponse:
    return FileResponse(STATIC_DIR / "faq.html")
