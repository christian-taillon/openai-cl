import openai
import os
import argparse
import subprocess

# Define argument parser
parser = argparse.ArgumentParser(description='Interactively chat with OpenAI.')
parser.add_argument('--api_key', type=str, help='Your OpenAI API key.')
parser.add_argument('-m', '--model', type=str, default="gpt-3.5-turbo", help='The model to be used for the conversation.')
parser.add_argument('-l', '--l-models', action='store_true', help='List available models.')

# Parse arguments
args = parser.parse_args()

if args.api_key:
    # Set API key from command line argument
    openai.api_key = args.api_key
else:
    # Get API key from environment variables
    openai.api_key = os.getenv("OPENAI_API_TOKEN")

# Check if API key is provided or not
if openai.api_key is None:
    print("No OpenAI API Key provided. Please provide your API key.")
    exit()

if args.l_models:
    # List available models
    models = ["gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"]
    for model in models:
        print(model)
    exit()

# Get model from command line arguments or use default
model = args.model

# Starting the conversation with the AI
messages = []

# Ask the user for a software name and get the man page
software_name = input("Please enter the name of the software you want to learn about: ")
try:
    man_page = subprocess.check_output(['man', software_name], universal_newlines=True)
    messages.append({"role": "assistant", "content": f"Here's the man page for {software_name}:\n{man_page}"})
except subprocess.CalledProcessError:
    messages.append({"role": "assistant", "content": f"I'm sorry, I couldn't find a man page for {software_name}."})

while True:
    # Get user input
    user_input = input("You: ")

    # Check if the user wants to exit the conversation
    if user_input.lower() == "exit":
        print("Ending the conversation. Goodbye!")
        break

    # Add user message to messages
    messages.append({"role": "user", "content": user_input})

    # Get AI response
    response = openai.ChatCompletion.create(
      model=model,
      messages=messages,
      temperature=0.7
    )

    # Print AI response
    print("AI: ", response['choices'][0]['message']['content'])

    # Add AI message to messages for the context of the next message
    messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
