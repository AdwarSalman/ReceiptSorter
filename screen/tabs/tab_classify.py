import customtkinter as ctk
from core.search_classifier import classify_text
from core.backward_chain import backward_reasoning

class TabClassify(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

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

        # Textbox Input
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

        # Tombol Klasifikasi
        classify_btn = ctk.CTkButton(
            left_card,
            text="🔍 Analisis Kategori",
            font=("Roboto", 15, "bold"),
            height=45,
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            corner_radius=20,
            command=self.run_classification
        )
        classify_btn.grid(row=2, column=0, padx=20, pady=(0, 25), sticky="ew")

        # ==========================================================
        # KARTU KANAN: HASIL KLASIFIKASI (RICH UI)
        # ==========================================================
        right_card = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=15, border_width=1, border_color="#333333")
        right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        right_card.grid_columnconfigure(0, weight=1)
        right_card.grid_rowconfigure(1, weight=1)

        # Header
        lbl_right = ctk.CTkLabel(right_card, text="📊 Hasil & Reasoning AI", font=("Roboto", 18, "bold"), text_color="#FFFFFF")
        lbl_right.grid(row=0, column=0, pady=20)

        # GANTI TEXTBOX DENGAN SCROLLABLE FRAME
        # Agar bisa memasukkan elemen warna-warni (Label/Button)
        self.result_container = ctk.CTkScrollableFrame(
            right_card,
            fg_color="transparent", # Transparan agar menyatu
            label_text=""
        )
        self.result_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 25))
        self.result_container.grid_columnconfigure(0, weight=1)

        # Placeholder Text awal
        self.placeholder_lbl = ctk.CTkLabel(
            self.result_container, 
            text="Belum ada analisis.\nSilakan masukkan teks & klik tombol.",
            font=("Roboto", 14),
            text_color="gray"
        )
        self.placeholder_lbl.pack(pady=50)

    def run_classification(self):
        text = self.input_box.get("0.0", "end").strip()

        # 1. Bersihkan hasil lama (Clear Widgets)
        for widget in self.result_container.winfo_children():
            widget.destroy()

        if not text:
            err = ctk.CTkLabel(self.result_container, text="⚠️ Teks kosong!", text_color="#FF5252")
            err.pack(pady=20)
            return

        # 2. Jalankan Logika (Sama seperti sebelumnya)
        best_category, score_table = classify_text(text)
        reasoning_tokens = backward_reasoning(text, best_category)

        # ==========================================================
        # 3. RENDER HASIL (BERWARNA & MODERN)
        # ==========================================================
        
        # A. Bagian Judul Kategori (Besar & Berwarna)
        lbl_title = ctk.CTkLabel(
            self.result_container, 
            text="KATEGORI TERBAIK:", 
            font=("Roboto", 12, "bold"), 
            text_color="#AAAAAA"
        )
        lbl_title.pack(anchor="w", pady=(10, 0))

        # Teks Kategori Besar (Hijau Neon seperti Video)
        lbl_category = ctk.CTkLabel(
            self.result_container,
            text=best_category.upper(),
            font=("Arial", 28, "bold"),
            text_color="#00E676" # Warna Hijau Matrix
        )
        lbl_category.pack(anchor="w", pady=(0, 20))

        # B. Divider (Garis Pembatas Halus)
        divider = ctk.CTkFrame(self.result_container, height=2, fg_color="#333333")
        divider.pack(fill="x", pady=(0, 20))

        # C. Bagian Reasoning (List Items)
        lbl_reason = ctk.CTkLabel(
            self.result_container,
            text="🔍 Reasoning (Kata Kunci Ditemukan):",
            font=("Roboto", 14, "bold"),
            text_color="white"
        )
        lbl_reason.pack(anchor="w", pady=(0, 10))

        if reasoning_tokens:
            for token in reasoning_tokens:
                # Buat "Card" kecil untuk setiap token
                token_card = ctk.CTkFrame(self.result_container, fg_color="#2B2B2B", corner_radius=8)
                token_card.pack(fill="x", pady=5)
                
                # Ikon Centang Hijau
                icon = ctk.CTkLabel(token_card, text="✅", font=("Arial", 16))
                icon.pack(side="left", padx=10, pady=8)
                
                # Teks Token
                txt = ctk.CTkLabel(token_card, text=token, font=("Consolas", 14, "bold"), text_color="#E0E0E0")
                txt.pack(side="left", padx=5)
        else:
            # Jika tidak ada token (misal kategori unknown)
            lbl_none = ctk.CTkLabel(
                self.result_container, 
                text="⚠️ Tidak ditemukan kata kunci spesifik.\n(Skor kategori mungkin 0)", 
                text_color="#FFB74D",
                justify="left"
            )
            lbl_none.pack(anchor="w", pady=5)

        # D. Bagian Score Detail (Opsional, dikecilkan di bawah)
        lbl_details = ctk.CTkLabel(
            self.result_container,
            text="\n--- Detail Skor ---",
            font=("Roboto", 12),
            text_color="gray"
        )
        lbl_details.pack(pady=(20, 5))

        # Tampilkan skor dalam label kecil
        scores_str = "\n".join([f"{k}: {v}" for k, v in score_table.items()])
        lbl_scores = ctk.CTkLabel(
            self.result_container,
            text=scores_str,
            font=("Consolas", 11),
            text_color="gray",
            justify="center"
        )
        lbl_scores.pack()