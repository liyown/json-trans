#!/usr/bin/env python3
"""
演示翻译进度显示功能的示例

运行此脚本将展示翻译过程中的进度显示，包括：
- 字段总数统计
- 实时翻译进度
- 完成状态显示
"""

import json
import tempfile
import os
from json_trans.index import JsonTranslator


class DemoTranslator:
    """演示用的翻译器"""

    def translate_to_chinese(self, english_text: str) -> str:
        """模拟翻译，添加延迟以展示进度效果"""
        import time

        time.sleep(0.8)  # 模拟API调用延迟

        # 简单的演示翻译
        translations = {
            "Hello World": "你好世界",
            "Welcome": "欢迎",
            "Settings": "设置",
            "Configuration": "配置",
            "User Profile": "用户资料",
            "Dashboard": "仪表板",
            "About": "关于",
            "Contact": "联系我们",
        }

        return translations.get(english_text, f"翻译: {english_text}")


def create_demo_data():
    """创建演示用的JSON数据"""
    return {
        "title": "Hello World",
        "navigation": {"home": "Welcome", "settings": "Settings", "about": "About"},
        "pages": [
            {"title": "User Profile", "description": "Manage your account settings"},
            {"title": "Dashboard", "description": "View your statistics and data"},
        ],
        "footer": {"title": "Contact", "description": "Get in touch with us"},
    }


def main():
    """主演示函数"""
    print("🎯 JSON翻译进度显示演示")
    print("=" * 50)

    # 创建演示数据
    demo_data = create_demo_data()

    # 创建临时文件
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as temp_file:
        json.dump(demo_data, temp_file, indent=2, ensure_ascii=False)
        input_file = temp_file.name

    output_file = input_file.replace(".json", "_translated.json")

    try:
        print(f"📄 原始文件: {input_file}")
        print("📋 原始内容:")
        print(json.dumps(demo_data, indent=2, ensure_ascii=False))
        print()

        # 创建翻译器
        translator = JsonTranslator(
            translator=DemoTranslator(),
            fields_to_translate=["title", "description", "home", "settings", "about"],
        )

        print("🚀 开始翻译...")
        print()

        # 执行翻译（会显示进度）
        translator.translate_json_file(input_file, output_file)

        print()
        print("📄 翻译结果:")
        with open(output_file, "r", encoding="utf-8") as f:
            result = json.load(f)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        print()
        print("✅ 演示完成！")
        print(f"翻译后的文件已保存到: {output_file}")

    except Exception as e:
        print(f"❌ 演示过程中出错: {e}")

    finally:
        # 清理临时文件
        for file_path in [input_file, output_file]:
            if os.path.exists(file_path):
                os.unlink(file_path)
                print(f"🧹 已清理临时文件: {file_path}")


if __name__ == "__main__":
    main()
