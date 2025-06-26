"""
测试翻译进度显示功能的单元测试
"""

import json
import tempfile
import os
import pytest
import io
from unittest.mock import patch
from json_trans.index import JsonTranslator, BaseTranslator


class MockTranslator(BaseTranslator):
    """模拟翻译器，用于测试进度显示"""

    def __init__(self, delay: float = 0.0):
        self.delay = delay
        self.call_count = 0

    def translate_to_chinese(self, english_text: str) -> str:
        """模拟翻译，可选添加延迟"""
        import time

        if self.delay > 0:
            time.sleep(self.delay)
        self.call_count += 1
        return f"翻译: {english_text}"


@pytest.fixture
def sample_json_data():
    """提供测试用的JSON数据"""
    return {
        "title": "Hello World",
        "description": "This is a test description",
        "items": [
            {"name": "Item 1", "title": "First Item", "value": 100},
            {"name": "Item 2", "title": "Second Item", "value": 200},
        ],
        "config": {
            "title": "Configuration",
            "settings": {"name": "Default Settings", "title": "Default Title"},
        },
    }


@pytest.fixture
def temp_json_file(sample_json_data):
    """创建临时JSON文件的fixture"""
    temp_file = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    json.dump(sample_json_data, temp_file, indent=2, ensure_ascii=False)
    temp_file.close()

    yield temp_file.name

    # 清理
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


class TestProgressDisplay:
    """测试翻译进度显示功能"""

    def test_count_translatable_fields(self, sample_json_data):
        """测试统计可翻译字段的功能"""
        translator = JsonTranslator(
            translator=MockTranslator(),
            fields_to_translate=["title", "name", "description"],
        )

        count = translator._count_translatable_fields(sample_json_data)
        # 应该有9个字段需要翻译:
        # - title: "Hello World"
        # - description: "This is a test description"
        # - items[0].name: "Item 1"
        # - items[0].title: "First Item"
        # - items[1].name: "Item 2"
        # - items[1].title: "Second Item"
        # - config.title: "Configuration"
        # - config.settings.name: "Default Settings"
        # - config.settings.title: "Default Title"
        assert count == 9

    def test_count_translatable_fields_empty(self):
        """测试空数据的字段统计"""
        translator = JsonTranslator(
            translator=MockTranslator(), fields_to_translate=["title", "name"]
        )

        assert translator._count_translatable_fields({}) == 0
        assert translator._count_translatable_fields([]) == 0
        assert translator._count_translatable_fields({"other": "value"}) == 0

    def test_count_excludes_already_translated(self):
        """测试已翻译字段不被重复统计"""
        data = {"title": "翻译: Already translated", "name": "Not translated yet"}

        translator = JsonTranslator(
            translator=MockTranslator(), fields_to_translate=["title", "name"]
        )

        count = translator._count_translatable_fields(data)
        assert count == 1  # 只有 "name" 需要翻译

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_progress_output(self, mock_stdout, sample_json_data):
        """测试进度输出功能"""
        translator = JsonTranslator(
            translator=MockTranslator(), fields_to_translate=["title"]
        )

        # 设置字段总数
        translator.total_fields = 2
        translator.translated_fields = 0

        # 测试进度输出
        translator._print_progress("Hello World")
        output = mock_stdout.getvalue()

        assert "翻译进度: [1/2] 50.0%" in output
        assert "翻译中: Hello World" in output

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_progress_long_text_truncation(self, mock_stdout):
        """测试长文本的截断显示"""
        translator = JsonTranslator(
            translator=MockTranslator(), fields_to_translate=["title"]
        )

        translator.total_fields = 1
        translator.translated_fields = 0

        long_text = (
            "This is a very long text that should be truncated in the progress display"
        )
        translator._print_progress(long_text)
        output = mock_stdout.getvalue()

        # 检查是否包含截断的文本（中文输出格式）
        assert "This is a very long text that" in output
        assert len(long_text) > 30  # 确保文本确实很长

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_translate_json_file_with_progress(self, mock_stdout, temp_json_file):
        """测试完整的JSON文件翻译进度显示"""
        output_file = temp_json_file.replace(".json", "_translated.json")

        try:
            mock_translator = MockTranslator()
            translator = JsonTranslator(
                translator=mock_translator,
                fields_to_translate=["title", "name", "description"],
            )

            translator.translate_json_file(temp_json_file, output_file)

            output = mock_stdout.getvalue()

            # 检查关键进度信息
            assert "正在读取文件:" in output
            assert "发现 9 个需要翻译的字段" in output
            assert "开始翻译..." in output
            assert "翻译进度:" in output
            assert "100.0%" in output
            assert "正在保存翻译结果到:" in output
            assert "翻译完成！" in output

            # 验证翻译器被调用了正确次数
            assert mock_translator.call_count == 9

            # 验证输出文件存在且内容正确
            assert os.path.exists(output_file)
            with open(output_file, "r", encoding="utf-8") as f:
                result = json.load(f)
                assert result["title"] == "翻译: Hello World"
                assert result["description"] == "翻译: This is a test description"

        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_no_translatable_fields_message(self, mock_stdout, temp_json_file):
        """测试没有可翻译字段时的消息"""
        output_file = temp_json_file.replace(".json", "_translated.json")

        try:
            translator = JsonTranslator(
                translator=MockTranslator(),
                fields_to_translate=["nonexistent_field"],  # 不存在的字段
            )

            translator.translate_json_file(temp_json_file, output_file)

            output = mock_stdout.getvalue()
            assert "没有找到需要翻译的字段" in output

        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_progress_counter_initialization(self):
        """测试进度计数器初始化"""
        translator = JsonTranslator(
            translator=MockTranslator(), fields_to_translate=["title"]
        )

        assert translator.total_fields == 0
        assert translator.translated_fields == 0

    def test_progress_counter_updates(self, sample_json_data):
        """测试进度计数器更新"""
        translator = JsonTranslator(
            translator=MockTranslator(), fields_to_translate=["title"]
        )

        # 统计字段
        translator.total_fields = translator._count_translatable_fields(
            sample_json_data
        )
        translator.translated_fields = 0

        assert translator.total_fields == 5  # 5个title字段

        # 模拟翻译过程中的计数器更新
        translator._print_progress("test1")
        assert translator.translated_fields == 1

        translator._print_progress("test2")
        assert translator.translated_fields == 2
