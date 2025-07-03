import re

class NaturalLanguageService:
    def __init__(self, model):
        self.model = model

    def extract_event_details(self, text):
        # Use the Gemini API to extract event details
        response = self.model.generate_content(
            f"Extract the event details from the following text: {text}"
            f"\n\nReturn the details in the following format:"
            f"\nsummary: [event summary]"
            f"\nstart_time: [event start time in ISO 8601 format]"
            f"\nend_time: [event end time in ISO 8601 format]"
        )

        # Parse the response to extract the event details
        event_details = {}
        for line in response.text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                event_details[key.strip()] = value.strip()

        return event_details
