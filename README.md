# LangGraph Medium Article Analyzer Agent

This project implements a text analysis agent using LangGraph, as described in the Data Science Collective article "The Complete Guide to Building Your First AI Agent with LangGraph."

The agent can:
1.  Classify a given text into predefined categories (News, Blog, Research, Other).
2.  Extract named entities (Person, Organization, Location) from the text.
3.  Generate a concise summary of the text.

## Project Structure

```
ai_agent_project/
├── agent_env/              # Virtual environment directory
├── .env                    # For API keys and environment variables
├── agent.py                # Main script for the agent
├── requirements.txt        # Python dependencies
├── test_setup.py           # Script to test environment setup
└── README.md               # This file
```

## Setup Instructions

Follow these steps to set up and run the agent on your local machine.

### 1. Create Project Directory
Open your terminal or command prompt and run:
```bash
mkdir ai_agent_project
cd ai_agent_project
```
*(This script handles this step if you run it in the desired parent directory)*

### 2. Create and Activate Virtual Environment

* **On macOS/Linux:**
    ```bash
    python3 -m venv agent_env
    source agent_env/bin/activate
    ```
* **On Windows:**
    ```bash
    python -m venv agent_env
    .\agent_env\Scripts\activate
    ```
    *(If `python3` or `python` doesn't work, ensure Python is installed and added to your system's PATH.)*
*(This script handles creation and activation for Unix-like systems)*

### 3. Install Necessary Packages
With your virtual environment activated, install the required libraries:
```bash
pip install -r requirements.txt
```
*(This script handles this step)*

### 4. Create `requirements.txt`
Create a file named `requirements.txt` in your `ai_agent_project` directory and add the content:
```text
langgraph
langchain
langchain-openai
python-dotenv
```
*(This script handles this step)*

### 5. Set Up OpenAI API Key

* Create a file named `.env` in the `ai_agent_project` directory.
* Add your OpenAI API key to this file:
    ```
    OPENAI_API_KEY=your-actual-openai-api-key-here
    ```
    Replace `your-actual-openai-api-key-here` with your real OpenAI API key.
*(This script creates a template .env file. You MUST edit it.)*

### 6. Create `test_setup.py`
Create a file named `test_setup.py` in your `ai_agent_project` directory with the provided test script content.
*(This script handles this step)*

### 7. Test Your Environment Setup
Run the test script to ensure your environment and API key are configured correctly:
```bash
python test_setup.py
```
If you see a response from the LLM (e.g., "Hello! I am working."), your setup is correct. **Remember to edit the `.env` file with your API key first!**

### 8. Create `agent.py`
Create a file named `agent.py` in your `ai_agent_project` directory with the provided agent script content.
*(This script handles this step)*

## Running the Agent

Once everything is set up AND you have edited the `.env` file with your API key, you can run the agent:

1.  Ensure your virtual environment (`agent_env`) is activated.
    ```bash
    # If not active:
    # On macOS/Linux:
    # source agent_env/bin/activate
    # On Windows:
    # .\agent_env\Scripts\activate
    ```
2.  Run the test script first (after editing `.env`):
    ```bash
    python test_setup.py
    ```
3.  If the test is successful, run the main agent script:
    ```bash
    python agent.py
    ```

The script will output the classification, extracted entities, and summary for the sample text. You can modify the `sample_text` variable in `agent.py` to analyze different articles.

## Deactivating the Virtual Environment
When you're done working on the project, you can deactivate the virtual environment:
```bash
deactivate
```
