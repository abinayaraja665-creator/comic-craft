from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routes import router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI comic story creator using Gemini and Hugging Face image generation.",
)

app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(router)


@app.get("/api")
def api_root():
    return {"message": "ComicCraft API is running.", "docs": "/docs"}
