import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
import sys
import google.generativeai as genai
# ...rest as needed
from functions.get_files_info import schema_get_files_info, handle_function_calls, available_functions, call_function
from config import system_prompt

# print(sys.argv)

# define working_directory as the current working directory
working_directory = os.getcwd()



# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Import genai library to create a new instance of the Gemini API client
genai.configure(api_key=api_key)



if __name__ == "__main__":

    # init is_verbose boolean variable
    is_verbose = "--verbose" in sys.argv
        # Your prompt-argument checks and agent logic go here


        # if len(sys.argv) == 1: skip the prompt argument check and run the script and return
    if len(sys.argv) == 1:
        print("No prompt provided. Running default agent behavior.")
        sys.exit(0)

    elif len(sys.argv) != 1:
        # Extract the user prompt from command line arguments, excluding any flags (arguments starting with '--')
        prompt_args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
        user_prompt = " ".join(prompt_args)
        # if user_prompt is only flag arguments, print error message and exit program with exit code 1
        if not user_prompt.strip():
            print("Error: Please provide a valid prompt.")
            sys.exit(1)
            

        # Define the model you want to use
    model_name = "gemini-2.5-flash" # A common and capable model





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
    result = handle_function_calls(response, is_verbose)

    # print result.parts[0].function_response.response if result and verbose flag is present
    if result and is_verbose:
        if hasattr(result, 'parts'):
                        # Object format
            if result.parts and result.parts[0].function_response:
                 print(f"-> {result.parts[0].function_response.response}")
                
                
        elif isinstance(result, dict) and 'parts' in result:
            if (result['parts'] and 
                len(result['parts']) > 0 and 
                'function_response' in result['parts'][0] and
                'response' in result['parts'][0]['function_response']):
                print(f"-> {result['parts'][0]['function_response']['response']}")
    

    # If verbose flag is present, print the user prompt and number of tokens used
    """if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        # Print number of tokens used
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")"""







