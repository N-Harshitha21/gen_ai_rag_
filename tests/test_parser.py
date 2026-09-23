from app.document_parser import extract_txt

def test_txt_parser():
    pages = extract_txt(b"hello\\nworld")
    assert pages == [(None, "hello\\nworld")]
