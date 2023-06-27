from flask import (Blueprint, render_template, request, 
                   flash, jsonify, redirect, url_for, send_file)
from . import db
from .models import OrderInfo, OrderItem, MenuItems
import os
from .invoice_generator import Invoice, generate_pdf


views = Blueprint('order_views', __name__)

RASA_SERVER_URL = os.getenv("RASA_SERVER_URL")

@views.route("/chat")
def chatroom():
    # url = "https://af34-103-232-154-60.ngrok-free.app/rasa_server/api"
    return render_template("chatroom.html", RASA_SERVER_URL=RASA_SERVER_URL)
    # return render_template("chatroom.html", RASA_SERVER_URL=url)

@views.route("/")
def show_orders():
    order_infos = OrderInfo.query.all()
    return render_template("order.html", orders=order_infos)


@views.route("/fetch_order_items")
def fetch_order_by_id():
    order_items = OrderItem.query.filter_by(order_id = int(request.args.get('order_id'))).all()
    response = [{
        "item": order_item.item,
        "quantity": order_item.quantity
    } for order_item in order_items]

    print(response)
    return jsonify(data=response)


@views.route("/update_order_status", methods=['POST'])
def update_order_status():
    print("order_id: ",request.form["order_token"] , "status:", request.form["new_status"] )
    order_token = request.form["order_token"]
    new_status = request.form["new_status"]
    print("#order token", order_token)
    if new_status not in ["pending", "delivering", "delivered", "cancelled"]:
        return jsonify({"message": "invalid new status option" }), 404
    
    order_info = OrderInfo.query.filter_by(token=order_token).first()
    
    if not order_info:
        return jsonify({"message": "Invalid token"}), 404
    elif order_info.status != "pending" and new_status == "cancelled":
        return jsonify({"message": "Cannot change non pending status"}), 405

    order_info.status = new_status
    db.session.commit()
    # flash("status changed successfully", category="success")
    return jsonify({"message": "status has been changed successfully"})
    


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

    return jsonify({"token": order.token})


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


@views.route("/get_order_status", methods=['GET'])
def get_order_status():
    token = request.args.get("token")
    order = OrderInfo.query.filter_by(token=token).first()
    if not order:
        return jsonify({"message": "token doesnot exist"}), 404
    
    return order.status


@views.route("/get_menu", methods=['GET'])
def get_menu():
    menu_file = "./static/images/menu.jpg"
    return send_file(menu_file, mimetype="image/jpeg")


@views.route("/gen_invoice", methods=['GET'])
def gen_invoice():
    token = request.args.get("token")
    order_info = OrderInfo.query.filter_by(token=token).first()
    if not order_info:
        return jsonify({"message": "token doesnot exist"}), 404
    
    invoice = Invoice(order_info.full_name,
                      order_info.contact_number,
                      order_info.token,
                      str(order_info.reg_date),
                      order_info.address)
    
    order_items = OrderItem.query.filter_by(order_id = order_info.id).all()
    menu_items = {
            item.cuisine_name.lower(): {
                    "rate": item.rate,
                    "category": item.category,
                    "discount": item.discount,
                    "discount_per": item.discount_per
                } for item in MenuItems.query.all()
            }
    
    for order_item in order_items:
        menu_item = menu_items[order_item.item.lower()]
        invoice.add_cuisine(
                    order_item.item,
                    order_item.quantity,
                    menu_item["rate"],
                    menu_item["discount"],
                    menu_item["discount_per"]
                )

    flag = generate_pdf(invoice)

    invoice_file_name = "../gen-invoice-pdfs/invoice_{}.pdf".format(token)
    # return jsonify({"link": invoice_file_name})
    return send_file(invoice_file_name, mimetype="application/pdf")


# @views.route("/get_invoice", methods=["GET"])
# def get_invoice():
#     token = request.args.get("token")
#     invoice_file_name = "./gen-invoice-pdfs/invoice_{}.pdf".format(token)

    