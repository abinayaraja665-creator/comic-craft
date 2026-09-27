from google import genai
from google.genai import types

from app.config import get_settings
from app.schemas import ComicOutline, ComicRequest


def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_outline(request: ComicRequest) -> ComicOutline:
    settings = get_settings()
    prompt = f"""
Create a coherent {settings.comic_panels}-panel comic outline.

User story idea: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Requirements:
- Exactly {settings.comic_panels} panels.
- Keep the same main character and visual identity across panels.
- Give each panel a concise title and scene description.
- Make each image prompt visually specific and suitable for text-to-image generation.
- Avoid text, speech bubbles, logos, watermarks, or readable writing inside generated images.
- The story must have a clear beginning, development, and ending.
"""

    response = _client().models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicOutline,
            temperature=0.8,
        ),
    )

    if getattr(response, "parsed", None):
        outline = response.parsed
    else:
        outline = ComicOutline.model_validate_json(response.text)

    if len(outline.panels) != settings.comic_panels:
        raise RuntimeError(
            f"Gemini returned {len(outline.panels)} panels; expected {settings.comic_panels}."
        )
    return outline
