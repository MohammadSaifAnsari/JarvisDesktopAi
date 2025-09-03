"""
This module defines the core functionality of the J.A.R.V.I.S. assistant.

It handles speech recognition, text-to-speech, and the main conversation
loop. It integrates with the GUI to provide feedback and display messages.
"""
import speech_recognition as sr
import pyttsx3
import threading
from commands import CommandManager


class Assistant:
    """
    The main class for the voice assistant.

    This class orchestrates the assistant's operations, including listening for
    commands, processing them, and providing spoken responses.

    Attributes:
        app (App): The main application instance for UI updates.
        engine (pyttsx3.Engine): The text-to-speech engine.
        command_manager (CommandManager): The command handler instance.
    """
    def __init__(self, app):
        """
        Initializes the Assistant.

        Args:
            app (App): The main application instance from the GUI.
        """
        self.app = app
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.voices = self.engine.getProperty('voices')
        self.command_manager = CommandManager(self)

    def speak(self, text):
        """
        Converts text to speech and displays the message in the GUI.

        Args:
            text (str): The text to be spoken by the assistant.
        """
        self.engine.say(text)
        self.engine.runAndWait()
        self.app.update_textbox(f"AI: {text}")

    def take_command(self):
        """
        Listens for a user command via the microphone and recognizes it.

        It updates the GUI status to "Listening..." and then "Recognizing...".
        If recognition fails, it returns an empty string.

        Returns:
            str: The recognized command as a string, or an empty string on error.
        """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.app.update_status("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                self.app.update_status("Recognizing...")
                query = r.recognize_google(audio, language="en-in")
                self.app.update_textbox(f"User: {query}")
                return query
            except Exception:
                self.app.update_status("Error")
                return ""

    def run(self):
        """
        The main loop of the assistant.

        It continuously listens for commands and passes them to the
        CommandManager to be handled.
        """
        self.speak("Hello, I am JARVIS. How can I help you?")
        while True:
            query = self.take_command().lower()
            if not query:
                continue

            if not self.command_manager.handle_command(query):
                self.speak("Sorry, I don't understand that command.")

    def start(self):
        """
        Starts the assistant's main loop in a separate thread.

        This allows the GUI to remain responsive while the assistant is running.
        """
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
