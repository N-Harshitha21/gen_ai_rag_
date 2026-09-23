import faiss
import numpy as np

from app.models import Chunk, SearchResult

class VectorStore:
    def __init__(self):
        self.index: faiss.Index | None = None
        self.chunks: list[Chunk] = []

    def build(self, chunks: list[Chunk], embeddings: np.ndarray) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks and embeddings must match.")
        if not chunks:
            raise ValueError("Cannot build a vector store with no chunks.")

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        self.chunks = chunks

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 5,
        min_similarity: float = 0.35,
    ) -> list[SearchResult]:
        if self.index is None:
            return []

        q = np.asarray(query_vector, dtype="float32").reshape(1, -1)
        scores, indices = self.index.search(q, min(top_k, len(self.chunks)))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            if float(score) < min_similarity:
                continue
            results.append(SearchResult(chunk=self.chunks[int(idx)], score=float(score)))
        return results

    def __len__(self):
        return len(self.chunks)
