import speech_recognition as sr
from playsound import playsound
import win32com.client
import webbrowser
import datetime
from AppOpener import open

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
                 ["Google", "https://www.google.com"], ]
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
        if "time".lower() in query.lower():
            strftime = datetime.datetime.now().strftime("%H:%M:%S")
            speaker.Speak(f"Sir the time is{strftime}")

        # Open Application
        apps = ["WhatsApp", "excel", "Word","chrome","firefox","settings"]
        for i in range(len(apps)):
            if f"open {apps[i]}".lower() in query.lower():
                speaker.Speak(f"Opening {apps[i]} sir..")
                open(apps[i].lower())  # Opens whatsapp

    #speaker.Speak(query)
