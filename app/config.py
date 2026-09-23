import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    llm_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    top_k: int = int(os.getenv("TOP_K", "5"))
    min_similarity: float = float(os.getenv("MIN_SIMILARITY", "0.35"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))

    @property
    def gemini_api_key(self) -> str:
        return os.getenv("GEMINI_API_KEY", "")


settings = Settings()