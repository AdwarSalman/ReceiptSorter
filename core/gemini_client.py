"""
gemini_client.py
-----------------
Modul ini menjadi jembatan antara aplikasi GUI dan Google Gemini API.

Fungsi:
1. Mengirim prompt ke Gemini
2. Menerima dan mem-format hasil
3. Mengembalikan jawaban ke TabInsight

Catatan:
- Kamu HARUS mengisi API key pada variabel API_KEY
- Gunakan API Key dari Google AI Studio: https://aistudio.google.com
- Modul ini memakai REST API supaya simpel dan stabil.

Dependency:
    pip install requests
"""

import requests

# ==========================================================
# MASUKKAN API KEY KAMU DI SINI
# ==========================================================
API_KEY = ""

# Endpoint Gemini generative AI (model 1.5 Flash gratis & cepat)
# PERBAIKAN (Ganti bagian ini)
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent?key="
)


def ask_gemini(prompt: str) -> str:
    """
    Mengirim prompt ke Gemini API dan mengambil jawaban.

    PARAMETER:
    prompt : string
        Pertanyaan dari user

    RETURN:
    result_text : string
        Teks jawaban dari Gemini.
        Jika error, akan mengembalikan pesan error-nya.
    """

    # ----------------------------------------------------------------------
    # Validasi API KEY
    # ----------------------------------------------------------------------
    if API_KEY == "YOUR_GEMINI_API_KEY" or API_KEY.strip() == "":
        return (
            "ERROR: API Key belum dimasukkan.\n"
            "Masukkan API key kamu di file core/gemini_client.py"
        )

    # ----------------------------------------------------------------------
    # Payload JSON sesuai format REST Gemini
    # ----------------------------------------------------------------------
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # ----------------------------------------------------------------------
    # Kirim ke API dengan exception handling
    # ----------------------------------------------------------------------
    try:
        response = requests.post(
            API_URL + API_KEY,
            json=data,
            timeout=60
        )

        # Jika status bukan 200
        if response.status_code != 200:
            return f"API ERROR {response.status_code}: {response.text}"

        result_json = response.json()

        # Ambil isi response model
        result_text = result_json["candidates"][0]["content"]["parts"][0]["text"]

        return result_text

    except requests.exceptions.Timeout:
        return "ERROR: Request timeout. Coba lagi."

    except Exception as e:
        return f"ERROR: {str(e)}"
