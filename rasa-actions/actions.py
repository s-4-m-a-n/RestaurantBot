from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
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

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cuisine_type = next(tracker.get_latest_entity_values("cuisine_type"), None)

        if cuisine_type == 'veg':
            output_msg = "veg list"
        elif cuisine_type == "non-veg":
            output_msg = "non veg list"
        else:
            output_msg = "general menu"

        dispatcher.utter_message(text=output_msg)
        
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

        return ["chicken tikka"]
    
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
            dispatcher.utter_message(text="invalid order!! please make the order with valid cuisine")
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
                    order: {order_info}\n\
                    Comments: {comments}\n\
                    Do you want to confirm your order?"
        
        dispatcher.utter_message(text=display_msg)
        return []


class ActionSubmitOrderDetail(Action):
    def name(self) -> Text:
        return "action_submit_order"

    @staticmethod
    def save_order(order_info):
        endpoint_API = f'{base_URL}/insert_order'  # Replace with the actual URL of your Flask API endpoint
        response = requests.post(endpoint_API, json=order_info)
        return  response
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # save order
        response = self.save_order(tracker.slots)
        # logging.debug("#response:", response)
        if response.status_code == 200:
            data = json.loads(response.text)
            print("#data: ", data)
            dispatcher.utter_message(text="order has been succssfully saved, your  order token: {}".format(data["token"]))
  
        return [SlotSet("orders", [])]

class ActionShowOrderStatus(Action):
    def name(self) -> Text:
        return "action_show_order_status"
    
    @staticmethod
    def fetch_order_status(token):
        endpoint_API = f'{base_URL}/get_order_status'
        response = requests.get(endpoint_API, params={'token': token})
        logger.debug("token: {}".format(token))
        logger.debug(f" response: {response}")
        return response

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = self.fetch_order_status(tracker.slots['token'])
        logger.info(response)
        buttons = []

        buttons.append({"title": "order food", "payload":"/browse_menu"})
        buttons.append({"title":"check status", "payload":"/ask_order_status"})

    
        if response.status_code == 404:
            message = "sorry, no data found. It seems you have entered invalid token: {}".format(tracker.slots['token'])
        elif response.status_code == 200:
            message = f"Order status: {response.text}"
        else:
            message = "server error 💀"
        
        dispatcher.utter_message(text=message, buttons=buttons)
        return [SlotSet("token", None)]
        
