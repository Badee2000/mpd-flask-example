import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app  # noqa: E402


@pytest.fixture
def client():
    return create_app().test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
    assert response.get_json()["version"] == "v2"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_unknown_route_returns_json_404(client):
    response = client.get("/nope")
    assert response.status_code == 404
    assert response.get_json() == {"error": "not found"}


def test_missing_secret_key_refuses_to_start(monkeypatch):
    monkeypatch.delenv("SECRET_KEY")
    with pytest.raises(RuntimeError):
        create_app()
