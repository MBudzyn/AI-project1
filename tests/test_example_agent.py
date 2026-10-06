"""Tests that do not require an API key."""

from fastapi.testclient import TestClient

from agents.example import build_example_graph
from api.main import app


def test_root_is_available() -> None:
    response = TestClient(app).get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_example_graph_echoes_message() -> None:
    graph = build_example_graph()
    result = graph.invoke({"message": "hello"})
    assert result["message"] == "hello"
