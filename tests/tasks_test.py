import pytest
import json
from app import create_app
from app.extansions import db
from app.models import Users, Category, Tasks


@pytest.fixture
def test_app():
    app = create_app(testing=True)
    app.config.update(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    with app.app_context():
        db.create_all()
        user = Users(title="testuser", token="TestToken")
        db.session.add(user)
        db.session.commit()
        category = Category(title="TestCategory", user_id=user.id)
        db.session.add(category)
        db.session.commit()
        user2 = Users(title="anotheruser", token="anothertoken")
        db.session.add(user2)
        db.session.commit()
        category2 = Category(title="anothercategory", user_id=user2.id)
        db.session.add(category2)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_create_task_success(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
        category = Category.query.filter_by(title="TestCategory").first()
    response = client.post(
        "/tasks/",
        data=json.dumps({"title": "Test Task", "description": "test", "category_id": category.id, "status": "new", "dead_line": "2025-01-26 16:00:00"}),
        content_type="application/json",
        headers={"token": user.token, "id": user.id}
    )
    assert response.status_code == 200
    assert response.json["message"] == "Задача успешно создана"


def test_create_task_missing_json(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
    response = client.post(
        "/tasks/",
        headers={"token": user.token, "id": user.id}
    )
    assert response.status_code == 415
    assert response.json["error"] == "Content-Type must be application/json"


def test_create_task_invalid_category(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
        category = Category.query.filter_by(title="TestCategory").first()
        user2 = Users.query.filter_by(title="anotheruser").first()
        category2 = Category.query.filter_by(title="anothercategory").first()
    data = {
        "title": "Test Task",
        "description": "Test",
        "category_id": 999,
        "status": "new",
        "dead_line": "2025-04-10 12:00:00"
    }
    response = client.post('/tasks/', json=data, headers={"token": user.token, "id": user.id})
    assert response.status_code == 404
    data = {
        "title": "Test Task",
        "description": "Test",
        "category_id": category2.id,
        "status": "new",
        "dead_line": "2025-04-10 12:00:00"
    }
    response = client.post('/tasks/', json=data, headers={"token": user.token, "id": user.id})
    assert response.status_code == 403
    assert response.json["error"] == "Invalid category"
    data = {
        "title": "Test Task",
        "description": "Test",
        "category_id": category.id,
        "status": "new",
        "dead_line": "2025-04-10 12:00:00"
    }
    response = client.post('/tasks/', json=data, headers={"token": user2.token, "id": user2.id})
    assert response.status_code == 403
    assert response.json["error"] == "Invalid category"


def test_create_task_invalid_deadline_format(client, test_app):
    with test_app.app_context():
        user = Users.query.filter_by(title="testuser").first()
        category = Category.query.filter_by(title="TestCategory").first()

    data = {
        "title": "Test Task",
        "description": "Test",
        "category_id": category.id,
        "status": "open",
        "dead_line": "invalid_date"
    }
    response = client.post('/tasks/', json=data, headers={"token": user.token, "id": user.id})
    assert response.status_code == 400
    assert response.json["error"] == "Incorrect date format"



