# 安全配置指南

## API 密钥管理

本项目使用 OpenAI 和 Anthropic 的 API，需要正确配置API密钥以确保安全性。

### 1. 环境变量配置

1. 复制 `env.example` 文件为 `.env`：
   ```bash
   cp env.example .env
   ```

2. 编辑 `.env` 文件，填入你的真实API密钥：
   ```bash
   # OpenAI API 密钥
   OPENAI_KEY=sk-your-actual-openai-key-here
   OPENAI_API_KEY=sk-your-actual-openai-key-here
   
   # Anthropic API 密钥  
   ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here
   ```

### 2. 安全注意事项

- ⚠️ **绝对不要**将 `.env` 文件提交到Git仓库
- ⚠️ **绝对不要**在代码中硬编码API密钥
- ⚠️ **绝对不要**将API密钥分享给他人或上传到公共平台

### 3. 已防护的文件类型

项目的 `.gitignore` 文件已配置防止以下敏感文件被提交：

- `.env` 及其变体文件
- 包含 `secret`、`password`、`token`、`credential` 等关键词的文件
- 各种配置文件如 `config.json`、`secrets.json` 等

### 4. 获取API密钥

- **OpenAI API密钥**: 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
- **Anthropic API密钥**: 访问 [Anthropic Console](https://console.anthropic.com/)

### 5. 验证配置

运行项目前，确保环境变量已正确加载：

```python
import os
from dotenv import load_dotenv

load_dotenv()

# 检查密钥是否已加载
if not os.getenv("OPENAI_KEY"):
    print("警告：未找到 OPENAI_KEY 环境变量")

if not os.getenv("ANTHROPIC_API_KEY"):
    print("警告：未找到 ANTHROPIC_API_KEY 环境变量")
```

### 6. 如果意外提交了密钥

如果你不小心将包含API密钥的文件提交到了Git仓库：

1. 立即撤销并重新生成API密钥
2. 从Git历史中删除敏感信息：
   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all
   ```
3. 强制推送到远程仓库：
   ```bash
   git push --force --all
   ``` 