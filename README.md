# Papersearch-w-MCP

## Introduction

这是一个基于Model Context Protocol (MCP) 的论文搜索项目，可以通过AI助手搜索和分析arXiv论文。

## How to use

1. 安装依赖：
   ```bash
   uv sync
   ```

2. 配置环境变量：
   ```bash
   cp env.example .env
   # 编辑 .env 文件，添加你的API密钥
   ```

3. 运行项目：
   ```bash
   uv run python chatbox.py
   ```

## Reference:

- [Model Context Protocol - Fetch Server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) - MCP官方的fetch服务器实现
- [Model Context Protocol - Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) - MCP官方的文件系统服务器实现
- [MCP Official Documentation](https://github.com/modelcontextprotocol/servers) - Model Context Protocol服务器集合

