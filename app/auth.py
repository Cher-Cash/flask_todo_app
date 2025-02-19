from functools import wraps
from flask import request, jsonify
from app.models import Users


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')  # Получаем токен из заголовков
        user_id = request.headers.get('id')
        if not token or not user_id:
            return jsonify({"message": "Token or user_id is missing!"}), 401
        user_id = int(user_id)
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"message": "Invalid user"}), 403
        if user.token != token:
            return jsonify({"message": "Invalid user"}), 403
        # Добавляем пользователя в аргументы маршрута, чтобы потом его использовать
        kwargs['user'] = user
        return f(*args, **kwargs)
    return decorator
