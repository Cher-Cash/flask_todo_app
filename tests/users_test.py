import json

import pytest

from app import create_app
from app.extansions import db
from app.models import Category, Users


@pytest.fixture
def test_app():
    app = create_app(testing=True)
    app.config.update(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        },
    )
    with app.app_context():
        db.create_all()
        user = Users(title="testuser", token="TestToken")
        db.session.add(user)
        db.session.commit()
        category = Category(title="TestCategory", user_id=user.id)
        db.session.add(category)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_create_user_success(test_app, client):
    response = client.post(
        "/user/",
        data=json.dumps({"username": "Oleg"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json["message"] == "Пользователь успешно создан"
    with test_app.app_context():
        user = Users.query.filter_by(title="Oleg").first()
    assert user is not None


def test_create_user_empty_json(client):
    response = client.post(
        "/user/",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.json["error"] == "Не был передан JSON"


def test_create_user_missing_json(client):
    response = client.post("/user/")
    assert response.status_code == 415
    assert response.json["error"] == "Content-Type must be application/json"


def test_patch_user_success(test_app, client):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.patch(
        "/user/",
        data=json.dumps({"username": "Oleg"}),
        content_type="application/json",
        headers={"token": user.token, "id": user.id},
    )
    assert response.status_code == 200
    assert response.json["message"] == "Пользователь Oleg обновлен"
    with test_app.app_context():
        user = Users.query.filter_by(title="Oleg").first()
    assert user is not None


def test_patch_user_empty_json(test_app, client):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.patch(
        "/user/",
        data=json.dumps({}),
        content_type="application/json",
        headers={"token": user.token, "id": user.id},
    )
    assert response.status_code == 400
    assert response.json["error"] == "Не получены данные"


def test_patch_user_missing_json(test_app, client):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.patch(
        "/user/",
        headers={"token": user.token, "id": user.id},
    )
    assert response.status_code == 415
    assert response.json["error"] == "Content-Type must be application/json"


def test_get_user_categories_success(test_app, client):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.get(
        "/user/categories",
        headers={"token": user.token, "id": user.id},
    )
    assert response.status_code == 200
