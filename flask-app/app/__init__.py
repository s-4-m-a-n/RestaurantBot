from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = "database.db"
BASE_DIR = "."
DB_ENGINE = f'sqlite:///{os.path.join(BASE_DIR, DB_NAME)}'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this is my secret key'
    print(os.path.join(BASE_DIR, DB_NAME))
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_ENGINE
    db.init_app(app)

    from .order_views import views
    from .menu_views import menu

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(menu, url_prefix='/menu')


    from .models import OrderInfo, OrderItem, MenuItems
    # create db
    with app.app_context():
        db.create_all()
        print("database is created")


    return app

