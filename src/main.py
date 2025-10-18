from dotenv import load_dotenv
from agent import CalendarAgent

load_dotenv()

def main():
    agent = CalendarAgent()

    print("Hello! I'm your Google Calendar assistant. How can I help you today?")

    while True:
        print("Enter input (Ctrl-D to end):")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        user_input = "\n".join(contents).strip()
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            break

        response = agent.process_request(user_input)
        print(response)

if __name__ == '__main__':
    main()
