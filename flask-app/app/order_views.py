from flask import (Blueprint, render_template, request, 
                   flash, jsonify, redirect, url_for)
from . import db
from .models import OrderInfo, OrderItem
import os

views = Blueprint('order_views', __name__)

RASA_SERVER_URL = os.getenv("RASA_SERVER_URL")

@views.route("/chat")
def chatroom():
    return render_template("chatroom.html", RASA_SERVER_URL=RASA_SERVER_URL)

@views.route("/")
def show_orders():
    order_infos = OrderInfo.query.all()
    return render_template("order.html", orders=order_infos)


@views.route("/fetch_order_items")
def fetch_order_by_id():
    order_items = OrderItem.query.filter_by(order_id = int(request.args.get('order_id'))).all()
    # query_order = [order for order in orders if order["id"] == )]
    print(order_items)

    response = [{
        "item": order_item.item,
        "quantity": order_item.quantity
    } for order_item in order_items]

    print(response)
    return jsonify(data=response)


@views.route("/update_order_status", methods=['POST'])
def update_order_status():
    print("order_id: ",request.form["order_id"] , "status:", request.form["new_status"] )
    order_id = request.form["order_id"]
    new_status = request.form["new_status"]
    
    if new_status not in ["pending", "delivering", "delivered"]:
        return {"status_code": 200, "message": "invalid new status option" }
    
    order_info = OrderInfo.query.get(order_id)
    order_info.status = new_status
    db.session.commit()

    # flash("status changed successfully", category="success")
    return {"status_code": 200, "message": "status has been changed successfully"}


@views.route("/insert_order", methods=["POST"])
def insert_order():
    print("=========", request.remote_addr)
    order_info = request.json
    name = order_info["full_name"]
    contact = order_info["contact_number"]
    address = order_info["delivery_address"]
    comment = order_info["comments"]

    order = OrderInfo(full_name=name,
                            contact_number=contact,
                            address=address,
                            comments=comment)
    db.session.add(order)
    db.session.commit()

    for order_item in order_info["orders"]:
        db.session.add(OrderItem(
            order_id= order.id,
            item= order_item["cuisine"],
            quantity=order_item["quantity"]
        ))
    
    db.session.commit()

    return jsonify({"order_id": order.id})


@views.route("/delete_order/<int:id>", methods=["GET"])
def delete_order(id):
    # Retrieve the object you want to delete
    order= OrderInfo.query.get(id)
    # Delete the object from order_info table
    db.session.delete(order)
    # Commit the changes
    db.session.commit()
    # Delete correspondig items
    return redirect(url_for("order_views.show_orders"))
