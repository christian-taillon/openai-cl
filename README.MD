# README for OpenAI Chat Application

## Description

This project was created by Christian. The main goal of this project was to provide a simple and user-friendly way to interact with the OpenAI API. There weren't any clean existing projects to talk to the OpenAI APIs easily, so this project was created to fill that gap.

According to OpenAI's documentation, they will not use API input to train future models. Specifically, they state:

> "OpenAI will not use data submitted by customers via our API to train or improve our models"

This project uses the OpenAI Python client and allows you to choose different models, list available models, and interactively chat with the chosen AI model.

## Installation

First, you need to install the OpenAI Python client. This can be done using pip:

```bash
pip install openai
```

## Setting up the OpenAI API Key

You'll need your OpenAI API key to run this application. This key can be set up as an environment variable. The steps to set an environment variable depend on your operating system.

### MacOS / Linux

1. Open Terminal
2. Run the following command, replacing `your_api_key` with your actual OpenAI API key:

```bash
export OPENAI_API_TOKEN="your_api_key"
```

### Windows

1. Open the Start Menu and search for "Environment Variables".
2. Click on "Edit the system environment variables".
3. In the System Properties window that appears, click on "Environment Variables".
4. In the Environment Variables window, click "New" under the "User variables" section.
5. Enter `OPENAI_API_TOKEN` for the Variable name and your actual OpenAI API key for the Variable value.
6. Click OK on all windows.

## Usage

You can interactively chat with an AI model by running the script:

```bash
python script.py --api_key YOUR_API_KEY
```

You can specify a model to use for the conversation:

```bash
python script.py --api_key YOUR_API_KEY -m text-davinci-002
```

You can list the available models:

```bash
python script.py --api_key YOUR_API_KEY -l
```

During the conversation, you can type "exit" to end the conversation and exit the program.
