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
    """A decorator to register a new command."""
    def decorator(func):
        for keyword in keywords:
            _commands[keyword.lower()] = func
        return func
    return decorator

class CommandManager:
    def __init__(self, assistant):
        self.assistant = assistant
        self.nlp = None
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Spacy 'en_core_web_sm' model not found. Run 'python -m spacy download en_core_web_sm'")
            self.assistant.speak("The natural language processing model is not loaded. Some commands may not work.")

        # Register all command methods
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'is_command'):
                keywords = getattr(attr, 'keywords')
                for keyword in keywords:
                    _commands[keyword.lower()] = attr

    def handle_command(self, query):
        """
        Finds and executes a command based on the query.
        Returns:
        - A dictionary for confirmation actions.
        - True for successful direct commands.
        - False if no command was found.
        """
        query = query.lower()
        if self.handle_easter_eggs(query):
            return True

        for keyword, func in _commands.items():
            if query.startswith(keyword):
                result = func(query)
                if isinstance(result, dict):
                    # Handle confirmation actions, e.g., for file deletion
                    self.handle_confirmation(result)
                return True
        return False

    def handle_confirmation(self, action):
        """Handles the confirmation logic for sensitive actions."""
        if action['action'] == 'confirm_delete':
            path_to_delete = action['path']
            self.assistant.speak(f"Are you sure you want to delete the file at {os.path.basename(path_to_delete)}? Please say yes to confirm.")

            # This requires a way to get a one-off response.
            # For now, we will proceed with a placeholder response.
            # In a real scenario, this would need to listen for a specific "yes" response.
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
        self.assistant.speak("I am online and ready. I can:")
        command_list_str = ", ".join(sorted(_commands.keys()))
        print(f"Available commands: {command_list_str}")
        self.assistant.speak(command_list_str)

    @register_command(["time"])
    def tell_time(self, query):
        self.assistant.speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")

    @register_command(["date"])
    def tell_date(self, query):
        self.assistant.speak(f"The date is {datetime.datetime.now().strftime('%A, %d %B %Y')}")

    @register_command(["day of the week"])
    def tell_day(self, query):
        self.assistant.speak(f"Today is {datetime.datetime.now().strftime('%A')}")

    @register_command(["exit", "stop"])
    def exit_app(self, query):
        self.assistant.speak("Goodbye!")
        self.assistant.app.quit()

    # --- Website and App Opening ---
    @register_command(["open"])
    def open_command(self, query):
        target = query.replace("open", "").strip()
        sites = {"youtube": "https://www.youtube.com", "wikipedia": "https://www.wikipedia.com", "google": "https://www.google.com", "github": "https://www.github.com"}
        apps = {"excel": "localc", "word": "lowriter", "chrome": "google-chrome", "firefox": "firefox", "settings": "gnome-control-center", "calculator": "gnome-calculator"}

        if target in sites:
            self.assistant.speak(f"Opening {target}...")
            webbrowser.open(sites[target])
        elif target in apps:
            self.assistant.speak(f"Opening {target}...")
            # Using open_app for wider compatibility
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
        path = '.' # Or parse from query
        self.assistant.speak("Here are the files in the current directory:")
        try:
            files = os.listdir(path)
            for f in files:
                self.assistant.app.update_textbox(f"- {f}")
        except Exception as e:
            self.assistant.speak(f"Error listing files: {e}")

    @register_command(["create file"])
    def create_file(self, query):
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
            self.assistant.speak("Format: create file [path] with content [content]")

    @register_command(["delete file"])
    def delete_file(self, query):
        match = re.search(r"delete file (.*)", query)
        if match:
            path = match.group(1).strip()
            if not os.path.exists(path):
                self.assistant.speak("Sorry, I could not find a file at that path.")
                return None
            # Return dict for confirmation
            return {'action': 'confirm_delete', 'path': path}
        else:
            self.assistant.speak("Format: delete file [path]")

    # --- Fun & Informational ---
    @register_command(["tell me a joke"])
    def tell_joke(self, query):
        jokes = ["Why don't scientists trust atoms? Because they make up everything!"]
        self.assistant.speak(random.choice(jokes))

    @register_command(["tell me a fun fact"])
    def tell_fun_fact(self, query):
        facts = ["A group of flamingos is called a 'flamboyance'."]
        self.assistant.speak(random.choice(facts))

    @register_command(["what is your name"])
    def what_is_your_name(self, query):
        self.assistant.speak("My name is JARVIS.")

    # --- Easter Eggs ---
    def handle_easter_eggs(self, query):
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
