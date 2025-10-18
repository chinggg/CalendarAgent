# A Simple Google Calendar Agent

This project implements a simple LLM-based agent that assists with scheduling events in your Google Calendar. The agent is capable of engaging in conversation, and should automatically schedule events when prompted.

## Features

*   **Conversational Interface**: Interact with the agent in natural language.
*   **Automatic Event Scheduling**: The agent can schedule events in your Google Calendar based on your requests.
*   **Google Gemini Integration**: The agent uses the Google Gemini LLM to understand and process user requests.

## Getting Started

### Prerequisites

*   Python 3.7+
*   Google Cloud Platform project with the Google Calendar API enabled
*   OAuth 2.0 Client ID for the Google Calendar API
*   Google Gemini API Key

### Installation

1.  Clone the repository
2.  Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up your credentials
    *   Place your Google Calendar API `credentials.json` file in the root of the project.
    *   Set your Google Gemini API key as an environment variable:
        ```bash
        export GEMINI_API_KEY="your-api-key"
        ```

### Usage

Run the agent:

```bash
python src/main.py
```

Then, you can start a conversation in terminal with the agent to schedule events in your Google Calendar.

A useful scenario would be delete events in batch. For example:

```
Delete all events in primary calendar from 2026-01-01 to 2026-04-01 that are not "Fuzzing Collaboration (Monthly)"
```