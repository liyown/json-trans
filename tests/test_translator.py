"""
Tests for the json-trans package.
"""

import json
import os
from pathlib import Path
import pytest
from unittest.mock import Mock, patch
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent.parent / '.env.test'
load_dotenv(env_path)

from json_trans import (
    JsonTranslator,
    BaiduTranslator,
    GoogleTranslator,
    translate_json_baidu,
    translate_json_google,
)
from json_trans.index import GeminiTranslator, translate_json_gemini

# 从环境变量获取测试用的 API keys 和配置
BAIDU_APP_ID = os.getenv('BAIDU_APP_ID', 'test_app_id')
BAIDU_SECRET_KEY = os.getenv('BAIDU_SECRET_KEY', 'test_secret_key')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'test_api_key')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')

# Test data
SAMPLE_JSON = {
    "title": "Test",
    "description": "This is a test description",
    "content": "This is test content",
    "items": [
        {
            "name": "Item 1",
            "description": "First item description",
            "content": "First item content",
            "summary": "First item summary"
        },
        {
            "name": "Item 2",
            "description": "Second item description",
            "content": "Second item content",
            "summary": "Second item summary"
        }
    ],
    "nested": {
        "description": "Nested description",
        "content": "Nested content",
        "other": "not translated"
    }
}

class MockTranslator:
    """Mock translator for testing"""
    def translate_to_chinese(self, text: str) -> str:
        # 如果文本已经被翻译过，直接返回
        if text.startswith('翻译: '):
            return text
        return f"翻译: {text}"

@pytest.fixture
def sample_json_file(tmp_path):
    """Create a temporary JSON file for testing"""
    input_file = tmp_path / "input.json"
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(SAMPLE_JSON, f, ensure_ascii=False)
    return str(input_file)

@pytest.fixture
def output_json_file(tmp_path):
    """Get path for output JSON file"""
    return str(tmp_path / "output.json")

def test_json_translator_init():
    """Test JsonTranslator initialization"""
    translator = MockTranslator()
    fields = ["title", "content"]
    json_translator = JsonTranslator(translator, fields_to_translate=fields)
    assert json_translator.translator == translator
    assert json_translator.fields_to_translate == fields

def test_json_translator_find_and_replace():
    """Test finding and replacing fields"""
    translator = MockTranslator()
    fields = ["content", "summary"]
    json_translator = JsonTranslator(translator, fields_to_translate=fields)
    
    test_data = SAMPLE_JSON.copy()
    json_translator.find_and_replace_titles(test_data)
    
    # 检查指定字段是否被翻译
    assert test_data["content"] == "翻译: This is test content"
    assert test_data["items"][0]["content"] == "翻译: First item content"
    assert test_data["items"][0]["summary"] == "翻译: First item summary"
    assert test_data["nested"]["content"] == "翻译: Nested content"
    
    # 检查其他字段是否保持不变
    assert test_data["description"] == "This is a test description"
    assert test_data["title"] == "Test"
    assert test_data["nested"]["other"] == "not translated"

def test_json_translator_file_processing(sample_json_file, output_json_file):
    """Test JSON file processing"""
    translator = MockTranslator()
    fields = ["description", "content"]
    json_translator = JsonTranslator(translator, fields_to_translate=fields)
    
    json_translator.translate_json_file(sample_json_file, output_json_file)
    
    with open(output_json_file, 'r', encoding='utf-8') as f:
        result = json.load(f)
    
    assert result["description"] == "翻译: This is a test description"
    assert result["content"] == "翻译: This is test content"
    assert result["items"][0]["description"] == "翻译: First item description"
    assert result["items"][0]["content"] == "翻译: First item content"
    assert result["title"] == "Test"  # 未指定翻译的字段持不变

