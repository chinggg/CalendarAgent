class CalendarService:
    def __init__(self, service):
        self.service = service

    def create_event(self, event_details):
        event = {
            'summary': event_details['summary'],
            'start': {
                'dateTime': event_details['start_time'],
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': event_details['end_time'],
                'timeZone': 'America/Los_Angeles',
            },
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
