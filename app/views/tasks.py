from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models import Users, Category, Tasks
from app.extansions import db


task_bp = Blueprint('task_bp', __name__)


@task_bp.route("/", methods=["POST"])
def new_task():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    title = data.get("title")
    description = data.get("description")
    user_id = data.get("user_id")
    created_on = datetime.now()
    category_id = data.get("category_id")
    status = data.get("status")
    date = data.get("dead_line")
    dead_line = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    category = Category.query.get_or_404(category_id)
    user = Users.query.get_or_404(user_id)
    n_task = Tasks(title=title, description=description, user_id=user.id, created_on=created_on,
                   category_id=category.id, status=status, dead_line=dead_line
                   )
    db.session.add(n_task)
    db.session.commit()
    return jsonify({"message": f"Задача успешно создана"}), 200