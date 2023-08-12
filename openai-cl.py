import openai
import os
import re
import argparse
import sys
import time
import threading
import subprocess
from prompt_toolkit.keys import Keys
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from pygments.lexers import PythonLexer, get_lexer_by_name, guess_lexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import PygmentsLexer
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from rich.console import Console
from rich.markdown import Markdown

# Set title.
print('\033]0;OpenAI Command-Line Chat\a', end='', flush=True)

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

    print("Welcome to openai-cl!")
    print("Simplicity meets the power of OpenAI's ChatGPT API.")
    print("Interact with ease: Your inputs and outputs are not used for OpenAI model training.")
    print(coffee_art)
    print("                                 Cheers (with coffee)")
    print("                                         - Christian ☕\n")
    print("Quick Guide:")
    print("- Simply type or paste your content below.")
    print("- Use `Ctrl+Space` after typing a prompt or command.")
    print("- Use `Ctrl+q` to end the session.\n")
def print_processing():
    sys.stdout.write("Processing...\n")
    sys.stdout.flush()

def clear_last_line():
    sys.stdout.write("\033[F")  # Move cursor up one line
    sys.stdout.write("\033[K")  # Clear to the end of line

class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_usage(self, usage, actions, groups, prefix):
        return "\nUsage:\n  openai-cl.py [options]\n"

    def _format_action(self, action):
        parts = super()._format_action(action)
        if action.option_strings:
            parts = '  ' + parts
        return parts

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')  # this line should remove the spinner character
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

# Create helper
def display_help():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("OpenAI Command-Line Interface (CLI) Help")
    print("=========================================")

    print("\nUsage:")
    print("  openai-cl.py [options]\n")

    print("Options:")
    print("  -h, --help                Display this help message.")
    print("  --api_key <key>           Provide your OpenAI API key.")
    print("  -m, --model <name>        Specify the model (default: gpt-3.5-turbo).")
    print("  -l, --l-models            List available models.")
    print("  -s, --software <name>     Learn about software using its man page.\n")

    print("Interactive Commands:")
    print("  help                      Show help message.")
    print("  clear                     Clear the terminal screen.")
    print("  exit                      End the interactive session.\n")

    print("Interactive Session Tips:")
    print("- Type or paste your messages into the terminal.")
    print("- Submit multi-line messages with `Ctrl+Space`.")
    print("- AI responses appear after the 'AI:' prompt.")
    print("- Use commands like help, clear, or exit by typing and submitting with `Ctrl+Space`.")
    print("- End the session with `Ctrl+q`.\n")

    print("Examples:")
    print("  openai-cl.py --api_key YOUR_API_KEY_HERE")
    print("  openai-cl.py -m gpt-3.5-turbo-16k")
    print("  openai-cl.py -s nano")
    print("  openai-cl.py --api_key YOUR_API_KEY_HERE -m gpt-3.5-turbo-16k -s vim\n")

    print("Note: Keep your API key confidential. Do not expose or share it in public spaces.")
    print()


# Teach GPT about a software
def get_software_info(software_name):
    try:
        man_page = subprocess.check_output(['man', software_name], universal_newlines=True)
        messages.append({"role": "assistant", "content": f"Here's the man page for {software_name}:\n{man_page}"})
    except subprocess.CalledProcessError:
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Display the message
        print(f"I'm sorry, I couldn't find a man page for {software_name}.")
        print("Please ensure that the software name is correct or that a man page exists for it.")
        print()
        # Prompt the user to press any key to continue
        print("Press any key to continue...")

        kb = KeyBindings()

        @kb.add(Keys.Any)
        def _(event):
            event.app.exit()

        session = PromptSession(key_bindings=kb)
        session.prompt()

        # Exit the script
        exit()
    print("\nNote: GPT has been trained on the software provided. You can now ask questions and have a conversation about the man page.\n")

def highlight_code_blocks(text):
    # Regular expression to identify code blocks
    code_block_pattern = re.compile(r'```(.*?)```', re.DOTALL)

    # Function to replace the block with highlighted code
    def replace_with_highlighted(match):
        code = match.group(1).strip()
        language = None
        if '\n' in code:
            maybe_lang, rest_of_code = code.split('\n', 1)
            if not maybe_lang.isalnum():
                # If the first line isn't a language name, treat the entire block as code
                rest_of_code = code
            else:
                language = maybe_lang
                code = rest_of_code

        # Guess the lexer if not specified
        if not language:
            lexer = guess_lexer(code)
        else:
            lexer = get_lexer_by_name(language)

        # Highlight the code
        return highlight(code, lexer, TerminalFormatter())

    # Replace each code block with its highlighted version
    highlighted_text = re.sub(code_block_pattern, replace_with_highlighted, text)

    return highlighted_text

# Define argument parser
# Help is handled in a custom way
parser = argparse.ArgumentParser(description='Interactively chat with OpenAI.', add_help=False)
parser.add_argument('--api_key', type=str, help='Your OpenAI API key.')
parser.add_argument('-m', '--model', type=str, default="gpt-3.5-turbo", help='The model to be used for the conversation.')
parser.add_argument('-l', '--l-models', action='store_true', help='List available models.')
parser.add_argument('-s', '--software', type=str, help='Learn about a software using its man page.')
parser.add_argument('-h', '--help', action='store_true', help='Display this help message and exit.')

# Parse arguments
args = parser.parse_args()

# Starting the conversation with the AI
messages = []

if args.help:
    display_help()
    sys.exit(0)

# Software information
if args.software:
    get_software_info(args.software)  # Pass the software name to the function

if not args.software:
    display_intro()

# Set API key from command line argument
if args.api_key:
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
    'you-prompt': 'bg:orange fg:white bold',
    ## 'you-prompt': 'bg:white fg:orange bold',
    # Currently the ai-prompt is defined inline using the FormattedText PromptSession near the bottom
})

# Create custom keybindings
kb = KeyBindings()

# Create a prompt session
session = PromptSession()

# Add keyboard shortcuts
@kb.add('c-space')
def _(event):
    global submit_flag
    submit_flag = True
    event.app.exit(result=event.app.current_buffer.text)


@kb.add('c-q')
def _(event):
    global exit_flag
    exit_flag = True
    event.app.exit()

# Prevent the script from existing
exit_flag = False

while True:
    # When prompting the user:
    user_input = session.prompt([('class:you-prompt', '    You:'), ('class:input', '\n    ')],
                               multiline=True,
                                key_bindings=kb,
                                style=style,
                                wrap_lines=True,
                                prompt_continuation=lambda width, line_number, is_soft_wrap: '    ')

    # Check for exit_flag
    if exit_flag:
        print("Ending the conversation. Goodbye!")
        break

    if not user_input:  # If the input is empty or None, just continue
        continue

    if user_input.strip().lower() == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
        continue

    if user_input.strip().lower() == "help":
        display_help()
        continue

    # Check if the user wants to exit the conversation
    if user_input.lower() in ["exit", "q"]:
        print("Ending the conversation. Goodbye!")
        break

    # Check the submit flag
    if submit_flag:
        submit_flag = False  # reset the flag

        # Add user message to messages
        messages.append({"role": "user", "content": user_input})

        print_processing()

        # Get AI response using spinner
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.7
        )

        # Clear the "Processing..." message:
        clear_last_line()

        # Print AI response in bold
        print()  # This will add a line break
        print_formatted_text(FormattedText([('bg:red fg:white bold', '    GPT:')]), style=style)
        print("    ", end="")
        print(response['choices'][0]['message']['content'].replace("\n", "\n    "))
        print()  # extra line break for visual separation

        # Add AI message to messages for the context of the next message
        messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
