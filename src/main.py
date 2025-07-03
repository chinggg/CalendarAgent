from dotenv import load_dotenv
from agent import CalendarAgent

load_dotenv()

def main():
    agent = CalendarAgent()

    print("Hello! I'm your Google Calendar assistant. How can I help you today?")

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = agent.process_request(user_input)
        print(response)

if __name__ == '__main__':
    main()
