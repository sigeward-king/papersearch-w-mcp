from dotenv import load_dotenv
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List
import asyncio
import nest_asyncio
import os

load_dotenv()
nest_asyncio.apply()



class MCP_ChatBot:

    def __init__(self):
        # Initialize session and client objects
        self.session: ClientSession = None
        
        # 检查OpenAI API密钥
        openai_api_key = os.getenv("OPENAI_KEY")
        if not openai_api_key:
            raise ValueError("请设置OPENAI_API_KEY环境变量")
        
        self.openai = AsyncOpenAI(
            api_key=openai_api_key
        )
        self.model_name = "gpt-4o"  # 或者 "gpt-4-turbo", "gpt-3.5-turbo" 等

        self.available_tools: List[dict] = []

    async def process_query(self, query):
        messages = [{'role':'user', 'content':query}]
        response = await self.openai.chat.completions.create(
            max_tokens=2024,
            model=self.model_name,
            tools=self.available_tools, # tools exposed to the LLM
            messages=messages
        )
        process_query = True
        while process_query:
            assistant_content = []
            message = response.choices[0].message
            
            if message.content:
                print(message.content)
                assistant_content.append({
                    "type": "text",
                    "text": message.content
                })
            
            if message.tool_calls:
                # 添加助手消息到对话历史
                messages.append({
                    'role': 'assistant', 
                    'content': message.content,
                    'tool_calls': message.tool_calls
                })
                
                for tool_call in message.tool_calls:
                    tool_id = tool_call.id
                    tool_args = tool_call.function.arguments
                    tool_name = tool_call.function.name
                    
                    # 解析JSON参数
                    import json
                    try:
                        tool_args_dict = json.loads(tool_args)
                    except json.JSONDecodeError:
                        tool_args_dict = {}
    
                    print(f"调用工具 {tool_name}，参数：{tool_args_dict}")
                    
                    # 通过MCP客户端会话调用工具
                    result = await self.session.call_tool(tool_name, arguments=tool_args_dict)
                    
                    # 添加工具结果到消息历史
                    messages.append({
                        "role": "tool", 
                        "tool_call_id": tool_id,
                        "content": str(result.content)
                    })
                
                # 获取下一个响应
                response = await self.openai.chat.completions.create(
                    max_tokens=2024,
                    model=self.model_name,
                    tools=self.available_tools,
                    messages=messages
                )
            else:
                process_query = False

    
    
    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP 聊天机器人已启动！")
        print("输入您的查询或 'quit' 退出。")
        
        while True:
            try:
                query = input("\n查询: ").strip()
        
                if query.lower() == 'quit':
                    break
                    
                await self.process_query(query)
                print("\n")
                    
            except Exception as e:
                print(f"\n错误: {str(e)}")
    
    async def connect_to_server_and_run(self):
        # Create server parameters for stdio connection
        server_params = StdioServerParameters(
            command="uv",  # Executable
            args=["run", "research_server.py"],  # Optional command line arguments
            env=None,  # Optional environment variables
        )
        
        print("正在连接到MCP服务器...")
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session
                    # Initialize the connection
                    await session.initialize()
        
                    # List available tools
                    response = await session.list_tools()
                    
                    tools = response.tools
                    print(f"\n已连接到服务器，可用工具: {[tool.name for tool in tools]}")
                    
                    # 转换工具格式为OpenAI格式
                    self.available_tools = [{
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema
                        }
                    } for tool in response.tools]
        
                    await self.chat_loop()
        except Exception as e:
            print(f"连接服务器时出错: {e}")
            print("请确保:")
            print("1. 已安装所有依赖: uv sync")
            print("2. research_server.py 文件存在且可执行")
            print("3. 已设置OPENAI_API_KEY环境变量")
            raise


async def main():
    chatbot = MCP_ChatBot()
    await chatbot.connect_to_server_and_run()
  

if __name__ == "__main__":
    asyncio.run(main())