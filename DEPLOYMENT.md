# 部署指南

## 本地开发环境设置

### 1. 创建 Telegram Bot

1. 在 Telegram 中搜索 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 命令
3. 按照提示设置机器人名称和用户名
4. 保存获得的 Bot Token

### 2. 配置环境变量

编辑 `.env` 文件：

```env
TELEGRAM_BOT_TOKEN=你的真实token
WEBHOOK_URL=https://你的域名.com
WEBHOOK_SECRET=可选的安全密钥
```

### 3. 本地测试（使用 ngrok）

1. 安装 ngrok: https://ngrok.com/download
2. 启动应用：
   ```bash
   python3 main.py
   ```
3. 在新终端中启动 ngrok：
   ```bash
   ngrok http 8000
   ```
4. 复制 ngrok 提供的 HTTPS URL，更新 `.env` 中的 `WEBHOOK_URL`
5. 重启应用

## 生产环境部署

### 方式一：使用 Docker

创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "run.py"]
```

构建和运行：

```bash
docker build -t telegram-echo-bot .
docker run -p 8000:8000 --env-file .env telegram-echo-bot
```

### 方式二：使用 systemd (Linux)

创建服务文件 `/etc/systemd/system/telegram-bot.service`：

```ini
[Unit]
Description=Telegram Echo Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/your/bot
Environment=PATH=/path/to/your/venv/bin
ExecStart=/path/to/your/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

### 方式三：使用 PM2 (Node.js 进程管理器)

安装 PM2：

```bash
npm install -g pm2
```

创建 `ecosystem.config.js`：

```javascript
module.exports = {
  apps: [{
    name: 'telegram-echo-bot',
    script: 'run.py',
    interpreter: 'python3',
    env: {
      NODE_ENV: 'production'
    }
  }]
}
```

启动：

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 云平台部署

### Heroku

1. 创建 `Procfile`：
   ```
   web: python run.py
   ```

2. 设置环境变量：
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=你的token
   heroku config:set WEBHOOK_URL=https://你的应用名.herokuapp.com
   ```

### Railway

1. 连接 GitHub 仓库
2. 设置环境变量
3. 自动部署

### Render

1. 连接 GitHub 仓库
2. 设置构建命令：`pip install -r requirements.txt`
3. 设置启动命令：`python run.py`
4. 配置环境变量

## 监控和日志

### 健康检查

应用提供了健康检查端点：

- `GET /health` - 检查服务状态
- `GET /` - 基本信息

### 日志监控

查看应用日志：

```bash
# systemd
sudo journalctl -u telegram-bot -f

# PM2
pm2 logs telegram-echo-bot

# Docker
docker logs container-name
```

## 安全建议

1. **使用 HTTPS**: Telegram 要求 webhook URL 必须是 HTTPS
2. **设置 Secret Token**: 在 `.env` 中设置 `WEBHOOK_SECRET`
3. **防火墙配置**: 只开放必要的端口
4. **定期更新**: 保持依赖库最新版本
5. **环境变量**: 不要在代码中硬编码敏感信息

## 故障排除

### 常见问题

1. **Webhook 设置失败**
   - 检查 URL 是否可访问
   - 确保使用 HTTPS
   - 验证证书有效性

2. **机器人无响应**
   - 检查 token 是否正确
   - 查看应用日志
   - 验证 webhook 端点

3. **端口冲突**
   - 修改 `PORT` 环境变量
   - 检查其他服务占用

### 调试命令

```bash
# 测试 webhook 端点
curl -X POST https://你的域名.com/webhook

# 检查机器人信息
curl "https://api.telegram.org/bot你的token/getMe"

# 检查 webhook 状态
curl "https://api.telegram.org/bot你的token/getWebhookInfo"
```
