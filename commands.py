"""
This module manages all the voice commands for the J.A.R.V.I.S. assistant.

It uses a decorator-based registration system to map keywords to specific
command functions. The `CommandManager` class is responsible for interpreting
user queries and executing the corresponding actions, from telling the time to
managing files.
"""
import datetime
import webbrowser
import random
import os
from playsound import playsound
from AppOpener import open as open_app
import spacy
import difflib
import subprocess
import zipfile
import shutil
import re
import psutil
import threading
import sys
import string
import pyperclip

# Command registry
_commands = {}


def register_command(keywords):
    """
    A decorator to register a function as a voice command.

    This decorator maps a list of keywords to a command function. When any of
    the keywords are detected in a user's query, the decorated function will be
    called.

    Args:
        keywords (list of str): A list of keywords that trigger the command.

    Returns:
        function: The decorator function.
    """
    def decorator(func):
        for keyword in keywords:
            _commands[keyword.lower()] = func
        # Mark the function so we can find it later
        func.is_command = True
        func.keywords = keywords
        return func
    return decorator


class CommandManager:
    """
    Manages the registration, discovery, and execution of commands.

    This class loads NLP models, handles incoming queries by matching them to
    registered commands, and executes the relevant function.

    Attributes:
        assistant (Assistant): The main assistant instance.
        nlp: The spaCy NLP model for natural language processing.
    """
    def __init__(self, assistant):
        """
        Initializes the CommandManager.

        Args:
            assistant (Assistant): The main assistant instance to interact with the GUI and TTS.
        """
        self.assistant = assistant
        self.nlp = None
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Spacy 'en_core_web_sm' model not found. Run 'python -m spacy download en_core_web_sm'")
            self.assistant.speak("The natural language processing model is not loaded. Some commands may not work.")

        # This part of the original code for registration is redundant if all commands are methods.
        # The decorator now handles registration directly into the global _commands dict.
        # If commands could be defined outside this class, this loop would be necessary.
        # For now, keeping the logic but noting its current limited use.
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'is_command'):
                # This registration is already done by the decorator.
                # It's harmless to re-register but is not strictly necessary.
                pass

    def handle_command(self, query):
        """
        Finds and executes a command based on the user's query.

        It first checks for any easter eggs, then iterates through the registered
        commands to find a match.

        Args:
            query (str): The user's voice command, converted to lowercase text.

        Returns:
            bool: True if a command or easter egg was handled, False otherwise.
        """
        query = query.lower()
        if self.handle_easter_eggs(query):
            return True

        for keyword, func in _commands.items():
            if query.startswith(keyword):
                # Pass the full query to the command function
                result = func(self, query)
                if isinstance(result, dict) and 'action' in result:
                    self.handle_confirmation(result)
                return True
        return False

    def handle_confirmation(self, action):
        """
        Handles confirmation steps for sensitive actions like file deletion.

        This method prompts the user for confirmation and waits for a "yes"
        response before proceeding with the action.

        Args:
            action (dict): A dictionary describing the action to confirm.
                           Example: {'action': 'confirm_delete', 'path': '/path/to/file'}
        """
        if action['action'] == 'confirm_delete':
            path_to_delete = action['path']
            self.assistant.speak(f"Are you sure you want to delete {os.path.basename(path_to_delete)}? Please say yes to confirm.")

            confirmation_query = self.assistant.take_command().lower()

            if "yes" in confirmation_query:
                try:
                    os.remove(path_to_delete)
                    self.assistant.speak("The file has been permanently deleted.")
                except Exception as e:
                    print(f"Error during confirmed deletion: {e}")
                    self.assistant.speak("Sorry, an error occurred during the final deletion.")
            else:
                self.assistant.speak("Deletion cancelled.")

    # --- Meta and Basic Commands ---
    @register_command(["report status", "what can you do"])
    def report_status_command(self, query):
        """
        Reports the assistant's status and lists available commands.

        Args:
            query (str): The user's command query (unused).
        """
        self.assistant.speak("I am online and ready. I can:")
        command_list_str = ", ".join(sorted(_commands.keys()))
        print(f"Available commands: {command_list_str}")
        self.assistant.speak(command_list_str)

    @register_command(["time"])
    def tell_time(self, query):
        """
        Tells the current time.

        Args:
            query (str): The user's command query (unused).
        """
        self.assistant.speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")

    @register_command(["date"])
    def tell_date(self, query):
        """
        Tells the current date.

        Args:
            query (str): The user's command query (unused).
        """
        self.assistant.speak(f"The date is {datetime.datetime.now().strftime('%A, %d %B %Y')}")

    @register_command(["day of the week"])
    def tell_day(self, query):
        """
        Tells the current day of the week.

        Args:
            query (str): The user's command query (unused).
        """
        self.assistant.speak(f"Today is {datetime.datetime.now().strftime('%A')}")

    @register_command(["exit", "stop"])
    def exit_app(self, query):
        """
        Exits the application.

        Args:
            query (str): The user's command query (unused).
        """
        self.assistant.speak("Goodbye!")
        self.assistant.app.quit()

    # --- Website and App Opening ---
    @register_command(["open"])
    def open_command(self, query):
        """
        Opens a website or a local application.

        Examples: "open youtube", "open chrome"

        Args:
            query (str): The user's command, e.g., "open google".
        """
        target = query.replace("open", "").strip()
        sites = {"youtube": "https://www.youtube.com", "wikipedia": "https://www.wikipedia.com", "google": "https://www.google.com", "github": "https://www.github.com"}
        apps = {"excel": "localc", "word": "lowriter", "chrome": "google-chrome", "firefox": "firefox", "settings": "gnome-control-center", "calculator": "gnome-calculator"}

        if target in sites:
            self.assistant.speak(f"Opening {target}...")
            webbrowser.open(sites[target])
        elif target in apps:
            self.assistant.speak(f"Opening {target}...")
            try:
                open_app(target)
            except Exception as e:
                self.assistant.speak(f"Sorry, I could not open {target}.")
                print(f"Error opening app: {e}")
        else:
            self.assistant.speak(f"Sorry, I don't know how to open {target}.")

    # --- Search Commands ---
    @register_command(["search"])
    def search_command(self, query):
        """
        Searches for a term on Google, Wikipedia, or YouTube.

        Example: "search google for cats"

        Args:
            query (str): The search command, e.g., "search wikipedia for Albert Einstein".
        """
        term = query.split("for")[-1].strip()
        if "wikipedia for" in query:
            self.assistant.speak(f"Searching Wikipedia for {term}...")
            webbrowser.open(f"https://en.wikipedia.org/wiki/{term.replace(' ', '_')}")
        elif "google for" in query:
            self.assistant.speak(f"Searching Google for {term}...")
            webbrowser.open(f"https://www.google.com/search?q={term.replace(' ', '+')}")
        elif "youtube for" in query:
            self.assistant.speak(f"Searching YouTube for {term}...")
            webbrowser.open(f"https://www.youtube.com/results?search_query={term.replace(' ', '+')}")
        else:
            self.assistant.speak("Please specify what to search for, like 'search google for cats'.")

    # --- File Management ---
    @register_command(["list files"])
    def list_files(self, query):
        """
        Lists files in the current directory.

        Args:
            query (str): The user's command query (unused).
        """
        path = '.'  # Can be extended to parse a path from the query
        self.assistant.speak("Here are the files in the current directory:")
        try:
            files = os.listdir(path)
            for f in files:
                self.assistant.app.update_textbox(f"- {f}")
        except Exception as e:
            self.assistant.speak(f"Error listing files: {e}")

    @register_command(["create file"])
    def create_file(self, query):
        """
        Creates a file with specified content.

        Example: "create file my_file.txt with content hello world"

        Args:
            query (str): The command containing the file path and content.
        """
        match = re.search(r"create file (.*) with content (.*)", query)
        if match:
            path, content = match.groups()
            try:
                with open(path.strip(), 'w') as f:
                    f.write(content.strip())
                self.assistant.speak(f"File {os.path.basename(path)} created.")
            except Exception as e:
                self.assistant.speak(f"Error creating file: {e}")
        else:
            self.assistant.speak("Please use the format: create file [path] with content [content]")

    @register_command(["delete file"])
    def delete_file(self, query):
        """
        Deletes a specified file after confirmation.

        Example: "delete file my_file.txt"

        Args:
            query (str): The command containing the file path.

        Returns:
            dict or None: A dictionary to trigger confirmation, or None if file not found.
        """
        match = re.search(r"delete file (.*)", query)
        if match:
            path = match.group(1).strip()
            if not os.path.exists(path):
                self.assistant.speak("Sorry, I could not find a file at that path.")
                return None
            return {'action': 'confirm_delete', 'path': path}
        else:
            self.assistant.speak("Please use the format: delete file [path]")

    # --- Fun & Informational ---
    @register_command(["tell me a joke"])
    def tell_joke(self, query):
        """
        Tells a random joke.

        Args:
            query (str): The user's command query (unused).
        """
        jokes = ["Why don't scientists trust atoms? Because they make up everything!"]
        self.assistant.speak(random.choice(jokes))

    @register_command(["tell me a fun fact"])
    def tell_fun_fact(self, query):
        """
        Tells a random fun fact.

        Args:
            query (str): The user's command query (unused).
        """
        facts = ["A group of flamingos is called a 'flamboyance'."]
        self.assistant.speak(random.choice(facts))

    @register_command(["what is your name"])
    def what_is_your_name(self, query):
        """
        States the assistant's name.

        Args:
            query (str): The user's command query (unused).
        """
        self.assistant.speak("My name is JARVIS.")

    # --- Easter Eggs ---
    def handle_easter_eggs(self, query):
        """
        Handles hidden, fun commands (easter eggs).

        Args:
            query (str): The user's full command query.

        Returns:
            bool: True if an easter egg was found and handled, False otherwise.
        """
        eggs = {
            "do a barrel roll": "Okay, here I go! Wee!",
            "make me a sandwich": "What? Make it yourself.",
            "i'm bored": "I can tell you a joke or a fun fact.",
            "are we there yet": "No.",
        }
        for egg, response in eggs.items():
            if egg in query:
                self.assistant.speak(response)
                return True
        return False
