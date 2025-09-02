import datetime
import webbrowser
import random
import os
from playsound import playsound
from AppOpener import open
import win32com.client
import spacy
import difflib
import subprocess
import zipfile

speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Load the spaCy model once
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Spacy 'en_core_web_sm' model not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None

# Command registry
_commands = {}

def register_command(keywords):
    """A decorator to register a new command."""
    def decorator(func):
        for keyword in keywords:
            _commands[keyword.lower()] = func
        return func
    return decorator

def handle_command(query):
    """
    Finds and executes a command based on the query.
    Returns True if a command was found and executed, False otherwise.
    """
    query = query.lower()
    for keyword, func in _commands.items():
        if keyword in query:
            func(query)
            return True
    return False

# --- Built-in Commands ---

@register_command(["time"])
def tell_time(query):
    """Tells the current time."""
    strftime = datetime.datetime.now().strftime("%H:%M:%S")
    speaker.Speak(f"Sir, the time is {strftime}")

@register_command(["open music"])
def play_music(query):
    """Plays a music file."""
    # This path is hardcoded and will likely not work on other systems.
    # This is a pre-existing issue with the code.
    music_file = 'C:/Users/s.k.f.ansari/Downloads/Lemon Fight.mp3'
    try:
        playsound(music_file)
    except Exception as e:
        print(f"Error playing sound file {music_file}: {e}")
        speaker.Speak("Sorry, I could not play the music file. Please check the file path.")

# --- Website Opening Commands ---

_sites = {
    "youtube": "https://www.youtube.com",
    "wikipedia": "https://www.wikipedia.com",
    "google": "https://www.google.com",
}

@register_command([f"open {site}" for site in _sites.keys()])
def open_website(query):
    """Opens a website."""
    for site_name, url in _sites.items():
        if f"open {site_name}" in query:
            speaker.Speak(f"Opening {site_name}, sir.")
            # This path is hardcoded and will likely not work on other systems.
            firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
            try:
                webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))
                webbrowser.get('firefox').open(url)
            except Exception as e:
                print(f"Error opening website: {e}")
                speaker.Speak(f"Sorry, I could not open {site_name}.")
            return

# --- Application Opening Commands ---

_apps = ["whatsapp", "excel", "word", "chrome", "firefox", "settings"]

@register_command([f"open {app}" for app in _apps])
def open_application(query):
    """Opens an application."""
    for app_name in _apps:
        if f"open {app_name}" in query:
            speaker.Speak(f"Opening {app_name}, sir.")
            try:
                open(app_name)
            except Exception as e:
                print(f"Error opening application {app_name}: {e}")
                speaker.Speak(f"Sorry, I could not open {app_name}.")
            return

# --- New Commands ---

