
# 🤖 OpenAI-API Compatible Command-Line Chat Application ☕️

## Description

Welcome to the OpenAI-API Compatible Command-Line Chat Application! This versatile tool is designed to work with any OpenAI API-compliant endpoints, allowing you to interact with various AI models, including self hosten models, through a refined terminal interface.

![Intro](/images/intro.png)

Whether you're seeking quick insights, engaging in in-depth conversations, or working with custom models, this application offers a seamless and feature-rich experience.

Key Features:
- Compatible with OpenAI API and custom endpoints
- Rapid "Training" Sessions for quick insights
- Copy-Paste & Multi-Line Input support
- Aesthetic Terminal Interface with Syntax Highlighting
- Platform Agnostic design (primary testing on Linux)

## Setting up the API Key

To use this application, you need to provide an API key. You have several options:

1. Use the `--api_key` command-line argument
2. Set the `OPENWEBUI_KEY` environment variable
3. Set the `OPENAI_API_TOKEN` environment variable

If no API key is provided, the application will prompt you with these options.

Example:
```bash
export OPENAI_API_TOKEN=your_api_key_here
```

## Installation
Note that these installations haven't been widely tested. It is possible to execute the python script your self and bypass the installers. Simply manually installing the python library requirements and manually adding your API key to your environment variables.

For those who would like install helpers, I have provided some based on other open source projects.

### macOS & Linux

1. **Clone the Repository (or Download the Zip)**:
   ```bash
   git clone https://github.com/christian-taillon/openai-cl.git
   cd openai-cl
   ```

   Alternatively, if you've provided a direct download, instruct the user to download and extract the zip, then navigate to its directory in the terminal.

2. **Run the Installation Script**:
   Make the installer script executable and run it:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   During the installation, you'll be prompted to set up a virtual environment. If you don't have `virtualenv` installed, you can choose to skip this step.

   You'll also have the option to set your OpenAI API token as an environment variable. You can either provide your token or skip this step.

3. **Usage**:
   Once the installation is complete, you can use the tool from anywhere by typing:
   ```bash
   openai-cl
   ```

### Windows

1. **Clone the Repository (or Download the Zip)**:
   Download the repository zip from the GitHub page or use a Git client if you have one installed.

   Once downloaded, extract the zip and navigate to its directory.

2. **Run the Installation Script**:

   Open a PowerShell prompt as administrator. Navigate to the directory containing the installation script and run:

   ```powershell
   .\install.ps1
   ```

   You'll have the option to set your OpenAI API token as an environment variable. You can either provide your token or skip this step.

## Usage

After installation, use the `openai-cl` command to start the application:

```bash
openai-cl
```

### Command-line Options

- `-h, --help`: Display the help message
- `--api_key <key>`: Provide your API key
- `-m, --model <name>`: Specify the model (default: gpt-4)
- `-l, --l-models`: List available models
- `-s, --software <name>`: Learn about software using its man page
- `-c, --code-helper <file_path>`: Let the AI help you with code from a file
- `--base_url <url>`: Specify the base URL for a custom API endpoint
- `--save_config`: Save the current configuration
- `--clear_config`: Clear the saved configuration

### Interactive Commands

During the chat session, you can use these commands:
- `help`: Show help message
- `clear`: Clear the terminal screen
- `exit`: End the interactive session
- `raw` or `markdown` or `md`: Display the last AI response in raw format, preserving markdown syntax

### Interactive Session Tips

- Type or paste your messages into the terminal
- Submit multi-line messages with `Ctrl+Space`
- AI responses appear after the 'AI:' prompt
- Use commands like help, clear, or exit by typing and submitting with `Ctrl+Space`
- End the session with `Ctrl+q`

## Examples

1. Using a specific API key:
   ```bash
   openai-cl --api_key YOUR_API_KEY_HERE
   ```

2. Choosing a different model:
   ```bash
   openai-cl -m llama3.2:3b
   ```

3. Learning about software using its man page:
   ```bash
   openai-cl -s nano
   ```

4. Using a custom API host:
   ```bash
   openai-cl --base_url https://your-custom-endpoint.com
   ```

5. Listing available models:
   ```bash
   openai-cl -l
   ```

## Listing Models

You can list the available models for your configured API using the `-l` or `--l-models` option. This is particularly useful when working with custom endpoints or to check which models are accessible with your current API key.

```bash
openai-cl -l
```

## Software Training

Train your session with the `-s` option on the manpage output of a tool you would like to learn about:

```bash
openai-cl -s ssh
```

![scp](/images/software_training_ssh.png)

_Note: You can obtain the non-rendered raw markdown by sending a `raw` response to the chat._

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Support

Encountering bugs or have questions? Feel free to open an issue on the GitHub repository.

Remember to keep your API key confidential and never share it in public spaces.