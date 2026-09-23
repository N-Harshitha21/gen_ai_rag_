from app.chunker import chunk_pages

def test_chunking_preserves_page():
    chunks = chunk_pages(
        [(2, "A" * 1000)],
        source="policy.pdf",
        chunk_size=300,
        overlap=50,
    )
    assert len(chunks) > 1
    assert all(c.source == "policy.pdf" for c in chunks)
    assert all(c.page == 2 for c in chunks)

def test_empty_page():
    assert chunk_pages([(1, "")], "x.pdf") == []
