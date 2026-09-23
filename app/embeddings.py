from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer

@lru_cache(maxsize=2)
def get_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)

def embed_texts(texts: list[str], model_name: str) -> np.ndarray:
    model = get_model(model_name)
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
        convert_to_numpy=True,
    )
    return vectors.astype("float32")

def embed_query(query: str, model_name: str) -> np.ndarray:
    return embed_texts([query], model_name)[0]
