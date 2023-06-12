import openai
import os

# Get API key from environment variables
openai.api_key = os.getenv("OPENAI_API_TOKEN")

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
