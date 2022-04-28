from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_share import Share

db = SQLAlchemy()

share = Share()

def create_app():
    application = app = Flask(__name__)
    app.config['SECRET_KEY'] = "RMIT"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@database-1.c6zd8f2bmusl.us-east-1.rds.amazonaws.com:3306/flaskdatabase'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like

    create_database(app)

    share.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
     db.create_all(app=app)
