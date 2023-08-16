# Check for the --uninstall flag
if ($args -contains "--uninstall") {
    Write-Host "Uninstalling..."

    # Remove environment variable
    [Environment]::SetEnvironmentVariable("OPENAI_API_TOKEN", $null, "User")

    # Remove virtual environment
    if (Test-Path .\env) {
        Remove-Item -Recurse -Force .\env
        Write-Host "Virtual environment removed."
    } else {
        Write-Host "Virtual environment not found."
    }

    # Remove the .cmd runner script
    $cmdScriptPath = "$pwd\openai-cl-runner.cmd"
    if (Test-Path $cmdScriptPath) {
        Remove-Item $cmdScriptPath
        Write-Host "CMD script removed from $cmdScriptPath."
    } else {
        Write-Host "CMD script not found at $cmdScriptPath."
    }

    # Remove the Windows Terminal profile JSON
    if (Test-Path $wtProfilePath) {
        Remove-Item $wtProfilePath
        Write-Host "Removed Windows Terminal profile at $wtProfilePath."
    }


    # Remove the desktop shortcut
    if (Test-Path $shortcutPath) {
        Remove-Item $shortcutPath
        Write-Host "Removed desktop shortcut at $shortcutPath."
    }


    Write-Host "Uninstallation complete."
    exit
}

# Check for Python
try {
    python --version
} catch {
    Write-Host "Python not found. Please ensure it's installed and added to PATH."
    exit
}

# Set up virtual environment
if (-not (Test-Path .\env)) {
    python -m venv .\env
    .\env\Scripts\Activate
    Write-Host "Virtual environment set up."
} else {
    Write-Host "Virtual environment already exists."
}

# Check for pip and install requirements
try {
    pip install -r requirements.txt
} catch {
    Write-Host "Pip not found or there was an error installing requirements. Please ensure pip is installed and accessible."
    exit
}

# Check if OPENAI_API_TOKEN environment variable is set
$token = [Environment]::GetEnvironmentVariable("OPENAI_API_TOKEN", "User")
if (-not $token) {
    $userToken = Read-Host "Please provide your OpenAI API token (or press enter to skip)"
    if ($userToken) {
        [Environment]::SetEnvironmentVariable("OPENAI_API_TOKEN", $userToken, "User")
        Write-Host "OPENAI_API_TOKEN set successfully."
    } else {
        Write-Host "Skipped adding OPENAI_API_TOKEN."
    }
} else {
    Write-Host "OPENAI_API_TOKEN is already set."
}

# Create the .cmd script to activate the virtual environment and run the Python script
$cmdScriptContent = @"
@echo off
call "$pwd\env\Scripts\activate.bat"
python "$pwd\openai-cl.py"
"@
# ... previous part of the script

# Debugging: Output the directory where the .cmd file will be created
Write-Host "Current directory: $pwd"

# Debugging: Output the .cmd script content to console
Write-Host "CMD Script Content:"
Write-Host $cmdScriptContent

# Create the .cmd script to activate the virtual environment and run the Python script
$cmdScriptPath = "$pwd\openai-cl-runner.cmd"
try {
    $cmdScriptContent | Out-File $cmdScriptPath -Encoding utf8
    Write-Host "CMD script created at $cmdScriptPath"
} catch {
    Write-Host "Error occurred while creating the CMD script: $_"
    exit
}

# Debugging: Log status after creating .cmd file
Write-Host "CMD script creation successful."

# Create the Windows Terminal profile JSON
$wtProfileContent = @"
{
    "guid": "{a1c6ff0a-1a8b-5f70-ac19-a3efed215f65}",
    "hidden": false,
    "name": "openai-cl",
    "commandline": "cmd.exe /k $cmdScriptPath",
    "startingDirectory": "$pwd"
}
"@
$wtProfilePath = "$pwd\openai-cl-wt-profile.json"
$wtProfileContent | Out-File $wtProfilePath -Encoding utf8


# Create a shortcut to launch Windows Terminal and run the CMD script
$wtPath = (Get-Command wt).Source
$shortcutPath = "$env:USERPROFILE\Desktop\openai-cl.lnk"
try {
    $WScriptShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $wtPath
    $Shortcut.Arguments = "-w 0 cmd.exe /k $cmdScriptPath"
    $Shortcut.Save()
    Write-Host "Shortcut created on desktop."
} catch {
    Write-Host "Error occurred while creating the desktop shortcut: $_"
    exit
}

# Debugging: Log status after creating shortcut
Write-Host "Desktop shortcut creation successful."

Write-Host "Installation complete. You can now use the openai-cl shortcut from your desktop!"
