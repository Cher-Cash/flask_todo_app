from flask import Blueprint, jsonify, request

from app.extansions import db
from app.models import Category, Users
from app.utils import to_dict

category_bp = Blueprint("category_bp", __name__)


@category_bp.route("/", methods=["POST"])
def new_category():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    name = data.get("title")
    user_id = data.get("user_id")
    user = Users.query.get_or_404(user_id)
    n_category = Category(title=name, user_id=user.id)
    db.session.add(n_category)
    db.session.commit()
    return jsonify({"message": f"Категория {name} успешно создана"}), 200


@category_bp.route("/<int:category_id>", methods=["PATCH"])
def patch_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    title = data.get("title")
    user_id = data.get("user_id")
    Users.query.get_or_404(user_id)
    category.title = title
    db.session.commit()
    return jsonify({"message": f"Категория {category.title} обновлена"}), 200


@category_bp.route("/", methods=["GET"])
def get_category():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    user_id = data.get("user_id")
    categories = Category.query.filter_by(user_id=user_id).all()
    return jsonify([to_dict(category) for category in categories])
