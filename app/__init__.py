from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from app.extansions import db
from app.models import Category, Tasks, Users

admin_ext = Admin(template_mode="bootstrap3")
migrate_ext = Migrate()
load_dotenv()


def create_app():
    new_app = Flask(__name__)
    new_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    db.init_app(new_app)
    migrate_ext.init_app(new_app, db)
    admin_ext.init_app(new_app)

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
    column_display_all_relations = True
    column_hide_backrefs = False


admin_ext.add_view(MyModelView(Tasks, db.session))
admin_ext.add_view(MyModelView(Users, db.session))
admin_ext.add_view(MyModelView(Category, db.session))
