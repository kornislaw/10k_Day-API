import json

from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello World"


def test_exercises_crud() -> None:
    """Go with all CRUD operation for Exercise"""

    # CREATE
    exe = {
        "name": "Exercise number {{$randomInt}}",
        "description": "Description: {{$randomCatchPhraseAdjective}} {{$randomCatchPhrase}}",
    }
    response = client.post("/exercise", data=json.dumps(exe))
    new_exe = response.json()
    assert response.status_code == 201
    assert "name" in new_exe

    # RETRIEVE
    response = client.get(f"/exercises/{new_exe['id']}")
    retrieved_exe = response.json()
    assert response.status_code == 200
    assert "name" in retrieved_exe
    assert "Exercise number " in retrieved_exe["name"]

    # UPDATE
    exe = {
        "name": "Updated exercise number {{$randomInt}}",
        "description": "Description: {{$randomCatchPhraseAdjective}} {{$randomCatchPhrase}}",
    }
    response = client.put(f"/exercises/{retrieved_exe['id']}", data=json.dumps(exe))
    updated_exe = response.json()
    assert response.status_code == 200
    assert "name" in updated_exe
    assert "Updated exercise " in updated_exe["name"]

    # DELETE
    response = client.delete(f"/exercises/{updated_exe['id']}")
    assert response.status_code == 204


def test_get_nonexisting_exe() -> None:
    """Get an exe that does not exist; expect 404"""
    response = client.get("/exercises/0")
    result = response.json()
    assert response.status_code == 404
    assert "detail" in result
    assert "not found" in result["detail"]
