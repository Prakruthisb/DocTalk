import requests, os

LANG_MAP = {
    "hi": "hin_Deva", "kn": "kan_Knda",
    "ta": "tam_Taml", "te": "tel_Telu",
    "ml": "mal_Mlym", "mr": "mar_Deva",
    "bn": "ben_Beng", "en": "eng_Latn"
}

def detect_and_translate_to_english(text):
    """Detect language + translate question to English for RAG"""
    # Use Sarvam translate API
    headers = {"Authorization": f"Bearer {os.getenv('SARVAM_API_KEY')}"}
    resp = requests.post(
        "https://api.sarvam.ai/translate",
        headers=headers,
        json={"input": text, "source_language_code": "auto",
              "target_language_code": "en-IN"}
    )
    result = resp.json()
    english_text = result.get("translated_text", text)
    detected_lang = result.get("source_language_code", "en")
    return english_text, detected_lang

def translate_answer(answer, target_lang_code):
    """Translate English answer back to user's language"""
    if target_lang_code == "en":
        return answer
    headers = {"Authorization": f"Bearer {os.getenv('SARVAM_API_KEY')}"}
    resp = requests.post(
        "https://api.sarvam.ai/translate",
        headers=headers,
        json={"input": answer, "source_language_code": "en-IN",
              "target_language_code": target_lang_code}
    )
    return resp.json().get("translated_text", answer)