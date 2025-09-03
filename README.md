# J.A.R.V.I.S - Desktop AI Assistant

J.A.R.V.I.S. is a simple, voice-activated desktop assistant built with Python. It can understand and respond to a variety of commands, helping you with everyday tasks like opening applications, searching the web, and getting information.

## Features

- **Voice-activated:** Control the assistant using natural voice commands.
- **Text-to-Speech:** Get audible responses from the assistant.
- **Application Launcher:** Open common applications like Chrome, Firefox, and more.
- **Web Search:** Search Google, Wikipedia, and YouTube directly.
- **Information:** Get the current time, date, and day of the week.
- **File Management:** Create, list, and delete files in the current directory.
- **Fun Commands:** Ask for a joke or a fun fact.

## Setup

Follow these steps to set up and run the J.A.R.V.I.S. assistant on your local machine.

### Prerequisites

- Python 3.x
- `pip` for installing packages
- A working microphone

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download the spaCy model:**
    The assistant uses the `spaCy` library for natural language processing. You need to download the English language model.
    ```bash
    python -m spacy download en_core_web_sm
    ```

## Usage

To start the assistant, run the `main.py` script from the project's root directory:

```bash
python main.py
```

This will open the application window. Click the **"Start Listening"** button to activate the assistant. The assistant will greet you, and you can start giving commands. The conversation history will be displayed in the text box.

## Available Commands

Here is a list of the commands you can use:

- **"report status" / "what can you do"**: Lists all available commands.
- **"time"**: Tells you the current time.
- **"date"**: Tells you the current date.
- **"day of the week"**: Tells you the current day.
- **"open [website/app]"**: Opens a website (e.g., "open google") or an application (e.g., "open chrome").
- **"search [engine] for [term]"**: Searches a specified engine (e.g., "search google for python").
- **"list files"**: Lists the files in the current directory.
- **"create file [filename] with content [content]"**: Creates a new file with the specified content.
- **"delete file [filename]"**: Deletes a file after asking for confirmation.
- **"tell me a joke"**: Tells you a joke.
- **"tell me a fun fact"**: Tells you a fun fact.
- **"what is your name"**: The assistant will tell you its name.
- **"exit" / "stop"**: Closes the application.
