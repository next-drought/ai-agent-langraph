# agent.py
# Main script for the LangGraph Medium Article Analyzer Agent.

import os
from typing import TypedDict, List
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate # Updated import
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage # Updated import

# Load environment variables from .env file
load_dotenv()

# --- 1. Define the State for the Agent's Memory ---
class AgentState(TypedDict):
    """
    Represents the state of our LangGraph agent.
    It holds the original text and the results from each processing step.
    """
    text: str               # Stores the original input text
    classification: str     # Represents the classification result (e.g., category)
    entities: List[str]     # Holds a list of extracted entities (e.g., named entities)
    summary: str            # Stores a summarized version of the text

# --- 2. Initialize the Language Model ---
try:
    llm = ChatOllama(
        model="deepseek-r1:8b",  # Your DeepSeek model in Ollama
        temperature=0,
        base_url="http://localhost:11434"  # default Ollama URL
    )
    print("LLM initialized successfully with DeepSeek model from Ollama.")
except Exception as e:
    print(f"Error initializing Ollama LLM. Ensure Ollama is running: {e}")
    exit()

# --- 3. Define Agent's Capabilities (Nodes) ---

# Node 1: Classification
def classification_node(state: AgentState) -> dict:
    """
    Classifies the input text into one of predefined categories.
    Categories: News, Blog, Research, Other.
    """
    print("\n--- Executing Classification Node ---")
    text_to_classify = state["text"]
    classification_prompt_template = PromptTemplate(
        input_variables=["text"],
        template=(
            "Classify the following text into one of these categories: News, Blog, Research, or Other.\n\n"
            "Text:\n{text}\n\n"
            "Classification:"
        )
    )
    formatted_prompt = classification_prompt_template.format(text=text_to_classify)
    message = HumanMessage(content=formatted_prompt)
    response = llm.invoke([message])
    classification_result = response.content.strip()
    print(f"Raw classification from LLM: '{classification_result}'")

    valid_categories = ["News", "Blog", "Research", "Other"]
    # Simple normalization
    normalized_classification = classification_result
    found_category = False
    for category in valid_categories:
        if category.lower() in classification_result.lower():
            normalized_classification = category
            found_category = True
            break
    if not found_category:
        normalized_classification = "Other" # Default if no clear match

    print(f"Final classification: {normalized_classification}")
    return {"classification": normalized_classification}

# Node 2: Entity Extraction
def entity_extraction_node(state: AgentState) -> dict:
    """
    Identifies and extracts named entities (Person, Organization, Location) from the text.
    """
    print("\n--- Executing Entity Extraction Node ---")
    text_to_extract_from = state["text"]
    entity_prompt_template = PromptTemplate(
        input_variables=["text"],
        template=(
            "Extract all named entities (Person, Organization, Location) from the following text. "
            "List them as comma-separated values. If no entities are found, respond with 'None'.\n\n"
            "Text:\n{text}\n\n"
            "Entities (comma-separated or None):"
        )
    )
    formatted_prompt = entity_prompt_template.format(text=text_to_extract_from)
    message = HumanMessage(content=formatted_prompt)
    response = llm.invoke([message])
    entities_str = response.content.strip()
    
    entities_list = []
    if entities_str and entities_str.lower() != "none":
        entities_list = [entity.strip() for entity in entities_str.split(",") if entity.strip()]
    
    print(f"Extracted entities: {entities_list}")
    return {"entities": entities_list}

# Node 3: Summarization
def summarize_node(state: AgentState) -> dict:
    """
    Generates a concise, one-sentence summary of the input text.
    """
    print("\n--- Executing Summarization Node ---")
    text_to_summarize = state["text"]
    summarization_prompt_template = PromptTemplate(
        input_variables=["text"],
        template=(
            "Summarize the following text in one short, concise sentence.\n\n"
            "Text:\n{text}\n\n"
            "Summary:"
        )
    )
    formatted_prompt = summarization_prompt_template.format(text=text_to_summarize)
    message = HumanMessage(content=formatted_prompt)
    response = llm.invoke([message])
    summary_result = response.content.strip()
    
    print(f"Generated summary: {summary_result}")
    return {"summary": summary_result}

# --- 4. Define the Agent's Workflow (Graph) ---
workflow = StateGraph(AgentState)
workflow.add_node("classification_node", classification_node)
workflow.add_node("entity_extraction_node", entity_extraction_node)
workflow.add_node("summarization_node", summarize_node)
workflow.set_entry_point("classification_node")
workflow.add_edge("classification_node", "entity_extraction_node")
workflow.add_edge("entity_extraction_node", "summarization_node")
workflow.add_edge("summarization_node", END)
app = workflow.compile()
print("\nLangGraph workflow compiled successfully.")

# --- 5. Test the Agent ---
if __name__ == "__main__":
    print("\nStarting Medium Article Analyzer Agent Test...")
    sample_text = (
        "Anthropic's MCP (Model Context Protocol) is an open-source powerhouse that lets "
        "developers build applications that can seamlessly interact with various API systems. "
        "It aims to standardize how models access external knowledge and tools, "
        "potentially revolutionizing how AI agents are built and deployed across different platforms."
    )
    initial_state_input = {"text": sample_text}
    print(f"\nInput Text:\n'''\n{sample_text}\n'''")

    try:
        result = app.invoke(initial_state_input)
        print("\n\n--- Agent Processing Complete ---")
        # Ensure all keys exist before printing, or provide defaults
        print(f"Original Text: '''\n{result.get('text', 'N/A')}'''")
        print(f"Classification: {result.get('classification', 'N/A')}")
        print(f"Entities: {result.get('entities', 'N/A')}")
        print(f"Summary: {result.get('summary', 'N/A')}")
    except Exception as e:
        print(f"\nAn error occurred while running the agent: {e}")
        print("Please check your API key, model configuration, and node implementations.")
