import os
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

def handle_confirmation(action):
    """Handles the confirmation logic for sensitive actions."""
    if action['action'] == 'confirm_delete':
        path_to_delete = action['path']
        speaker.Speak(f"Are you sure you want to delete the file at {os.path.basename(path_to_delete)}? Please say yes to confirm.")

        print("Waiting for confirmation...")
        confirmation_query = takeCommmand().lower()

        if "yes" in confirmation_query:
            try:
                os.remove(path_to_delete)
                speaker.Speak("The file has been permanently deleted.")
            except Exception as e:
                print(f"Error during confirmed deletion: {e}")
                speaker.Speak("Sorry, an error occurred during the final deletion.")
        else:
            speaker.Speak("Deletion cancelled.")

if __name__ == '__main__':
    speaker.Speak("Hello, I am Jarvis. How can I assist you today?")
    while True:
        print("Listening...")
        query = takeCommmand()
        print("Recognizing...")

        if query != "Some error occurred":
            command_result = commands.handle_command(query)

            if isinstance(command_result, dict):
                # This is a confirmation action
                handle_confirmation(command_result)
            elif command_result is False:
                # No command was found
                # speaker.Speak("Sorry, I don't understand that command.")
                pass
            # If command_result is True, we do nothing, as the command has already run.
