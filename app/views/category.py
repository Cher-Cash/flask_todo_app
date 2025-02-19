from flask import Blueprint, jsonify, request

from app.auth import token_required
from app.extansions import db
from app.models import Category

category_bp = Blueprint("category_bp", __name__)


@category_bp.route("/", methods=["POST"])
@token_required
def new_category(user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    name = data.get("title")
    n_category = Category(title=name, user_id=user.id)
    db.session.add(n_category)
    db.session.commit()
    return jsonify({"message": f"Категория {name} успешно создана"}), 200


@category_bp.route("/<int:category_id>", methods=["PATCH"])
@token_required
def patch_category(category_id, user):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    if category.user_id != user.id:
        return jsonify({"error": "Invalid user"}), 403
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    title = data.get("title")
    category.title = title
    db.session.commit()
    return jsonify({"message": f"Категория {category.title} обновлена"}), 200
