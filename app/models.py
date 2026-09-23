from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Chunk:
    chunk_id: str
    text: str
    source: str
    page: Optional[int] = None
    metadata: dict = field(default_factory=dict)

@dataclass
class SearchResult:
    chunk: Chunk
    score: float

@dataclass
class Answer:
    text: str
    sources: list[SearchResult]
    found: bool
