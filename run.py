#!/usr/bin/env python3
"""
启动脚本 - 用于生产环境
"""
import uvicorn
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

if __name__ == "__main__":
    # 从环境变量获取配置，提供默认值
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))
    
    print(f"🚀 启动 Telegram Echo Bot")
    print(f"📍 地址: {host}:{port}")
    print(f"👥 工作进程: {workers}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        log_level="info",
        access_log=True
    )
