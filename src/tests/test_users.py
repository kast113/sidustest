from datetime import datetime
import json

from app.api.users import views
from app.api.users.entity import UserEntity


def test_create_with_invalid_data(test_app):
    response = test_app.post(
        "/api/v1/users/", data=json.dumps({"description": "description"}))
    assert response.status_code == 422


def test_create_user(test_app, monkeypatch):
    async def mock_create_user(payload):
        return 1

    monkeypatch.setattr(views, "create_user", mock_create_user)

    user = {
        "name": "Sasha",
        "email": "sasha@outloo.k",
        "password": "qwerty"
    }
    response = test_app.post(
        "/api/v1/users/", data=json.dumps(user))
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Sasha",
        "email": "sasha@outloo.k"
    }


def test_get_user(test_app, monkeypatch):
    async def mock_get_user(id):
        return UserEntity(
            id=1, name="Ivan", email="em@mail.r", password="hashed", 
            created_at=datetime.now(), updated_at=datetime.now())

    monkeypatch.setattr(views, "get_user_by_id", mock_get_user)
    response = test_app.get("/api/v1/users/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Ivan",
        "email": "em@mail.r"
    }

    # response = test_app.post("/api/v1/users/")
    # assert response.status_code == 200
    # assert response.json() == {"success": True}
