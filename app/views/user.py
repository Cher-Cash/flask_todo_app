from tkinter.font import names

from flask import Blueprint, render_template, abort, request, current_app, jsonify
from app.models import Users, Category, Tasks
from app.extansions import db
'''
V/user method=POST #создание нового пользователя
V/patch_user/<user.id> method=PATCH #изменение данных пользователя
V/user/<user.id>/tasks method=GET #получения списка задач пользователя
/user/<user.id>/category method=GET #получение списка категорий пользователя
/user/<user.id>/category/<category.id> method=GET #получение списка задач по категории
/user/<user.id>/tasks?tasks.status=status method=GET #получение списка задач по статусу
'''
user_bp = Blueprint('user', __name__)


@user_bp.route("/user", methods=["POST"])
def new_user():
    data = request.get_json()
    if data:
        name = data.get("username")
        return jsonify({"username":name}), 200
    else:
        return jsonify({"error":"Не был передан JSON"}), 400
    user = Users(title=name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"Пользователь успешно создан"}), 200

@user_bp.route("/user/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    user = Users.query.get_or_404(user_id)
    data = request.get_json()
    if  not data:
        return jsonify({"error":"Пользователь не найден"}), 404
    user.title = data.get('username', user.title)
    db.session.commit()
    return jsonify({"message": f"Пользователь {user.title} обновлен"}), 200

@user_bp.route("/user/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    user = Users.query.get_or_404(user_id)
    tasks = Tasks.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks])

@user_bp.route("/user/<int:user_id>/category", methods=["GET"])
def get_category_tasks(user_id):
    user = Users.query.get_or_404(user_id)
    data = request.get_json()
    if not data:
        return jsonify({"error":"Категории не найдены"}), 404
    categories = Category.query.filter_by(user_id=user_id).all()
    return jsonify([categories.to_dict() for category in categories])

