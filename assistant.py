import speech_recognition as sr
import pyttsx3
import threading
from commands import CommandManager

class Assistant:
    def __init__(self, app):
        self.app = app
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.voices = self.engine.getProperty('voices')
        self.command_manager = CommandManager(self)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        self.app.update_textbox(f"AI: {text}")

    def take_command(self):
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
        self.speak("Hello, I am JARVIS. How can I help you?")
        while True:
            query = self.take_command().lower()
            if not query:
                continue

            if not self.command_manager.handle_command(query):
                self.speak("Sorry, I don't understand that command.")

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