@register_command(["joke"])
def tell_joke(query):
    """Tells a random joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call fake spaghetti? An Impasta!",
    ]
    joke = random.choice(jokes)
    speaker.Speak(joke)

@register_command(["date", "today's date"])
def tell_date(query):
    """Tells the current date."""
    today = datetime.datetime.now().strftime("%B %d, %Y")
    speaker.Speak(f"Sir, today's date is {today}")

@register_command(["search wikipedia for"])
def search_wikipedia(query):
    """Searches Wikipedia for a topic."""
    search_term = query.replace("search wikipedia for", "").strip()
    if not search_term:
        speaker.Speak("What would you like me to search for on Wikipedia?")
        return

    speaker.Speak(f"Searching Wikipedia for {search_term}")
    url = f"https://en.wikipedia.org/wiki/{search_term.replace(' ', '_')}"

    firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    try:
        webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))
        webbrowser.get('firefox').open(url)
    except Exception as e:
        print(f"Error opening website: {e}")
        speaker.Speak(f"Sorry, I could not open Wikipedia for {search_term}.")

@register_command(["fun fact", "tell me a fact"])
def fun_fact(query):
    """Tells a random fun fact."""
    facts = [
        "The national animal of Scotland is the unicorn.",
        "A group of flamingos is called a flamboyance.",
        "Honey never spoils.",
        "The Eiffel Tower can be 15 cm taller during the summer.",
    ]
    fact = random.choice(facts)
    speaker.Speak(fact)

# --- File Management Commands ---

@register_command(["read file"])
def read_file_command(query):
    """Reads the content of a file and speaks a summary."""
    # Assumes query is "read file [path]"
    try:
        path = query.lower().split("read file")[1].strip()
        if not path:
            speaker.Speak("Please specify a file path to read.")
            return

        speaker.Speak(f"Reading file from {path}")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            print(f"Full content of {path}:\n{content}")

            summary = content[:200] # Read the first 200 characters as a summary
            speaker.Speak("Here is the beginning of the file content:")
            speaker.Speak(summary)
        else:
            speaker.Speak("Sorry, I could not find a file at that path.")
    except Exception as e:
        print(f"Error reading file: {e}")
        speaker.Speak("Sorry, I encountered an error while trying to read the file.")

@register_command(["create file"])
def create_file_command(query):
    """Creates a new file with specified content."""
    # Assumes query is "create file [path] with content [content]"
    try:
        parts = query.lower().split(" with content ")
        if len(parts) != 2:
            speaker.Speak("Sorry, I didn't understand the format. Please say 'create file [path] with content [your content]'.")
            return

        path_part = parts[0].replace("create file", "").strip()
        content = parts[1].strip()

        if not path_part:
            speaker.Speak("Please specify a file path to create.")
            return

        if not content:
            speaker.Speak("Please specify content for the file.")
            return

        speaker.Speak(f"Creating file at {path_part}")
        with open(path_part, 'w', encoding='utf-8') as f:
            f.write(content)

        speaker.Speak(f"I have successfully created the file at {path_part}.")

    except Exception as e:
        print(f"Error creating file: {e}")
        speaker.Speak("Sorry, I encountered an error while trying to create the file.")

@register_command(["delete file"])
def delete_file_command(query):
    """Deletes a specified file."""
    # Assumes query is "delete file [path]"
    try:
        path = query.lower().split("delete file")[1].strip()
        if not path:
            speaker.Speak("Please specify a file path to delete.")
            return

        speaker.Speak(f"Attempting to delete file at {path}")
        if os.path.exists(path):
            os.remove(path)
            speaker.Speak("File has been successfully deleted.")
        else:
            speaker.Speak("Sorry, I could not find a file at that path.")
    except Exception as e:
        print(f"Error deleting file: {e}")
        speaker.Speak("Sorry, I encountered an error while trying to delete the file.")

@register_command(["create directory"])
def create_directory_command(query):
    """Creates a new directory."""
    # Assumes query is "create directory [path]"
    try:
        path = query.lower().split("create directory")[1].strip()
        if not path:
            speaker.Speak("Please specify a directory path to create.")
            return

        speaker.Speak(f"Creating directory at {path}")
        if not os.path.exists(path):
            os.makedirs(path)
            speaker.Speak("Directory has been successfully created.")
        else:
            speaker.Speak("That directory already exists.")
    except Exception as e:
        print(f"Error creating directory: {e}")
        speaker.Speak("Sorry, I encountered an error while trying to create the directory.")

@register_command(["append to file"])
def append_to_file_command(query):
    """Appends content to an existing file."""
    # Assumes query is "append to file [path] with content [content]"
    try:
        parts = query.lower().split(" with content ")
        if len(parts) != 2:
            speaker.Speak("Sorry, I didn't understand the format. Please say 'append to file [path] with content [your content]'.")
            return

        path_part = parts[0].replace("append to file", "").strip()
        content_to_append = parts[1].strip()

        if not path_part:
            speaker.Speak("Please specify a file path.")
            return

        if not content_to_append:
            speaker.Speak("Please specify content to append.")
            return

        speaker.Speak(f"Appending content to file at {path_part}")
        if os.path.exists(path_part):
            with open(path_part, 'a', encoding='utf-8') as f:
                f.write(f"\\n{content_to_append}") # Add a newline before appending
            speaker.Speak("Content has been successfully appended.")
        else:
            speaker.Speak("Sorry, I could not find a file at that path. I can only append to existing files.")
    except Exception as e:
        print(f"Error appending to file: {e}")
        speaker.Speak("Sorry, I encountered an error while trying to append to the file.")

# --- Content Analysis Commands ---

@register_command(["summarize file"])
def summarize_file_command(query):
    """Reads a file and provides a longer summary."""
    # Assumes query is "summarize file [path]"
    try:
        path = query.lower().split("summarize file")[1].strip()
        if not path:
            speaker.Speak("Please specify a file path to summarize.")
            return

        speaker.Speak(f"Summarizing file from {path}")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # A simple summary: the first 500 characters.
            # A more advanced implementation could use an NLP library for abstractive summarization.
            summary = content[:500]

            print(f"Summary for {path}:\n{summary}")

            speaker.Speak("Here is a summary of the file:")
            speaker.Speak(summary)
        else:
            speaker.Speak("Sorry, I could not find a file at that path.")
    except Exception as e:
        print(f"Error summarizing file: {e}")
        speaker.Speak("Sorry, I encountered an error while trying to summarize the file.")

@register_command(["find entities in"])
def identify_entities_command(query):
    """Identifies named entities in a sentence using spaCy."""
    if nlp is None:
        speaker.Speak("The natural language processing model is not loaded. Please check the setup.")
        return

    # Assumes query is "find entities in [sentence]"
    try:
        sentence = query.lower().split("find entities in")[1].strip()
        if not sentence:
            speaker.Speak("Please provide a sentence to analyze.")
            return

        speaker.Speak("Analyzing the sentence for named entities.")

        doc = nlp(sentence)

        entities = [(ent.text, ent.label_) for ent in doc.ents]

        if not entities:
            speaker.Speak("I did not find any recognized entities in that sentence.")
            return

        response = "I found the following entities: "
        for text, label in entities:
            # Make the label more human-readable
            label_description = spacy.explain(label_)
            response += f"{text}, which is a {label_description}. "

        print(f"Found entities: {entities}")
        speaker.Speak(response)

    except Exception as e:
        print(f"Error identifying entities: {e}")
        speaker.Speak("Sorry, I encountered an error while analyzing the sentence.")

@register_command(["compare file", "compare files"])
def compare_files_command(query):
    """Compares two files and reports the differences."""
    # Assumes query is "compare file [path1] and file [path2]"
    try:
        # Normalize the query
        query = query.lower().replace("compare files", "compare file")
        parts = query.split("compare file")[1].strip().split(" and file ")

        if len(parts) != 2:
            speaker.Speak("Sorry, I didn't understand the format. Please say 'compare file [path A] and file [path B]'.")
            return

        path_a, path_b = parts[0].strip(), parts[1].strip()

        if not os.path.exists(path_a) or not os.path.exists(path_b):
            speaker.Speak("Sorry, one or both of the files could not be found.")
            return

        speaker.Speak(f"Comparing file {os.path.basename(path_a)} and file {os.path.basename(path_b)}.")

        with open(path_a, 'r', encoding='utf-8') as f_a:
            lines_a = f_a.readlines()
        with open(path_b, 'r', encoding='utf-8') as f_b:
            lines_b = f_b.readlines()

        diff = list(difflib.unified_diff(lines_a, lines_b, fromfile=os.path.basename(path_a), tofile=os.path.basename(path_b)))

        if not diff:
            speaker.Speak("The files are identical.")
            return

        diff_summary = [line for line in diff if line.startswith('+') or line.startswith('-')]

        speaker.Speak(f"I found {len(diff_summary)} differing lines between the two files.")

        print("--- File Comparison Diff ---")
        for line in diff:
            print(line, end='')
        print("\n--- End of Diff ---")

    except Exception as e:
        print(f"Error comparing files: {e}")
        speaker.Speak("Sorry, I encountered an error while comparing the files.")

@register_command(["clone repository"])
def clone_repository_command(query):
    """Clones a Git repository from a URL to a local path."""
    # Assumes query is "clone repository [url] to [path]"
    try:
        parts = query.lower().split(" to ")
        if len(parts) != 2:
            speaker.Speak("Sorry, I didn't understand the format. Please say 'clone repository [url] to [path]'.")
            return

        url_part = parts[0].replace("clone repository", "").strip()
        path_part = parts[1].strip()

        if not url_part or not path_part:
            speaker.Speak("Please specify both a repository URL and a destination path.")
            return

        speaker.Speak(f"Cloning repository from {url_part} into {path_part}")

        # Using subprocess for better security and control
        result = subprocess.run(['git', 'clone', url_part, path_part], capture_output=True, text=True)

        if result.returncode == 0:
            speaker.Speak("Repository has been successfully cloned.")
            print(result.stdout)
        else:
            speaker.Speak("Sorry, I encountered an error while cloning the repository.")
            print(f"Git clone error:\n{result.stderr}")

    except Exception as e:
        print(f"Error cloning repository: {e}")
        speaker.Speak("Sorry, I encountered an error while trying to clone the repository.")

@register_command(["compress file"])
def compress_file_command(query):
    """Compresses a single file into a zip archive."""
    # Assumes query is "compress file [source_path] to [zip_path]"
    try:
        parts = query.lower().split(" to ")
        if len(parts) != 2:
            speaker.Speak("Sorry, I didn't understand the format. Please say 'compress file [source path] to [destination zip path]'.")
            return

        source_path = parts[0].replace("compress file", "").strip()
        zip_path = parts[1].strip()

        if not source_path or not zip_path:
            speaker.Speak("Please specify both a source file and a destination zip path.")
            return

        if not os.path.exists(source_path):
            speaker.Speak("Sorry, the source file does not exist.")
            return

        speaker.Speak(f"Compressing {os.path.basename(source_path)} into {os.path.basename(zip_path)}.")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(source_path, os.path.basename(source_path))

        speaker.Speak("File has been successfully compressed.")

    except Exception as e:
        print(f"Error compressing file: {e}")
        speaker.Speak("Sorry, I encountered an error while compressing the file.")

# --- Creative & Reasoning Commands ---

_brainstorming_map = {
    "writer's block": [
        "Try the Pomodoro Technique: write for 25 minutes, then take a 5-minute break.",
        "Just start writing anything that comes to mind, even if it's not perfect.",
        "Change your environment. Go to a coffee shop or a library.",
        "Read a book or article on a new topic to get inspired.",
    ],
    "being unproductive": [
        "Break down large tasks into smaller, more manageable steps.",
        "Use the two-minute rule: if a task takes less than two minutes, do it now.",
        "Schedule your tasks and stick to the schedule.",
        "Make sure to get enough sleep and exercise.",
    ],
    "learning a new skill": [
        "Set clear, achievable goals.",
        "Practice consistently, even if it's just for a short time each day.",
        "Find a mentor or a community to learn with.",
        "Teach what you've learned to someone else to solidify your knowledge.",
    ]
}

@register_command(["brainstorm solutions for"])
def brainstorm_solutions_command(query):
    """Provides a list of generic solutions for a common problem."""
    try:
        problem = query.lower().split("brainstorm solutions for")[1].strip()

        if problem in _brainstorming_map:
            speaker.Speak(f"Here are some ideas for {problem}:")
            solutions = _brainstorming_map[problem]
            for i, solution in enumerate(solutions):
                speaker.Speak(f"Idea {i+1}: {solution}")
        else:
            speaker.Speak(f"Sorry, I don't have any specific ideas for {problem}. My knowledge in this area is still growing.")

    except Exception as e:
        print(f"Error brainstorming solutions: {e}")
        speaker.Speak("Sorry, I encountered an error while brainstorming.")

# --- Meta Commands ---

@register_command(["report status", "what can you do"])
def report_status_command(query):
    """Reports the status of the AI by listing all available commands."""
    try:
        speaker.Speak("I am online and ready to help. I currently know how to do the following:")

        # Get a unique list of command keywords
        command_keywords = sorted(list(_commands.keys()))

        # Create a more readable string
        command_list_str = ", ".join(command_keywords)

        print(f"Available commands: {command_list_str}")
        speaker.Speak(command_list_str)

        speaker.Speak("What would you like me to do?")

    except Exception as e:
        print(f"Error reporting status: {e}")
        speaker.Speak("Sorry, I encountered an error while reporting my status.")
