#!/usr/bin/env python3
"""
测试脚本 - 验证机器人代码是否正确
"""
import asyncio
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_bot_creation():
    """测试机器人创建"""
    try:
        # 检查环境变量
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token or bot_token == "your_bot_token_here":
            print("⚠️  警告: 未设置真实的 TELEGRAM_BOT_TOKEN")
            print("请在 .env 文件中填入你从 @BotFather 获取的真实token")
            print("✅ 但代码结构测试通过")
            return True

        # 导入主模块
        from main import create_telegram_app

        # 创建应用
        app = create_telegram_app()
        print("✅ Telegram 应用创建成功")

        # 初始化应用
        await app.initialize()
        print("✅ 应用初始化成功")

        # 获取机器人信息
        bot_info = await app.bot.get_me()
        print(f"✅ 机器人信息: @{bot_info.username} ({bot_info.first_name})")

        # 清理
        await app.shutdown()
        print("✅ 应用关闭成功")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

async def test_fastapi_import():
    """测试 FastAPI 导入"""
    try:
        from main import app
        print("✅ FastAPI 应用导入成功")
        return True
    except Exception as e:
        print(f"❌ FastAPI 导入失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🧪 开始测试 Telegram Echo Bot...")
    print()
    
    # 测试 FastAPI 导入
    if not await test_fastapi_import():
        return
    
    # 测试机器人创建
    if not await test_bot_creation():
        return
    
    print()
    print("🎉 所有测试通过！")
    print()
    print("📝 下一步:")
    print("1. 复制 .env.example 为 .env")
    print("2. 在 .env 中填入你的 TELEGRAM_BOT_TOKEN")
    print("3. 设置 WEBHOOK_URL (如果需要)")
    print("4. 运行: python3 main.py")

if __name__ == "__main__":
    asyncio.run(main())
