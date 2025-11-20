"""
text_cleaner.py
----------------
Modul ini melakukan proses pembersihan teks (NLP dasar)
sebelum teks dikirim ke modul klasifikasi heuristic.

Fungsi yang dilakukan:
1. Lowercase seluruh teks
2. Hilangkan karakter tidak penting
3. Hilangkan simbol dan noise OCR
4. Tokenisasi sederhana (berbasis spasi)
5. Mengembalikan list token bersih yang siap dipakai classifier

Catatan:
- Modul ini menggunakan pendekatan sederhana karena tugas ini
  tidak mengharuskan NLP kompleks seperti stemming atau stopword removal.
"""

import re


def clean_text(raw_text: str) -> list:
    """
    Membersihkan teks OCR dan mengubahnya menjadi token.

    PARAMETER:
    raw_text : string
        Teks mentah dari hasil OCR

    RETURN:
    tokens : list
        List token (kata) yang sudah dibersihkan
    """

    # -------------------------------------------------------------------
    # 1. Lowercase → agar pencocokan kata kunci lebih konsisten
    # -------------------------------------------------------------------
    text = raw_text.lower()

    # -------------------------------------------------------------------
    # 2. Hilangkan karakter yang tidak penting:
    #    - simbol
    #    - karakter aneh hasil OCR
    #    - tanda baca
    # -------------------------------------------------------------------
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # -------------------------------------------------------------------
    # 3. Ganti multiple spaces --> single space
    # -------------------------------------------------------------------
    text = re.sub(r"\s+", " ", text).strip()

    # -------------------------------------------------------------------
    # 4. Tokenisasi sederhana berdasarkan spasi
    # -------------------------------------------------------------------
    tokens = text.split(" ")

    # Hilangkan token kosong jika ada
    tokens = [t for t in tokens if t.strip() != ""]

    return tokens


def debug_clean(raw_text: str):
    """
    Fungsi tambahan untuk debugging.
    Menghasilkan string penjelasan step-by-step cleaning.

    Tidak digunakan di aplikasi, tapi berguna jika kamu ingin
    menganalisis hasil OCR yang messy.
    """

    step1 = raw_text.lower()
    step2 = re.sub(r"[^a-z0-9\s]", " ", step1)
    step3 = re.sub(r"\s+", " ", step2).strip()
    step4 = step3.split(" ")

    return {
        "lowercase": step1,
        "remove_symbols": step2,
        "normalize_space": step3,
        "tokens": step4
    }
