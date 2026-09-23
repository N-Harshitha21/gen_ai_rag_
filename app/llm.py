from google import genai
from google.genai import types

from app.models import SearchResult, Answer


SYSTEM_PROMPT = """You are a document question-answering assistant.

Rules:
1. Answer only from the supplied document context.
2. Do not use outside knowledge to fill gaps.
3. If the context does not contain enough evidence to answer the question,
   return exactly: NOT_FOUND
4. Keep the answer concise and factual.
5. When useful, mention document names or page numbers, but do not invent citations.
"""


def _build_context(results: list[SearchResult]) -> str:
    blocks = []

    for i, result in enumerate(results, start=1):
        chunk = result.chunk

        location = f"{chunk.source}"

        if chunk.page is not None:
            location += f", page {chunk.page}"

        blocks.append(
            f"[SOURCE {i} | {location} | similarity={result.score:.3f}]\n"
            f"{chunk.text}"
        )

    return "\n\n".join(blocks)


def answer_question(
    question: str,
    results: list[SearchResult],
    api_key: str,
    model: str,
    base_url=None,
) -> Answer:

    if not results:
        return Answer(
            text="I couldn't find enough information in the uploaded documents to answer that question.",
            sources=[],
            found=False,
        )

    client = genai.Client(api_key=api_key)

    user_prompt = f"""Document context:

{_build_context(results)}

Question:
{question}

Answer using only the document context above.
"""

    response = client.models.generate_content(
        model=model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
    )

    text = (response.text or "").strip()

    if text == "NOT_FOUND":
        return Answer(
            text="I couldn't find enough information in the uploaded documents to answer that question.",
            sources=results,
            found=False,
        )

    return Answer(
        text=text,
        sources=results,
        found=True,
    )