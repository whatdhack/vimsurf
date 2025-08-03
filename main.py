import requests
import os
from dotenv import load_dotenv
from datetime import datetime


# Load environment variables (for security, store your API key/secret in .env)
load_dotenv()

# Replace with your Inworld API key and secret
headers = {
    "Authorization": f"Basic {os.getenv('INWORLD_API_KEY')}",
    "Content-Type": "application/json"
}

# Replace with the Model ID of the Inworld character you want to interact with
INWORLD_MODEL_ID = "tenstorrent/Llama-3.3-70B-Instruct" 

# Base URL for the Inworld LLM API
url = "https://api.inworld.ai/llm/v1alpha/completions:completeChat"

print("Welcome to the Inworld AI chatbot! Type 'exit' to end the conversation.")

def sessid():
    current_datetime = datetime.now()
    timestamp_string = current_datetime.strftime("%Y%m%d_%H%M%S")
    session_id = timestamp_string 
    return session_id

model_tt = "tenstorrent/Llama-3.3-70B-Instruct"
user_id = "sg1"
session_id = sessid()


def send_message_to_inworld(message, model_id=model_tt, user_id=user_id, session_id=session_id):
    """Sends a message to the Inworld API and returns the response."""
    data = {
        "servingId": {
            "modelId": {
                "model": model_id,
                "serviceProvider": "SERVICE_PROVIDER_TENSTORRENT" 
            },
            "userId": user_id,
            "sessionId": session_id
        },
        "responseFormat": "RESPONSE_FORMAT_UNSPECIFIED",
        "textGenerationConfig": {
            "maxTokens": 100
        },
        "messages": [
            {
                "role": "MESSAGE_ROLE_USER",
                "content": message
            }
        ]
    }
    
    # We are using Basic authentication for this example
    response = requests.post(
        url,
        headers=headers,
        json=data,
    )
    
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def file_content(file_path, ):
    """
    Reads a Python file's content and sends it to the Inworld ChatCompletion API.
    """
    try:
        with open(file_path, "r") as file:
            code = file.read()

        # You can format the message to provide context to the AI
        # user_message = f"Here is a Python script:\n```python\n{python_code}\n```\nWhat does this script do, and are there any potential issues or improvements?"

        return code

    except FileNotFoundError:
        print(f"Error: Python file not found at {file_path}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Inworld AI: {e}")
        return None

while True:
    user_input = input("You: ")
    if user_input.startswith("file=="):
       fname = user_input.split("=")[-1]
       file_content = file_content(fname)
       print (f"debug - file read")
       continue
    if user_input.lower() == 'exit':
        break
    final_input = f" With file {file_content} answer or do { user_input}"
    try:
        inworld_response = send_message_to_inworld(final_input, )
        # Extract the assistant's reply from the Inworld response
		# inworld_response["result"]['choices'][0]['message']['content']
        #for message in inworld_response["result"]['choices'][0]:
        message = inworld_response["result"]['choices'][0]['message']
        if message["role"] == "MESSAGE_ROLE_ASSISTANT":
                print(f"Inworld AI: {message['content']}")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Inworld AI: {e}")

print("Chat ended. Goodbye!")


