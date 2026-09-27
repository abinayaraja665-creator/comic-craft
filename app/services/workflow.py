from app.config import get_settings
from app.schemas import ComicRequest
from app.services.exporters import save_pdf
from app.services.layout_builder import build_comic_layout
from app.services import gemini_flash, gemini_pro, image_generator, mock_ai


def generate_comic(request: ComicRequest):
    settings = get_settings()

    if settings.ai_mock_mode:
        outline = mock_ai.generate_outline(request)
        story = mock_ai.generate_story(request, outline)
        image_fn = mock_ai.generate_image
    else:
        outline = gemini_flash.generate_outline(request)
        story = gemini_pro.generate_story(request, outline)
        image_fn = image_generator.generate_image

    image_urls = [
        image_fn(panel.image_prompt, panel.panel_number)
        for panel in story.panels
    ]

    layout = build_comic_layout(story, image_urls)
    pdf_url = save_pdf(
        title=f"{request.character_name}'s Comic",
        panels=layout,
    )
    return layout, pdf_url
