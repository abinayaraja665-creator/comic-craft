from google import genai
from google.genai import types

from app.config import get_settings
from app.schemas import ComicOutline, ComicRequest, ComicStory


def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_story(request: ComicRequest, outline: ComicOutline) -> ComicStory:
    settings = get_settings()
    outline_json = outline.model_dump_json(indent=2)

    prompt = f"""
Expand this comic outline into a polished, family-friendly comic script.

Character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Outline:
{outline_json}

Requirements:
- Return exactly {settings.comic_panels} panels in the same order.
- Preserve the outline's events and visual continuity.
- Each panel needs a short caption, narration, optional dialogue lines, and an image prompt.
- Keep dialogue concise enough for comic panels.
- Do not include unsafe, graphic, sexual, or hateful content.
- Image prompts must describe the same recurring character consistently.
"""

    response = _client().models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicStory,
            temperature=0.85,
        ),
    )

    if getattr(response, "parsed", None):
        story = response.parsed
    else:
        story = ComicStory.model_validate_json(response.text)

    if len(story.panels) != settings.comic_panels:
        raise RuntimeError(
            f"Gemini returned {len(story.panels)} story panels; expected {settings.comic_panels}."
        )
    return story
