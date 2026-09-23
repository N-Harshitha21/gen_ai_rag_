import streamlit as st
from app.config import settings
# from app.rag import answer_question
from app.rag import DocumentAssistant
# from app.models import ...


st.set_page_config(
    page_title="Smart Document Assistant",
    page_icon="📚",
    layout="wide",
)

@st.cache_resource
def get_assistant():
    return DocumentAssistant(
        embedding_model=settings.embedding_model,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        top_k=settings.top_k,
        min_similarity=settings.min_similarity,
    )

assistant = get_assistant()

st.title("📚 Smart Document Assistant")
st.caption("Ask questions about your uploaded PDF and TXT documents using grounded RAG.")

if "ready" not in st.session_state:
    st.session_state.ready = False

with st.sidebar:
    st.header("1. Upload documents")
    uploaded_files = st.file_uploader(
        "Choose PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.write("Uploaded:")
        for f in uploaded_files:
            st.write(f"• {f.name}")

        if st.button("Process documents", type="primary"):
            with st.spinner("Extracting, chunking, and indexing documents..."):
                try:
                    count = assistant.ingest_files(uploaded_files)
                    st.session_state.ready = True
                    st.success(f"Indexed {count} text chunks.")
                except Exception as exc:
                    st.error(f"Could not process documents: {exc}")

    st.divider()
    st.header("Configuration")
    st.write(f"Embedding model: `{settings.embedding_model}`")
    st.write(f"LLM: `{settings.llm_model}`")
    st.write(f"Top-k retrieval: `{settings.top_k}`")

if not settings.gemini_api_key:
    st.warning(
        "GEMINI_API_KEY is not configured. Add it to your .env file before asking questions."
    )

st.subheader("2. Ask a question")

question = st.text_area(
    "Question",
    placeholder="Example: How many annual leaves does an employee get?",
    height=100,
)

if st.button("Ask", type="primary", disabled=not st.session_state.ready):
    if not question.strip():
        st.error("Please enter a question.")
    elif not settings.gemini_api_key:
        st.error("GEMINI_API_KEY is missing.")
    else:
        with st.spinner("Searching documents and generating an answer..."):
            try:
                result = assistant.ask(
    question.strip(),
    api_key=settings.gemini_api_key,
    llm_model=settings.llm_model,
)

                st.subheader("Answer")
                st.write(result.text)

                st.subheader("Sources")
                if result.sources:
                    for source in result.sources:
                        location = source.chunk.source
                        if source.chunk.page is not None:
                            location += f" — page {source.chunk.page}"
                        with st.expander(
                            f"{location} | similarity {source.score:.3f}"
                        ):
                            st.write(source.chunk.text)
                else:
                    st.info("No sufficiently relevant source was retrieved.")
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")

st.divider()
st.caption(
    "Hallucination control: retrieval threshold + prompt grounding + explicit NOT_FOUND handling."
)
