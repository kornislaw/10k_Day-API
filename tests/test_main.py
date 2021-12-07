import json

from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)
import uuid
import secrets

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello World"


def _test_get_nonexisting_noun(noun: str) -> None:
    """An abstract test with the noun provided; expect 404"""
    response = client.get(f"/{noun}/0")
    result = response.json()
    assert response.status_code == 404
    assert "detail" in result
    assert "not found" in result["detail"]


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
    _test_get_nonexisting_noun('exercises')


def test_users_crud() -> None:
    """Go with all CRUD operation for User"""

    # CREATE
    rand_hex = uuid.uuid4().hex
    user = {
        "email": f"{rand_hex[0:8]}@{rand_hex[8:16]}.com",
        "password": secrets.token_hex(8),
    }
    response = client.post("/users", data=json.dumps(user))
    new_user = response.json()
    assert response.status_code == 201
    assert "email" in new_user

    # RETRIEVE
    response = client.get(f"/users/{new_user['id']}")
    retrieved_user = response.json()
    assert response.status_code == 200
    assert "email" in retrieved_user
    assert "password" not in retrieved_user
    assert "id" in retrieved_user

    # UPDATE
    rand_hex = uuid.uuid4().hex
    user = {
        "email": f"{rand_hex[0:8]}@{rand_hex[8:16]}.com",
        "password": secrets.token_hex(8),
    }
    response = client.put(f"/users/{retrieved_user['id']}", data=json.dumps(user))
    updated_user = response.json()
    assert response.status_code == 200
    assert "email" in updated_user
    assert "password" not in updated_user
    assert "id" in updated_user

    # DELETE
    response = client.delete(f"/users/{updated_user['id']}")
    assert response.status_code == 204


def test_get_nonexisting_user() -> None:
    """Get a user that does not exist; expect 404"""
    _test_get_nonexisting_noun('users')