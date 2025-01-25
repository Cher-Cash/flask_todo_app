from datetime import datetime

from flask import Blueprint, jsonify, request

from app.extansions import db
from app.models import Category, Tasks, Users
from app.utils import to_dict

task_bp = Blueprint("task_bp", __name__)


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
                   category_id=category.id, status=status, dead_line=dead_line,
                   )
    db.session.add(n_task)
    db.session.commit()
    return jsonify({"message": "Задача успешно создана"}), 200


@task_bp.route("/<int:task_id>", methods=["PATCH"])
def patch_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    task: Tasks = Tasks.query.get_or_404(task_id)
    for key in data:
        if hasattr(task, key):
            if key == "dead_line" and data[key]:
                value = datetime.strptime(data[key], "%Y-%m-%d %H:%M:%S")
            else:
                value = data[key]
            setattr(task, key, value)
    db.session.commit()
    return jsonify({"message": f"Задача {task.title} успешно изменена"}), 200


@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task: Tasks = Tasks.query.get_or_404(task_id)
    task.delete_on = datetime.now()
    db.session.commit()
    return jsonify({"message": f"Задача {task.title} успешно удалена"}), 200


# Залипуха для разработки
def get_user_id(request):  # noqa: ARG001
    return 1


@task_bp.route("/", methods=["GET"])
def task_list():
    user_id = get_user_id(request)
    tasks = Tasks.query.filter_by(user_id=user_id).all()
    return jsonify([to_dict(task) for task in tasks])
