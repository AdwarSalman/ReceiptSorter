"""
tab_ocr.py
-----------
Tab OCR berfungsi untuk:
1. Upload gambar struk
2. Menampilkan preview gambar (250x250)
3. Menjalankan proses OCR menggunakan modul core/ocr_processor.py
4. Menampilkan hasil teks OCR di textbox
5. Mengirim teks OCR ke tab Classification (opsional nanti)

Desain UI:
- Kiri: preview gambar + tombol upload
- Kanan: Textbox OCR result + tombol run OCR
"""

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

# Import modul OCR dari folder core
from core.ocr_processor import run_ocr


class TabOCR(ctk.CTkFrame):
    """
    Kelas TabOCR adalah container GUI untuk proses OCR:
    Upload → Preview → OCR → Tampilkan teks
    """

    def __init__(self, master):
        """
        Konstruktor TabOCR

        PARAMETER:
        master : frame tab dari MainWindow
        """
        super().__init__(master, fg_color="#101010")

        # ---------------------------------------------------------------
        # CONFIG LAYOUT
        # ---------------------------------------------------------------
        self.grid_columnconfigure(0, weight=1)  # kolom sebelah kiri
        self.grid_columnconfigure(1, weight=2)  # kolom kanan lebih lebar
        self.grid_rowconfigure(0, weight=1)

        # Variabel internal
        self.loaded_image_path = None
        self.preview_image = None  # untuk menahan image agar tidak garbage collected

        # ---------------------------------------------------------------
        # FRAME KIRI: PREVIEW + UPLOAD BUTTON
        # ---------------------------------------------------------------
        left_frame = ctk.CTkFrame(self, fg_color="#181818", corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        title_left = ctk.CTkLabel(
            left_frame,
            text="Receipt Image Preview",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_left.pack(pady=(15, 5))

        # Tempat preview gambar
        self.image_label = ctk.CTkLabel(left_frame, text="No Image", fg_color="#222222",
                                        width=250, height=250, corner_radius=10)
        self.image_label.pack(pady=10)

        # Tombol Upload
        upload_btn = ctk.CTkButton(
            left_frame,
            text="Upload Image",
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            command=self.upload_image
        )
        upload_btn.pack(pady=10)

        # ---------------------------------------------------------------
        # FRAME KANAN: OCR RESULT
        # ---------------------------------------------------------------
        right_frame = ctk.CTkFrame(self, fg_color="#181818", corner_radius=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        title_right = ctk.CTkLabel(
            right_frame,
            text="OCR Result (Extracted Text)",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_right.pack(pady=(15, 5))

        # Textbox untuk hasil OCR
        self.ocr_textbox = ctk.CTkTextbox(
            right_frame,
            width=400,
            height=400,
            fg_color="#202020",
            text_color="#DDDDDD",
            font=ctk.CTkFont(size=14)
        )
        self.ocr_textbox.pack(padx=10, pady=10, fill="both", expand=True)

        # Tombol OCR
        ocr_btn = ctk.CTkButton(
            right_frame,
            text="Run OCR",
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            command=self.run_ocr_process
        )
        ocr_btn.pack(pady=10)

    # ------------------------------------------------------------------
    # FUNCTION: UPLOAD IMAGE
    # ------------------------------------------------------------------
    def upload_image(self):
        """
        Fungsi untuk memilih gambar dari File Explorer.
        Gambar harus JPG atau PNG.
        Setelah dipilih → tampilkan preview.
        """
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )

        if not path:
            return  # user tekan cancel

        self.loaded_image_path = path

        # Load image + resize agar pas 250x250
        img = Image.open(path)
        img = img.resize((250, 250))

        # Convert ke format yang bisa ditampilkan di CTkLabel
        self.preview_image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=self.preview_image, text="")

    # ------------------------------------------------------------------
    # FUNCTION: RUN OCR
    # ------------------------------------------------------------------
    def run_ocr_process(self):
        """
        Menjalankan OCR menggunakan modul core/ocr_processor.py

        LANGKAH:
        1. Pastikan ada gambar
        2. Panggil run_ocr(path)
        3. Tampilkan hasil di textbox
        """
        if self.loaded_image_path is None:
            self.ocr_textbox.delete("0.0", "end")
            self.ocr_textbox.insert("0.0", "ERROR: No image uploaded.")
            return

        # Jalankan OCR
        text_result = run_ocr(self.loaded_image_path)

        # Tampilkan hasil OCR
        self.ocr_textbox.delete("0.0", "end")
        self.ocr_textbox.insert("0.0", text_result)
