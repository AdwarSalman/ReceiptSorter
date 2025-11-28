import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from core.ocr_processor import run_ocr

class TabOCR(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent") # Transparan agar ikut warna induk

        # Grid utama
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) # 50:50 ratio agar seimbang
        self.grid_rowconfigure(0, weight=1)

        self.loaded_image_path = None
        self.preview_image = None

        # ==========================================================
        # KARTU KIRI: IMAGE PREVIEW
        # ==========================================================
        left_card = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=15, border_width=1, border_color="#333333")
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        left_card.grid_columnconfigure(0, weight=1)
        left_card.grid_rowconfigure(1, weight=1)

        # Header Kartu Kiri
        lbl_left = ctk.CTkLabel(left_card, text="📄 Preview Struk", font=("Roboto", 18, "bold"), text_color="#FFFFFF")
        lbl_left.grid(row=0, column=0, pady=20)

        # Area Gambar (Dibuat seperti kotak putus-putus jika kosong)
        self.image_container = ctk.CTkFrame(left_card, fg_color="#151515", corner_radius=10)
        self.image_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        self.image_label = ctk.CTkLabel(
            self.image_container, 
            text="Belum ada gambar dipilih\nKlik Upload Image", 
            text_color="#555555",
            font=("Roboto", 14)
        )
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)

        # Tombol Upload (Style Outline/Secondary)
        upload_btn = ctk.CTkButton(
            left_card,
            text="📂 Upload Image",
            font=("Roboto", 14, "bold"),
            height=40,
            fg_color="transparent",
            border_width=2,
            border_color="#7A3DB8",
            text_color="#7A3DB8",
            hover_color="#2A2A2A",
            command=self.upload_image
        )
        upload_btn.grid(row=2, column=0, padx=20, pady=(0, 25), sticky="ew")

        # ==========================================================
        # KARTU KANAN: OCR RESULT
        # ==========================================================
        right_card = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=15, border_width=1, border_color="#333333")
        right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        right_card.grid_columnconfigure(0, weight=1)
        right_card.grid_rowconfigure(1, weight=1)

        # Header Kartu Kanan
        lbl_right = ctk.CTkLabel(right_card, text="📝 Hasil Ekstraksi Teks", font=("Roboto", 18, "bold"), text_color="#FFFFFF")
        lbl_right.grid(row=0, column=0, pady=20)

        # Textbox Modern
        self.ocr_textbox = ctk.CTkTextbox(
            right_card,
            font=("Consolas", 14), # Font monospaced untuk data
            fg_color="#151515",
            text_color="#E0E0E0",
            corner_radius=10,
            border_width=1,
            border_color="#333333"
        )
        self.ocr_textbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        # Tombol Run OCR (Style Solid/Primary)
        ocr_btn = ctk.CTkButton(
            right_card,
            text="⚡ Jalankan OCR",
            font=("Roboto", 14, "bold"),
            height=40,
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            command=self.run_ocr_process
        )
        ocr_btn.grid(row=2, column=0, padx=20, pady=(0, 25), sticky="ew")

    # --- (Fungsi logika upload_image dan run_ocr_process tetap sama seperti sebelumnya) ---
    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not path: return
        self.loaded_image_path = path
        
        # Load logic
        img = Image.open(path)
        # Ratio aspect resize agar rapi
        base_width = 300
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        # Batasi tinggi max
        if h_size > 300: h_size = 300
        
        img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=self.preview_image, text="")

    def run_ocr_process(self):
        if self.loaded_image_path is None:
            self.ocr_textbox.delete("0.0", "end")
            self.ocr_textbox.insert("0.0", "⚠️ ERROR: Harap upload gambar terlebih dahulu.")
            return
        
        # UI Feedback
        self.ocr_textbox.delete("0.0", "end")
        self.ocr_textbox.insert("0.0", "Sedang memproses OCR...\nMohon tunggu...")
        self.update() # Force update UI

        text_result = run_ocr(self.loaded_image_path)
        self.ocr_textbox.delete("0.0", "end")
        self.ocr_textbox.insert("0.0", text_result)