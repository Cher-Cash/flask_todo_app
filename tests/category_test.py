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
        user = Users(title="testuser", token="BearerSampleToken")
        db.session.add(user)
        db.session.commit()
        category = Category(title="Test Patch Category", user_id=user.id)
        db.session.add(category)
        db.session.commit()
        user2 = Users(title="anotheruser", token="anothertoken")
        db.session.add(user2)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_create_category_missing_json(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.post(
        "/categories/",
        headers={"token": user.token, "id": user.id},
    )
    assert response.status_code == 415
    assert response.json["error"] == "Content-Type must be application/json"


def test_create_category_empty_json(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.post(
        "/categories/",
        data=json.dumps({}),
        content_type="application/json",
        headers={"token": user.token, "id": user.id},
    )
    assert response.status_code == 415
    assert response.json["error"] == "Тело запроса пустое"


def test_create_category_wrong_title(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.post(
        "/categories/",
        data=json.dumps({"cat_name": "Test Category"}),
        content_type="application/json",
        headers={"token": user.token, "id": user.id},
    )
    assert response.status_code == 400


def test_create_category_invalid_token(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.post(
        "/categories/",
        data=json.dumps({"title": "Test Category"}),
        content_type="application/json",
        headers={"token": "InvalidToken", "id": user.id},
    )
    assert response.status_code == 403
    assert response.json["error"] == "Invalid user"


def test_create_category_success(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    new_category = {"title": "Test Category"}
    response = client.post(
        "/categories/",
        data=json.dumps(new_category),
        content_type="application/json",
        headers={"token": user.token, "id": user.id},
    )
    assert response.status_code == 200
    assert response.json["message"] == "Категория Test Category успешно создана"
    with test_app.app_context():
        category = Category.query.filter_by(title="Test Category").first()
    assert category is not None
    assert category.user_id == user.id


def test_patch_category_success(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
        category = Category.query.first()
    data = {"title": "Updated Category"}

    response = client.patch(f"/categories/{category.id}",
                            headers={"token": user.token, "id": user.id},
                            data=json.dumps(data),
                            content_type="application/json")

    assert response.status_code == 200
    assert response.json["message"] == "Категория Updated Category обновлена"
    with test_app.app_context():
        category = Category.query.get(category.id)
    assert category.title == "Updated Category"


def test_patch_category_invalid_user(client, test_app):
    with test_app.app_context():
        user2 = Users.query.filter_by(title="anotheruser").first()
        category = Category.query.first()
    data = {"title": "Updated Category"}

    response = client.patch(f"/categories/{category.id}",
                            headers={"token": user2.token, "id": user2.id},
                            data=json.dumps(data),
                            content_type="application/json")
    assert response.status_code == 403
    assert response.json["error"] == "Invalid user"


def test_patch_category_no_json(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
        category = Category.query.first()
    response = client.patch(f"/categories/{category.id}",
                            headers={"token": user.token, "id": user.id})
    assert response.status_code == 415
    assert response.json["error"] == "Content-Type must be application/json"


def test_patch_category_category_not_found(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.patch("/categories/9999",
                            headers={"token": user.token, "id": user.id},
                            data=json.dumps({"title": "New Category"}),
                            content_type="application/json")
    assert response.status_code == 404
