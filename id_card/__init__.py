"""
Application factory

Initialize application extensions, register blueprints and return the ready application instance
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect



db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    config_object.init_app()

    # TODO: initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # import and register blueprints
    from .student import student
    from .admin import admin
    app.register_blueprint(student)
    app.register_blueprint(admin)

    return app