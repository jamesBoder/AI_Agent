import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Import genai library to create a new instance of the Gemini API client
client = genai.Client(api_key=api_key)

# Update code to accept a command line argument for the prompt, if prompt not provided, print error message and exit program with exit code 1
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command line argument.")
    sys.exit(1)



prompt_args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
user_prompt = " ".join(prompt_args)

# if user_prompt is only flag arguments, print error message and exit program with exit code 1
if not user_prompt.strip():
    print("Error: Please provide a valid prompt.")
    sys.exit(1)


# create new list of types.Content and set the only message as the user's prompt'
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]



# Generate content using the Gemini API client
response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages,
)


# Print the generated content
print(response.text)

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    # Print number of tokens used
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")








