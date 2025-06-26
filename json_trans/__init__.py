"""
json-trans
~~~~~~~~~~

A tool for translating JSON files from English to Chinese using various translation APIs.
"""

from .index import (
    JsonTranslator,
    BaiduTranslator,
    GoogleTranslator,
    GeminiTranslator,
    translate_json_baidu,
    translate_json_google,
    translate_json_gemini,
)

__version__ = "0.1.0"
__all__ = [
    "JsonTranslator",
    "BaiduTranslator",
    "GoogleTranslator",
    "GeminiTranslator",
    "translate_json_baidu",
    "translate_json_google",
    "translate_json_gemini",
]
