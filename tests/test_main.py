import json

from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()["message"] == "Hello World"


def test_get_one_exe() -> None:
    """Get one exercise"""
    response = client.get("/exercises/1")
    result = response.json()
    assert response.status_code == 200
    assert result['name'] == "The best exercise ever"


def test_get_nonexisting_exe() -> None:
    """Get an exe that does not exist; expect 404"""
    response = client.get("/exercises/0")
    result = response.json()
    assert response.status_code == 404
    assert 'detail' in result
    assert 'not found' in result['detail']



def test_post_exercise() -> None:
    """Get a hello for someone"""
    exe = {
        "name": "Excercise number {{$randomInt}}",
        "description": "Description: {{$randomCatchPhraseAdjective}} {{$randomCatchPhrase}}"
    }
    response = client.post('/exercise', data=json.dumps(exe))
    result = response.json()
    assert response.status_code == 201
    assert "name" in result


def test_delete_exercise() -> None:
    """Delete an exercise by ID"""
    response = client.delete("/exercises/1")
    result = response.json()
    assert response.status_code == 204
    assert result == None




