# OpenAI Interactive Chat CommandLine
State: Pre-Release
#### Author: Christian Taillon

This script allows you to interactively chat with the OpenAI using the `openai` Python client. This script is cross-platform and can be run on any system that supports Python and has the OpenAI Python client installed.

According to OpenAI's current Security policies at [openai.com](https://openai.com/security), input provided to API's is not currently used to train future models. While this doesn't mean OpenaAI doesn't store prompts, this does offer a method of leveraging OpenAI's services in a way that policy prohibits the use of said prompts for future training.

## Setup

1. Ensure that Python is installed on your system. If not, you can download and install it from the [official Python website](https://www.python.org/downloads/).

2. Install the `openai` Python client by running the following command in your terminal:

    ```bash
    pip install openai
    ```

3. Clone or download this repository and navigate to its directory in your terminal.

## Usage

This script accepts an optional command line argument, `--api_token`, to set the OpenAI API key. If not provided, the script will look for an environment variable named `OPENAI_API_TOKEN`.

### Using the `--api_token` Argument

To use the `--api_token` argument, run the script as follows:

```bash
python openai-keyset.py --api_token YOUR_OPENAI_API_TOKEN
```

Replace `YOUR_OPENAI_API_TOKEN` with your actual OpenAI API token.

This will set the API token for the current script execution only. It does not permanently save the API token as an environment variable.

### Using the `OPENAI_API_TOKEN` Environment Variable

To use the `OPENAI_API_TOKEN` environment variable, you need to set it in your system settings. The process to do this varies depending on your operating system.

Once the `OPENAI_API_TOKEN` environment variable is set, you can run the script as follows:

```bash
python openai-keyset.py
```

## Note

Remember, the `OPENAI_API_TOKEN` environment variable set via the command line will only persist for the duration of the script. If you want to avoid providing your API token each time, save your API token as an environment variable in your system settings.

This script will continue the conversation until you manually end the program, such as by pressing `Ctrl+C`.

---
