# 故障排除指南

## Webhook 相关问题

### 1. "Bad webhook: failed to resolve host" 错误

**问题描述**: 应用启动时出现 webhook 设置失败的错误。

**原因**: 
- WEBHOOK_URL 配置不正确
- 域名无法解析
- 网络连接问题

**解决方案**:

#### 方案一：跳过 Webhook 设置（开发环境）
在 `.env` 文件中设置：
```env
ENVIRONMENT=development
WEBHOOK_URL=
```

#### 方案二：使用正确的生产环境 URL
确保 WEBHOOK_URL 是有效的 HTTPS 地址：
```env
ENVIRONMENT=production
WEBHOOK_URL=https://your-actual-domain.com
```

#### 方案三：使用 ngrok 进行本地测试
1. 安装 ngrok: https://ngrok.com/
2. 启动应用: `python3 main.py`
3. 在新终端运行: `ngrok http 8000`
4. 复制 ngrok 的 HTTPS URL 到 `.env`:
   ```env
   WEBHOOK_URL=https://abc123.ngrok.io
   ```

### 2. 应用启动但机器人无响应

**检查步骤**:

1. **验证 Bot Token**:
   ```bash
   curl "https://api.telegram.org/bot你的token/getMe"
   ```

2. **检查 Webhook 状态**:
   ```bash
   curl "https://api.telegram.org/bot你的token/getWebhookInfo"
   ```

3. **测试 Webhook 端点**:
   ```bash
   curl -X POST https://你的域名.com/webhook
   ```

### 3. 部署平台特定问题

#### Zeabur 部署
```env
# .env 配置
ENVIRONMENT=production
WEBHOOK_URL=https://your-app.zeabur.app
PORT=8000
```

#### Railway 部署
```env
# .env 配置
ENVIRONMENT=production
WEBHOOK_URL=https://your-app.railway.app
PORT=$PORT
```

#### Heroku 部署
```env
# .env 配置
ENVIRONMENT=production
WEBHOOK_URL=https://your-app.herokuapp.com
PORT=$PORT
```

## 配置问题

### 环境变量未生效

**检查**:
1. `.env` 文件是否存在
2. 文件格式是否正确（无空格、正确的等号）
3. 重启应用

**示例正确格式**:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
WEBHOOK_URL=https://example.com
ENVIRONMENT=production
```

### Token 无效

**症状**: 
- 测试时显示 "Bot Token 配置: ❌"
- API 调用返回 401 错误

**解决**:
1. 检查 token 是否完整
2. 确认从 @BotFather 获取的是正确的 token
3. 检查是否有多余的空格或换行符

## 网络问题

### 防火墙设置

确保以下端口开放:
- 入站: 8000 (或你设置的 PORT)
- 出站: 443 (HTTPS)

### SSL/TLS 证书

Telegram 要求 webhook URL 必须使用有效的 HTTPS 证书。

**检查证书**:
```bash
curl -I https://你的域名.com
```

## 日志调试

### 启用详细日志

在 `.env` 中设置:
```env
DEBUG=true
```

### 查看应用日志

**本地运行**:
```bash
python3 main.py
```

**Docker 运行**:
```bash
docker logs container-name
```

**系统服务**:
```bash
sudo journalctl -u telegram-bot -f
```

## 常用调试命令

### 测试机器人连接
```bash
python3 test_bot.py
```

### 检查健康状态
```bash
curl http://localhost:8000/health
```

### 手动设置 Webhook
```bash
curl -X POST "https://api.telegram.org/bot你的token/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://你的域名.com/webhook"}'
```

### 删除 Webhook
```bash
curl -X POST "https://api.telegram.org/bot你的token/deleteWebhook"
```

## 性能优化

### 生产环境建议

1. **使用多个工作进程**:
   ```env
   WORKERS=2
   ```

2. **关闭调试模式**:
   ```env
   DEBUG=false
   ```

3. **使用反向代理** (Nginx):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 联系支持

如果问题仍然存在:

1. 检查 GitHub Issues
2. 提供完整的错误日志
3. 说明部署环境和配置
4. 包含复现步骤
