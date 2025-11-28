import customtkinter as ctk
from screen.main_window import MainWindow

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#0F0F0F") # Background utama gelap pekat

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Card Container di Tengah ---
        # Memberikan kesan "mengambang"
        container = ctk.CTkFrame(
            self, 
            fg_color="#181818", 
            corner_radius=20,
            border_width=2,
            border_color="#2A2A2A" # Border halus
        )
        container.grid(row=0, column=0, sticky="ns", padx=50, pady=50)

        # Grid config untuk container
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # --- 1. Logo / Icon Placeholder ---
        # Karena kita tidak pakai gambar eksternal, kita buat "Logo" dari Text
        logo_frame = ctk.CTkFrame(container, fg_color="#7A3DB8", width=80, height=80, corner_radius=40)
        logo_frame.grid(row=0, column=0, pady=(40, 0))
        logo_label = ctk.CTkLabel(logo_frame, text="RS", font=("Arial", 32, "bold"), text_color="white")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- 2. Judul Utama ---
        title = ctk.CTkLabel(
            container,
            text="ReceiptSorter AI",
            font=ctk.CTkFont(family="Roboto", size=36, weight="bold"),
            text_color="white"
        )
        title.grid(row=1, column=0, pady=(10, 5))

        # --- 3. Deskripsi ---
        subtitle = ctk.CTkLabel(
            container,
            text="Kelola Struk Belanja Anda\ndengan Kekuatan AI & OCR",
            font=ctk.CTkFont(family="Roboto", size=16),
            text_color="#A0A0A0",
            justify="center"
        )
        subtitle.grid(row=2, column=0, pady=(0, 20))

        # --- 4. Tombol Start Modern ---
        start_btn = ctk.CTkButton(
            container,
            text="MULAI SEKARANG",
            width=220,
            height=50,
            corner_radius=25, # Tombol bulat (pill shape)
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            command=self.start_app
        )
        start_btn.grid(row=3, column=0, pady=(0, 50))

    def start_app(self):
        self.destroy()
        MainWindow(master=self.master)