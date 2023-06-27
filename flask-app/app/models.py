from . import db, DB_ENGINE 
from sqlalchemy.sql import func
from sqlalchemy import event
import random, string
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Create the SQLite engine
db_engine = create_engine(DB_ENGINE)

def get_random_string(length=5):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generate_unique_token():
    rand_str = get_random_string()
    # # possibility of same random number is very low.
    # # but if you want to make sure, here you can check id exists in database.
    # db_session_maker = sessionmaker(bind=db_engine)
    # db_session = db_session_maker()
    # while db_session.query(OrderInfo).filter(token == rand_str).limit(1).first() is not None:
    #     rand_str = get_random_string()
    return rand_str

class MenuItems(db.Model):
    c_id= db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    cuisine_name = db.Column(db.String, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False, default=0.0)
    discount_per = db.Column(db.Integer, nullable=False, default=1) 


class OrderInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String,  default=generate_unique_token, unique=True)
    full_name = db.Column(db.String(50))
    contact_number = db.Column(db.String(15))
    address = db.Column(db.String(30))
    comments = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(15), default="pending")
    reg_date = db.Column(db.DateTime(timezone=True), default=func.now())
    order_item = db.relationship('OrderItem', cascade='all, delete-orphan', backref='order_info')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_info.id'))
    item = db.Column(db.String(50))
    quantity = db.Column(db.Integer)

if __name__ == "__main__":
    print(generate_unique_token())