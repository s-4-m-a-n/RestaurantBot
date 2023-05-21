from . import db 
from sqlalchemy.sql import func
from sqlalchemy import event

class OrderInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    contact_number = db.Column(db.String(15))
    address = db.Column(db.String(30))
    comments = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(15), default="pending")
    reg_date = db.Column(db.DateTime(timezone=True), default=func.now())
    order_item = db.relationship('OrderItem', cascade='all, delete-orphan', backref='order_info')

# @event.listens_for(OrderInfo, 'before_insert')
# def set_auto_incrementing_id(mapper, connection, target):
#     query = db.session.query(OrderInfo)
#     max_id = query.order_by(OrderInfo.id.desc()).first()
#     if max_id is None:
#         target.id = 100
#     else:
        # target.id = max_id.id + 1


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_info.id'))
    item = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
