# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionHelloWorld(Action):


    def name(self) -> Text:
         return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!, this is the first custom action you built")

         return []


class ActionCoronaStateTracker(Action):

    def name(self) -> Text:
        return "action_corona_state_tracker"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         response = requests.get("https://api.covid19india.org/data.json").json()

         entities = tracker.latest_message["entities"]
         print("Last message",entities)

         state = None

         for e in entities:
             if e["entity"] == "state":
                 state = e["value"]

         message = "Kindly enter the correct state name"

         if state == "india":
             state = "Total"

         for data in response["statewise"]:
             if data["state"] == state.title():
                 print(data)
                 message = "Active Cases: "+data["active"] + " Confirmed Cases: "+data["confirmed"] + " Recovered Cases: "+ data["recovered"] + " Deaths: "+data["deaths"] + " last updated on: "+data["lastupdatedtime"]


         print(message)
         dispatcher.utter_message(text=message)

         return []

class ActionCoronadistrictTracker(Action):

    def name(self) -> Text:
        return "action_corona_district_tracker"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         response = requests.get("https://api.covid19india.org/state_district_wise.json").json()

         entities = tracker.latest_message["entities"]
         print("Last message",entities)

         district = None

         for e in entities:
             if e["entity"] == "district":
                 district = e["value"]

         message = "Kindly enter the correct district name"

         if district == "india":
             district = "Total"

         for data in response["districtwise"]:
             if data["district"] == district.title():
                 print(data)
                 message = "Active Cases: "+data["active"] + " Confirmed Cases: "+data["confirmed"] + " Recovered Cases: "+ data["recovered"] + " Deceased: "+data["deceased"] + " last updated on: "+data["lastupdatedtime"]


         print(message)
         dispatcher.utter_message(text=message)

         return [] 



