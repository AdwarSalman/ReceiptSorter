import customtkinter as ctk
from core.search_classifier import classify_text
from core.backward_chain import backward_reasoning

class TabClassify(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent") # Ikut warna background utama

        # Layout Grid 50:50
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================================
        # KARTU KIRI: INPUT TEKS
        # ==========================================================
        left_card = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=15, border_width=1, border_color="#333333")
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        left_card.grid_columnconfigure(0, weight=1)
        left_card.grid_rowconfigure(1, weight=1)

        # Header
        lbl_left = ctk.CTkLabel(left_card, text="⌨️ Input Teks Struk", font=("Roboto", 18, "bold"), text_color="#FFFFFF")
        lbl_left.grid(row=0, column=0, pady=20)

        # Textbox Input (Background sedikit lebih gelap dari kartu)
        self.input_box = ctk.CTkTextbox(
            left_card,
            font=("Roboto", 14),
            fg_color="#151515",
            text_color="#E0E0E0",
            corner_radius=10,
            border_width=1,
            border_color="#333333"
        )
        self.input_box.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        # Tombol Klasifikasi (Warna Utama/Primary)
        classify_btn = ctk.CTkButton(
            left_card,
            text="🔍 Analisis Kategori",
            font=("Roboto", 15, "bold"),
            height=45,
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            corner_radius=20, # Lebih bulat
            command=self.run_classification
        )
        classify_btn.grid(row=2, column=0, padx=20, pady=(0, 25), sticky="ew")

        # ==========================================================
        # KARTU KANAN: HASIL KLASIFIKASI
        # ==========================================================
        right_card = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=15, border_width=1, border_color="#333333")
        right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        right_card.grid_columnconfigure(0, weight=1)
        right_card.grid_rowconfigure(1, weight=1)

        # Header
        lbl_right = ctk.CTkLabel(right_card, text="📊 Hasil & Reasoning AI", font=("Roboto", 18, "bold"), text_color="#FFFFFF")
        lbl_right.grid(row=0, column=0, pady=20)

        # Textbox Output (Menggunakan Font Monospace 'Consolas' agar tabel rapi)
        self.result_box = ctk.CTkTextbox(
            right_card,
            font=("Consolas", 14), 
            fg_color="#151515",
            text_color="#00E676", # Warna hijau matrix/terminal
            corner_radius=10,
            border_width=1,
            border_color="#333333"
        )
        self.result_box.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 25))

    def run_classification(self):
        text = self.input_box.get("0.0", "end").strip()

        if not text:
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", "⚠️ ERROR: Text input is empty.")
            return

        # STEP 1 → Klasifikasi dengan heuristic
        best_category, score_table = classify_text(text)

        # STEP 2 → Reasoning backward chaining
        reasoning_tokens = backward_reasoning(text, best_category)

        # Susun output yang rapi
        output = "=== CLASSIFICATION RESULT ===\n\n"
        output += f"🏆 KATEGORI TERBAIK: {best_category.upper()}\n"
        output += "="*30 + "\n\n"

        output += "--- Skor per Kategori ---\n"
        # Format tabel rapi
        for k, v in score_table.items():
            output += f"{k.ljust(25)} : {v}\n"

        output += "\n--- Reasoning (Why?) ---\n"
        if reasoning_tokens:
            output += "Token kata kunci ditemukan:\n"
            for token in reasoning_tokens:
                output += f" ✅ {token}\n"
        else:
            output += "⚠️ Tidak ditemukan keyword spesifik.\n(Skor mungkin 0 atau default)\n"

        # Munculkan di textbox
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", output)