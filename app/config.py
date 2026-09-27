from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000

    gemini_api_key: str | None = None
    gemini_outline_model: str = "gemini-2.5-flash"
    gemini_story_model: str = "gemini-2.5-pro"

    hf_token: str | None = None
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    hf_provider: str = "auto"

    ai_mock_mode: bool = False
    comic_panels: int = 5

    static_dir: Path = BASE_DIR / "static"
    templates_dir: Path = BASE_DIR / "templates"
    panels_dir: Path = BASE_DIR / "static" / "panels"
    exports_dir: Path = BASE_DIR / "static" / "exports"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.panels_dir.mkdir(parents=True, exist_ok=True)
    settings.exports_dir.mkdir(parents=True, exist_ok=True)
    return settings
