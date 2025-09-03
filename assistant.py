import speech_recognition as sr
# from playsound3 import playsound
import pyttsx3
import webbrowser
import datetime
import os
import threading

class Assistant:
    def __init__(self, app):
        self.app = app
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

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
            except Exception as e:
                self.app.update_status("Error")
                self.speak("Sorry, I could not understand that.")
                return "Some error occurred"

    def run(self):
        self.speak("Hello, I am JARVIS. How can I help you?")
        while True:
            query = self.take_command().lower()

            if "open youtube" in query:
                self.speak("Opening YouTube...")
                webbrowser.open("https://www.youtube.com")
            elif "open wikipedia" in query:
                self.speak("Opening Wikipedia...")
                webbrowser.open("https://www.wikipedia.com")
            elif "open google" in query:
                self.speak("Opening Google...")
                webbrowser.open("https://www.google.com")
            # elif "open music" in query:
            #     self.speak("Playing music...")
            #     playsound('C:/Users/s.k.f.ansari/Downloads/Lemon Fight.mp3')
            elif "time" in query:
                strftime = datetime.datetime.now().strftime("%H:%M:%S")
                self.speak(f"Sir, the time is {strftime}")
            elif "open whatsapp" in query:
                self.speak("Opening WhatsApp...")
                os.system("whatsapp")
            elif "open excel" in query:
                self.speak("Opening Excel...")
                os.system("localc") # LibreOffice Calc
            elif "open word" in query:
                self.speak("Opening Word...")
                os.system("lowriter") # LibreOffice Writer
            elif "open chrome" in query:
                self.speak("Opening Chrome...")
                os.system("google-chrome")
            elif "open firefox" in query:
                self.speak("Opening Firefox...")
                os.system("firefox")
            elif "open settings" in query:
                self.speak("Opening Settings...")
                os.system("gnome-control-center")
            elif "exit" in query or "stop" in query:
                self.speak("Goodbye!")
                self.app.quit()
                break
            else:
                self.speak("I can only perform the programmed tasks.")

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
