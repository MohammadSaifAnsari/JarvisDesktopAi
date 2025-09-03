import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import threading
import random
import platform
import subprocess
import re
import psutil
import time
import pwd
import socket
import shutil
import sys
import string
import pyperclip

class Assistant:
    def __init__(self, app):
        self.app = app
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.voices = self.engine.getProperty('voices')
        self.todo_list = []
        self.capitals = {"france": "paris", "germany": "berlin", "japan": "tokyo", "united states": "washington d.c.", "canada": "ottawa", "united kingdom": "london", "china": "beijing", "india": "new delhi"}
        self.conversion_rates = {
            ("inches", "cm"): 2.54, ("cm", "inches"): 1/2.54,
            ("feet", "meters"): 0.3048, ("meters", "feet"): 1/0.3048,
            ("miles", "km"): 1.60934, ("km", "miles"): 1/1.60934,
            ("pounds", "kg"): 0.453592, ("kg", "pounds"): 1/0.453592,
        }
        self.jokes = ["Why don't scientists trust atoms? Because they make up everything!"]
        self.fun_facts = ["A group of flamingos is called a 'flamboyance'."]
        self.quotes = ["The only way to do great work is to love what you do. - Steve Jobs"]
        self.stories = ["Once upon a time, in a land of code and circuits, a young AI dreamed of speaking to the world."]
        self.riddles = {"What has to be broken before you can use it?": "An egg"}

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
            if not query: continue
            if self.route_command(query): continue

    def route_command(self, query):
        handlers = {
            "open ": self.handle_open_commands, "search ": self.handle_search_commands,
            "tell me ": self.handle_tell_me, "what": self.handle_what_is,
            "calculate": self.handle_calculate, "remind me to": self.handle_reminder,
            "set an alarm for": self.handle_alarm, "change ": self.handle_change,
            "convert ": self.handle_unit_conversion, "count words in": self.handle_count_words,
            "reverse": self.handle_reverse, "say": self.handle_say,
            "pick a number": self.handle_pick_number, "generate a password": self.handle_password_generator,
            "add ": self.handle_todo_list_commands, "what's on my to-do list": self.handle_todo_list_commands,
            "remove ": self.handle_todo_list_commands, "clear my to-do list": self.handle_todo_list_commands,
            "copy ": self.handle_clipboard, "paste from clipboard": self.handle_clipboard,
            "rename ": self.handle_file_commands, "list files": self.handle_file_commands,
            "move ": self.handle_file_commands, "file size": self.handle_file_commands,
            "last modified": self.handle_file_commands,
            "time": lambda q: self.speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}"),
            "date": lambda q: self.speak(f"The date is {datetime.datetime.now().strftime('%A, %d %B %Y')}"),
            "day of the week": lambda q: self.speak(f"Today is {datetime.datetime.now().strftime('%A')}"),
            "clear screen": self.handle_clear_screen,
            "how are you": lambda q: self.speak("I am functioning as expected. Thanks for asking!"),
            "are you an ai": lambda q: self.speak("Yes, I am a simple AI assistant."),
            "thank you": lambda q: self.speak("You're welcome!"),
            "who are you": lambda q: self.handle_tell_me("tell me about yourself"),
            "exit": lambda q: (self.speak("Goodbye!"), self.app.quit()),
            "stop": lambda q: (self.speak("Goodbye!"), self.app.quit()),
        }
        if self.handle_easter_eggs(query): return True
        for keyword, handler in handlers.items():
            if query.startswith(keyword):
                handler(query); return True
        return False

    def handle_open_commands(self, query):
        target = query.replace("open ", "").strip()
        sites = {"youtube": "https://www.youtube.com", "wikipedia": "https://www.wikipedia.com", "google": "https://www.google.com", "github": "https://www.github.com", "stack overflow": "https://www.stackoverflow.com", "reddit": "https://www.reddit.com", "twitter": "https://www.twitter.com", "x": "https://www.twitter.com", "amazon": "https://www.amazon.com", "netflix": "https://www.netflix.com", "linkedin": "https://www.linkedin.com", "instagram": "https://www.instagram.com", "facebook": "https://www.facebook.com", "imdb": "https://www.imdb.com", "ebay": "https://www.ebay.com", "pinterest": "https://www.pinterest.com", "twitch": "https://www.twitch.tv", "bbc news": "https://www.bbc.com/news"}
        apps = {"excel": "localc", "word": "lowriter", "chrome": "google-chrome", "firefox": "firefox", "settings": "gnome-control-center", "calculator": "gnome-calculator", "text editor": "gedit"}
        if target in sites: self.speak(f"Opening {target}..."); webbrowser.open(sites[target])
        elif target in apps: self.speak(f"Opening {target}..."); os.system(apps[target])
        else: self.speak(f"Sorry, I don't know how to open {target}.")

    def handle_search_commands(self, query):
        term = query.split("for")[-1].strip()
        if "wikipedia for" in query: self.speak(f"Searching Wikipedia..."); webbrowser.open(f"https://en.wikipedia.org/wiki/{term.replace(' ', '_')}")
        elif "amazon for" in query: self.speak(f"Searching Amazon..."); webbrowser.open(f"https://www.amazon.com/s?k={term.replace(' ', '+')}")
        elif "google for" in query: self.speak(f"Searching Google..."); webbrowser.open(f"https://www.google.com/search?q={term.replace(' ', '+')}")
        elif "youtube for" in query: self.speak(f"Searching YouTube..."); webbrowser.open(f"https://www.youtube.com/results?search_query={term.replace(' ', '+')}")

    def handle_file_commands(self, query):
        try:
            if "list files" in query: self.speak("Files:"); [self.app.update_textbox(f"- {f}") for f in os.listdir('.')]
            elif "rename" in query: match = re.search(r"rename (.*) to (.*)", query); os.rename(match.group(1).strip(), match.group(2).strip()) if match else self.speak("Format: rename [old] to [new]"); self.speak("Renamed.")
            elif "copy" in query: match = re.search(r"copy (.*) to (.*)", query); shutil.copy(match.group(1).strip(), match.group(2).strip()) if match else self.speak("Format: copy [source] to [destination]"); self.speak("Copied.")
            elif "move" in query: match = re.search(r"move (.*) to (.*)", query); shutil.move(match.group(1).strip(), match.group(2).strip()) if match else self.speak("Format: move [source] to [destination]"); self.speak("Moved.")
            elif "file size" in query: match = re.search(r"size of (.*)", query); self.speak(f"Size is {os.path.getsize(match.group(1).strip())} bytes.") if match else self.speak("Format: file size of [filename]")
            elif "last modified" in query: match = re.search(r"modified date of (.*)", query); self.speak(f"Modified: {datetime.datetime.fromtimestamp(os.path.getmtime(match.group(1).strip()))}") if match else self.speak("Format: last modified date of [filename]")
        except Exception as e: self.speak(f"File operation failed: {e}")

    def handle_todo_list_commands(self, query):
        if "add" in query:
            match = re.search(r"add '(.*)' to my to-do list", query)
            if match: self.todo_list.append(match.group(1)); self.speak("Added.")
        elif "what's on" in query:
            if self.todo_list: self.speak("To-do list:"); [self.app.update_textbox(f"- {item}") for item in self.todo_list]
            else: self.speak("Your to-do list is empty.")
        elif "remove" in query:
            match = re.search(r"remove '(.*)' from my to-do list", query)
            if match and match.group(1) in self.todo_list: self.todo_list.remove(match.group(1)); self.speak("Removed.")
            else: self.speak("Item not found.")
        elif "clear" in query: self.todo_list.clear(); self.speak("To-do list cleared.")

    def handle_tell_me(self, query):
        if "joke" in query: self.speak(random.choice(self.jokes))
        elif "fun fact" in query: self.speak(random.choice(self.fun_facts))
        elif "quote" in query: self.speak(random.choice(self.quotes))
        elif "story" in query: self.speak(random.choice(self.stories))
        elif "riddle" in query:
            riddle, answer = random.choice(list(self.riddles.items()))
            self.speak(riddle); self.speak(f"The answer is... {answer}")
        elif "about yourself" in query: self.speak("I am a desktop voice assistant named JARVIS. I can perform a variety of tasks, from opening websites to telling jokes and managing files. I am constantly learning and evolving.")

    def handle_what_is(self, query):
        if "your name" in query: self.speak("My name is JARVIS.")
        elif "ip address" in query: self.speak(f"IP: {subprocess.check_output(['curl', '-s', 'ifconfig.me']).decode('utf-8').strip()}")
        elif "python version" in query: self.speak(f"Python version: {sys.version}")
        elif "capital of" in query:
            match = re.search(r"capital of (.*)", query)
            if match and match.group(1) in self.capitals: self.speak(f"The capital is {self.capitals[match.group(1)]}.")
            else: self.speak("I don't know that capital.")
        elif "memory usage" in query: self.speak(f"Memory: {psutil.virtual_memory().percent}% used.")
        elif "cpu usage" in query: self.speak(f"CPU: {psutil.cpu_percent()}% used.")
        elif "battery" in query:
            battery = psutil.sensors_battery()
            if battery: self.speak(f"Battery: {battery.percent}% {'(charging)' if battery.power_plugged else ''}")
            else: self.speak("No battery detected.")
        else: self.speak("I'm not sure what that is.")

    def handle_calculate(self, query):
        match = re.search(r"calculate (.*)", query)
        if match:
            expression = match.group(1).strip().replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
            try:
                if not re.match(r"^[\d\s\.\+\-\*\/()]+$", expression): raise ValueError("Invalid characters")
                result = eval(expression); self.speak(f"The result is {result}")
            except: self.speak("Sorry, I can't calculate that.")
        else: self.speak("Format: calculate 5 plus 5")

    def handle_reminder(self, query):
        match = re.search(r"remind me to (.*) in (\d+) (seconds|second|minutes|minute)", query)
        if match:
            task, time_val, unit = match.groups()
            time_in_seconds = int(time_val) * (60 if unit.startswith("minute") else 1)
            self.speak(f"Okay, reminder set for {time_val} {unit}.")
            threading.Timer(time_in_seconds, lambda: self.speak(f"Reminder: It's time to {task}!")).start()
        else: self.speak("Format: remind me to [task] in [number] [seconds/minutes]")

    def handle_alarm(self, query):
        match = re.search(r"(\d{1,2}):(\d{2}) ?(am|pm)?", query)
        if match:
            hour, minute, am_pm = match.groups(); hour, minute = int(hour), int(minute)
            if am_pm == "pm" and hour < 12: hour += 12
            if am_pm == "am" and hour == 12: hour = 0
            now = datetime.datetime.now(); alarm_time = now.replace(hour=hour, minute=minute, second=0)
            if alarm_time < now: alarm_time += datetime.timedelta(days=1)
            delta = (alarm_time - now).total_seconds()
            threading.Timer(delta, lambda: self.speak("Alarm! It's time!")).start()
            self.speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}.")
        else: self.speak("Format: set an alarm for HH:MM am/pm")

    def handle_change(self, query):
        if "voice" in query:
            current_voice_id = self.engine.getProperty('voice')
            new_voice_id = self.voices[1].id if len(self.voices) > 1 and current_voice_id == self.voices[0].id else self.voices[0].id
            self.engine.setProperty('voice', new_voice_id); self.speak("I have changed my voice.")
        elif "speaking rate" in query:
            if "fast" in query: self.engine.setProperty('rate', 200)
            elif "slow" in query: self.engine.setProperty('rate', 100)
            else: self.engine.setProperty('rate', 150)
            self.speak("My speaking rate has been updated.")

    def handle_unit_conversion(self, query):
        match = re.search(r"convert ([\d\.]+) (.*) to (.*)", query)
        if match:
            val, unit_from, unit_to = match.groups(); val = float(val)
            if (unit_from, unit_to) in self.conversion_rates: self.speak(f"{val} {unit_from} is {val * self.conversion_rates[(unit_from, unit_to)]:.2f} {unit_to}.")
            elif (unit_to, unit_from) in self.conversion_rates: self.speak(f"{val} {unit_from} is {val / self.conversion_rates[(unit_to, unit_from)]:.2f} {unit_to}.")
            elif unit_from == "fahrenheit" and unit_to == "celsius": self.speak(f"{val} Fahrenheit is {(val - 32) * 5/9:.2f} Celsius.")
            elif unit_from == "celsius" and unit_to == "fahrenheit": self.speak(f"{val} Celsius is {(val * 9/5) + 32:.2f} Fahrenheit.")
            else: self.speak("I don't know how to convert between those units.")
        else: self.speak("Format: convert [value] [unit] to [unit]")

    def handle_count_words(self, query):
        match = re.search(r"count words in '(.*)'", query)
        if match: self.speak(f"There are {len(match.group(1).split())} words.")
        else: self.speak("Format: count words in 'your sentence'")

    def handle_reverse(self, query):
        match = re.search(r"reverse '(.*)'", query)
        if match: self.speak(match.group(1)[::-1])
        else: self.speak("Format: reverse 'your text'")

    def handle_say(self, query):
        match = re.search(r"say '(.*)'", query)
        if match: self.speak(match.group(1))

    def handle_pick_number(self, query):
        match = re.search(r"pick a number between (\d+) and (\d+)", query)
        if match: start, end = map(int, match.groups()); self.speak(f"I pick {random.randint(start, end)}")
        else: self.speak("Format: pick a number between X and Y")

    def handle_password_generator(self, query):
        match = re.search(r"(\d+)", query); length = int(match.group(1)) if match else 12
        chars = string.ascii_letters + string.digits + string.punctuation
        self.speak(f"Password: {''.join(random.choice(chars) for _ in range(length))}")

    def handle_clipboard(self, query):
        if "copy" in query:
            match = re.search(r"copy '(.*)'", query)
            if match: pyperclip.copy(match.group(1)); self.speak("Copied.")
        elif "paste" in query: self.speak(f"Clipboard: {pyperclip.paste()}")

    def handle_clear_screen(self, query=None): self.app.clear_textbox(); self.speak("Screen cleared.")

    def handle_easter_eggs(self, query):
        eggs = {
            "do a barrel roll": "Okay, here I go! Wee!", "make me a sandwich": "What? Make it yourself.",
            "i'm bored": "I can tell you a joke, a fun fact, a story, or a riddle.", "tell me your secrets": "I'm not telling you. It's a secret.",
            "first rule of fight club": "We don't talk about Fight Club.", "beam me up": "I'm sorry Captain, I can't do that.",
            "are we there yet": "No.", "what is love": "Baby don't hurt me, don't hurt me, no more.",
            "can you rap": "I'm the AI in the machine, my responses are clean. Got a query? Just ask, I'm a multitasking machine."
        }
        for egg, response in eggs.items():
            if egg in query: self.speak(response); return True
        return False

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
