import customtkinter as ctk
from PIL import Image, ImageDraw
from screen.main_window import MainWindow

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#0F0F0F")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ============================================================
        # 1. AUTO-GENERATED GRADIENT BACKGROUND
        # ============================================================
        # Kita buat agak lebih besar (1920x1080) agar aman di layar besar
        gradient_img = self.create_gradient(width=1920, height=1080, start_hex="#32004F", end_hex="#050505")
        
        bg_image = ctk.CTkImage(light_image=gradient_img, dark_image=gradient_img, size=(1920, 1080))
        
        bg_label = ctk.CTkLabel(self, image=bg_image, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ============================================================
        # 2. CARD CONTAINER (Menu Tengah)
        # ============================================================
        # PENTING: Kita ganti sticky/grid dengan PLACE agar 'Floating' di tengah
        container = ctk.CTkFrame(
            self, 
            fg_color="#181818", 
            corner_radius=20,
            border_width=2,
            border_color="#333333"
        )
        
        # LOGIKA BARU:
        # relx=0.5, rely=0.5 -> Titik tengah frame ada di tengah layar
        # anchor="center" -> Jangkar ada di tengah objek
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Grid config untuk isi container (tetap sama)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # --- Logo ---
        logo_frame = ctk.CTkFrame(container, fg_color="#7A3DB8", width=80, height=80, corner_radius=40)
        logo_frame.grid(row=0, column=0, pady=(40, 0))
        
        logo_label = ctk.CTkLabel(logo_frame, text="RS", font=("Arial", 32, "bold"), text_color="white")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- Judul ---
        title = ctk.CTkLabel(
            container,
            text="ReceiptSorter AI",
            font=ctk.CTkFont(family="Roboto", size=36, weight="bold"),
            text_color="white"
        )
        # padx horizontal ditambah agar card otomatis melebar proporsional
        title.grid(row=1, column=0, pady=(10, 5), padx=50)

        # --- Deskripsi ---
        subtitle = ctk.CTkLabel(
            container,
            text="Kelola Struk Belanja Anda\ndengan Kekuatan AI & OCR",
            font=ctk.CTkFont(family="Roboto", size=16),
            text_color="#A0A0A0",
            justify="center"
        )
        # padx=100 membuat kartu terlihat lebar ("Gendut") tapi tidak melar
        subtitle.grid(row=2, column=0, pady=(0, 20), padx=100)

        # --- Tombol Start ---
        start_btn = ctk.CTkButton(
            container,
            text="MULAI SEKARANG",
            width=220,
            height=50,
            corner_radius=25,
            fg_color="#7A3DB8",
            hover_color="#5A2B8A",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            command=self.start_app
        )
        start_btn.grid(row=3, column=0, pady=(0, 50))

    def create_gradient(self, width, height, start_hex, end_hex):
        """
        Fungsi untuk membuat gambar gradasi vertikal.
        """
        base = Image.new('RGB', (width, height), start_hex)
        top = Image.new('RGB', (width, height), end_hex)
        mask = Image.new('L', (width, height))
        mask_data = []

        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)
        
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base

    def start_app(self):
        self.destroy()
        MainWindow(master=self.master)