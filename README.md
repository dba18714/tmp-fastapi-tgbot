# Telegram Echo Bot

一个使用 FastAPI 和 python-telegram-bot 构建的简单回声机器人，支持 webhook 方式。

## 功能特性

- 🔄 回声功能：重复用户发送的消息
- 🚀 基于 FastAPI 的高性能 web 服务
- 🔗 支持 Telegram webhook
- 📝 完整的日志记录
- 🛡️ Webhook 安全验证
- 💻 支持命令处理（/start, /help）

## 快速开始

### 1. 创建 Telegram Bot

1. 在 Telegram 中找到 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 命令
3. 按照提示设置机器人名称和用户名
4. 获取 Bot Token

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
TELEGRAM_BOT_TOKEN=你的机器人token
WEBHOOK_URL=https://你的域名.com
WEBHOOK_SECRET=可选的密钥
```

### 4. 运行应用

#### 开发环境

```bash
python main.py
```

#### 生产环境

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API 端点

- `GET /` - 根路径，返回服务状态
- `POST /webhook` - Telegram webhook 端点
- `GET /health` - 健康检查端点

## 部署说明

### 本地测试（使用 ngrok）

1. 安装 ngrok: https://ngrok.com/
2. 运行应用：`python main.py`
3. 在另一个终端运行：`ngrok http 8000`
4. 将 ngrok 提供的 HTTPS URL 设置为 `WEBHOOK_URL`

### 生产部署

1. 确保你有一个支持 HTTPS 的域名
2. 设置正确的 `WEBHOOK_URL`
3. 可选：设置 `WEBHOOK_SECRET` 增强安全性
4. 使用进程管理器（如 PM2、systemd）运行应用

## 机器人命令

- `/start` - 开始使用机器人
- `/help` - 显示帮助信息

## 项目结构

```
.
├── main.py              # 主应用文件
├── requirements.txt     # Python 依赖
├── .env.example        # 环境变量示例
├── .env               # 环境变量（需要创建）
└── README.md          # 项目说明
```

## 开发说明

### 添加新功能

1. 在 `main.py` 中添加新的处理器函数
2. 在 `create_telegram_app()` 中注册处理器
3. 重启应用

### 日志

应用使用 Python 标准日志库，日志级别设置为 INFO。在生产环境中可以调整日志级别。

## 故障排除

### 常见问题

1. **Bot Token 无效**
   - 检查 `.env` 文件中的 `TELEGRAM_BOT_TOKEN`
   - 确保 token 来自 @BotFather

2. **Webhook 设置失败**
   - 确保 `WEBHOOK_URL` 是有效的 HTTPS URL
   - 检查服务器是否可以从外网访问

3. **消息无响应**
   - 检查应用日志
   - 确认 webhook 端点可以正常访问

## 许可证

MIT License
