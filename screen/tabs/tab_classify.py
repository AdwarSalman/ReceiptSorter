"""
tab_classify.py
----------------
Tab ini berfungsi untuk:
1. Menerima input teks (hasil OCR atau manual)
2. Melakukan klasifikasi kategori menggunakan:
   - Best-First Search (heuristic kecocokan kata kunci)
3. Menampilkan skor kategori dan kategori terbaik
4. Menjalankan reasoning (Backward Chaining):
   - Menampilkan token kunci yang menyebabkan kategori tersebut dipilih
"""

import customtkinter as ctk

from core.search_classifier import classify_text
from core.backward_chain import backward_reasoning


class TabClassify(ctk.CTkFrame):
    """
    Kelas TabClassify menyediakan interface untuk:
    - Memasukkan teks (dari OCR atau input manual)
    - Menjalankan proses klasifikasi
    - Menampilkan hasil
    """

    def __init__(self, master):
        super().__init__(master, fg_color="#101010")

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -------------------------------------------------------------
        # FRAME KIRI: INPUT TEKS
        # -------------------------------------------------------------
        left_frame = ctk.CTkFrame(self, fg_color="#181818", corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        title_left = ctk.CTkLabel(
            left_frame,
            text="Input Text for Classification",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_left.pack(pady=(15, 10))

        # Textbox input
        self.input_box = ctk.CTkTextbox(
            left_frame,
            width=350,
            height=420,
            fg_color="#202020",
            text_color="#DDDDDD",
            font=ctk.CTkFont(size=14)
        )
        self.input_box.pack(padx=10, pady=10, fill="both", expand=True)

        # Tombol klasifikasi
        classify_btn = ctk.CTkButton(
            left_frame,
            text="Run Classification",
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            command=self.run_classification
        )
        classify_btn.pack(pady=10)

        # -------------------------------------------------------------
        # FRAME KANAN: HASIL KLASIFIKASI
        # -------------------------------------------------------------
        right_frame = ctk.CTkFrame(self, fg_color="#181818", corner_radius=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        title_right = ctk.CTkLabel(
            right_frame,
            text="Classification Result",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_right.pack(pady=(15, 10))

        # Textbox untuk output AI
        self.result_box = ctk.CTkTextbox(
            right_frame,
            width=350,
            height=420,
            fg_color="#202020",
            text_color="#DDDDDD",
            font=ctk.CTkFont(size=14)
        )
        self.result_box.pack(padx=10, pady=10, fill="both", expand=True)

    # ======================================================================
    # FUNCTION: RUN CLASSIFICATION
    # ======================================================================
    def run_classification(self):
        """
        - Ambil teks dari input box
        - Jalankan classify_text() → Best-First Search
        - Jalankan backward_reasoning() → token yang relevan
        - Tampilkan:
            * Skor tiap kategori
            * Kategori terbaik
            * Token kunci hasil reasoning
        """
        text = self.input_box.get("0.0", "end").strip()

        if not text:
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", "ERROR: Text input is empty.")
            return

        # STEP 1 → Klasifikasi dengan heuristic
        best_category, score_table = classify_text(text)

        # STEP 2 → Reasoning backward chaining
        reasoning_tokens = backward_reasoning(text, best_category)

        # Susun output yang rapi
        output = "=== CLASSIFICATION RESULT ===\n\n"
        output += "Kategori terbaik: " + best_category.upper() + "\n\n"

        output += "--- Skor per kategori ---\n"
        for k, v in score_table.items():
            output += f"{k:<20} : {v}\n"

        output += "\n--- Reasoning (Backward Chaining) ---\n"
        if reasoning_tokens:
            output += "Token pendukung kategori:\n"
            for token in reasoning_tokens:
                output += f" - {token}\n"
        else:
            output += "Tidak ditemukan token pendukung.\n"

        # Munculkan di textbox
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", output)
