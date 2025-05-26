# utils/language_manager.py
import json
import os

class LanguageManager:
    def __init__(self, language="en"):
        self.language = language
        self.texts = self.load_language()

    def load_language(self):
        """Carga los textos según el idioma seleccionado."""
        locale_file = os.path.join("locales", f"{self.language}.json")
        with open(locale_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_text(self, module, key):
        """Obtiene un texto específico para un módulo y clave."""
        return self.texts.get(module, {}).get(key, f"[{key} not found]")

    def set_language(self, language):
        """Cambia el idioma y recarga los textos."""
        self.language = language
        self.texts = self.load_language()