"""
search_classifier.py
---------------------
Modul ini mengimplementasikan algoritma:
    🎯 BEST-FIRST SEARCH (Greedy Heuristic Search)

Sistem akan memilih kategori dengan nilai heuristic tertinggi.
Heuristic berbasis:
    h(n) = jumlah kata pada struk yang cocok dengan kata kunci kategori n

Modul ini dipakai oleh TabClassify.

Alur:
1. Teks → clean_text() → list token
2. Hitung skor kecocokan token terhadap kata kunci setiap kategori
3. Simpan skor ke dictionary
4. Pilih kategori dengan skor terbesar (Greedy)
"""

from core.text_cleaner import clean_text


# ======================================================================
# 1. DEFINISI KATA KUNCI UNTUK SETIAP KATEGORI
# ======================================================================
# Kamu bisa memperluas daftar kategori kapan pun
category_keywords = {
    "makanan": [
        "mie", "ayam", "nasi", "minum", "air", "kopi", "gula", "coklat",
        "roti", "snack", "teh", "susu", "burger", "kentang", "ikan"
    ],
    "elektronik": [
        "charger", "kabel", "lampu", "baterai", "hp", "listrik",
        "headset", "earphone", "powerbank", "adapter"
    ],
    "kebutuhan rumah tangga": [
        "sabun", "detergen", "pel", "sapu", "ember", "gas", "refill",
        "shampoo", "piring", "gelas"
    ],
    "fashion": [
        "baju", "celana", "hoodie", "kaos", "sepatu", "sendal",
        "topi", "jaket"
    ],
    "kesehatan": [
        "obat", "vitamin", "masker", "handsanitizer", "paracetamol",
        "supplement"
    ]
}


# ======================================================================
# 2. BEST-FIRST SEARCH / GREEDY HEURISTIC
# ======================================================================
def classify_text(text: str):
    """
    Melakukan klasifikasi kategori berdasarkan heuristic kecocokan kata.

    PARAMETER:
    text : string
        Teks input (hasil OCR atau manual)

    RETURN:
    best_category : str
        Kategori dengan skor heuristic tertinggi
    score_table : dict
        Dictionary: kategori → skor heuristic
    """

    # ---------------------------------------------------------------
    # STEP 1: CLEANING → ubah teks menjadi token bersih
    # ---------------------------------------------------------------
    tokens = clean_text(text)

    # Jika teks kosong setelah cleaning → tidak bisa diklasifikasi
    if len(tokens) == 0:
        return "unknown", {k: 0 for k in category_keywords}

    # ---------------------------------------------------------------
    # STEP 2: Hitung skor heuristic untuk setiap kategori
    # ---------------------------------------------------------------
    score_table = {}

    for category, keywords in category_keywords.items():

        # Hitung jumlah kata yang cocok
        score = sum(1 for token in tokens if token in keywords)

        # Simpan skor kategori
        score_table[category] = score

    # ---------------------------------------------------------------
    # STEP 3: BEST-FIRST SEARCH (Greedy)
    # Pilih kategori dengan skor terbesar → O(N) sederhana
    # ---------------------------------------------------------------
    best_category = max(score_table, key=score_table.get)

    return best_category, score_table


# ======================================================================
# 3. DEBUGGING FUNCTION
# ======================================================================
def debug_classify(text: str):
    """
    Fungsi opsional untuk debugging proses heuristic.
    Mengembalikan token dan skor penuh.

    Tidak dipakai GUI, tapi bagus untuk laporan.
    """
    tokens = clean_text(text)
    best_cat, scores = classify_text(text)

    return {
        "tokens": tokens,
        "scores": scores,
        "best_category": best_cat
    }
