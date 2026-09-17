"""Routes that render the site's Jinja2 page templates."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from lustrum_oblomow.templating import templates

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {"active_page": "home"})


@router.get("/activiteiten", response_class=HTMLResponse)
async def activiteiten(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "activiteiten.html", {"active_page": "activiteiten"})


@router.get("/lustrumreis", response_class=HTMLResponse)
async def lustrumreis(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "lustrumreis.html", {"active_page": "lustrumreis"})


@router.get("/spaarplannen", response_class=HTMLResponse)
async def spaarplannen(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "spaarplannen.html", {"active_page": "spaarplannen"})


@router.get("/gadgets", response_class=HTMLResponse)
async def gadgets(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "gadgets/index.html", {"active_page": "gadgets"})


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "contact.html", {"active_page": "contact"})


@router.get("/faq", response_class=HTMLResponse)
async def faq(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "faq.html", {"active_page": "faq"})
