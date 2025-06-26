# json-trans

[![PyPI version](https://badge.fury.io/py/json-trans.svg)](https://badge.fury.io/py/json-trans)
[![Python Support](https://img.shields.io/pypi/pyversions/json-trans.svg)](https://pypi.org/project/json-trans/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python tool for translating JSON files from English to Chinese, supporting multiple translation APIs.

一个支持多种翻译API的JSON文件英译中工具。

## Features | 特性

- Translate JSON files while preserving structure
- Support for multiple translation services:
  - Baidu Translate API
  - Google Cloud Translation API
  - Google Gemini API
- Automatic handling of nested JSON structures
- Customizable fields for translation
- Type hints for better IDE support
- Comprehensive test coverage

---

- 在保持结构的同时翻译JSON文件
- 支持多种翻译服务：
  - 百度翻译API
  - 谷歌云翻译API
  - 谷歌 Gemini API
- 自动处理嵌套的JSON结构
- 支持自定义翻译字段
- 提供类型提示以获得更好的IDE支持
- 全面的测试覆盖

## Installation | 安装

```bash
pip install json-trans
```

## Quick Start | 快速开始

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

### Using Google Gemini API | 使用谷歌 Gemini API

```python
from json_trans import translate_json_gemini

# Basic usage | 基本用法
translate_json_gemini(
    input_file="input.json",
    output_file="output.json",
    api_key="your_gemini_api_key",
    fields_to_translate=["title", "content", "description"]
)

# With custom model and role | 使用自定义模型和角色
translate_json_gemini(
    input_file="input.json",
    output_file="output.json",
    api_key="your_gemini_api_key",
    fields_to_translate=["title", "content", "description"],
    model="gemini-pro",  # Optional | 可选
    role="translator"    # Optional | 可选
)
```

## Configuration | 配置

### Environment Variables | 环境变量

You can set up environment variables for different environments:
可以为不同环境设置环境变量：

```bash
# Baidu Translate API credentials
BAIDU_APP_ID=your_baidu_app_id
BAIDU_SECRET_KEY=your_baidu_secret_key

# Google Gemini API configuration
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash-exp

# Google Cloud Translation credentials path
GOOGLE_CREDENTIALS_PATH=path/to/your/credentials.json
```

### API Configuration | API配置

1. Baidu Translate API:
   - Register at [Baidu Translate](http://api.fanyi.baidu.com/api/trans/product/desktop)
   - Get your APP ID and Secret Key

2. Google Cloud Translation API:
   - Create a project in [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Cloud Translation API
   - Create a service account and download credentials

3. Google Gemini API:
   - Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Choose appropriate model (default: gemini-2.0-flash-exp)

## Development | 开发

### Setup | 设置

```bash
# Clone the repository | 克隆仓库
git clone https://github.com/liyown/json-trans.git
cd json-trans

# Install dependencies | 安装依赖
poetry install

# Set up environment variables | 设置环境变量
cp .env.example .env
# Edit .env with your credentials | 编辑 .env 填入您的凭证

# Run tests | 运行测试
poetry run pytest
```

### Testing | 测试

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
2. Create your feature branch | 创建特性分支
3. Commit your changes | 提交更改
4. Push to the branch | 推送到分支
5. Open a Pull Request | 开启拉取请求

## License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## Authors | 作者

- CuiZhengPeng & Liuyaowen

## Changelog | 更新日志

### 0.2.0
- Added Google Gemini API support
- Added environment variables support
- Improved test coverage
- Added custom model selection for Gemini API

### 0.1.1
- Initial release
- Support for Baidu and Google Cloud Translation APIs
- Basic JSON translation functionality

## Acknowledgments | 致谢

- Thanks to Baidu Translate API, Google Cloud Translation API, and Google Gemini API for providing translation services
- Built with [Poetry](https://python-poetry.org/)
