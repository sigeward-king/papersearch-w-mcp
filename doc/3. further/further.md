## MCP with more tools


## 背景：
通过上一章内容的介绍，大家已经学会如何使用MCP的PDK实现简单的 Client 和 Server。既然MCP很好的解决了不同LLM, 使用相同工具的问题，同时MCP协议的出现也很大程度上构建了很多可以复用的工具，因此这一章的内容，就是来教如何实现让LLM实现更多工具的调用，下面将逐步实现更多工具的调用。




![Reference_server](Reference_server.png)

- [Model Context Protocol - Fetch Server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch "MCP官方的fetch服务器实现")

- [Model Context Protocol - Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) - MCP官方的文件系统服务器实现

通过这两个官方提供的MCP服务，我们可以在本地实现更为方便的文件抓取，和系统管理，在此之后我们将进一步挖掘如何通过组合这些MCP 工具让LLM实现非常复杂的工具调用和任务实现。


## 代码部分：
和之前的MCP Client 和 MCP Server的设计方法一样，首先我们需要配置 MCP 的配置文件，来告诉LLM有那些MCP服务可以使用。

```json

```


```python

```