import speech_recognition as sr
import win32com.client
import commands

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
            print(f"Speech recognition error: {e}")
            return "Some error occurred"

if __name__ == '__main__':
    speaker.Speak("Hello, I am Jarvis. How can I assist you today?")
    while True:
        print("Listening...")
        query = takeCommmand()
        print("Recognizing...")

        if query != "Some error occurred":
            if not commands.handle_command(query):
                # You can add a default response if no command is matched
                # speaker.Speak("Sorry, I don't understand that command.")
                pass
