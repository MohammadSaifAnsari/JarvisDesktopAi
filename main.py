import speech_recognition as sr
from playsound import playsound
import win32com.client
import webbrowser
import datetime
from AppOpener import open as open_app

speaker = win32com.client.Dispatch("SAPI.SpVoice")


def takeCommmand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        # r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error occurred"


while 1:
    # print("Enter the word you want to speak by the computer")
    # s = input()
    speaker.Speak("Hello I am AI How can i help you")
    while True:
        print("Listening...")
        query = takeCommmand()
        print("Recog..")

        # Add more sites
        sites = [["YouTube", "https://www.youtube.com"], ["Wikipedia", "https://www.wikipedia.com"],
                 ["Google", "https://www.google.com"], ["Facebook", "https://www.facebook.com"], ["Twitter", "https://www.twitter.com"],
                 ["Instagram", "https://www.instagram.com"], ["LinkedIn", "https://www.linkedin.com"],
                 ["Reddit", "https://www.reddit.com"], ["Amazon", "https://www.amazon.com"], ["Netflix", "https://www.netflix.com"],
                 ["Gmail", "https://www.gmail.com"], ["Yahoo", "https://www.yahoo.com"], ["Outlook", "https://www.outlook.com"],
                 ["eBay", "https://www.ebay.com"], ["Stack Overflow", "https://www.stackoverflow.com"],
                 ["GitHub", "https://www.github.com"],
                 ["Pinterest", "https://www.pinterest.com"], ["Tumblr", "https://www.tumblr.com"], ["BBC News", "https://www.bbc.com/news"],
                 ["CNN", "https://www.cnn.com"], ["The New York Times", "https://www.nytimes.com"], ["ESPN", "https://www.espn.com"],
                 ["National Geographic", "https://www.nationalgeographic.com"]]

        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} sir..")
                # getting path
                firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
                # First registers the new browser
                webbrowser.register('firefox', None,
                                    webbrowser.BackgroundBrowser(firefox_path))
                webbrowser.get('firefox').open(site[1])

        # Play music
        if "open music" in query:
            playsound('C:/Users/s.k.f.ansari/Downloads/Lemon Fight.mp3')

        # Tell Time
        elif "time".lower() in query.lower():
            strftime = datetime.datetime.now().strftime("%H:%M:%S")
            speaker.Speak(f"Sir the time is{strftime}")

        # Tell Date
        elif "date".lower() in query.lower():
            strdate = datetime.datetime.now().strftime("%d %B %Y")
            speaker.Speak(f"Sir the date is {strdate}")

        # Tell Day
        elif "day".lower() in query.lower():
            strday = datetime.datetime.now().strftime("%A")
            speaker.Speak(f"Sir the day is {strday}")

        # Search on Google
        elif "search on google" in query.lower():
            speaker.Speak("What do you want to search on Google?")
            search_query = takeCommmand()
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.get('firefox').open(url)

        # Search on YouTube
        elif "search on youtube" in query.lower():
            speaker.Speak("What do you want to search on YouTube?")
            search_query = takeCommmand()
            url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.get('firefox').open(url)

        # Tell a joke
        elif "tell me a joke" in query.lower():
            speaker.Speak("Why don't scientists trust atoms? Because they make up everything!")

        # Ask for name
        elif "what is your name" in query.lower():
            speaker.Speak("My name is AI.")

        # Ask who created me
        elif "who created you" in query.lower():
            speaker.Speak("I was created by a developer.")

        # Say hello
        elif "hello" in query.lower():
            speaker.Speak("Hello Sir, how are you?")

        # Say goodbye
        elif "goodbye" in query.lower():
            speaker.Speak("Goodbye Sir, have a nice day.")
            break

        # Open Application
        # The application names are best-guesses. AppOpener is a Windows-only library and could not be tested in the development environment.
        apps = ["WhatsApp", "excel", "word", "chrome", "firefox", "settings", "calculator", "notepad", "paint",
                "command prompt", "powershell", "task manager", "file explorer", "control panel", "snipping tool",
                "vlc", "spotify", "discord", "slack", "zoom", "skype", "visual studio code", "sublime text", "atom", "photoshop",
                "illustrator"]
        for i in range(len(apps)):
            if f"open {apps[i]}".lower() in query.lower():
                speaker.Speak(f"Opening {apps[i]} sir..")
                open_app(apps[i].lower())

    # speaker.Speak(query)
