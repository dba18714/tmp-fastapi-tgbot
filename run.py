#!/usr/bin/env python3
"""
启动脚本 - 用于生产环境
"""
import uvicorn
import os
from config import config

if __name__ == "__main__":
    # 从环境变量获取配置，提供默认值
    workers = int(os.getenv("WORKERS", "1"))

    print(f"🚀 启动 Telegram Echo Bot")
    print(f"📍 地址: {config.HOST}:{config.PORT}")
    print(f"🌍 环境: {config.ENVIRONMENT}")
    print(f"👥 工作进程: {workers}")

    # 验证配置
    config_errors = config.validate()
    if config_errors:
        print("⚠️  配置警告:")
        for error in config_errors:
            print(f"   - {error}")
        print()

    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        workers=workers,
        log_level="debug" if config.DEBUG else "info",
        access_log=True
    )
