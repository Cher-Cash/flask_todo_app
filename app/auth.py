from functools import wraps

from flask import jsonify, request

from app.models import Users


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("token")
        user_id = request.headers.get("id")
        if not token or not user_id:
            return jsonify({"message": "Token or user_id is missing!"}), 401
        user_id = int(user_id)
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"message": "Invalid user"}), 403
        if user.token != token:
            return jsonify({"message": "Invalid user"}), 403
        kwargs["user"] = user
        return f(*args, **kwargs)
    return decorator
