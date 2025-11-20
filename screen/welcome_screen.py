"""
welcome_screen.py
-----------------
Halaman pertama yang muncul saat aplikasi dijalankan.
Menampilkan:
- Judul aplikasi
- Deskripsi singkat
- Tombol "Start"

Setelah tombol ditekan:
- WelcomeScreen dihancurkan (destroy)
- MainWindow diload (dari screen/main_window.py)
"""

import customtkinter as ctk
from screen.main_window import MainWindow


class WelcomeScreen(ctk.CTkFrame):
    """
    Welcome screen adalah halaman awal sebelum user masuk
    ke program utama. Dibuat sebagai CTkFrame agar mudah
    dihancurkan/diganti dengan window selanjutnya.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="#0F0F0F")

        # Layout stretch
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame utama
        container = ctk.CTkFrame(self, fg_color="#151515", corner_radius=15)
        container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)

        # ------------------------------------------------------------
        # JUDUL BESAR
        # ------------------------------------------------------------
        title = ctk.CTkLabel(
            container,
            text="ReceiptSorter",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        title.grid(row=0, column=0, pady=(60, 10))

        # ------------------------------------------------------------
        # SUBTITLE / DESKRIPSI
        # ------------------------------------------------------------
        subtitle = ctk.CTkLabel(
            container,
            text="Pengelompokan Struk Belanja Berbasis AI dan OCR",
            font=ctk.CTkFont(size=18),
            text_color="#AAAAAA"
        )
        subtitle.grid(row=1, column=0, pady=(10, 20))

        # ------------------------------------------------------------
        # TOMBOL START
        # ------------------------------------------------------------
        start_btn = ctk.CTkButton(
            container,
            text="Start",
            width=180,
            height=45,
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.start_app
        )
        start_btn.grid(row=2, column=0, pady=(40, 60))

    # =================================================================
    #  FUNCTION: MULAI PROGRAM → DARI WELCOME KE MAIN WINDOW
    # =================================================================
    def start_app(self):
        """
        Fungsi ini dipanggil saat tombol Start ditekan.
        - Menghancurkan welcome screen
        - Membuka MainWindow
        """
        self.destroy()  # hilangkan welcome screen

        # Load window utama
        MainWindow(master=self.master)
