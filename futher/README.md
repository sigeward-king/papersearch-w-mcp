## Lecture 6
    
    在这一章的内容中，我们将介绍，如何构建多个MCP Client 和  多个MCP Server的程序设计。


## Lecture 7

'''bash

'''


### 1. mcp 是如何定义资源的

'''python
## 使用装饰函数来定义可以从 paper://folders 获得不同的folder
@mcp.resource("papers://folders")


@mcp.resource("papers://{topic}")
'''


### 2. mcp 是如何定义提示词的：
    为什么需要提前定义好提示词信息，其主要的原因是用户本身不希望输入复杂的提示词，但是精确复杂的提示词可以实现更为稳定和优良的效果，为此我们提前设计好 Prompt templete，来帮助提升效果，他由 Server 发送给 Client 来实现这一功能。

    因此其主要是对MCP Server的代码进行修改：
    重点修改，

'''python
@mcp.prompt()

'''



### 3. MCP 如何使用资源和设计好的提示词，实现更为强大的功能。


