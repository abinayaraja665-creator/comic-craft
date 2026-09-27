from io import BytesIO
from pathlib import Path
import re
import uuid

from PIL import Image
from huggingface_hub import InferenceClient

from app.config import get_settings


def _safe_filename(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-")
    return value[:60] or "panel"


def _client() -> InferenceClient:
    settings = get_settings()
    if not settings.hf_token:
        raise RuntimeError("HF_TOKEN is not configured.")
    return InferenceClient(
        provider=settings.hf_provider,
        api_key=settings.hf_token,
    )


def generate_image(image_prompt: str, panel_number: int) -> str:
    settings = get_settings()
    enhanced_prompt = (
        f"{image_prompt}. "
        "Clean family-friendly comic illustration, strong composition, "
        "consistent character appearance, expressive faces, cinematic lighting, "
        "no words, no captions, no speech bubbles, no watermark."
    )

    image = _client().text_to_image(
        enhanced_prompt,
        model=settings.hf_image_model,
    )

    if not isinstance(image, Image.Image):
        image = Image.open(BytesIO(image))

    filename = f"panel-{panel_number}-{_safe_filename(uuid.uuid4().hex)}.png"
    output_path = settings.panels_dir / filename
    image.convert("RGB").save(output_path, format="PNG")
    return f"/static/panels/{filename}"
