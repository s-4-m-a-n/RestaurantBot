from flask import (Blueprint, render_template, request, 
                   flash, jsonify, redirect, url_for, send_file)
from . import db
from .models import MenuItems
import os


menu = Blueprint('menu_views', __name__)

RASA_SERVER_URL = os.getenv("RASA_SERVER_URL")


@menu.route("/")
def show_menu_items():
    menu_items = MenuItems.query.all()
    return render_template("menu.html", menu_items=menu_items)


@menu.route("/insert_item", methods=["POST"])
def insert_menu_item():
    menu_item = request.form
    cuisine_name = menu_item["cuisine_name"]
    category = menu_item["category"]
    rate = float(menu_item["rate"])
    discount = float(menu_item["discount"])
    discount_per = int(menu_item["discount_per"])

    item = MenuItems(category=category,
                      cuisine_name=cuisine_name,
                      rate=rate,
                      discount=discount,
                      discount_per=discount_per)
    
    db.session.add(item)
    db.session.commit()

    return redirect(url_for("menu_views.show_menu_items"))

@menu.route("/delete_item/<int:id>", methods=["GET"])
def delete_item(id):
    # Retrieve the object you want to delete
    item= MenuItems.query.get(id)
    # Delete the object from order_info table
    db.session.delete(item)
    # Commit the changes
    db.session.commit()
    # Delete correspondig items
    return redirect(url_for("menu_views.show_menu_items"))

@menu.route("/get_all_cuisine_name", methods=["GET"])
def get_all_cuisine_name():
    menu_items = [name["cuisine_name"].lower() for name in MenuItems.query.with_entities(MenuItems.cuisine_name)]
    return menu_items

@menu.route("/get_all_menu_items", methods=["GET"])
def get_all_menu_items():
    menu_items =  [{
            "name": item.cuisine_name,
            "rate": item.rate,
            "category": item.category,
            "discount": item.discount,
            "discount_per": item.discount_per
        } for item in MenuItems.query.all()]

    return jsonify(data=menu_items)