from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from fuzzywuzzy import process

class ActionProvideSolution(Action):

    def name(self) -> Text:
        return "action_provide_solution"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        issue = tracker.get_slot('issue')
        
        # Convert issue to lowercase for matching
        issue = issue.lower() if issue else "unknown"
        
        # Define possible causes and parts, with keys in lowercase
        issue_causes = {
            "television not starting": ["Power supply issue", "Faulty door switch", "Motor failure"],
            "tv has sound but no picture": ["Faulty water inlet valve", "clogged filter"],
            "multiple vertical lines run across the screen": ["Broken belt", "Faulty Motor", "Faulty lid switch"],
            "tv has a picture, but no sound": ["Blocked drain hose", "Faulty drain pump"],
            "tv flickers and turns off suddenly": ["Unbalanced load", "Worn out bearings"],
            "the picture is unnaturally long or squeezed": ["Faulty door latch", "Control board issue"],
            "half the screen is grayed out": ["Loose hose connections", "Faulty door seal"],
            "the remote control isn’t working properly": ["Faulty heating element", "Thermostat issue"],
            "tv won’t power up but the power light blinks": ["Faulty water level switch", "Blocked drain hose"],
            "image is breaking up or pixelating.": ["Mold or mildew buildup", "Clogged drain pump"],
            "the screen of the tv is grainy.": ["Various sensor issues", "Faulty control board"]
        }
        
        issue_parts = {
            "television not starting": ("door switch or motor", "700 - 1,300 INR"),
            "tv has sound but no picture": ("water inlet valve", "1,000 - 2,500 INR"),
            "multiple vertical lines run across the screen": ("belt or motor", "3,400 - 8,000 INR"),
            "tv has a picture, but no sound": ("drain pump", "2,500 - 4,500 INR"),
            "tv flickers and turns off suddenly": ("bearings", "1,800 - 4,500 INR"),
            "the picture is unnaturally long or squeezed": ("door latch", "1,000 - 2,200 INR"),
            "half the screen is grayed out": ("door seal", "900 - 2,300 INR"),
            "the remote control isn’t working properly": ("heating element", "2,500 - 6,500 INR"),
            "tv won’t power up but the power light blinks": ("water level sensors", "1,100 - 2,800 INR"),
            "image is breaking up or pixelating.": ("drain pump", "300 - 800 INR"),
            "the screen of the tv is grainy.": ("various parts", "4,500 - 10,000 INR")
        }
        
        # Define synonyms for issues to enhance matching
        synonyms = {
            "television not starting": ["tv not starting", "television won't start", "tv won't start", "television is not working", "tv is not working"],
            "tv has sound but no picture": ["television has sound but no picture", "tv sound no picture", "television sound no picture"],
            "multiple vertical lines run across the screen": ["tv vertical lines", "television vertical lines", "tv screen lines", "television screen lines"],
            "tv has a picture, but no sound": ["television has a picture but no sound", "tv picture no sound", "television picture no sound"],
            "tv flickers and turns off suddenly": ["television flickers and turns off", "tv flickers and shuts off", "television flickers and shuts off"],
            "the picture is unnaturally long or squeezed": ["tv picture stretched", "television picture stretched", "tv picture squeezed", "television picture squeezed"],
            "half the screen is grayed out": ["tv screen half gray", "television screen half gray", "tv screen half grey", "television screen half grey"],
            "the remote control isn’t working properly": ["tv remote not working", "television remote not working", "tv remote broken", "television remote broken"],
            "tv won’t power up but the power light blinks": ["television won't power up", "tv won't turn on", "television won't turn on", "tv power light blinks", "television power light blinks"],
            "image is breaking up or pixelating.": ["tv image pixelated", "television image pixelated", "tv image breaking up", "television image breaking up"],
            "the screen of the tv is grainy.": ["tv screen grainy", "television screen grainy", "tv screen static", "television screen static"]
        }

        # Flatten the synonyms dictionary for easier fuzzy matching
        issue_synonyms = {synonym: key for key, synonyms_list in synonyms.items() for synonym in synonyms_list}
        
        # Fuzzy match the issue to find the closest key in issue_synonyms
        matched_issue, confidence = process.extractOne(issue, issue_synonyms.keys())
        
        # Debugging output
        print(f"Issue provided: {issue}")
        print(f"Matched issue: {matched_issue}")
        print(f"Confidence score: {confidence}")
        
        if confidence < 70:
            matched_issue = "unknown"
        else:
            matched_issue = issue_synonyms.get(matched_issue, "unknown")
        
        causes = issue_causes.get(matched_issue, ["Unknown cause"])
        issue_part, cost_estimate = issue_parts.get(matched_issue, ("parts", "1,000 - 2,500 INR"))
        
        dispatcher.utter_message(text=f"The possible causes for {matched_issue} could be: {', '.join(causes)}")
        dispatcher.utter_message(text=f"The estimated cost for repairing or replacing {issue_part} is approximately {cost_estimate}.")
        dispatcher.utter_message(text="Would you like to book a ticket with us?")
        
        return []

class ActionBookTicket(Action):

    def name(self) -> Text:
        return "action_book_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Thank you for booking a ticket with us!")
        
        return []

class ActionDenyBooking(Action):

    def name(self) -> Text:
        return "action_deny_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="No problem! If you need any further assistance, feel free to ask.")
        
        return []
