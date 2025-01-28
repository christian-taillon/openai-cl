# Standard libraries
import argparse
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path
import json
import requests
import logging

# Prompt Toolkit
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style

# Pygments
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers import PythonLexer, get_lexer_by_name, guess_lexer

# Rich
from rich.console import Console
from rich.markdown import Markdown

# Halo
from halo import Halo

# Set title.
try:
    print('\033]0;OpenAI API Compatible Command-Line Client\a', end='', flush=True)
except AttributeError:
    pass  # Silently pass if there's an issue setting the terminal title

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
# Add these lines to disable markdown_it debug messages
markdown_it_logger = logging.getLogger('markdown_it')
markdown_it_logger.setLevel(logging.ERROR)  # or logging.ERROR to only show errors

# Define the API endpoint and headers
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def open_web_ui_api_request(prompt, model, api_key, base_url):
    """Make a request to the OpenWebUI API"""
    # Construct the full endpoint URL
    if base_url == None:
        endpoint = API_ENDPOINT
    else:
        # Otherwise, construct the endpoint using the base_url
        endpoint = f"{base_url}/api/chat/completions"
    
    logger.info(f"Making API request to OpenWebUI model: {model}")
    logger.info(f"Using endpoint: {endpoint}")
    # Set up headers
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Set up the request data
    data = {
        'model': model,
        'messages': messages
    }
    
    try:
        # Make the POST request
        response = requests.post(endpoint, headers=headers, json=data)
        
        logger.debug(f"API Response: {response.text}")
        logger.info("API request completed")
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise

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
    print("Simplicity meets the power of OpenAI API Compatible models.")
    print("Interact with ease: Your inputs and outputs are not used for model training.")
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



# Create helper
def display_help():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("OpenAI API Compatible Command-Line Interface (CLI) Help")
    print("======================================================")

    print("\nUsage:")
    print("  openai-cl.py [options]\n")

    print("Options:")
    print("  -h, --help                     Display this help message.")
    print("  --api_key <key>                Provide your API key.")
    print("  -m, --model <name>             Specify the model (default: gpt-4).")
    print("  -l, --l-models                 List available models.")
    print("  -s, --software <name>          Learn about software using its man page.\n")
    print("  -c, --code-helper <file_path>  Let the AI help you with code from a file.\n")
    print("  --base_url <url>               Specify the base URL for a custom API endpoint.")
    print("  --save_config                  Save the current configuration.")
    print("  --clear_config                 Clear the saved configuration.\n")

    print("Interactive Commands:")
    print("  help                      Show help message.")
    print("  clear                     Clear the terminal screen.")
    print("  exit                      End the interactive session.")
    print("  raw                       Display the last AI response in raw format, preserving markdown syntax.")
    print("  markdown or md            Equivalent to 'raw', shows the last AI response preserving markdown.\n")

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
    print("  openai-cl.py --api_key YOUR_API_KEY_HERE -m gpt-3.5-turbo-16k -s vim")
    print("  openai-cl.py --base_url https://your-custom-endpoint.com/v1\n")

    print("Note: Keep your API key confidential. Do not expose or share it in public spaces.")
    print()

