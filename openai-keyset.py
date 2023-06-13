import openai
import os
import argparse

# Define argument parser
parser = argparse.ArgumentParser(description='Interactively chat with OpenAI.')
parser.add_argument('--api_key', type=str, help='Your OpenAI API key.')

# Parse arguments
args = parser.parse_args()

if args.api_key:
    # Set API key from command line argument
    openai.api_key = args.api_key
    print("API Key has been set for this session.")
else:
    # Get API key from environment variables
    openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is provided or not
if openai.api_key is None:
    print("No OpenAI API Key provided. Please provide your API key.")
    exit()

print("Remember, this environment variable will only persist for the duration of this script. "
      "If you want to avoid providing your API key each time, please save your API key as "
      "an environment variable in your system settings.")

# Starting the conversation with the AI
messages = []

while True:
    # Get user input
    user_input = input("You: ")

    # Add user message to messages
    messages.append({"role": "user", "content": user_input})

    # Get AI response
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages,
      temperature=0.7
    )

    # Print AI response
    print("AI: ", response['choices'][0]['message']['content'])

    # Add AI message to messages for the context of the next message
    messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
