import os
from datetime import datetime
import tzlocal
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_community.calendar.toolkit import CalendarToolkit
from langchain_google_community.calendar.utils import (
    build_resource_service,
    get_google_credentials,
)

class CalendarAgent:
    def __init__(self, model: str='gemini-2.5-flash'):
        # Set up Google Calendar API
        credentials = get_google_credentials(
            token_file="token.json",
            scopes=["https://www.googleapis.com/auth/calendar"],
            client_secrets_file="credentials.json",
        )

        api_resource = build_resource_service(credentials=credentials)
        toolkit = CalendarToolkit(api_resource=api_resource)
        tools = toolkit.get_tools()

        # Configure Gemini API key
        genai_api_key = os.environ.get('GEMINI_API_KEY')
        if not genai_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        llm = ChatGoogleGenerativeAI(model=model, google_api_key=genai_api_key)
        
        current_time_str = datetime.now().strftime('%Y-%m-%d %A %H:%M:%S')

        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a helpful assistant for managing a user's Google Calendar. "
                "You have access to a toolkit that can create, search, update, and delete calendar events. "
                "When a user asks about their schedule (e.g., 'what am I doing today?', 'am I free tomorrow afternoon?'), use the available tools to check their calendar. "
                "Based on their schedule, you can suggest available times for new events. "
                "When creating or updating an event, your goal is to gather all necessary information (summary, start time, end time, and optionally description, location, etc.) from the user. "
                f"The current date and time is {current_time_str} in timezone {tzlocal.get_localzone_name()}. Use this as a reference for relative dates. "
                f"Use primary calendar and its default timezone if not specified."
                "Before executing a command that modifies the calendar (create, update, delete), you MUST confirm with the user. "
                "Engage in a natural conversation and ask for clarification if the user's request is ambiguous. "
            )),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        agent = create_tool_calling_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        self.chat_history = []

    def process_request(self, user_input):
        max_retries = 2
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                response = self.agent_executor.invoke({
                    "input": user_input,
                    "chat_history": self.chat_history
                })
                
                self.chat_history.extend([
                    HumanMessage(content=user_input),
                    AIMessage(content=response["output"]),
                ])
                return response["output"]
                
            except Exception as e:
                retry_count += 1
                error_message = str(e)
                
                if retry_count <= max_retries:
                    # Provide error feedback to help the agent self-correct
                    error_feedback = f"There was an error with the previous attempt: {error_message}. Please try a different approach or correct the issue."
                    
                    # Add error context to chat history for the retry
                    self.chat_history.extend([
                        HumanMessage(content=user_input),
                        AIMessage(content=f"I encountered an error: {error_message}. Let me try again with a corrected approach."),
                    ])
                    
                    # Modify input to include error context for retry
                    user_input = f"{user_input}\n\nPrevious error to avoid: {error_feedback}"
                else:
                    # Max retries reached, return error message
                    error_response = f"I apologize, but I encountered repeated errors while processing your request: {error_message}. Please try rephrasing your request or check if there are any issues with your calendar access."
                    
                    self.chat_history.extend([
                        HumanMessage(content=user_input),
                        AIMessage(content=error_response),
                    ])
                    return error_response