def get_software_info(software_name):
    try:
        # Use 'man -P cat' to get raw man page content without formatting
        process = subprocess.Popen(['man', '-P', 'cat', software_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        man_page, stderr = process.communicate()

        if process.returncode == 0:
            # Man page found successfully
            if stderr:
                logger.warning(f"Warnings while retrieving man page for {software_name}:\n{stderr}")
            
            # Clean up the man page content
            cleaned_man_page = re.sub(r'\n{3,}', '\n\n', man_page)  # Reduce multiple newlines
            
            return f"Here's the man page for {software_name}:\n{cleaned_man_page}"
        else:
            # Man page not found, try -h flag
            print(f"No man page found for {software_name}. Trying '{software_name} -h'...")
            help_process = subprocess.Popen([software_name, '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            help_output, help_stderr = help_process.communicate()

            if help_process.returncode == 0:
                # -h flag worked
                print(f"\nNote: GPT has been provided with the help output for {software_name}. You can now ask questions about it.\n")
                return f"Here's the help output for {software_name}:\n{help_output}"
            else:
                # Both man page and -h flag failed
                error_message = f"Unable to retrieve information for {software_name}. "
                error_message += "No man page entry exists and it could not be executed with the '-h' flag. "
                error_message += "Ensure the software is installed and the name is spelled correctly."
                print(f"\nWarning: {error_message}\n")
                return error_message

    except FileNotFoundError:
        error_message = f"The command 'man' was not found. This feature may not be available on your system."
        print(f"\nError: {error_message}\n")
        return error_message
    except Exception as e:
        error_message = f"An unexpected error occurred while trying to get information for {software_name}: {str(e)}"
        print(f"\nError: {error_message}\n")
        return error_message

def get_file_content(file_path):
    try:
        # Read the file's contents
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        # Append a message indicating the file's contents are being submitted
        messages.append({"role": "assistant", "content": f"Submitting the contents of {file_path} to OpenAI for assistance. I need help or assistance with some code that I am working on.\n{file_contents}"})
        print(f"GPT has been provided the code of {file_path} you're currently working on. You can now ask questions about your code.\n")
    except FileNotFoundError:
         messages.append({"role": "assistant", "content": f"No file was found at this path."})

# Function to load configuration
def load_config():
    config_path = Path.home() / '.openai-cl-config.json'
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            logger.info(f"Loaded configuration: {config}")  
            return config
    logger.info("No saved configuration found.")  
    return {}

# Function to save configuration
def save_config(config):
    config_path = Path.home() / '.openai-cl-config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f)
        print(f"Saved configuration: {config}")  

# Add this function near the top of the file
def validate_api_response(response):
    """Validates the API response format and returns appropriate error messages."""
    if not isinstance(response, dict):
        return False, f"Invalid response type: {type(response)}"
    if 'choices' not in response:
        return False, f"Missing 'choices' in response: {response}"
    if not response['choices']:
        return False, "Empty choices array in response"
    if 'message' not in response['choices'][0]:
        return False, f"Missing 'message' in first choice: {response['choices'][0]}"
    if 'content' not in response['choices'][0]['message']:
        return False, f"Missing 'content' in message: {response['choices'][0]['message']}"
    return True, None


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
parser = argparse.ArgumentParser(description='Interactively chat with LLMs.', add_help=False)
parser.add_argument('--api_key', type=str, help='Your OpenAI API key. Can be set as environment variable.')
parser.add_argument('-m', '--model', type=str, help='The model to be used for the conversation.')
parser.add_argument('-l', '--l-models', action='store_true', help='List available models.')
parser.add_argument('-s', '--software', type=str, help='Learn about a software using its man page.')
parser.add_argument('-h', '--help', action='store_true', help='Display this help message and exit.')
parser.add_argument('-c', '--code-helper', type=str, metavar='FILE', help='Provide a file for code assistance.')
parser.add_argument('--base_url', type=str, help='Base URL for custom OpenAI API endpoint')
parser.add_argument('--save_config', action='store_true', help='Save the current configuration')
parser.add_argument('--clear_config', action='store_true', help='Clear the saved configuration')

# Load existing config
config = load_config()
if config:
    print("Loaded saved configuration.")

# Parse arguments
args = parser.parse_args()

def get_api_key():
    if args.api_key:
        logger.info("Using API key from command-line argument")
        return args.api_key

    if os.getenv("OPENWEBUI_KEY"):
        logger.info("Using API key from OPENWEBUI_KEY environment variable")
        return os.getenv("OPENWEBUI_KEY")
    
    if os.getenv("OPENAI_API_TOKEN"):
        logger.info("Using API key from OPENAI_API_TOKEN environment variable")
        return os.getenv("OPENAI_API_TOKEN")
    
    logger.error("No API key found")
    return None

api_key = get_api_key()

if api_key is None:
    print("No OpenAI API Key provided. Please use one of the following methods:")
    print("1. Use the --api_key command-line argument")
    print("2. Set the OPENWEBUI_KEY environment variable")
    print("3. Set the OPENAI_API_TOKEN environment variable")
    exit(1)


if args.software:
    SYSTEM_PROMPT = (
        "Expert CLI assistant focused on delivering single-command solutions. "
        "Always prioritize using provided documentation. "
        "Respond with exactly one command unless complexity requires alternatives. "
        "Format commands as inline code. "
        "Prioritize brevity - no examples or extra text unless absolutely needed."
    )
else:
    SYSTEM_PROMPT = (
        "You are a helpful assistant communicating with a user. "
        "Be concise in your responses. Your output will be rendered in markdown, "
        "so feel free to use markdown formatting for clarity and structure."
    )

# Initialize messages list with the system prompt
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if args.help:
    display_help()
    sys.exit(0)

# Initialize software_info as an empty string
software_info = ""

if args.software:
    if os.name == 'nt':
        print("Sorry, the man page functionality is not available on Windows.")
        sys.exit(1)
    software_info = get_software_info(args.software)
    if software_info:
        # Temp - instead of system prompt, I want to try adding it to the first message. 
        print(f"\nNote: GPT has been provided with the man page for {args.software}. You can now ask questions about it.\n")
    else:
        print("Unable to provide information about the specified software. Continuing without software context.")


if args.code_helper:
    get_file_content(args.code_helper)

if not args.software and not args.code_helper:
    display_intro()

if args.clear_config:
    save_config({})
    print("Configuration cleared.")
    sys.exit(0)

if args.model:
    config['model'] = args.model
if args.base_url:
    config['base_url'] = args.base_url

# Save config if requested
if args.save_config:
    save_config(config)
    print("Configuration saved.")

# Use config values
model = args.model or config.get('model', "llama3.1:8b")  # Modified this line

if 'model' in config: 
    model = config['model']
if args.model:
    config['model'] = args.model

base_url = config.get('base_url')

if 'base_url' in config:
    API_ENDPOINT = config['base_url']

# Check if API key is provided or not
if api_key is None:
    print("No OpenAI API Key provided. Please provide your API key.")
    exit()

if args.l_models:
    # List available models
    models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"]
    for model in models:
        print(model)
    exit()

# Get model from command line arguments or use default
# model = args.model

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

# Initialize last_response
last_response = ""

# Intialize first_message_sent to only send software on first message
first_message_sent = False

while True:
    user_input = session.prompt(
        [('class:you-prompt', f'{"You:":>11}'), ('class:input', '\n')],
        multiline=True,
        key_bindings=kb,
        style=style,
        wrap_lines=True,
        complete_while_typing=True,
        enable_history_search=True,
        prompt_continuation=lambda width, line_number, is_soft_wrap: '')

    # Check for exit_flag
    if exit_flag:
        print("Ending the conversation. Goodbye!")
        break

    if not user_input:  # If the input is empty or None, just continue
        continue

    if user_input.strip().lower() in ["markdown", "md"]:
        print(last_response) 
    
    if user_input.strip().lower() in ["raw"]:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(last_response) 
        print('')
        print('-------------------------')
        print('')
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
        
        if not first_message_sent and software_info:
            # Combine the software info with the user's first message
            combined_message = f"Documentation for the specified CLI tool:\n\n{software_info}\n\nUser's question: {user_input}"
            messages.append({"role": "user", "content": combined_message})
            first_message_sent = True
        else:
            # For subsequent messages, just add the user input
            messages.append({"role": "user", "content": user_input})

        spinner = Halo(text='Processing...', spinner='dots')
        spinner.start()

        # Get AI response using spinner
        try:
            logger.debug(f"Using model: {model}")
            logger.debug(f"Messages: {messages}")
            logger.debug(f"Type of model: {type(model)}")
            logger.debug(f"Model value: {model}")
            logger.debug(f"Type of api_key: {type(api_key)}")
            logger.debug(f"Base URL: {base_url}")
            
            response = open_web_ui_api_request(messages, model, api_key, base_url)
            
            # Validate response
            is_valid, error_message = validate_api_response(response)
            if not is_valid:
                logger.error(f"API Response Error: {error_message}")
                last_response = f"Error: {error_message}"
                continue
    
            # Access the response content
            last_response = response['choices'][0]['message']['content']
            
            # Add AI message to messages for the context of the next message
            messages.append({"role": "assistant", "content": last_response})
        except Exception as e:
            last_response = f"An error occurred: {str(e)}"
            logger.error(f"Error details: {e}")
            
        spinner.stop()

        def display_response(response_content: str):
            """Displays the AI response with markdown rendering."""
            console = Console()
            md_content = Markdown(response_content)
            console.print(md_content, end="")

        # Print AI response in bold
        print()  # This will add a line break
        ai_prompt = f'{(model[:8]+":" if len(model) > 8 else model+":"):>11}'
        print_formatted_text(FormattedText([('bg:red fg:white bold', ai_prompt)]), style=style)
        
        if last_response is not None:
            display_response(last_response)
        else:
            print("No response to display.")
            display_response(str(last_response))
        
        print()  # extra line break for visual separation

        # Add AI message to messages for the context of the next message
        messages.append({"role": "assistant", "content": last_response})