@patch('json_trans.index.requests.get')
def test_baidu_translator(mock_get):
    """Test BaiduTranslator implementation"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'trans_result': [{'dst': '测试文本'}]
    }
    mock_get.return_value = mock_response
    
    translator = BaiduTranslator(BAIDU_APP_ID, BAIDU_SECRET_KEY)
    result = translator.translate_to_chinese('test text')
    
    assert result == '测试文本'
    assert mock_get.called

@patch('json_trans.index.google_translate.Client')
def test_google_translator(mock_client):
    """Test GoogleTranslator implementation"""
    mock_instance = Mock()
    mock_instance.translate.return_value = {
        'translatedText': '测试文本'
    }
    mock_client.return_value = mock_instance
    
    translator = GoogleTranslator()
    result = translator.translate_to_chinese('test text')
    
    assert result == '测试文本'
    assert mock_instance.translate.called

def test_translate_json_baidu(sample_json_file, output_json_file):
    """Test baidu translation convenience function"""
    with patch('json_trans.index.BaiduTranslator') as MockBaiduTranslator:
        mock_translator = MockTranslator()
        MockBaiduTranslator.return_value = mock_translator
        
        translate_json_baidu(
            sample_json_file,
            output_json_file,
            BAIDU_APP_ID,
            BAIDU_SECRET_KEY,
            fields_to_translate=["title", "content"]
        )
        
        with open(output_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        
        assert result["title"] == "翻译: Test"
        assert result["content"] == "翻译: This is test content"
        assert result["description"] == "This is a test description"  # 未翻译

def test_translate_json_google(sample_json_file, output_json_file):
    """Test google translation convenience function"""
    with patch('json_trans.index.GoogleTranslator') as MockGoogleTranslator:
        mock_translator = MockTranslator()
        MockGoogleTranslator.return_value = mock_translator
        
        translate_json_google(
            sample_json_file,
            output_json_file,
            fields_to_translate=["summary", "content"],
            credentials_path=None
        )
        
        with open(output_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        
        assert result["content"] == "翻译: This is test content"
        assert result["items"][0]["summary"] == "翻译: First item summary"
        assert result["title"] == "Test"  # 未翻译

def test_file_not_found():
    """Test handling of non-existent input file"""
    translator = MockTranslator()
    json_translator = JsonTranslator(
        translator,
        fields_to_translate=["title", "content"]
    )
    
    with pytest.raises(FileNotFoundError):
        json_translator.translate_json_file(
            "nonexistent.json",
            "output.json"
        )

def test_invalid_json(tmp_path):
    """Test handling of invalid JSON input"""
    input_file = tmp_path / "invalid.json"
    with open(input_file, "w") as f:
        f.write("invalid json content")
    
    translator = MockTranslator()
    json_translator = JsonTranslator(
        translator,
        fields_to_translate=["title", "content"]
    )
    
    with pytest.raises(json.JSONDecodeError):
        json_translator.translate_json_file(
            str(input_file),
            str(tmp_path / "output.json")
        )

def test_empty_fields_list():
    """Test initialization with empty fields list"""
    translator = MockTranslator()
    with pytest.raises(ValueError):
        JsonTranslator(translator, fields_to_translate=[])

@patch('json_trans.index.requests.post')
def test_gemini_translator(mock_post):
    """Test GeminiTranslator implementation"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'candidates': [{
            'content': {
                'parts': [{
                    'text': '测试文本'
                }]
            }
        }]
    }
    mock_post.return_value = mock_response
    
    translator = GeminiTranslator(GEMINI_API_KEY, model=GEMINI_MODEL)
    result = translator.translate_to_chinese('test text')
    
    assert result == '测试文本'
    assert mock_post.called
    
    # 验证请求参数
    call_args = mock_post.call_args
    assert GEMINI_API_KEY in call_args[1]['params']['key']
    assert 'test text' in call_args[1]['json']['contents'][0]['parts'][0]['text']

@patch('json_trans.index.requests.post')
def test_gemini_translator_with_custom_model(mock_post):
    """Test GeminiTranslator implementation with custom model"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'candidates': [{
            'content': {
                'parts': [{
                    'text': '测试文本'
                }]
            }
        }]
    }
    mock_post.return_value = mock_response
    
    translator = GeminiTranslator(
        GEMINI_API_KEY,
        model=GEMINI_MODEL,
        role='translator'
    )
    result = translator.translate_to_chinese('test text')
    
    assert result == '测试文本'
    assert mock_post.called
    
    # 验证请求参数
    call_args = mock_post.call_args
    # 检查 URL 中是否包含模型名称
    assert GEMINI_MODEL in call_args[0][0]  # 第一个参数是 URL
    assert 'translator' in call_args[1]['json']['contents'][0]['role']

def test_translate_json_gemini(sample_json_file, output_json_file):
    """Test gemini translation convenience function"""
    with patch('json_trans.index.GeminiTranslator') as MockGeminiTranslator:
        mock_translator = MockTranslator()
        MockGeminiTranslator.return_value = mock_translator
        
        translate_json_gemini(
            sample_json_file,
            output_json_file,
            GEMINI_API_KEY,
            fields_to_translate=["title", "content"],
            role="model"
        )
        
        with open(output_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        
        assert result["title"] == "翻译: Test"
        assert result["content"] == "翻译: This is test content"
        assert result["description"] == "This is a test description"  # 未翻译

def test_translate_json_gemini_with_custom_model(sample_json_file, output_json_file):
    """Test gemini translation convenience function with custom model"""
    with patch('json_trans.index.GeminiTranslator') as MockGeminiTranslator:
        mock_translator = MockTranslator()
        MockGeminiTranslator.return_value = mock_translator
        
        translate_json_gemini(
            sample_json_file,
            output_json_file,
            GEMINI_API_KEY,
            fields_to_translate=["title", "content"],
            model=GEMINI_MODEL,
            role="translator"
        )
        
        # 验证传递给 GeminiTranslator 的参数
        MockGeminiTranslator.assert_called_once_with(
            api_key=GEMINI_API_KEY,
            model=GEMINI_MODEL,
            role='translator'
        )
  