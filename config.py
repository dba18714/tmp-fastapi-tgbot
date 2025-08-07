"""
配置文件 - 管理环境变量和应用配置
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""
    
    # Telegram Bot 配置
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # 环境配置
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    @property
    def is_production(self) -> bool:
        """判断是否为生产环境"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """判断是否为开发环境"""
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def has_valid_bot_token(self) -> bool:
        """检查是否有有效的Bot Token"""
        return (
            self.TELEGRAM_BOT_TOKEN and 
            self.TELEGRAM_BOT_TOKEN != "your_bot_token_here" and
            len(self.TELEGRAM_BOT_TOKEN) > 10
        )
    
    @property
    def has_valid_webhook_url(self) -> bool:
        """检查是否有有效的Webhook URL"""
        return (
            self.WEBHOOK_URL and 
            self.WEBHOOK_URL != "https://your-domain.com/webhook" and
            self.WEBHOOK_URL.startswith("https://")
        )
    
    @property
    def should_set_webhook(self) -> bool:
        """判断是否应该设置webhook"""
        return self.has_valid_bot_token and self.has_valid_webhook_url
    
    def validate(self) -> list:
        """验证配置，返回错误列表"""
        errors = []
        
        if not self.has_valid_bot_token:
            errors.append("TELEGRAM_BOT_TOKEN 未设置或无效")
        
        if self.is_production and not self.has_valid_webhook_url:
            errors.append("生产环境必须设置有效的 WEBHOOK_URL")
        
        return errors

# 创建全局配置实例
config = Config()
