from pydantic import BaseModel, Field, field_validator


class ComicRequest(BaseModel):
    story_prompt: str = Field(min_length=5, max_length=2000)
    character_name: str = Field(default="Alex", min_length=1, max_length=80)
    setting: str = Field(default="enchanted forest", min_length=1, max_length=120)
    tone: str = Field(default="light-hearted", min_length=1, max_length=80)
    art_style: str = Field(default="comic book", min_length=1, max_length=80)

    @field_validator("story_prompt", "character_name", "setting", "tone", "art_style")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class PanelOutline(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str


class ComicOutline(BaseModel):
    panels: list[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: list[str] = Field(default_factory=list)
    image_prompt: str


class ComicStory(BaseModel):
    panels: list[PanelStory]


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    image_url: str
    scene_description: str
    caption: str
    narration: str
    dialogue: list[str] = Field(default_factory=list)
    image_prompt: str


class ComicResponse(BaseModel):
    title: str
    panels: list[ComicPanel]
    pdf_url: str
