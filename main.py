import customtkinter as ctk
from screen.welcome_screen import WelcomeScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ReceiptSorter – AI Receipt Categorization")
        self.geometry("1200x700")

        # Tampilkan welcome screen
        welcome = WelcomeScreen(self)
        welcome.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
