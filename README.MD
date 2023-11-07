
---

# 🤖 OpenAI Command-Line Chat Application ☕️

## Description
Welcome to the OpenAI Command-Line Chat Application! Born out of a desire for a refined terminal client for OpenAI, this tool bridges the gap between functionality and finesse.

![Intro](/images/intro.png)   

Whether you're diving in for quick insights or seeking a seamless interaction experience, this tool has got you covered.

- **Rapid "Training" Sessions:** Jump straight in, ask your questions, and receive real-time insights without a hitch.
- **Mindful of Content Sensitivity:** Your peace of mind matters. Share with confidence, knowing your inputs won't be part of future model training.
- **Copy-Paste & Multi-Line Inputs:** Enhance your interactions with support for effortless copy-pasting and multi-line inputs.
- **Aesthetic Terminal Interface:** A delightful terminal experience awaits because aesthetics matter.
- **Syntax Highlighting:** ChatGPT's responses include syntax highlighting, making code and technical responses easier to read.
- **Platform Agnostic (Mostly):** Efforts have been made to ensure this tool feels at home, regardless of your OS. However, it's worth noting that my primary testing ground is Linux. If you encounter quirks elsewhere, do give me a shout!

Per OpenAI's documentation:

> "OpenAI will not use data submitted by customers via our API to train or improve our models."

The project harnesses the OpenAI Python client. It provides functionalities to select different models, list available models, send the man page output to OpenAI to discuss it, and engage in an interactive chat with the chosen AI model.

## Setting up the OpenAI API Key
To get started, you'll require an OpenAI API key. Secure yours from the [API Keys Settings](https://platform.openai.com/account/api-keys) on the OpenAI platform.
> **Note:** Always keep your API key confidential.


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

3. **Usage**:
   Once the installation is complete, you can use the tool from anywhere by typing `openai-cl` in a command prompt or PowerShell window.


## Uninstall

To uninstall simply pass the `--uninstall` argument to the install script.

### macOS & Linux
```bash
./install.sh --uninstall
```

### Windows
```powershell
.\install.ps1 --uninstall
```

## Software Training
Train your session with the -s on the manpage output of a tool you would like to learn about.

```bash
openai-cl -s scp
```

*Output*:
![scp](/images/scp.png)   

## Usage

After installation, you can use the `openai-cl` shortcut from anywhere on your system. This allows you to engage in an interactive chat with an AI model:

## Syntax Highlighting
This tool includes syntax highlighting for improved readability and use of the chat output.
![syntax](/images/syntax.png)  

_Note: you can obtain the non-rendered raw markdown by sending a `raw` response to the chat to aid in copying and pasting the markdown content to programs that don't support the stylized rendered content._



```bash
openai-cl
```

You can provide the helper page by passing the `-h` argument.
![Help](/images/help.png)   

You can specify a model for the conversation:

```bash
openai-cl -m gpt-3.5-turbo
```

To see a list of available models:

```bash
openai-cl -l
```

To learn about a software using its man page:

```bash
openai-cl -s SOFTWARE_NAME
```

A few examples of this:
```bash
openai-cl -s cat
openai-cl -s yara
openai-cl -s docker
openai-cl -s scp
```

During the interactive session:
- Type or paste your messages into the terminal.
- For multi-line messages, use `Ctrl+Space` to submit.
- AI responses will follow the 'AI:' prompt.
- Commands like `help`, `clear`, or `exit` can be typed and submitted with `Ctrl+Space`.
- Use `Ctrl+q` to end the session.

---

This project was primary made for my own use cases but I wondered if it might be beneficial to others, particularly as it offers a method off accessing OpenAI's services without providing ones prompt for future model training (as of the time of writing).

Encountering bugs? I'm here to help. 😉

**Contributing**: If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.
