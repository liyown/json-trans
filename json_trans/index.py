"""
json-trans
~~~~~~~~~~

A tool for translating JSON files from English to Chinese using various translation APIs.
"""

import json
import time
import hashlib
import random
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import requests
from google.cloud import translate_v2 as google_translate

JSONType = Union[Dict[str, Any], List[Any]]


class BaseTranslator(ABC):
    """Abstract base class for translators."""

    @abstractmethod
    def translate_to_chinese(self, english_text: str) -> str:
        """
        Translate English text to Chinese.

        Args:
            english_text: The English text to translate

        Returns:
            The translated Chinese text
        """
        pass


class BaiduTranslator(BaseTranslator):
    """Translator that uses Baidu Translate API."""

    def __init__(self, app_id: str, secret_key: str) -> None:
        """
        Initialize the Baidu translator.

        Args:
            app_id: Baidu Translate API APP ID
            secret_key: Baidu Translate API secret key
        """
        self.app_id = app_id
        self.secret_key = secret_key
        self._base_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"

    def translate_to_chinese(self, english_text: str) -> str:
        """
        Translate English text to Chinese using Baidu API.

        Args:
            english_text: The English text to translate

        Returns:
            The translated Chinese text
        """
        time.sleep(1)  # Rate limiting

        salt = str(random.randint(32768, 65536))
        sign = self.app_id + english_text + salt + self.secret_key
        sign = hashlib.md5(sign.encode()).hexdigest()

        params = {
            "q": english_text,
            "from": "en",
            "to": "zh",
            "appid": self.app_id,
            "salt": salt,
            "sign": sign,
        }

        try:
            response = requests.get(self._base_url, params=params)
            response.raise_for_status()

            result = response.json()
            if "trans_result" in result and result["trans_result"]:
                return result["trans_result"][0]["dst"]

        except (requests.RequestException, KeyError, IndexError) as e:
            print(f"Translation error: {e}")

        return english_text


class GoogleTranslator(BaseTranslator):
    """Translator that uses Google Cloud Translation API."""

    def __init__(self, credentials_path: str = None) -> None:
        """
        Initialize the Google translator.

        Args:
            credentials_path: Path to Google Cloud credentials JSON file.
                            If None, uses default credentials.
        """
        self.client = (
            google_translate.Client.from_service_account_json(credentials_path)
            if credentials_path
            else google_translate.Client()
        )

    def translate_to_chinese(self, english_text: str) -> str:
        """
        Translate English text to Chinese using Google API.

        Args:
            english_text: The English text to translate

        Returns:
            The translated Chinese text
        """
        try:
            result = self.client.translate(
                english_text, target_language="zh", source_language="en"
            )
            return result["translatedText"]

        except Exception as e:
            print(f"Translation error: {e}")
            return english_text


class GeminiTranslator(BaseTranslator):
    """Translator that uses Google Gemini API."""

    def __init__(
        self, api_key: str, model: str = "gemini-2.0-flash-exp", role: str = "model"
    ) -> None:
        """
        Initialize the Gemini translator.

        Args:
            api_key: Gemini API key
            model: Model name to use (default: "gemini-2.0-flash-exp")
            role: Role for the translation model (default: "model")
        """
        self.api_key = api_key
        self.model = model
        self.role = role
        self._base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def translate_to_chinese(self, english_text: str) -> str:
        """
        Translate English text to Chinese using Gemini API.

        Args:
            english_text: The English text to translate

        Returns:
            The translated Chinese text
        """
        try:
            headers = {"Content-Type": "application/json", "Accept": "*/*"}

            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"Translate this English text to Chinese: {english_text}"
                            }
                        ],
                        "role": self.role,
                    }
                ]
            }

            params = {"key": self.api_key}

            response = requests.post(
                self._base_url, headers=headers, params=params, json=data
            )
            response.raise_for_status()

            result = response.json()
            if "candidates" in result and result["candidates"]:
                translated_text = result["candidates"][0]["content"]["parts"][0]["text"]
                # 清理可能的提示词
                translated_text = translated_text.replace("翻译：", "").strip()
                return translated_text

        except Exception as e:
            print(f"Translation error: {e}")

        return english_text


