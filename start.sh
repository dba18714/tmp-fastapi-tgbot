#!/bin/bash

# Telegram Echo Bot 启动脚本

echo "🤖 Telegram Echo Bot 启动脚本"
echo "================================"

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 检查依赖是否安装
if ! python3 -c "import fastapi, telegram" &> /dev/null; then
    echo "📦 安装依赖..."
    pip3 install -r requirements.txt
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件，复制示例文件..."
    cp .env.example .env
    echo "📝 请编辑 .env 文件并填入你的 TELEGRAM_BOT_TOKEN"
    echo "然后重新运行此脚本"
    exit 1
fi

# 检查 token 是否设置
if grep -q "your_bot_token_here" .env; then
    echo "⚠️  请在 .env 文件中设置真实的 TELEGRAM_BOT_TOKEN"
    echo "📝 从 @BotFather 获取 token 后填入 .env 文件"
    exit 1
fi

# 运行测试
echo "🧪 运行测试..."
python3 test_bot.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 启动 Telegram Echo Bot..."
    echo "📍 访问 http://localhost:8000 查看状态"
    echo "🛑 按 Ctrl+C 停止服务"
    echo ""
    python3 main.py
else
    echo "❌ 测试失败，请检查配置"
    exit 1
fi
