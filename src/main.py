import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google.generativeai as genai
from dotenv import load_dotenv

from services.calendar_service import CalendarService
from services.natural_language_service import NaturalLanguageService

load_dotenv()

def main():
    # Set up Google Calendar API
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', ['https://www.googleapis.com/auth/calendar.events'])
    creds = flow.run_local_server(port=0)
    service = build('calendar', 'v3', credentials=creds)

    calendar_service = CalendarService(service)

    # Set up Google Gemini API
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel('gemini-2.5-flash')

    natural_language_service = NaturalLanguageService(model)

    print("Hello! I'm your Google Calendar assistant. How can I help you today?")

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        event_details = natural_language_service.extract_event_details(user_input)

        if event_details:
            calendar_service.create_event(event_details)
            print("Event created successfully!")
        else:
            print("I'm sorry, I didn't understand that. Could you please rephrase?")

if __name__ == '__main__':
    main()
