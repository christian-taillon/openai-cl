#!/bin/bash

# Determine the directory of the original script (resolving symbolic links)
DIR="$( cd "$( dirname "$(readlink -f "${BASH_SOURCE[0]}")" )" && pwd )"

# Activate the virtual environment
if [ -d "$DIR/env" ]; then
    source "$DIR/env/bin/activate"
else
    echo "Virtual environment not found. Running without it..."
fi

# Run the main script
python "$DIR/openai-cl.py" "$@"

# Deactivate the virtual environment
if [ -d "$DIR/env" ]; then
    deactivate
fi