class JsonTranslator:
    """A translator that converts English text in JSON files to Chinese."""

    def __init__(
        self, translator: BaseTranslator, fields_to_translate: List[str]
    ) -> None:
        """
        Initialize the JSON translator.

        Args:
            translator: The translator implementation to use
            fields_to_translate: List of field names to translate
        """
        self.translator = translator
        if not fields_to_translate:
            raise ValueError("fields_to_translate cannot be empty")
        self.fields_to_translate = fields_to_translate
        self.total_fields = 0
        self.translated_fields = 0

    def _count_translatable_fields(self, data: JSONType) -> int:
        """
        Count the total number of fields that need to be translated.

        Args:
            data: The JSON data to count

        Returns:
            The number of translatable fields
        """
        count = 0
        if isinstance(data, dict):
            for key, value in data.items():
                if key in self.fields_to_translate and isinstance(value, str):
                    # 只在值是字符串且未被翻译过时才计数
                    if not value.startswith("翻译: "):
                        count += 1
                else:
                    count += self._count_translatable_fields(value)
        elif isinstance(data, list):
            for item in data:
                count += self._count_translatable_fields(item)
        return count

    def _print_progress(self, text: str) -> None:
        """
        Print translation progress.

        Args:
            text: The text being translated
        """
        self.translated_fields += 1
        percentage = (
            (self.translated_fields / self.total_fields) * 100
            if self.total_fields > 0
            else 0
        )

        # 限制显示的文本长度
        display_text = text[:30] + "..." if len(text) > 30 else text

        print(
            f"\r翻译进度: [{self.translated_fields}/{self.total_fields}] {percentage:.1f}% - 翻译中: {display_text}",
            end="",
            flush=True,
        )

        # 完成时换行
        if self.translated_fields >= self.total_fields:
            print()

    def find_and_replace_titles(self, data: JSONType) -> None:
        """
        Recursively find and replace specified fields in JSON data.

        Args:
            data: The JSON data to process
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if key in self.fields_to_translate and isinstance(value, str):
                    # 只在值是字符串且未被翻译过时才翻译
                    if not value.startswith("翻译: "):
                        self._print_progress(value)
                        data[key] = self.translator.translate_to_chinese(value)
                else:
                    self.find_and_replace_titles(value)
        elif isinstance(data, list):
            for item in data:
                self.find_and_replace_titles(item)

    def translate_json_file(self, input_filename: str, output_filename: str) -> None:
        """
        Translate specified fields in a JSON file.

        Args:
            input_filename: Input JSON filename
            output_filename: Output JSON filename
        """
        try:
            print(f"正在读取文件: {input_filename}")
            with open(input_filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            # 统计需要翻译的字段总数
            self.total_fields = self._count_translatable_fields(data)
            self.translated_fields = 0

            if self.total_fields == 0:
                print("没有找到需要翻译的字段")
                return

            print(f"发现 {self.total_fields} 个需要翻译的字段")
            print("开始翻译...")

            self.find_and_replace_titles(data)

            print(f"正在保存翻译结果到: {output_filename}")
            with open(output_filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            print("翻译完成！")

        except Exception as e:
            print(f"Error processing JSON file: {e}")
            raise


def translate_json_baidu(
    input_file: str,
    output_file: str,
    app_id: str,
    secret_key: str,
    fields_to_translate: List[str],
) -> None:
    """
    Convenience function to translate a JSON file using Baidu API.

    Args:
        input_file: Input JSON filename
        output_file: Output JSON filename
        app_id: Baidu Translate API APP ID
        secret_key: Baidu Translate API secret key
        fields_to_translate: List of field names to translate
    """
    translator = JsonTranslator(
        BaiduTranslator(app_id, secret_key), fields_to_translate=fields_to_translate
    )
    translator.translate_json_file(input_file, output_file)


def translate_json_google(
    input_file: str,
    output_file: str,
    fields_to_translate: List[str],
    credentials_path: str = None,
) -> None:
    """
    Convenience function to translate a JSON file using Google API.

    Args:
        input_file: Input JSON filename
        output_file: Output JSON filename
        fields_to_translate: List of field names to translate
        credentials_path: Path to Google Cloud credentials JSON file
    """
    translator = JsonTranslator(
        GoogleTranslator(credentials_path), fields_to_translate=fields_to_translate
    )
    translator.translate_json_file(input_file, output_file)


def translate_json_gemini(
    input_file: str,
    output_file: str,
    api_key: str,
    fields_to_translate: List[str],
    model: str = "gemini-2.0-flash-exp",
    role: str = "model",
) -> None:
    """
    Convenience function to translate a JSON file using Gemini API.

    Args:
        input_file: Input JSON filename
        output_file: Output JSON filename
        api_key: Gemini API key
        fields_to_translate: List of field names to translate
        model: Model name to use (default: "gemini-2.0-flash-exp")
        role: Role for the translation model (default: "model")
    """
    translator = JsonTranslator(
        GeminiTranslator(api_key=api_key, model=model, role=role),
        fields_to_translate=fields_to_translate,
    )
    translator.translate_json_file(input_file, output_file)
