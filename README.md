# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI + Jinja2 web application that turns a user prompt into a five-panel comic. It follows the supplied project specification: form input, Gemini outline generation, Gemini story/dialogue generation, AI image generation, panel layout, PDF export, browser preview, and JSON APIs.

## Architecture

- Frontend: HTML + CSS + JavaScript + Jinja2
- Backend: FastAPI
- Story outline: Gemini structured JSON
- Story/dialogue: Gemini structured JSON
- Images: Hugging Face Inference Providers text-to-image
- PDF: fpdf2
- Local testing: `AI_MOCK_MODE=true`

The supplied document describes the original project with Gemini 1.5 Flash/Pro and Stable Diffusion. This implementation keeps the same architecture and workflow but uses the current Google GenAI SDK and a hosted Hugging Face text-to-image API so the project is practical to run without downloading a multi-gigabyte diffusion model.

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routes.py
│   ├── schemas.py
│   └── services/
│       ├── __init__.py
│       ├── exporters.py
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       ├── mock_ai.py
│       └── workflow.py
├── static/
│   ├── css/style.css
│   ├── js/app.js
│   ├── panels/
│   └── exports/
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── tests/test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## VS Code setup — Windows

1. Open the `ComicCraft` folder in VS Code.
2. Install Python 3.11 or newer.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
py -3.11 -m venv .venv
```

5. Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Copy `.env.example` to `.env`.

For PowerShell:

```powershell
Copy-Item .env.example .env
```

## First run without API keys

This verifies that FastAPI, Jinja2, routing, PDF export, and the frontend work before connecting remote AI services.

In `.env`:

```env
AI_MOCK_MODE=true
```

Then:

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/api/health

The mock mode generates simple placeholder panel images, but exercises the complete application workflow and PDF export.

## Enable real AI

Set:

```env
AI_MOCK_MODE=false
GEMINI_API_KEY=your_key
HF_TOKEN=your_token
```

The default text models are:

```env
GEMINI_OUTLINE_MODEL=gemini-2.5-flash
GEMINI_STORY_MODEL=gemini-2.5-pro
```

The default image model is:

```env
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
HF_PROVIDER=auto
```

If your Google or Hugging Face account has different model/provider availability, change those environment variables rather than changing application code.

## Run

```powershell
uvicorn app.main:app --reload
```

## Test

Run all automated tests:

```powershell
pytest -q
```

The test suite forces mock mode so it does not require API keys.

## API endpoints

### `GET /`
Main web form.

### `POST /generate`
HTML form workflow.

Fields:
- `story_prompt`
- `character_name`
- `setting`
- `tone`
- `art_style`

### `POST /api/generate-comic`
JSON API.

Example:

```json
{
  "story_prompt": "A brave fox discovers a hidden library.",
  "character_name": "Milo",
  "setting": "enchanted forest",
  "tone": "funny",
  "art_style": "comic book"
}
```

### `POST /test-image`
Image-generation test endpoint.

Form field:

```text
prompt=A fox reading a magical book in a forest
```

### `GET /api/health`
Configuration and server health.

### `GET /export-success?pdf_url=...`
Export confirmation page.

### `GET /download/{filename}`
Downloads a generated PDF.

## Troubleshooting

### `GEMINI_API_KEY is not configured`
Check `.env` and set `AI_MOCK_MODE=false` only after adding a valid Gemini key.

### `HF_TOKEN is not configured`
Add a Hugging Face token with permission to use Inference Providers.

### Image model/provider error
Change `HF_IMAGE_MODEL` or `HF_PROVIDER` to a model/provider available to your Hugging Face account.

### PDF encoding issue
The PDF exporter intentionally uses simple text-safe output for broad compatibility. If you later need full Unicode/Tamil text in PDFs, add a Unicode TTF font to the PDF exporter and register it with fpdf2.

### Port already in use

```powershell
uvicorn app.main:app --reload --port 8001
```

Then open http://127.0.0.1:8001.

## Production notes

For production deployment:
- Keep `.env` out of source control.
- Put generated files in object storage rather than the local filesystem.
- Add authentication/rate limiting before exposing generation endpoints publicly.
- Add background jobs for image generation so long requests do not occupy web workers.
- Add cleanup for old images and PDFs.
- Pin tested dependency versions after deployment validation.
