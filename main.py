import os 
from dotenv import load_dotenv
# from google import genai
import google.generativeai as genai
from google.generativeai import types # Keep this for GenerateContentConfig
import sys
from functions.get_files_info import schema_get_files_info, handle_function_calls, available_functions
from config import system_prompt

# print(sys.argv)



# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Import genai library to create a new instance of the Gemini API client
genai.configure(api_key=api_key)

# Define the model you want to use
model_name = "gemini-1.5-flash" # A common and capable model



# Update code to accept a command line argument for the prompt, if prompt not provided, print error message and exit program with exit code 1
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command line argument.")
    sys.exit(1)

# Extract the user prompt from command line arguments, excluding any flags (arguments starting with '--')
prompt_args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
user_prompt = " ".join(prompt_args)

# if user_prompt is only flag arguments, print error message and exit program with exit code 1
if not user_prompt.strip():
    print("Error: Please provide a valid prompt.")
    sys.exit(1)


# create new list of types.Content and set the only message as the user's prompt'
messages = [user_prompt]

# Replace your client creation and response generation with:
model = genai.GenerativeModel(
    model_name=model_name,
    system_instruction=system_prompt
)

# Temp comment out the actual API call to avoid making a real request
response = model.generate_content(
    user_prompt,  # or whatever variable holds your prompt
    tools=[available_functions],
)

# Mock response for testing 
"""
class MockResponse:
    def __init__(self):
        self.text = "I'M JUST A ROBOT"

response = MockResponse()
"""


# Print the generated content
handle_function_calls(response)

# If verbose flag is present, print the user prompt and number of tokens used
if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    # Print number of tokens used
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")








