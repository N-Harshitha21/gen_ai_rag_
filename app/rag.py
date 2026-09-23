from app.chunker import chunk_pages
from app.document_parser import parse_document
from app.embeddings import embed_query, embed_texts
from app.models import Answer
from app.vector_store import VectorStore
from app.llm import answer_question
class DocumentAssistant:
    def __init__(
        self,
        embedding_model: str,
        chunk_size: int,
        chunk_overlap: int,
        top_k: int,
        min_similarity: float,
    ):
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.min_similarity = min_similarity
        self.store = VectorStore()
        self.documents: list[str] = []

    def ingest_files(self, uploaded_files) -> int:
        all_chunks = []

        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.getvalue()
            pages = parse_document(file_bytes, uploaded_file.name)
            chunks = chunk_pages(
                pages,
                source=uploaded_file.name,
                chunk_size=self.chunk_size,
                overlap=self.chunk_overlap,
            )
            all_chunks.extend(chunks)

            if uploaded_file.name not in self.documents:
                self.documents.append(uploaded_file.name)

        if not all_chunks:
            raise ValueError("No readable text was found in the uploaded files.")

        embeddings = embed_texts(
            [chunk.text for chunk in all_chunks],
            self.embedding_model,
        )
        self.store.build(all_chunks, embeddings)
        return len(all_chunks)

    def ask(self, question: str, api_key: str, llm_model: str, base_url=None) -> Answer:
        query_vector = embed_query(question, self.embedding_model)
        results = self.store.search(
            query_vector,
            top_k=self.top_k,
            min_similarity=self.min_similarity,
        )
        return answer_question(
            question,
            results,
            api_key=api_key,
            model=llm_model,
            base_url=base_url,
        )
