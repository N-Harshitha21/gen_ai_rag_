# Smart Document Assistant

A small RAG-based document question-answering application built for the GenAI take-home assignment.

# Smart Document Assistant

A RAG-based application that allows users to upload PDF and TXT documents
and ask questions based on the uploaded documents.

## Features

- PDF and TXT document upload
- Document chunking
- Semantic retrieval
- Grounded question answering
- Retrieval threshold for hallucination control
- Explicit NOT_FOUND handling

## Demo Video

[Watch the Demo Video](https://drive.google.com/file/d/17xWzAxpt0-gciAdlNt_9a0nCoPv9U5kB/view?usp=sharing)

## What it does

1. Upload PDF/TXT documents.
2. Extract document text.
3. Split text into page-aware chunks.
4. Generate semantic embeddings.
5. Store embeddings in an in-memory FAISS index.
6. Retrieve relevant chunks for a question.
7. Ask an LLM to answer using only the retrieved context.
8. Display the answer and source chunks/pages.
9. Refuse to confidently answer when retrieval/context is insufficient.

## Architecture

```text
User
  |
  v
Streamlit UI
  |
  +--> Upload PDF/TXT
  |
  v
Document Parser (PyMuPDF)
  |
  v
Page-aware Chunking
  |
  v
Sentence-Transformers Embeddings
  |
  v
FAISS Vector Store
  |
  +<-- User Question
  |
  v
Semantic Retrieval
  |
  v
Grounded Prompt
  |
  v
OpenAI-compatible LLM
  |
  v
Answer + Retrieved Sources
```

## Technology choices

- **Python**: fast to implement and has mature document/ML tooling.
- **Streamlit**: minimal UI suitable for an 8-hour take-home assignment.
- **PyMuPDF**: PDF text extraction with page numbers.
- **Sentence Transformers**: local embeddings, avoiding an additional embedding API.
- **FAISS**: simple local vector search with no external database required.
- **OpenAI-compatible chat API**: LLM generation. The endpoint and model are configurable through environment variables.

## Prerequisites

- Python 3.10+
- An OpenAI API key (or a compatible endpoint/model)
- Internet access on first run to download the Sentence Transformer model
- Git is recommended

## Setup

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add your API key.

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then edit `.env`.

## Run

```bash
streamlit run -m app.main
```

If your Streamlit installation does not accept module execution, use:

```bash
streamlit run app/main.py
```

## How to test

Upload a sample policy document and ask:

- A question whose answer is clearly present.
- A question requiring information from another document.
- A question whose answer is absent.

For the absent question, the application should say it could not find enough information rather than inventing an answer.

## Hallucination reduction

This implementation uses several controls:

1. **Semantic retrieval**: only relevant chunks are sent to the LLM.
2. **Similarity threshold**: weak matches are filtered out.
3. **Grounded system prompt**: the LLM is instructed to use only retrieved context.
4. **Explicit NOT_FOUND contract**: the LLM is instructed to return `NOT_FOUND` if context is insufficient.
5. **Source metadata**: retrieved chunks retain document names and PDF page numbers.

These controls reduce hallucination risk but do not guarantee that an LLM can never make a mistake.

## Limitations

- The FAISS index is in memory and is rebuilt when the application process/session is restarted.
- Only PDF and TXT are supported.
- PDF extraction quality depends on whether the PDF contains machine-readable text. Scanned PDFs need OCR, which is not included.
- Character-based chunking is intentionally simple.
- The similarity threshold is a heuristic and should be evaluated against representative documents.
- Source chunks are displayed, but the generated answer itself is not automatically annotated sentence-by-sentence.
- The LLM still requires external API access unless you configure a compatible local endpoint.

## Creative feature

The application provides an **evidence view**: every answer can be expanded to inspect the retrieved source text, document name, page number, and retrieval similarity.

## AI tools used

For the take-home submission, disclose the actual tools you used. For example:

- ChatGPT: architecture discussion, debugging assistance, code review.
- Official library documentation: API verification.
- GitHub/Stack Overflow: troubleshooting, if actually used.

Do not claim tools you did not use.

## Security

- API keys are loaded from `.env`.
- `.env` is ignored by Git.
- Never commit real API keys, passwords, or other secrets.

## Suggested demo flow

1. Start the application.
2. Upload two policy documents.
3. Ask a question with an answer in one document.
4. Show the answer and source page.
5. Ask an unanswerable question.
6. Show the grounded "not found" response.
7. Expand a source to show the evidence.
8. Explain the architecture.
9. Explain limitations and future improvements.

## Suggested future improvements

With additional development time:

- Persistent vector database.
- DOCX/CSV/XLSX support.
- OCR for scanned PDFs.
- Hybrid keyword + semantic retrieval.
- Reranking.
- Better page/section citations.
- Conversation memory.
- Evaluation dataset and retrieval metrics.
- Authentication and per-user document isolation.
