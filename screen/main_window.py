"""
main_window.py
----------------
Window utama aplikasi setelah user menekan tombol Start pada welcome screen.

Berisi:
- TabView (OCR, Classification, Insight)
- Integrasi seluruh modul GUI

Tab:
1. OCR → upload & ekstraksi teks
2. Classification → heuristic search + reasoning
3. Insight → generative AI Gemini chatbot

Semua tab sudah didefinisikan di folder screen/tabs/.
"""

import customtkinter as ctk

# Import Tab Classes
from screen.tabs.tab_ocr import TabOCR
from screen.tabs.tab_classify import TabClassify
from screen.tabs.tab_insight import TabInsight


class MainWindow(ctk.CTkFrame):
    """
    MainWindow adalah container besar yang memuat TabView utama.

    Menggunakan CTkFrame agar bisa diletakkan di root master
    setelah WelcomeScreen dihancurkan.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="#0F0F0F")

        # Atur frame agar memenuhi seluruh window
        self.pack(fill="both", expand=True)

        # ------------------------------------------------------------
        # TAB VIEW UTAMA
        # ------------------------------------------------------------
        self.tab_view = ctk.CTkTabview(
            self,
            fg_color="#151515",
            segmented_button_fg_color="#1E1E1E",
            segmented_button_selected_color="#7A3DB8",
            segmented_button_selected_hover_color="#5A2B8A",
            segmented_button_unselected_color="#2A2A2A",
            segmented_button_unselected_hover_color="#333333",
            text_color="#FFFFFF"
        )

        self.tab_view.pack(fill="both", expand=True, padx=20, pady=20)

        # ------------------------------------------------------------
        # BUAT TAB-TAB
        # ------------------------------------------------------------
        # Tab 1: OCR
        tab_ocr_frame = self.tab_view.add("OCR")
        self.tab_ocr = TabOCR(tab_ocr_frame)

        # Tab 2: Classification
        tab_classify_frame = self.tab_view.add("Classification")
        self.tab_classify = TabClassify(tab_classify_frame)

        # Tab 3: Insight
        tab_insight_frame = self.tab_view.add("Insight")
        self.tab_insight = TabInsight(tab_insight_frame)

        # ------------------------------------------------------------
        # NOTE:
        # Semua Tab adalah CTkFrame yang otomatis tampil dalam TabView.
        # ------------------------------------------------------------
