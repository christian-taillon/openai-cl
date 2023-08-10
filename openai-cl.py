import openai
import os
import argparse
import sys
import time
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

def display_intro():
    coffee_art = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⡇⠀⢶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⢋⡼⠁⠀⣸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣳⠏⠀⣠⠞⣡⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⡄⢸⣯⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⠸⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣁⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⡟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⢻⢿⣷⢀⣀⣀⣀⡀⠀
⢸⡇⠀⣶⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠶⣒⣒⣿⣋⣥⣄⡉⢻⣆
⢸⣿⠈⣇⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠶⠶⢶⣿⠁⠀⢸⡇⢰⣿
⠀⢻⣆⢻⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠒⣾⣯⣤⣴⠟⣡⣿⠃
⠀⠈⢿⣎⠻⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⣿⣿⣭⣥⣴⡿⠟⠁⠀
⠀⠀⠈⢿⣷⣄⠑⣦⡄⠀⠀⠀⣀⠀⢛⣻⣿⡟⠉⠉⠉⠀⠀⠀⠀⠀
⠀⣴⡶⠶⠿⠿⢿⣶⣤⣤⣤⣤⣽⣿⠿⠛⣛⣟⣷⡆⠀⠀⠀⠀⠀⠀
⠀⠛⠷⠶⣤⣤⣤⣤⣴⣾⣿⣿⣶⣦⣤⣶⣶⡾⠟⠁⠀⠀⠀⠀⠀⠀
    '''

    print("Welcome to openai-cl by Christian Taillon!")
    print("Simplicity meets the power of OpenAI's ChatGPT API.")
    print("Interact with ease: Your inputs and outputs are not used for OpenAI model training.")
    print(coffee_art)
    print("\nQuick Guide:")
    print("- Simply type or paste your content below.")
    print("- For multi-line inputs, press `Ctrl+Space` to submit.")
    print("- Commands available: help, clear, exit. Use `Ctrl+Space` after typing a command to activate it.\n")
display_intro()


# Spinner Class
class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, traceback):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

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
    print("API Key has been set for this session.")
    print("Remember, this environment variable will only persist for the duration of this script. "
          "If you want to avoid providing your API key each time, please save your API key as "
          "an environment variable in your system settings.")
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

# Create a flag to indicate submission
submit_flag = False

# Define a custom style for the prompt
style = Style.from_dict({
    'prompt': 'bold',
    'input': 'green',
    'you-prompt': 'bg:white fg:orange bold',
    # Currently the ai-prompt is defined inline using the FormattedText PromptSession near the bottom
})

# Create custom keybindings
kb = KeyBindings()

# Create a prompt session
session = PromptSession()

@kb.add('c-space')
def _(event):
    global submit_flag
    submit_flag = True
    event.app.exit(result=event.app.current_buffer.text)

# Starting the conversation with the AI
messages = []

while True:
    # When prompting the user:
    user_input = session.prompt([('class:you-prompt', '    You :'), ('class:input', '\n    ')],
                               multiline=True,
                                key_bindings=kb,
                                style=style,
                                wrap_lines=False,
                                prompt_continuation=lambda width, line_number, is_soft_wrap: '    ')

    if not user_input:  # If the input is empty or None, just continue
        continue

    if user_input.strip().lower() == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
        continue

    if user_input.strip().lower() == "help":
        print("\n    Instructions:")
        print("    1. Type your message to the AI and press Ctrl+Space to send.")
        print("    2. You can type multi-line messages. Each new line starts after pressing Enter.")
        print("    3. To exit the chat, simply type 'exit'.")
        print("    4. Enjoy chatting with the AI!\n")
        continue

    # Check the submit flag
    if submit_flag:
        submit_flag = False  # reset the flag

        # Check if the user wants to exit the conversation
        if user_input.lower() == "exit":
            print("Ending the conversation. Goodbye!")
            break

        # Add user message to messages
        messages.append({"role": "user", "content": user_input})

        # Get AI response using spinner
        with Spinner():
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.7
            )

        # Print AI response in bold
        print()  # This will add a line break
        print_formatted_text(FormattedText([('bg:white fg:red bold', '    AI:')]), style=style)
        print("    ", end="")
        print(response['choices'][0]['message']['content'].replace("\n", "\n    "))
        print()  # extra line break for visual separation


        # Add AI message to messages for the context of the next message
        messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
