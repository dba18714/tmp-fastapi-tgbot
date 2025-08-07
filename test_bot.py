#!/usr/bin/env python3
"""
测试脚本 - 验证机器人代码是否正确
"""
import asyncio
from config import config

async def test_config():
    """测试配置"""
    print(f"📋 配置信息:")
    print(f"   环境: {config.ENVIRONMENT}")
    print(f"   调试模式: {config.DEBUG}")
    print(f"   服务器: {config.HOST}:{config.PORT}")
    print(f"   Bot Token 配置: {'✅' if config.has_valid_bot_token else '❌'}")
    print(f"   Webhook URL 配置: {'✅' if config.has_valid_webhook_url else '❌'}")

    # 验证配置
    errors = config.validate()
    if errors:
        print("⚠️  配置警告:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ 配置验证通过")

    return True

async def test_bot_creation():
    """测试机器人创建"""
    try:
        if not config.has_valid_bot_token:
            print("⚠️  跳过机器人连接测试（Token无效）")
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

    # 测试配置
    if not await test_config():
        return
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

    if not config.has_valid_bot_token:
        print("📝 下一步:")
        print("1. 在 .env 中填入你的 TELEGRAM_BOT_TOKEN")
        print("2. 设置 WEBHOOK_URL (生产环境)")
        print("3. 运行: python3 main.py")
    else:
        print("🚀 配置完成，可以启动应用:")
        print("   开发环境: python3 main.py")
        print("   生产环境: python3 run.py")

if __name__ == "__main__":
    asyncio.run(main())
