import io
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def make_data(content: bytes, doc_id: str, filename: str = "file.pdf"):
    return {
        "documentId": doc_id,
        "file": (io.BytesIO(content), filename)
    }
