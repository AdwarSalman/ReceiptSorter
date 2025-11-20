"""
backward_chain.py
-------------------
Modul ini berfungsi untuk memberikan REASONING (penjelasan) mengapa
kategori tertentu dipilih oleh sistem berdasarkan heuristic.

Reasoning dilakukan dengan pendekatan:
    🔎 BACKWARD CHAINING SEDERHANA

Alur:
1. Ambil kategori hasil heuristic
2. Ambil kata kunci kategori tersebut
3. Periksa token mana dari input yang cocok dengan kata kunci
4. Kembalikan list token pendukung

Ini memberikan penjelasan logis untuk ditampilkan di GUI.
"""

from core.text_cleaner import clean_text
from core.search_classifier import category_keywords


def backward_reasoning(text: str, selected_category: str) -> list:
    """
    Melacak token pendukung kategori tertentu.

    PARAMETER:
    text : string
        Teks input dari OCR / manual
    selected_category : string
        Kategori terbaik hasil heuristic search

    RETURN:
    matches : list
        Token-token yang mendukung (matching keywords)
    """

    # Safety check
    if selected_category not in category_keywords:
        return []

    # Cleaning + tokenisasi teks
    tokens = clean_text(text)

    # Daftar kata kunci kategori terpilih
    keywords = category_keywords[selected_category]

    # Cek token mana yang cocok dengan kata kunci
    matches = [t for t in tokens if t in keywords]

    return matches


# Debugging optional untuk laporan
def debug_backward(text: str, category: str):
    """
    Fungsi opsional untuk debugging reasoning.
    Mengembalikan semua informasi penting.

    Tidak digunakan di GUI, tapi bagus jika ingin menjelaskan alur reasoning
    secara detail di proposal atau laporan akhir.
    """
    tokens = clean_text(text)
    keywords = category_keywords.get(category, [])
    matches = backward_reasoning(text, category)

    return {
        "tokens": tokens,
        "category_keywords": keywords,
        "matched_tokens": matches
    }
