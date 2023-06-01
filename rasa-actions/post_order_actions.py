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

        buttons = [{"title": "order food", "payload":"/browse_menu"},
                   {"title":"check status", "payload":"/ask_order_status"}]
    
        if response.status_code == 404:
            message = "sorry, no data found. It seems you have entered invalid token: {}".format(tracker.slots['token'])
        elif response.status_code == 200:
            message = f"Order status: {response.text}"
        else:
            message = "server error 💀"
        
        dispatcher.utter_message(text=message, buttons=buttons)

        prev_token = tracker.get_slot("token")

        return [SlotSet("token", None), SlotSet("prev_token", prev_token)]
        

class ActionAskToken(Action):
    def name(self) -> Text:
        return "action_ask_token"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        prev_token = tracker.get_slot("prev_token")
        buttons = None
        if prev_token:
            buttons = [{"title": "Prev token " + prev_token, "payload": prev_token}]
            
        dispatcher.utter_message(text="please! enter the token to check the status ",
                                 buttons= buttons)
   
        return []