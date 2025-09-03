"""
This module contains the graphical user interface for the J.A.R.V.I.S. desktop assistant.

It uses the customtkinter library to create a modern, themed UI. The main window
provides a text box for conversation history, a status label, and a button to
activate the assistant.
"""
import customtkinter as ctk
from assistant import Assistant


class App(ctk.CTk):
    """
    The main application window for the J.A.R.V.I.S. assistant.

    This class initializes the UI components, including the textbox for displaying
    conversation, a status label, and the 'Start Listening' button. It also
    manages the interaction with the Assistant instance.

    Attributes:
        textbox (ctk.CTkTextbox): The text area for showing user and AI messages.
        status_label (ctk.CTkLabel): A label to show the assistant's current status.
        button (ctk.CTkButton): The button to start the voice recognition.
        assistant (Assistant): An instance of the assistant logic.
    """
    def __init__(self):
        """Initializes the main application window and its widgets."""
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("J.A.R.V.I.S")
        self.geometry("400x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(master=self, width=400, height=400)
        self.textbox.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.status_label = ctk.CTkLabel(master=self, text="Status: Idle")
        self.status_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.button = ctk.CTkButton(master=self, text="Start Listening", command=self.start_assistant)
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.assistant = Assistant(self)

    def start_assistant(self):
        """
        Disables the button and starts the assistant's listening thread.

        This method is called when the 'Start Listening' button is clicked. It
        updates the button to show a 'Listening...' state and prevents further clicks
        while the assistant is active.
        """
        self.button.configure(state="disabled", text="Listening...")
        self.assistant.start()

    def update_textbox(self, text):
        """
        Appends a new message to the conversation textbox.

        Args:
            text (str): The text to add to the textbox.
        """
        self.textbox.insert("end", text + "\n")
        self.textbox.see("end")

    def update_status(self, text):
        """
        Updates the status label with a new message.

        Args:
            text (str): The new status text to display.
        """
        self.status_label.configure(text=f"Status: {text}")

    def clear_textbox(self):
        """Clears all text from the conversation textbox."""
        self.textbox.delete("1.0", "end")


if __name__ == "__main__":
    app = App()
    app.mainloop()
