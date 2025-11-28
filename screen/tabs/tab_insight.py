import customtkinter as ctk
from core.gemini_client import ask_gemini

class TabInsight(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Layout utama
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Chat history area
        self.grid_rowconfigure(1, weight=0) # Input area (fixed height)

        # ==========================================================
        # 1. CHAT HISTORY CONTAINER
        # ==========================================================
        # Kita bungkus dalam frame agar punya border halus
        chat_container = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=15, border_width=1, border_color="#333333")
        chat_container.grid(row=0, column=0, sticky="nsew", padx=0, pady=(10, 10))
        chat_container.grid_columnconfigure(0, weight=1)
        chat_container.grid_rowconfigure(0, weight=1)

        # Textbox Chat (Read Only style look)
        self.chat_box = ctk.CTkTextbox(
            chat_container,
            font=("Roboto", 15),
            fg_color="#1E1E1E", # Blend dengan container
            text_color="#DDDDDD",
            wrap="word",
            corner_radius=0
        )
        self.chat_box.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # Pesan pembuka
        self.chat_box.insert("0.0", "🤖 Gemini AI: Halo! Saya siap membantu menganalisis pengeluaranmu.\n\n")

        # ==========================================================
        # 2. INPUT AREA (MODERN PILL SHAPE)
        # ==========================================================
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)

        # Entry Field yang Bulat (Pill Shape)
        self.entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Tanyakan sesuatu... (Misal: 'Analisis struk ini')",
            height=50, # Lebih tinggi biar lega
            corner_radius=25, # Membuat ujungnya bulat penuh
            fg_color="#151515",
            border_width=1,
            border_color="#444444",
            text_color="white",
            font=("Roboto", 14)
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Bind tombol Enter untuk kirim
        self.entry.bind("<Return>", lambda event: self.send_message())

        # Tombol Send
        send_btn = ctk.CTkButton(
            input_frame,
            text="➤ Kirim",
            width=100,
            height=50,
            corner_radius=25,
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            font=("Roboto", 14, "bold"),
            command=self.send_message
        )
        send_btn.grid(row=0, column=1, sticky="e")

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text: return

        # Tampilkan pesan user
        self.chat_box.insert("end", f"\n👤 You: {user_text}\n")
        self.chat_box.see("end")
        
        # Clear entry & Disable sementara (efek loading)
        self.entry.delete(0, "end")
        self.entry.configure(placeholder_text="Sedang mengetik...")
        self.update()

        # Panggil API
        ai_response = ask_gemini(user_text)

        # Tampilkan balasan AI
        self.chat_box.insert("end", f"\n🤖 Gemini: {ai_response}\n")
        self.chat_box.insert("end", "-"*40 + "\n") # Separator line
        self.chat_box.see("end")
        
        