import re
import uuid
from app.models import Chunk

def _clean(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def chunk_pages(
    pages: list[tuple[int | None, str]],
    source: str,
    chunk_size: int = 900,
    overlap: int = 150,
) -> list[Chunk]:
    """
    Character-based chunking with overlap.
    Page metadata is preserved. Chunks do not cross page boundaries,
    which makes source citations easier.
    """
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be > 0 and overlap must be >= 0 and < chunk_size")

    chunks: list[Chunk] = []

    for page, raw_text in pages:
        text = _clean(raw_text)
        if not text:
            continue

        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    Chunk(
                        chunk_id=str(uuid.uuid4()),
                        text=chunk_text,
                        source=source,
                        page=page,
                    )
                )

            if end >= len(text):
                break
            start = end - overlap

    return chunks
