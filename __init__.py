from flask import Flask, current_app,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from os import path
from flask_login import LoginManager, current_user


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'opesdjnfopwjfgopjweqg sdpgfjnpoajgosajoj'
    username = "sa"
    password = "indocyber"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://"+username+":"+password+"@LAPTOP-0K3QVKUD/PyKuis?driver=ODBC+Driver+17+for+SQL+Server"

    db.init_app(app)

    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_User(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    err_hendler(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    
    from .models import User, SkorUser, Question

    create_database(app)

    return app


def create_database(app):
    if not path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
        with app.app_context():
            db.create_all()
        print("Database created successfully.")
    else:
        print("Database already exists.")


def err_hendler(app):
    @app.errorhandler(404)
    def invalid_route(e):
        user = getattr(current_user, 'nickname', None)
        return render_template("404.html.jinja",user=user)

    @app.errorhandler(500)
    def internal_server_error(e):
        user = getattr(current_user, 'nickname', None)
        return render_template("500.html.jinja",user=user)

