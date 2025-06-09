import os 
from dotenv import load_dotenv
from google import genai
import sys

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Import genai library to create a new instance of the Gemini API client
client = genai.Client(api_key=api_key)

# Generate content using the Gemini API client
response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
)

# Update code to accept a command line argument for the prompt, if prompt not provided, print error message and exit program with exit code 1
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command line argument.")
    sys.exit(1)
prompt = sys.argv[1]

# Print the generated content
print(response.text)

# Print number of tokens used
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

# Update code to accept a command line argument for the prompt, if prompt not provided, print error message and exit program with exit code 1
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command line argument.")
    sys.exit(1)
prompt = sys.argv[1]

