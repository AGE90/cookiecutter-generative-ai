from fastapi.testclient import TestClient
from langchain_core.language_models import BaseChatModel

from {{ cookiecutter.module_name }}.api import app, get_graph
from {{ cookiecutter.module_name }}.graph import build_graph


def test_chat_endpoint(fake_llm: BaseChatModel) -> None:
    app.dependency_overrides[get_graph] = lambda: build_graph(fake_llm)
    try:
        client = TestClient(app)
        assert client.get("/health").json() == {"status": "ok"}
        response = client.post("/chat", json={"message": "What time is it?"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"answer": "It is noon."}
