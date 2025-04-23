import os
# Ensure Ollama is installed and running, and you have pulled a model.
# Example: ollama pull llama3

# --- Thinking Step 1: Import necessary modules ---
# Note: ChatOllama is in langchain_community
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Thinking Step 2: Instantiate the Ollama Chat Model ---
# Replace "llama3" with the specific Ollama model you have pulled and want to use
# (e.g., "mistral", "phi3", "qwen2")
# Temperature=0 encourages more deterministic, less creative output for reasoning.
# Make sure the Ollama service is running in the background!
try:
    llm = ChatOllama(model="qwen2.5:0.5b")
    # You can optionally specify the base_url if Ollama runs elsewhere:
    # llm = ChatOllama(model="llama3", temperature=0, base_url="http://<your_ollama_ip>:11434")

    # Optional: Test connection with a simple generation (good for debugging)
    # print("Testing Ollama connection...")
    # llm.invoke("Say hi")
    # print("Ollama connection successful.")

except Exception as e:
    print(f"Error initializing Ollama: {e}")
    print("Please ensure Ollama is installed, running, and the model 'llama3' (or your chosen model) is pulled.")
    exit() # Exit if we can't connect to the LLM

# --- Thinking Step 3: Design the Prompt Template with CoT ---
# This is identical to the previous example. The CoT instruction is key.
cot_prompt_template = """
Question: {question}

Let's think step by step to arrive at the solution. Break down the problem, show your reasoning calculations, and then state the final answer clearly.

Step-by-step thinking:
"""

# Create the Langchain Prompt Template object
prompt = ChatPromptTemplate.from_template(cot_prompt_template)

# --- Thinking Step 4: Define the Output Parser ---
# Simple string output parser.
output_parser = StrOutputParser()

# --- Thinking Step 5: Create the Chain using LCEL ---
# Connect the components: Prompt -> LLM -> Output Parser
chain_of_thought_chain = prompt | llm | output_parser

# --- Thinking Step 6: Define the Input Question ---
input_question = ("Roger has 5 tennis balls. He buys 2 more cans of tennis balls. "
                  "Each can contains 3 tennis balls. How many tennis balls does "
                  "Roger have now?")

# --- Thinking Step 7: Invoke the Chain ---
# Pass the input question to the chain.
print(f"--- Running Chain of Thought with Ollama ({llm.model}) ---")
print(f"Question: {input_question}\n")

try:
    response = chain_of_thought_chain.invoke({"question": input_question})

    # --- Thinking Step 8: Print the Result ---
    print("--- LLM Response (with Chain of Thought) ---")
    print(response)
    print("-" * 30)

except Exception as e:
     print(f"Error during chain invocation: {e}")


# --- Optional: Comparison without CoT ---
# simple_prompt_template = "Question: {question}\nAnswer:"
# simple_prompt = ChatPromptTemplate.from_template(simple_prompt_template)
# simple_chain = simple_prompt | llm | output_parser
#
# print(f"\n--- Running Simple Chain (No CoT) with Ollama ({llm.model}) ---")
# print(f"Question: {input_question}\n")
# try:
#     simple_response = simple_chain.invoke({"question": input_question})
#     print("--- LLM Response (without CoT) ---")
#     print(simple_response)
#     print("-" * 30)
# except Exception as e:
#     print(f"Error during simple chain invocation: {e}")