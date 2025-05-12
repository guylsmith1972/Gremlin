# Gremlin Voice Assistant

**Project Repository:** [https://github.com/guylsmith1972/Gremlin](https://github.com/guylsmith1972/Gremlin)

Gremlin is a Python-based voice-controlled assistant designed to execute commands, manage applications, interact with a Large Language Model (LLM), and automate tasks on your computer via speech.

## Features

*   **Voice-to-Command Execution:** Speak commands and have them executed.
*   **Multiple Operational Modes:**
    *   **Command Mode:** Interpret speech as commands and arguments.
    *   **Interactive Mode:** Dictate text directly into applications.
    *   **Chatter Mode:** Engage in a conversation with an LLM using your speech history.
    *   **Suspend Mode:** Temporarily pause command processing.
*   **Built-in Commands:** A rich set of commands for common tasks like application management, text input, web searches, and more.
*   **Alias System:** Create custom shortcuts for frequently used commands.
*   **Extensible with Custom Scripts:** Add your own Python scripts to expand Gremlin's capabilities.
*   **LLM Integration:** Query a local LLM (e.g., Llama 3 via Ollama) for information or assistance.
*   **Application Management:** List running and available applications, and bring specific applications to the foreground (primarily Windows).

## Installation

### Prerequisites

*   Python 3.x
*   `pip` (Python package installer)
*   **Windows Operating System:** Required for full application management features using `pywinauto`. Some features might work on other OSes, but window interaction is Windows-specific.

### Steps

1.  **Clone or Download:**
    Get the Gremlin source files. You can clone the repository from GitHub:
    ```bash
    git clone https://github.com/guylsmith1972/Gremlin.git
    cd Gremlin
    ```
    Alternatively, you can download the source code as a ZIP file from the [project page](https://github.com/guylsmith1972/Gremlin) and extract it.

2.  **Install Dependencies:**
    Navigate to the project's root directory (where `requirements.txt` is located) and run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ollama (for LLM features - Optional):**
    If you plan to use the `chat` command or Chatter Mode:
    *   Install Ollama from [ollama.ai](https://ollama.ai/).
    *   Pull a model, for example, Llama 3:
        ```bash
        ollama pull llama3
        ```
    *   Ensure Ollama is running. Gremlin attempts to interact with it at `http://localhost:11434`. The `llama.py` script is configured to use the "llama3" model by default.

4.  **Speech Model (Vosk):**
    The Vosk speech recognition model will be downloaded automatically the first time you run Gremlin if it's not found in the `./models/` directory. This might take a few minutes depending on your internet connection.

## Configuration (`config.json`)

The `config.json` file stores settings for Gremlin. You can modify it to customize behavior:

*   `commands.prefix` (string | null): An optional prefix required before speaking a command (e.g., "Gremlin"). If `null`, no prefix is needed, and the first spoken word is treated as the command.
*   `commands.directory` (string): The directory where custom command scripts are stored (default: `"commands"`).
*   `commands.builtins`: Defines the keywords, descriptions, and types (command/mode) for built-in functionalities. You can change the keyword to invoke a built-in command here.
*   `speech.model` (string): Name of the Vosk speech model directory (e.g., `"vosk-model-en-us-0.21"`).
*   `speech.default` (string): URL to download the default speech model if not present.
*   `applications.monitoring.interval` (integer): How often (in seconds) the list of running applications is updated (default: `1`).

## Running Gremlin

1.  Navigate to the directory containing `Gremlin.py` (the root of the cloned/extracted project).
2.  Run the application from your terminal:
    ```bash
    python Gremlin.py
    ```
3.  Upon successful startup, you should see a message like:
    `Listening. Say "help" to get a listing of available voice commands.`

## Basic Usage

*   **Speak Clearly:** Ensure your microphone is set up correctly and speak clearly.
*   **Command Structure:**
    *   If `commands.prefix` is set in `config.json` (e.g., to "computer"), start your utterance with that prefix:
        `computer show notepad`
    *   If `commands.prefix` is `null`, the first word you speak is treated as the command:
        `show notepad`
    *   Subsequent words are treated as arguments to the command.

## Modes of Operation

Gremlin operates in different modes, which affect how it interprets your speech. You can switch modes using specific voice commands.

*   **Command Mode:**
    *   **Activation:** Default mode on startup. Can be explicitly entered by saying `command` or `resume`.
    *   **Behavior:** The first word (after the prefix, if any) is treated as a command, and the rest as arguments.
    *   Example: `search latest tech news`

*   **Interactive Mode:**
    *   **Activation:** Say `interactive`.
    *   **Behavior:** All spoken words are treated as text to be typed into the currently active window. This is useful for dictation.
    *   Example: Say `interactive`. Then say `Hello world, this is a test message.` The sentence will be typed out.
    *   **Exiting:** To exit Interactive Mode, you must use a mode-switching command (e.g., `command`, `suspend`).

*   **Chatter Mode:**
    *   **Activation:** Say `chatter <optional_instructions_for_llm>`.
    *   **Behavior:** The entire transcript of your current session (and any previous interactions in this mode) is sent to an LLM (e.g., Llama via Ollama) along with any instructions you provided when entering the mode. The LLM's response is printed to the console.
    *   Example: `chatter please summarize the following conversation and highlight action items`
    *   **Exiting:** Use a mode-switching command (e.g., `command`).

*   **Suspend Mode:**
    *   **Activation:** Say `suspend`.
    *   **Behavior:** Gremlin stops processing most commands. Only mode-switching commands (like `resume`, `command`, `terminate`) are recognized. Useful to temporarily pause Gremlin.
    *   **Exiting:** Say `resume` (switches to Command Mode) or another mode command.

## Built-in Commands

Gremlin comes with a set of built-in commands. The keywords listed below are defaults from `config.json` and can be changed there.
Say `help` to see a dynamic list of all available commands, aliases, and scripts.

*   `help`: Displays a list of available commands.
    *   `help aliases`: Lists all defined aliases.
    *   `help built-ins`: Lists built-in commands and modes.
    *   `help commands`: Lists built-in commands.
    *   `help modes`: Lists available modes.
    *   `help scripts`: Lists custom scripts.
    *   `help <command_name>`: Shows detailed help for a specific command.

### General Commands

*   `input <text_to_type>`: Types the given text into the active window.
    *   Example: `input Hello there!`
*   `enter`: Simulates pressing the Enter key.
*   `search <query_terms>`: Performs a Google web search.
    *   Example: `search python programming tutorials`
*   `clear`: Clears the current speech transcript memory.
*   `transcript`: Prints the accumulated speech transcript to the console.
*   `terminate`: Exits Gremlin.

### Alias Management

*   `alias <name> <command_and_args>`: Creates a new alias.
    *   Example: `alias mymail open mail dot google dot com`
*   `delete <alias_name>`: Deletes an existing alias.
    *   Example: `delete mymail`
*   `list aliases`: Displays all currently defined aliases.

### Application Management (Primarily Windows)

*   `list running`: Lists currently running applications that have visible windows.
*   `list available`: Lists executable files found in your system's PATH environment variable.
*   `find <substring>`: Searches for running or available applications whose name or title contains the substring.
    *   Example: `find editor`
*   `show <app_name_substring>`: Brings an application window to the foreground. It chooses the first match for the substring in window titles or process names.
    *   Example: `show notepad`

### LLM Interaction (Requires Ollama setup)

*   `chat <prompt>`: Sends the prompt directly to the LLM and prints the response.
    *   Example: `chat what is the capital of France`

### Mode Switching Commands

*   `command`: Switches to Command Mode.
*   `interactive`: Switches to Interactive Mode.
*   `chatter <optional_instructions>`: Switches to Chatter Mode, providing instructions to the LLM.
*   `suspend`: Suspends command processing (only mode-switching commands work).
*   `resume`: Resumes command processing (switches to Command Mode from Suspend Mode).

## Aliases

Aliases are custom shortcuts for longer or more complex commands. They are stored in `aliases.json`.

*   **Creating an Alias:** Use the `alias` command (see above).
*   **Using an Alias:** Simply say the alias name as if it were a command.
*   **Listing Aliases:** Use the `list aliases` command.
*   **Deleting an Alias:** Use the `delete <alias_name>` command.

The `aliases.json` file is created with some example aliases. You can manually edit this file, but using the voice commands is generally recommended.

```json
{
    "aliases": "help aliases",
    "defense": "open https://new.reddit.com/r/NonCredibleDefense/new/",
    "email": "open mail dot google dot com",
    "google": "search",
    "lama": "chat",
    "news": "open news dot google dot com"
}
```

## Custom Scripts

You can extend Gremlin's functionality by creating your own Python scripts and placing them in the directory specified by `commands.directory` in `config.json` (default is a folder named "commands").

*   **Naming:** The voice command to invoke a script is its filename without the `.py` extension.
    *   Example: A script named `my_task.py` in the `commands` directory can be run by saying `my task`.
*   **Arguments:** Words spoken after the script command are passed as command-line arguments to the script. You can access these in your Python script using `sys.argv[1:]`.
*   **Examples:**
    *   `commands/open.py`: Opens a URL in a web browser. It intelligently handles "dot" for "." and can append ".com" if no top-level domain is specified.
        *   Usage: `open google dot com` or `open reddit`
    *   `commands/launch.py`: Launches an executable.
        *   Usage: `launch notepad`
    *   `commands/hello.py`: A simple script that prints "Hello world!" to the console.
        *   Usage: `hello`

## Troubleshooting and Notes

*   **Microphone:** Ensure your microphone is properly configured in your operating system and is set as the default input device.
*   **Permissions (Windows):** For `pywinauto` to interact with all application windows (especially those running with administrative privileges), you might need to run Gremlin with administrative privileges.
*   **LLM Server:** The `chat` command and Chatter Mode require an Ollama server to be running and accessible (typically at `http://localhost:11434`). If it's not, these features will fail.
*   **First Run Model Download:** The initial download of the Vosk speech model can take some time. Subsequent runs will be faster as the model will be cached locally.
*   **Windows Focus:** Application management features (like `show <app_name>`) are heavily reliant on `pywinauto` and are thus best supported on Windows. While other parts of Gremlin might be cross-platform, window manipulation is Windows-specific.
