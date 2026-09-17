from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from lustrum_oblomow.routes.pages import router as pages_router
from lustrum_oblomow.security import SecurityHeadersMiddleware

ASSETS_DIR = Path(__file__).parent / "static" / "assets"

app = FastAPI()
app.add_middleware(SecurityHeadersMiddleware)
app.include_router(pages_router)
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
