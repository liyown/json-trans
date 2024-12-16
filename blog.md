# json-trans: 一个强大的 JSON 文件翻译工具

在开发国际化应用时，我们经常需要处理大量的翻译工作。特别是当面对复杂的 JSON 配置文件时，手动翻译不仅耗时，还容易出错。今天我要介绍一个强大的工具：json-trans，它可以帮助你自动化这个过程。

## 特点

json-trans 的主要特点包括：

1. **灵活的翻译字段选择**
   - 可以指定任意字段进行翻译
   - 支持嵌套 JSON 结构
   - 保持原始 JSON 结构不变

2. **多平台支持**
   - 支持百度翻译 API
   - 支持谷歌云翻译 API
   - 可扩展的翻译器接口

3. **开发者友好**
   - 完整的类型提示
   - 详细的文档
   - 全面的测试覆盖

## 安装

使用 pip 安装：

```bash
pip install json-trans
```

## 基本使用

### 使用百度翻译

```python
from json_trans import translate_json_baidu

# 翻译指定字段
translate_json_baidu(
    input_file="config.json",
    output_file="config.zh.json",
    app_id="your_baidu_app_id",
    secret_key="your_baidu_secret_key",
    fields_to_translate=["title", "description", "content"]
)
```

### 使用谷歌翻译

```python
from json_trans import translate_json_google

translate_json_google(
    input_file="config.json",
    output_file="config.zh.json",
    fields_to_translate=["title", "description", "content"],
    credentials_path="path/to/google_credentials.json"
)
```

## 实际应用场景

### 1. 产品文档国际化

假设你有一个产品文档的 JSON 文件：

```json
{
    "product": {
        "name": "Smart Home Hub",
        "description": "A central control system for your smart home",
        "features": [
            {
                "title": "Voice Control",
                "description": "Control your home with voice commands"
            },
            {
                "title": "Energy Monitoring",
                "description": "Track and optimize your energy usage"
            }
        ]
    }
}
```

使用 json-trans，只需要几行代码就能完成翻译：

```python
translate_json_baidu(
    input_file="product_doc.json",
    output_file="product_doc.zh.json",
    app_id="your_app_id",
    secret_key="your_secret_key",
    fields_to_translate=["description", "title"]
)
```

### 2. API 响应本地化

对于需要支持多语言的 API 服务，可以这样使用：

```python
import json
from json_trans import JsonTranslator, BaiduTranslator

class APITranslator:
    def __init__(self):
        self.translator = JsonTranslator(
            BaiduTranslator(app_id="xxx", secret_key="xxx"),
            fields_to_translate=["message", "description"]
        )
    
    def translate_response(self, response_data: dict) -> dict:
        translated_data = response_data.copy()
        self.translator.find_and_replace_titles(translated_data)
        return translated_data

# 使用示例
api_translator = APITranslator()
response = {
    "status": "success",
    "message": "Operation completed successfully",
    "data": {
        "description": "User profile updated"
    }
}
chinese_response = api_translator.translate_response(response)
```

### 3. 自定义翻译器

如果你想使用其他翻译服务，可以轻松实现自己的翻译器：

```python
from json_trans import BaseTranslator, JsonTranslator

class MyTranslator(BaseTranslator):
    def translate_to_chinese(self, text: str) -> str:
        # 实现你的翻译逻辑
        return translated_text

translator = JsonTranslator(
    MyTranslator(),
    fields_to_translate=["title", "description"]
)
```

## 最佳实践

1. **选择性翻译**
   - 仔细选择需要翻译的字段
   - 避免���译不需要翻译的技术字段

2. **错误处理**
   - 翻译失败时会保留原文
   - 建议在生产环境中添加日志记录

3. **性能优化**
   - 批量处理大文件
   - 注意 API 调用限制

## 未来展望

json-trans 还在持续发展中，计划添加的功能包括：

1. 支持更多翻译服务
2. 添加缓存机制
3. 支持更多的文件格式
4. 提供命令行界面

## 结论

json-trans 是一个强大而灵活的 JSON 翻译工具，它可以显著提高国际化开发的效率。无论是处理文档、API 响应还是配置文件，json-trans 都能帮你轻松完成翻译工作。

## 相关链接

- [GitHub 仓库](https://github.com/yourusername/json-trans)
- [完整文档](https://github.com/yourusername/json-trans#readme)
- [PyPI 页面](https://pypi.org/project/json-trans/)

## 作者

CuiZhengPeng & Liuyaowen

欢迎贡献代码或提出建议！ 