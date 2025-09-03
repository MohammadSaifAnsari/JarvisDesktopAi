import customtkinter as ctk
from assistant import Assistant

class App(ctk.CTk):
    def __init__(self):
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
        self.button.configure(state="disabled", text="Listening...")
        self.assistant.start()

    def update_textbox(self, text):
        self.textbox.insert("end", text + "\n")
        self.textbox.see("end")

    def update_status(self, text):
        self.status_label.configure(text=f"Status: {text}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
