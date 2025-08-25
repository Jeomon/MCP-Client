from src.mcp.types.tools import ToolResult as MCPToolResult, Tool as MCPTool
from src.tool.registry.views import Function,ToolResult
from src.mcp.client.session import Session
from functools import partial
from src.tool import Tool

class Registry:
    def __init__(self,tools:list[Tool]=[]):
        self.tools=tools
        self.mcp_tools=[]
    
    def get_tools_schema(self):
        tools_schema=[tool.get_tool_schema() for tool in self.tools+self.mcp_tools]
        return '\n\n'.join(tools_schema)
    
    def registry(self)->dict[str,Function]:
        return {tool.name:Function(
            name=tool.name,
            description=tool.description,
            params=tool.params,
            function=tool.func
        ) for tool in self.tools+self.mcp_tools}
    
    def add_tools(self,tools:list[Tool]):
        self.tools.extend(tools)
    
    async def add_tools_from_session(self,session:Session):
        mcp_tools:list[MCPTool]=await session.tools_list()
        tools=[Tool(
            name=mcp_tool.name,
            description=mcp_tool.description,
            schema=mcp_tool.inputSchema,
            func=partial(session.tools_call,mcp_tool.name)
        ) for mcp_tool in mcp_tools]
        self.mcp_tools.extend(tools)
    
    async def add_tools_from_sessions(self,sessions:list[Session]):
        self.mcp_tools=[]
        for session in sessions:
            await self.add_tools_from_session(session)

    async def async_execute(self,name:str,input:dict,**kwargs)->ToolResult:
        registry=self.registry()
        tool=registry.get(name)
        try:
            if tool is None:
                raise ValueError('Tool not found. Check the available tools.')
            if tool.params:
                tool_params=tool.params.model_validate(input)
                params=tool_params.model_dump()|kwargs
            else:
                params=input
            content=await tool.function(**params)
            if isinstance(content,MCPToolResult):
                content=content.content[0].text
        except Exception as e:
            content=str(e)
            print(f'Error: {e}')
        return ToolResult(name=name,content=content)

    def execute(self,name:str,input:dict,**kwargs)->ToolResult:
        registry=self.registry()
        tool=registry.get(name)
        try:
            if tool is None:
                raise ValueError('Tool not found. Check the available tools.')
            if tool.params:
                tool_params=tool.params.model_validate(input)
                params=tool_params.model_dump()|kwargs
            else:
                params=input
            content=tool.function(**params)
            if isinstance(content,MCPToolResult):
                content=content.content[0].text
        except Exception as e:
            content=str(e)
            print(f'Error: {e}')
        return ToolResult(name=name,content=content)
    
