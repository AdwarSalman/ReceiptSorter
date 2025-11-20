"""
ocr_processor.py
----------------
Modul ini menangani semua proses OCR pada gambar struk.

Fitur:
1. Load gambar dari path
2. Preprocessing dasar:
   - Convert ke grayscale
   - Thresholding (biner)
   - Noise removal sederhana
3. OCR menggunakan pytesseract
4. Mengembalikan teks yang berhasil diekstrak

NOTE:
- Pastikan sudah menginstall:
  pip install pillow pytesseract opencv-python

- Jika Tesseract tidak terdeteksi, kamu perlu mengatur path:
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
"""

import cv2
import pytesseract
from PIL import Image


def preprocess_image(path):
    """
    Melakukan preprocessing pada gambar agar OCR lebih akurat.

    PARAMETER:
    path : string
        Lokasi file gambar struk (jpg/png)

    RETURN:
    preprocessed_image : numpy array
        Hasil gambar setelah preprocessing
    """

    # Load gambar menggunakan OpenCV (hasil: array BGR)
    img = cv2.imread(path)

    # Jika gambar gagal dibaca
    if img is None:
        raise FileNotFoundError("Gambar tidak ditemukan atau format tidak terbaca.")

    # Convert BGR -> Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold (biner) untuk meningkatkan kontras
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Noise removal (Gaussian blur)
    blur = cv2.GaussianBlur(thresh, (3, 3), 0)

    return blur


def run_ocr(path):
    """
    Menjalankan OCR pada gambar struk.

    LANGKAH:
    1. Preprocessing gambar
    2. Konversi ke format PIL (pytesseract memakai PIL image)
    3. Jalankan OCR
    4. Return teks ekstraksi

    PARAMETER:
    path : string
        Path gambar lokasi file

    RETURN:
    text_result : string
        Teks hasil OCR
    """

    # Preprocess gambar
    processed = preprocess_image(path)

    # Konversi dari array OpenCV ke image PIL
    pil_img = Image.fromarray(processed)

    # Jalankan OCR
    # Jika ingin engine lebih akurat untuk number, gunakan config:
    # config = "--psm 6"
    try:
        text = pytesseract.image_to_string(pil_img)
    except Exception as e:
        text = f"OCR ERROR: {str(e)}"

    return text
