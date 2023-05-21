from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = "database.db"
BASE_DIR = "."

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this is my secret key'
    print(os.path.join(BASE_DIR, DB_NAME))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, DB_NAME)}'
    db.init_app(app)

    from .order_views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import OrderInfo, OrderItem
    # create db
    with app.app_context():
        db.create_all()
        print("database is created")


    return app

