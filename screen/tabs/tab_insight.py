"""
tab_insight.py
----------------
Tab Insight adalah Chat-Based Assistant yang menggunakan model
Gemini untuk memberikan insight finansial, summary, penjelasan kategori,
deteksi anomali, dan menjawab pertanyaan pengguna.

Fitur:
1. Textbox besar untuk percakapan
2. Input field untuk mengirim pertanyaan
3. Tombol Send
4. Terhubung dengan core/gemini_client.py (fungsi ask_gemini)

UI tetap memakai tema gelap modern.
"""

import customtkinter as ctk
from core.gemini_client import ask_gemini


class TabInsight(ctk.CTkFrame):
    """
    TabInsight menyediakan interface chat antara user dan Gemini.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="#101010")

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # --------------------------------------------------------------
        # TEXTBOX CHAT (HISTORY)
        # --------------------------------------------------------------
        self.chat_box = ctk.CTkTextbox(
            self,
            width=600,
            height=430,
            fg_color="#181818",
            text_color="#DDDDDD",
            font=ctk.CTkFont(size=14)
        )
        self.chat_box.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # --------------------------------------------------------------
        # INPUT FRAME (UNTUK KIRIM PESAN)
        # --------------------------------------------------------------
        input_frame = ctk.CTkFrame(self, fg_color="#181818")
        input_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))

        input_frame.grid_columnconfigure(0, weight=1)

        # Input field
        self.entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Tanyakan apa saja tentang pengeluaran, kategori, anomali...",
            fg_color="#202020",
            text_color="#EEEEEE",
            font=ctk.CTkFont(size=14)
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(10, 10), pady=10)

        # Tombol Send
        send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            width=80,
            command=self.send_message
        )
        send_btn.grid(row=0, column=1, padx=(0, 10), pady=10)

    # =================================================================
    # FUNCTION: SEND MESSAGE
    # =================================================================
    def send_message(self):
        """
        Proses kirim pesan ke Gemini:
        1. Ambil teks dari entry
        2. Tampilkan di chat_box
        3. Panggil ask_gemini(prompt)
        4. Tampilkan respons AI

        Jika input kosong → tidak melakukan apa pun.
        """
        user_text = self.entry.get().strip()

        if not user_text:
            return  # ignore pesan kosong

        # Tampilkan pesan user ke chat window
        self.chat_box.insert("end", f"\nYou: {user_text}\n")
        self.chat_box.see("end")

        # Kosongkan entry
        self.entry.delete(0, "end")

        # Dapatkan jawaban dari Gemini
        ai_response = ask_gemini(user_text)

        # Tampilkan respons
        self.chat_box.insert("end", f"Gemini: {ai_response}\n")
        self.chat_box.see("end")
