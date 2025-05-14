# test_setup.py
# Script to verify the Python environment and OpenAI API key setup.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
# This will look for a .env file in the current directory and load it.
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "your-actual-openai-api-key-here":
    print("Error: OPENAI_API_KEY not found or not set in .env file.")
    print("Please ensure you have a .env file in the project root (ai_agent_project directory)")
    print("and replace 'your-actual-openai-api-key-here' with your actual OpenAI API key.")
else:
    print("OpenAI API Key found in .env file.")
    try:
        # Initialize the ChatOpenAI instance
        # The article uses "gpt-4o-mini", ensure this model is available to your API key.
        llm = ChatOpenAI(model="gpt-4o-mini")

        # Test the setup by invoking the model
        print("Testing LLM connection...")
        response = llm.invoke("Hello! Are you working?")

        # Print the content of the response
        print("\nLLM Response:")
        print(response.content)
        print("\nSetup test successful! Your environment is ready.")

    except Exception as e:
        print(f"\nAn error occurred during the LLM test: {e}")
        print("Please check your API key, model availability (gpt-4o-mini), and internet connection.")
