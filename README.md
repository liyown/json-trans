# json-trans

[![PyPI version](https://badge.fury.io/py/json-trans.svg)](https://badge.fury.io/py/json-trans)
[![Python Support](https://img.shields.io/pypi/pyversions/json-trans.svg)](https://pypi.org/project/json-trans/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python tool for translating JSON files from English to Chinese, supporting both Baidu Translate API and Google Cloud Translation API.

一个支持百度翻译API和谷歌云翻译API的JSON文件英译中工具。

## Features | 特性

- Translate JSON files while preserving structure
- Support for both Baidu and Google translation services
- Automatic handling of nested JSON structures
- Customizable fields for translation
- Type hints for better IDE support
- Comprehensive test coverage

---

- 在保持结构的同时翻译JSON文件
- 同时支持百度和谷歌翻译服务
- 自动处理嵌套的JSON结构
- 支持自定义翻译字段
- 提供类型提示以获得更好的IDE支持
- 全面的测试覆盖

## Installation | 安装

```bash
pip install json-trans
```

## Quick Start | 快��开始

### Using Baidu Translate API | 使用百度翻译API

```python
from json_trans import translate_json_baidu

translate_json_baidu(
    input_file="input.json",
    output_file="output.json",
    app_id="your_baidu_app_id",
    secret_key="your_baidu_secret_key",
    fields_to_translate=["title", "content", "description"]  # Required | 必需
)
```

### Using Google Cloud Translation API | 使用谷歌云翻译API

```python
from json_trans import translate_json_google

translate_json_google(
    input_file="input.json",
    output_file="output.json",
    fields_to_translate=["summary", "details", "text"],  # Required | 必需
    credentials_path="path/to/google_credentials.json"  # Optional | 可选
)
```

## Advanced Usage | 高级用法

### Custom Translation Implementation | 自定义翻译实现

```python
from json_trans import BaseTranslator, JsonTranslator

class MyCustomTranslator(BaseTranslator):
    def translate_to_chinese(self, english_text: str) -> str:
        # Implement your translation logic here | 在这里实现您的翻译逻辑
        return translated_text

# Use your custom translator | 使用您的自定义翻译器
translator = MyCustomTranslator()
json_translator = JsonTranslator(
    translator,
    fields_to_translate=["title", "content", "description"]  # Required | 必需
)
json_translator.translate_json_file("input.json", "output.json")
```

## Example JSON | JSON示例

Input | 输入:
```json
{
    "title": "Product Manual",
    "description": "User guide for the product",
    "content": "Detailed content here",
    "sections": [
        {
            "title": "Getting Started",
            "description": "How to begin",
            "text": "Step by step guide"
        }
    ]
}
```

Output (with `fields_to_translate=["description", "text"]`) | 输出:
```json
{
    "title": "Product Manual",
    "description": "产品使用指南",
    "content": "Detailed content here",
    "sections": [
        {
            "title": "Getting Started",
            "description": "如何开始",
            "text": "分步指南"
        }
    ]
}
```

## API Reference | API参考

### Classes | 类

#### JsonTranslator

Main class for handling JSON translation.

用于处理JSON翻译的主类。

```python
translator = JsonTranslator(translator_instance)
translator.translate_json_file(input_filename, output_filename)
```

#### BaiduTranslator

Implementation for Baidu Translation API.

百度翻译API的实现。

```python
translator = BaiduTranslator(app_id, secret_key)
result = translator.translate_to_chinese(text)
```

#### GoogleTranslator

Implementation for Google Cloud Translation API.

谷歌云翻译API的实现。

```python
translator = GoogleTranslator(credentials_path=None)
result = translator.translate_to_chinese(text)
```

### Convenience Functions | 便捷函数

- `translate_json_baidu(input_file, output_file, app_id, secret_key)`
- `translate_json_google(input_file, output_file, credentials_path=None)`

## Configuration | 配置

### Baidu Translation API | 百度翻译API

1. Register at [Baidu Translate](http://api.fanyi.baidu.com/api/trans/product/desktop)
2. Get your APP ID and Secret Key
3. Use these credentials in your code

---

1. 在[百度翻译](http://api.fanyi.baidu.com/api/trans/product/desktop)注册
2. 获取您的APP ID和密钥
3. 在代码中使用这些凭证

### Google Cloud Translation API | 谷歌云翻译API

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Cloud Translation API
3. Create a service account and download credentials
4. Either:
   - Set GOOGLE_APPLICATION_CREDENTIALS environment variable
   - Or provide credentials_path in code

---

1. 在[谷歌云控制台](https://console.cloud.google.com/)创建项目
2. 启用云翻译API
3. 创建服务账号并下载凭证
4. 选择���下方式之一：
   - 设置GOOGLE_APPLICATION_CREDENTIALS环境变量
   - 或在代码中提供credentials_path

## Development | 开发

### Setup | 设置

```bash
# Clone the repository | 克隆仓库
git clone https://github.com/yourusername/json-trans.git
cd json-trans

# Install dependencies | 安装依赖
poetry install

# Run tests | 运行测试
poetry run pytest
```

### Running Tests | 运行测试

```bash
# Run all tests | 运行所有测试
poetry run pytest

# Run with coverage report | 运行并生成覆盖率报告
poetry run pytest --cov

# Run specific test | 运行特定测试
poetry run pytest tests/test_translator.py::test_json_translator_init
```

## Contributing | 贡献

1. Fork the repository | 复刻仓库
2. Create your feature branch | 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. Commit your changes | 提交更改 (`git commit -m 'Add some amazing feature'`)
4. Push to the branch | 推送到分支 (`git push origin feature/amazing-feature`)
5. Open a Pull Request | 开启拉取请求

## License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## Authors | 作者

- CuiZhengPeng & Liuyaowen

## Acknowledgments | 致��

- Thanks to Baidu Translate API and Google Cloud Translation API for providing translation services
- Built with [Poetry](https://python-poetry.org/)

---

- 感谢百度翻译API和谷歌云翻译API提供的翻译服务
- 使用[Poetry](https://python-poetry.org/)构建
