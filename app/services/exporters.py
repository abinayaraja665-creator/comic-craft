import os
from datetime import datetime
from fpdf import FPDF

def sanitize_text(text: str) -> str:
    """
    Replaces non-latin-1 / Unicode characters with standard ASCII equivalents
    to prevent FPDF character encoding errors.
    """
    if not text:
        return ""
        
    replacements = {
        "—": "-",   # Em-dash
        "–": "-",   # En-dash
        "“": '"',   # Left double quote
        "”": '"',   # Right double quote
        "‘": "'",   # Left single quote
        "’": "'",   # Right single quote
        "…": "...",  # Ellipsis
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    
    return text.encode("latin-1", "replace").decode("latin-1")


class PDF(FPDF):
    def __init__(self, doc_title="ComicCraft - AI Generated Comic"):
        super().__init__()
        self.doc_title = doc_title

    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, sanitize_text(self.doc_title), ln=True, align='C')
        self.ln(5)


def save_pdf(layout: list = None, title: str = "ComicCraft - AI Generated Comic", **kwargs) -> str:
    """
    Compiles full comic layout into a multi-page PDF document.
    Defaults layout to an empty list if None is passed to prevent missing positional argument errors.
    """
    if layout is None:
        layout = []

    pdf = PDF(doc_title=title)
    pdf.set_auto_page_break(auto=True, margin=15)
    EXPORT_FOLDER = "static/exports"
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    for panel in layout:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 14)
        
        # Sanitize panel title
        title_text = sanitize_text(f"Panel {panel.get('panel', '')}: {panel.get('title', '')}")
        pdf.cell(0, 10, title_text, ln=True, align="C")
        pdf.ln(5)

        image_path = panel.get('image_path', '')
        y_image = 35
        image_height = 90

        if image_path and os.path.exists(image_path):
            pdf.image(image_path, x=35, y=y_image, w=140, h=image_height)
        else:
            pdf.set_y(y_image)
            pdf.multi_cell(0, 10, f"Image missing: {image_path}")

        pdf.set_y(y_image + image_height + 10)
        pdf.set_font('Helvetica', 'I', 11)
        
        # Sanitize scene description
        scene_desc = sanitize_text(f"Scene: {panel.get('scene_description', '')}")
        pdf.multi_cell(0, 7, scene_desc)
        pdf.ln(3)

        pdf.set_font('Helvetica', '', 11)
        
        # Sanitize story text
        cleaned_text = sanitize_text(panel.get('text', ''))
        pdf.multi_cell(0, 7, cleaned_text)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(pdf_path)

    return pdf_path