import os
import typing

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from flask_migrate import Migrate

from app.extansions import db
from app.models import Category, Tasks, Users

admin_ext = Admin(template_mode="bootstrap3")
migrate_ext = Migrate()


def create_app():
    load_dotenv()
    new_app = Flask(__name__)
    new_app.secret_key = os.getenv("SECRET_KEY")
    new_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    new_app.config["CORS_HEADERS"] = "Content-Type"
    db.init_app(new_app)
    migrate_ext.init_app(new_app, db)
    admin_ext.init_app(new_app)
    CORS(new_app, resources={r"/*": {"origins": "*"}})

    @new_app.route("/ping")
    def init_route():
        return jsonify({"status": "ok"})

    from app.views.category import category_bp
    from app.views.tasks import task_bp
    from app.views.user import user_bp

    new_app.register_blueprint(user_bp, url_prefix="/user")
    new_app.register_blueprint(category_bp, url_prefix="/categories")
    new_app.register_blueprint(task_bp, url_prefix="/tasks")
    return new_app


class MyModelView(ModelView):
    column_hide_backrefs = False


class UsersView(MyModelView):
    column_list = ("id", "title", "created_on", "delete_on", "token")
    form_columns: typing.ClassVar = ["title", "created_on", "delete_on", "token"]


class CategoryView(MyModelView):
    column_list = ["id", "title", "delete_on", "user_id"]
    form_columns: typing.ClassVar = ["title", "delete_on", "user_id"]


class TasksView(MyModelView):
    column_hide_backrefs = False
    column_list = ("id", "title", "description", "status", "created_on", "dead_line",
                   "user", "category_id", "delete_on", "parent_id", "done_on")
    form_columns: typing.ClassVar = ["title", "description", "user_id", "status", "dead_line",
                                     "category_id", "delete_on", "parent_id", "done_on"]


admin_ext.add_view(TasksView(Tasks, db.session))
admin_ext.add_view(UsersView(Users, db.session))
admin_ext.add_view(CategoryView(Category, db.session))
