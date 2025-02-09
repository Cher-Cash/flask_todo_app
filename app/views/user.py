from flask import Blueprint, jsonify, request

from app.extansions import db
from app.models import Category, Tasks, Users
from app.utils import to_dict

user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["POST"])
def new_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    name = data.get("username")
    user = Users(title=name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Пользователь успешно создан"}), 200


@user_bp.route("/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    user = Users.query.get_or_404(user_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Пользователь не найден"}), 404
    user.title = data.get("username", user.title)
    db.session.commit()
    return jsonify({"message": f"Пользователь {user.title} обновлен"}), 200


@user_bp.route("/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    user = Users.query.get_or_404(user_id)
    tasks = Tasks.query.filter_by(user_id=user.id).all()
    return jsonify([task.to_dict() for task in tasks])


@user_bp.route("/<int:user_id>/categories", methods=["GET"])
def get_user_categories(user_id):
    user = Users.query.get_or_404(user_id)
    categories = Category.query.filter_by(user_id=user.id).all()
    return jsonify([to_dict(category) for category in categories])
