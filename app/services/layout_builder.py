from app.schemas import ComicPanel, ComicStory


def build_comic_layout(story: ComicStory, image_urls: list[str]) -> list[ComicPanel]:
    if len(story.panels) != len(image_urls):
        raise ValueError("Every story panel must have exactly one generated image.")

    return [
        ComicPanel(
            panel_number=panel.panel_number,
            title=panel.title,
            image_url=image_url,
            scene_description=panel.scene_description,
            caption=panel.caption,
            narration=panel.narration,
            dialogue=panel.dialogue,
            image_prompt=panel.image_prompt,
        )
        for panel, image_url in zip(story.panels, image_urls)
    ]
