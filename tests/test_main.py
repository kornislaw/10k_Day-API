from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()["message"] == "Hello World"


def test_say_hello() -> None:
    """Get a hello for someone"""
    response = client.get("/hello/Jacek")
    result = response.json()
    assert response.status_code == 200
    assert result["message"] == "Hello Jacek"
