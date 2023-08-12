#!/bin/bash

# Check for the --uninstall flag
if [[ "$1" == "--uninstall" ]]; then
    echo "Uninstalling..."

    # Remove symbolic link
    LINK_PATH="$HOME/.local/bin/openai-cl"
    if [ -L "$LINK_PATH" ]; then
        rm "$LINK_PATH"
        echo "Removed symbolic link from $LINK_PATH."
    else
        echo "Symbolic link not found at $LINK_PATH."
    fi

    # Remove virtual environment
    if [ -d "env" ]; then
        rm -rf env
        echo "Removed virtual environment."
    else
        echo "Virtual environment not found."
    fi

    # Offer to undo PATH modifications
    if [[ -n "$RC_FILE" ]]; then
        read -p "Remove ~/.local/bin from your PATH in $RC_FILE? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sed -i '/export PATH=$PATH:$HOME\/.local\/bin/d' $RC_FILE
            echo "PATH modification removed from $RC_FILE."
        else
            echo "Skipped removal of PATH modification."
        fi
    fi

    echo "Uninstallation complete."
    exit
fi

# Check if ~/.local/bin is in PATH
if [[ ! ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
    # Determine which shell the user is using
    CURRENT_SHELL=$(basename $SHELL)
    RC_FILE=""

    if [[ "$CURRENT_SHELL" == "bash" ]]; then
        RC_FILE="$HOME/.bashrc"
    elif [[ "$CURRENT_SHELL" == "zsh" ]]; then
        RC_FILE="$HOME/.zshrc"
    else
        echo "Unsupported shell. Please manually add ~/.local/bin to your PATH."
        exit
    fi

    # Prompt the user to modify the appropriate rc file
    read -p "Add ~/.local/bin to your PATH in $RC_FILE? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo 'export PATH=$PATH:$HOME/.local/bin' >> $RC_FILE
        echo "PATH updated in $RC_FILE. Please restart your terminal or source $RC_FILE."
    else
        echo "Installation cannot proceed without updating PATH."
        exit
    fi
fi

# Check for the --uninstall flag
if [[ "$1" == "--uninstall" ]]; then
    echo "Uninstalling..."

    # Remove symbolic link
    LINK_PATH="$HOME/.local/bin/openai-cl"
    if [ -L "$LINK_PATH" ]; then
        rm "$LINK_PATH"
        echo "Removed symbolic link from $LINK_PATH."
    else
        echo "Symbolic link not found at $LINK_PATH."
    fi

    # Remove virtual environment
    if [ -d "env" ]; then
        rm -rf env
        echo "Removed virtual environment."
    else
        echo "Virtual environment not found."
    fi

    # Offer to undo PATH modifications
    if [[ -n "$RC_FILE" ]]; then
        read -p "Remove ~/.local/bin from your PATH in $RC_FILE? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sed -i '/export PATH=$PATH:$HOME\/.local\/bin/d' $RC_FILE
            echo "PATH modification removed from $RC_FILE."
        else
            echo "Skipped removal of PATH modification."
        fi
    fi

    echo "Uninstallation complete."
    exit
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "python3 could not be found!"
    exit
else
    echo "Found python3."
fi

USE_VENV=true

# Check for python3-venv
echo "Checking for python3-venv..."
if ! python3 -m venv test_venv &> /dev/null; then
    echo "python3-venv is not installed!"
    read -p "Would you like to proceed without a virtual environment? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        USE_VENV=false
    else
        exit
    fi
else
    # Clean up the test virtual environment
    rm -rf test_venv
    echo "python3-venv is available."
fi

# Create and activate virtual environment only if user wants it
if $USE_VENV; then
    echo "Creating virtual environment..."
    if [ -d "env" ]; then
        read -p "Virtual environment already exists. Overwrite? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit
        fi
    fi
    python3 -m venv env
    source env/bin/activate
    echo "Virtual environment created."

    # Install dependencies (optional, based on if you have a requirements.txt)
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Skipping virtual environment setup."
fi

# Symbolic link location
LINK_PATH="$HOME/.local/bin/openai-cl"

# Create symbolic link for easy access
echo "Creating symbolic link in $LINK_PATH..."
if [ -L "$LINK_PATH" ]; then
    read -p "Symbolic link already exists. Overwrite? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ln -sf "$(pwd)/openai-cl-runner.sh" "$LINK_PATH"
        echo "Symbolic link overwritten."
    else
        echo "Symbolic link not changed."
    fi
else
    # Check if directory exists, create if not
    if [ ! -d "$HOME/.local/bin" ]; then
        mkdir -p "$HOME/.local/bin"
    fi

    ln -s "$(pwd)/openai-cl-runner.sh" "$LINK_PATH"
    echo "Symbolic link created."
fi

# Check if OPENAI_API_TOKEN is already set
echo "Checking for OPENAI_API_TOKEN..."
if [[ -z "${OPENAI_API_TOKEN}" ]]; then
    read -p "Please provide your OpenAI API token (or press enter to skip): " TOKEN
    if [[ ! -z "${TOKEN}" ]]; then
        echo "export OPENAI_API_TOKEN=$TOKEN" >> ~/.bashrc
        echo "Added OPENAI_API_TOKEN to ~/.bashrc."

        # Export the token for the current session
        export OPENAI_API_TOKEN=$TOKEN
    else
        echo "Skipped adding OPENAI_API_TOKEN."
    fi
else
    echo "OPENAI_API_TOKEN is already set."
fi

# Provide execute permission for the runner script
chmod +x openai-cl-runner.sh

echo "Installation complete. You can now use openai-cl from anywhere!"
