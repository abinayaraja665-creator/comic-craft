from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.schemas import ComicRequest, ComicResponse
from app.services.image_generator import generate_image
from app.services.workflow import generate_comic

router = APIRouter()
settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@router.post("/generate")
def generate_from_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        payload = ComicRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        layout, pdf_url = generate_comic(payload)
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "app_name": settings.app_name,
                "layout": layout,
                "pdf_url": pdf_url,
                "title": f"{payload.character_name}'s Comic",
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "app_name": settings.app_name,
                "error": str(exc),
            },
            status_code=500,
        )


@router.post("/api/generate-comic", response_model=ComicResponse)
def generate_from_json(payload: ComicRequest):
    try:
        layout, pdf_url = generate_comic(payload)
        return ComicResponse(
            title=f"{payload.character_name}'s Comic",
            panels=layout,
            pdf_url=pdf_url,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/test-image")
def test_image(prompt: str = Form(...)):
    if settings.ai_mock_mode:
        from app.services.mock_ai import generate_image as mock_generate_image
        return JSONResponse({"image_url": mock_generate_image(prompt, 0)})

    try:
        return JSONResponse({"image_url": generate_image(prompt, 0)})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/export-success")
def export_success(request: Request, pdf_url: str):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"app_name": settings.app_name, "pdf_url": pdf_url},
    )


@router.get("/download/{filename}")
def download_pdf(filename: str):
    safe_name = settings.exports_dir / filename
    if safe_name.parent != settings.exports_dir or not safe_name.is_file():
        raise HTTPException(status_code=404, detail="PDF not found.")
    return FileResponse(
        path=safe_name,
        media_type="application/pdf",
        filename=safe_name.name,
    )


@router.get("/api/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
        "mock_mode": settings.ai_mock_mode,
        "gemini_configured": bool(settings.gemini_api_key),
        "huggingface_configured": bool(settings.hf_token),
    }
