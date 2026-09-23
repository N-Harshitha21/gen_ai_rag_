from pathlib import Path
import fitz  # PyMuPDF

from app.models import Chunk

def extract_pdf_pages(file_bytes: bytes, filename: str) -> list[tuple[int, str]]:
    """Return [(page_number, text), ...]. Page numbers are 1-based."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    try:
        for page_index, page in enumerate(doc):
            text = page.get_text("text").strip()
            if text:
                pages.append((page_index + 1, text))
    finally:
        doc.close()
    return pages

def extract_txt(file_bytes: bytes) -> list[tuple[int | None, str]]:
    text = file_bytes.decode("utf-8", errors="replace").strip()
    return [(None, text)] if text else []

def parse_document(file_bytes: bytes, filename: str) -> list[tuple[int | None, str]]:
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        return extract_pdf_pages(file_bytes, filename)
    if ext == ".txt":
        return extract_txt(file_bytes)
    raise ValueError(f"Unsupported file type: {ext}. Only PDF and TXT are supported.")
