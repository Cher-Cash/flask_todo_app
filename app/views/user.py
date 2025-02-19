from flask import Blueprint, jsonify, request

from app.auth import token_required
from app.extansions import db
from app.models import Category, Users
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


@user_bp.route("/", methods=["PATCH"])
@token_required
def patch_user(user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не получены данные"}), 404
    user.title = data.get("username", user.title)
    db.session.commit()
    return jsonify({"message": f"Пользователь {user.title} обновлен"}), 200


@user_bp.route("/categories", methods=["GET"])
@token_required
def get_user_categories(user):
    categories = Category.query.filter_by(user_id=user.id).all()
    return jsonify([to_dict(category) for category in categories])
