from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
import base64
import requests
import json
import os
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG")

base_URL = os.getenv("base_URL")

class ActionShowMenu(Action):
    def name(self) -> Text:
        return "action_show_menu"

    @staticmethod
    def fetch_menu():
        endpoint_API = f'{base_URL}/get_menu'
        menu_img = requests.get(endpoint_API)
        return menu_img  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cuisine_type = next(tracker.get_latest_entity_values("cuisine_type"), None)

        if cuisine_type == 'veg':
            output_msg = "veg list"
        elif cuisine_type == "non-veg":
            output_msg = "non veg list"
        else:
            output_msg = "general menu image"
            # response = self.fetch_menu()

        dispatcher.utter_message(text=output_msg, image='http://localhost:5000/get_menu')
        
        return []
    

class ActionExtractOrder(Action):
    def name(self) -> Text:
        return "action_extract_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extracting quantities and cuisines from entities
        entities = tracker.latest_message["entities"]
        orders = tracker.get_slot("orders") or []
        quantity = 1

        for entity in entities:
            if entity["entity"] == "quantity":
                quantity = entity["value"]
            elif entity["entity"] == "cuisine":
                cuisine = entity["value"]
                orders.append({"quantity": quantity, "cuisine": cuisine})
                quantity = 1
        
        return [SlotSet("orders", orders)]

class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_form"

    @staticmethod
    def cuisine_db() -> List[Text]:
        """Database of supported cuisines"""
        return ["chicken tikka", "pizza"]
    
    @staticmethod
    def clean_name(name):
        name = ' '.join(name.title().split())
        return  ''.join([c for c in name if c.isalpha() or c == ' '])


    def validate_orders(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        validated_orders = []
        print("validate slot value: ", slot_value)

        for order in slot_value:
            if order['cuisine'] in self.cuisine_db():
                validated_orders.append(order)
        
        if validated_orders:
            # dispatcher.utter_message(text=f"validated_orders: {validated_orders}")
            logging.debug("validated orders: ",validated_orders)
            return {"orders": validated_orders}
        
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="invalid order!! please make the order with a valid cuisine")
            return {"orders": None}

    def validate_full_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        clean_name = self.clean_name(slot_value)

        if len(clean_name) > 5:
            return {"full_name": clean_name}
        else:
            dispatcher.utter_message(text="invalid full name, please re-enter your name")
            return {"full_name": None}


class ActionShowOrderDetail(Action):
    def name(self) -> Text:
        return "action_show_order_detail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extracting quantities and cuisines from entities
        slots = tracker.slots
       
        name = slots["full_name"]
        contact_number = slots["contact_number"]
        delivery_address = slots['delivery_address']
        comments = slots["comments"]
        order_info = ""

        for order in slots['orders']:
            order_info += "Cuisine: {0} | quantity: {1} \n".format(order['cuisine'], order['quantity'])

        display_msg = f"Your order details:\n\
                        Name: {name}\n\
                        Contact number: {contact_number}\n\
                        Delivery_address: {delivery_address}\n\
                        order: {order_info}"
        
        dispatcher.utter_message(text=display_msg)
        dispatcher.utter_message(text=f"Comments: {comments}")
        dispatcher.utter_message(text= "Do you want to confirm your order?")
        return []


class ActionSubmitOrderDetail(Action):
    def name(self) -> Text:
        return "action_submit_order"

    @staticmethod
    def save_order(order_info):
        endpoint_API = f'{base_URL}/insert_order'  # Replace with the actual URL of your Flask API endpoint
        response = requests.post(endpoint_API, json=order_info)
        return  response
    
    @staticmethod
    def generate_invoice(token):
        endpoint_API = f"{base_URL}/gen_invoice"
        response = requests.get(endpoint_API, params={"token": token})
        return response
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # save order
        response = self.save_order(tracker.slots)
        # logging.debug("#response:", response)
        if response.status_code == 200:
            data = json.loads(response.text)
            token = data["token"]
            dispatcher.utter_message(text="order has been succssfully saved, your  order token: {}".format(token))
            print("token", data["token"])
            # response_2 = self.generate_invoice(token)

            # if response_2.status_code == 200:
            #     data = json.loads(response_2.text)
        
            #     # dispatcher.utter_message(text="click the link to download the invoice \n{}".format(data["link"]))
            #     pdf_base64 = base64.b64encode(data).decode("utf-8")

            #     # Construct the message payload
            #     message = {
            #         "attachment": {
            #             "payload": pdf_base64,
            #             "type": "application/pdf"
            #         }
            #     }

                # dispatcher.utter_message(text="Here is the order invoice: ", json_message=message)
            # dispatcher.utter_message(text="Visit the link to download the pdf", attachement=f'http://localhost:5000/gen_invoice?token={token}')
            dispatcher.utter_message(text=f"Visit the link to download the pdf: http://localhost:5000/gen_invoice?token={token}")


            return [SlotSet("orders", []), SlotSet("token", token)]
        
        return [SlotSet("orders", [])]
