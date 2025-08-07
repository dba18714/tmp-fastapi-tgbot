import os
import logging
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import uvicorn

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 从环境变量获取配置
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
    print("⚠️  警告: 请在.env文件中设置真实的TELEGRAM_BOT_TOKEN")
    if not BOT_TOKEN:
        BOT_TOKEN = "dummy_token_for_testing"

# 创建FastAPI应用
app = FastAPI(title="Telegram Echo Bot", version="1.0.0")

# 创建Telegram应用实例
telegram_app: Optional[Application] = None


async def start_command(update: Update, context) -> None:
    """处理 /start 命令"""
    user = update.effective_user
    await update.message.reply_text(
        f"你好 {user.first_name}! 👋\n"
        f"我是一个简单的回声机器人。\n"
        f"发送任何消息给我，我会重复你说的话！"
    )


async def help_command(update: Update, context) -> None:
    """处理 /help 命令"""
    help_text = """
🤖 回声机器人帮助

可用命令：
/start - 开始使用机器人
/help - 显示此帮助信息

功能：
• 发送任何文本消息，我会重复给你
• 支持表情符号和特殊字符
• 简单易用的回声功能
    """
    await update.message.reply_text(help_text)


async def echo_message(update: Update, context) -> None:
    """回声功能 - 重复用户发送的消息"""
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    # 构造回复消息
    reply_text = f"🔄 {user_name} 说: {user_message}"
    
    await update.message.reply_text(reply_text)


def create_telegram_app() -> Application:
    """创建并配置Telegram应用"""
    # 创建应用
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加命令处理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # 添加消息处理器（处理所有文本消息）
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    return application


@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    global telegram_app
    
    # 创建Telegram应用
    telegram_app = create_telegram_app()
    
    # 初始化应用
    await telegram_app.initialize()
    
    # 设置webhook
    if WEBHOOK_URL:
        webhook_url = f"{WEBHOOK_URL}/webhook"
        await telegram_app.bot.set_webhook(
            url=webhook_url,
            secret_token=WEBHOOK_SECRET
        )
        logger.info(f"Webhook设置成功: {webhook_url}")
    else:
        logger.warning("未设置WEBHOOK_URL，请确保在生产环境中配置")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理"""
    global telegram_app
    if telegram_app:
        await telegram_app.shutdown()


@app.get("/")
async def root():
    """根路径 - 健康检查"""
    return {
        "message": "Telegram Echo Bot is running!",
        "status": "healthy",
        "bot_info": "Echo bot using python-telegram-bot + FastAPI"
    }


@app.post("/webhook")
async def webhook(request: Request):
    """处理Telegram webhook请求"""
    global telegram_app
    
    if not telegram_app:
        raise HTTPException(status_code=500, detail="Telegram应用未初始化")
    
    try:
        # 获取请求体
        body = await request.body()
        
        # 验证secret token（如果设置了）
        if WEBHOOK_SECRET:
            secret_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
            if secret_header != WEBHOOK_SECRET:
                logger.warning("Webhook secret token验证失败")
                raise HTTPException(status_code=403, detail="Forbidden")
        
        # 解析更新
        update = Update.de_json(await request.json(), telegram_app.bot)
        
        # 处理更新
        await telegram_app.process_update(update)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"处理webhook时出错: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误")


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "telegram-echo-bot",
        "webhook_configured": bool(WEBHOOK_URL)
    }


if __name__ == "__main__":
    # 开发环境运行
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
