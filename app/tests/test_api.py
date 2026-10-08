from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_healthz_returns_ok() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_greet_returns_message() -> None:
    response = client.get("/greet", params={"name": "Ruan"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Ruan!"}


def test_greet_requires_name() -> None:
    response = client.get("/greet")
    assert response.status_code == 422


def test_greet_rejects_empty_name() -> None:
    response = client.get("/greet", params={"name": ""})
    assert response.status_code == 422


def test_openapi_is_available() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert app.title == "branch-protection-poc-api"
