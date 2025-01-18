from flask import Blueprint, render_template, abort, request, current_app, jsonify
from app.models import Users, Category, Tasks
from app.extansions import db


category_bp = Blueprint('category_bp', __name__)

@category_bp.route("/", methods=["POST"])
def new_category():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Не был передан JSON"}), 400
    name = data.get("title")
    user_id = data.get("user_id")
    user = Users.query.get_or_404(user_id)
    n_category = Category(title=name, user_id=user.id)
    db.session.add(n_category)
    db.session.commit()
    return jsonify({"message":f"Категория {name} успешно создана"}), 200