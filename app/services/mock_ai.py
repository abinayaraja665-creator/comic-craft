from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from app.config import get_settings
from app.schemas import (
    ComicOutline,
    ComicRequest,
    ComicStory,
    PanelOutline,
    PanelStory,
)


def generate_outline(request: ComicRequest) -> ComicOutline:
    settings = get_settings()
    panels = []
    for i in range(1, settings.comic_panels + 1):
        panels.append(
            PanelOutline(
                panel_number=i,
                title=f"Panel {i}: {['The Beginning', 'A New Clue', 'The Challenge', 'The Turning Point', 'The Ending'][i-1]}",
                scene_description=(
                    f"{request.character_name} explores {request.setting}. "
                    f"The scene advances the {request.tone} story."
                ),
                image_prompt=(
                    f"{request.character_name} in {request.setting}, "
                    f"{request.art_style}, panel {i}, cinematic comic composition"
                ),
            )
        )
    return ComicOutline(panels=panels)


def generate_story(request: ComicRequest, outline: ComicOutline) -> ComicStory:
    panels = []
    for item in outline.panels:
        panels.append(
            PanelStory(
                panel_number=item.panel_number,
                title=item.title,
                scene_description=item.scene_description,
                caption=f"Scene {item.panel_number} — the adventure continues.",
                narration=(
                    f"{request.character_name} moves through the scene, "
                    f"discovering what the next moment of the story brings."
                ),
                dialogue=[f"{request.character_name}: Let's see what happens next!"],
                image_prompt=item.image_prompt,
            )
        )
    return ComicStory(panels=panels)


def generate_image(image_prompt: str, panel_number: int) -> str:
    settings = get_settings()
    width, height = 1200, 800
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((30, 30, width - 30, height - 30), outline="black", width=8)
    draw.text((70, 70), f"ComicCraft — Panel {panel_number}", fill="black")
    draw.text(
        (70, 150),
        "Mock image mode",
        fill="black",
    )
    draw.text(
        (70, 220),
        image_prompt[:120],
        fill="black",
    )
    filename = f"mock-panel-{panel_number}.png"
    output_path = settings.panels_dir / filename
    image.save(output_path)
    return f"/static/panels/{filename}"
