import customtkinter as ctk

# Import Tab Classes
from screen.tabs.tab_ocr import TabOCR
from screen.tabs.tab_classify import TabClassify
from screen.tabs.tab_insight import TabInsight

class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#0F0F0F") # Background utama Hitam Pekat
        self.pack(fill="both", expand=True)

        # ============================================================
        # 1. HEADER AREA (TOMBOL KEMBALI)
        # ============================================================
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        # Tombol Kembali
        self.btn_back = ctk.CTkButton(
            header_frame,
            text="< Menu Utama",
            font=("Roboto", 14, "bold"),
            width=120,
            height=35,
            fg_color="#1F1F1F",     # Abu gelap solid biar jelas
            text_color="#A0A0A0",
            hover_color="#333333",  # Animasi hover
            corner_radius=18,       # Bulat kapsul
            command=self.back_to_menu
        )
        self.btn_back.pack(side="left")

        # ============================================================
        # 2. NAVBAR ANIMASI (CUSTOM TABVIEW)
        # ============================================================
        self.tab_view = ctk.CTkTabview(
            self,
            fg_color="#151515",     # Warna isi konten (Background Tab)
            corner_radius=20,       # Sudut membulat konten
            
            # --- PENGATURAN NAVBAR "FLOATING PILL" ---
            segmented_button_fg_color="#1A1A1A",       # Warna Trek/Wadah Navbar (Gelap)
            segmented_button_selected_color="#7A3DB8", # Warna Ungu Neon (YANG BERGERAK/ANIMASI)
            segmented_button_selected_hover_color="#5A2B8A",
            segmented_button_unselected_color="#1A1A1A", # Samakan dengan trek agar rapi
            segmented_button_unselected_hover_color="#333333", # Efek saat kursor di atas tab lain
            
            text_color="#FFFFFF"
        )
        
        # PENTING: Kita akses komponen internal tombol untuk mempercantik
        # Mengatur agar tombol navbar lebih "gemuk" dan font-nya lebih modern
        self.tab_view._segmented_button.configure(
            font=("Roboto", 15, "bold"),
            corner_radius=25, # Membuat navbar jadi BULAT PENUH (Kapsul)
            height=45         # Lebih tinggi biar elegan
        )

        # Padding agar navbar tidak nempel banget dengan konten
        self.tab_view.pack(fill="both", expand=True, padx=25, pady=(10, 25))

        # --- Tab 1: OCR ---
        tab_ocr_frame = self.tab_view.add("OCR")
        self.tab_ocr = TabOCR(tab_ocr_frame)
        self.tab_ocr.pack(fill="both", expand=True)

        # --- Tab 2: Classification ---
        tab_classify_frame = self.tab_view.add("Classification")
        self.tab_classify = TabClassify(tab_classify_frame)
        self.tab_classify.pack(fill="both", expand=True)

        # --- Tab 3: Insight ---
        tab_insight_frame = self.tab_view.add("Insight")
        self.tab_insight = TabInsight(tab_insight_frame)
        self.tab_insight.pack(fill="both", expand=True)

    def back_to_menu(self):
        """
        Fungsi untuk kembali ke Welcome Screen.
        """
        self.destroy()
        from screen.welcome_screen import WelcomeScreen
        welcome = WelcomeScreen(self.master)
        welcome.pack(fill="both", expand=True)