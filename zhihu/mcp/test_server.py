#!/usr/bin/env python3
"""
简单的MCP Server测试脚本
用于在没有Inspector的情况下测试MCP Server功能
"""

import subprocess
import json
import sys

def test_mcp_server(server_script="server.py"):
    """测试MCP Server的基本功能"""
    
    # 初始化请求
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    try:
        # 启动服务器进程
        process = subprocess.Popen(
            ["uv", "run", "python", server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 发送初始化请求
        request_str = json.dumps(init_request) + "\n"
        stdout, stderr = process.communicate(input=request_str, timeout=10)
        
        print("=== MCP Server 测试结果 ===")
        print(f"返回状态码: {process.returncode}")
        print(f"标准输出: {stdout}")
        if stderr:
            print(f"错误输出: {stderr}")
            
        # 尝试解析响应
        if stdout.strip():
            try:
                response = json.loads(stdout.strip())
                print("✅ Server响应格式正确")
                print(f"响应内容: {json.dumps(response, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print("❌ Server响应不是有效的JSON格式")
        
    except subprocess.TimeoutExpired:
        print("❌ Server响应超时")
        process.kill()
    except FileNotFoundError:
        print("❌ 无法找到server.py文件或uv命令")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    server_file = sys.argv[1] if len(sys.argv) > 1 else "server.py"
    test_mcp_server(server_file) 