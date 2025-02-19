from datetime import datetime

from flask import Blueprint, jsonify, request

from app.extansions import db
from app.models import Category, Tasks, Users
from app.utils import to_dict
from app.auth import token_required

task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/", methods=["POST"])
@token_required
def new_task(user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    title = data.get("title")
    description = data.get("description")
    created_on = datetime.now()
    category_id = data.get("category_id")
    status = data.get("status")
    date = data.get("dead_line")
    dead_line = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    category = Category.query.get_or_404(category_id)
    n_task = Tasks(title=title, description=description, user_id=user.id, created_on=created_on,
                   category_id=category.id, status=status, dead_line=dead_line,
                   )
    db.session.add(n_task)
    db.session.commit()
    return jsonify({"message": "Задача успешно создана"}), 200


@task_bp.route("/<int:task_id>", methods=["PATCH"])
@token_required
def patch_task(task_id, user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Не был передан JSON"}), 400
    task: Tasks = Tasks.query.get_or_404(task_id)
    if task.user_id != user.id:
        return jsonify({"error": "Invalid user"}), 403
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
@token_required
def delete_task(task_id, user):
    task: Tasks = Tasks.query.get_or_404(task_id)
    if task.user_id != user.id:
        return jsonify({"error": "Invalid user"}), 403
    task.delete_on = datetime.now()
    db.session.commit()
    return jsonify({"message": f"Задача {task.title} успешно удалена"}), 200


# Залипуха для разработки
def get_user_id(request):  # noqa: ARG001
    return 1


@task_bp.route("/", methods=["GET"])
@token_required
def task_list(user):
    status = request.args.get("status")
    date_ = request.args.get("dead_line")
    dead_line = date_ and datetime.strptime(date_, "%Y-%m-%d/%H:%M:%S")
    category_id = request.args.get("category_id")
    tasks = Tasks.query.filter(Tasks.delete_on.is_(None)).filter_by(user_id=user.id)
    if category_id:
        tasks = tasks.filter_by(category_id=category_id)
    if status:
        tasks = tasks.filter_by(status=status)
    if dead_line:
        start_of_day = dead_line.replace(hour=0, minute=0, second=0, microsecond=0)
        tasks = tasks.filter(Tasks.dead_line <= dead_line).filter(Tasks.dead_line >= start_of_day)
    return jsonify([to_dict(task) for task in tasks.all()])


@task_bp.route("/<int:task_id>", methods=["GET"])
@token_required
def task_from_id(task_id, user):
    task = Tasks.query.get_or_404(task_id)
    if task.user_id != user.id:
        return jsonify({"error": "Invalid user"}), 403
    return jsonify(to_dict(task))
