from src.mcp.types.json_rpc import JSONRPCRequest, JSONRPCResponse, JSONRPCNotification, Method
from src.mcp.types.initialize import InitializeResult,InitializeParams
from src.mcp.types.capabilities import ClientCapabilities
from src.mcp.transport.base import BaseTransport
from src.mcp.types.tools import Tool, ToolRequest, ToolResult
from src.mcp.types.prompts import Prompt, PromptResult
from src.mcp.types.resources import Resource, ResourceResult, ResourceTemplate
from src.mcp.types.info import ClientInfo
from typing import Optional,Any

from uuid import uuid4

class Session:
    def __init__(self,transport:BaseTransport)->None:
        self.id=str(uuid4())
        self.transport=transport

    async def connect(self)->None:
        await self.transport.connect()

    async def initialize(self)->InitializeResult:
        client_version="2024-11-05"
        params=InitializeParams(clientInfo=ClientInfo(),capabilities=ClientCapabilities(),protocolVersion=client_version)

        request=JSONRPCRequest(id=self.id,method=Method.INITIALIZE,params=params.model_dump())
        response=await self.transport.send_request(request=request)

        json_rpc_notification=JSONRPCNotification(method=Method.NOTIFICATION_INITIALIZED)
        await self.transport.send_notification(json_rpc_notification)

        return InitializeResult.model_validate(response.result)
    
    async def ping(self)->bool:
        request=JSONRPCRequest(id=self.id,method=Method.PING)
        response=await self.transport.send_request(request=request)
        return response is not None

    async def prompts_list(self)->list[Prompt]:
        request=JSONRPCRequest(id=self.id,method=Method.PROMPTS_LIST)
        response=await self.transport.send_request(request=request)
        return [Prompt.model_validate(prompt) for prompt in response.result.get("prompts")]
    
    async def prompts_get(self,name:str,arguments:Optional[dict[str,Any]]=None)->PromptResult:
        request=JSONRPCRequest(id=self.id,method=Method.PROMPTS_GET,params={"name":name,"arguments":arguments})
        response=await self.transport.send_request(request=request)
        return PromptResult.model_validate(response.result)
    
    async def resources_list(self,cursor:Optional[str]=None)->list[Resource]:
        request=JSONRPCRequest(id=self.id,method=Method.RESOURCES_LIST,params={"cursor":cursor} if cursor else {})
        response=await self.transport.send_request(request=request)
        return [Resource.model_validate(resource) for resource in response.result.get("resources")]
    
    async def resources_read(self,uri:str)->ResourceResult:
        request=JSONRPCRequest(id=self.id,method=Method.RESOURCES_READ,params={"uri":uri})
        response=await self.transport.send_request(request=request)
        return [ResourceResult.model_validate(resource) for resource in response.result.get("contents")]
    
    async def resources_templates_list(self)->list[ResourceTemplate]:
        request=JSONRPCRequest(id=self.id,method=Method.RESOURCES_TEMPLATES_LIST)
        response=await self.transport.send_request(request=request)
        return [ResourceTemplate.model_validate(template) for template in response.result.get("resourceTemplates")]
    
    async def tools_list(self,cursor:Optional[str]=None)->list[Tool]:
        message=JSONRPCRequest(id=self.id,method=Method.TOOLS_LIST,params={"cursor":cursor} if cursor else {})
        response=await self.transport.send_request(request=message)
        return [Tool.model_validate(tool) for tool in response.result.get("tools")]
    
    async def tools_call(self,name:str,arguments:dict[str,Any])->ToolResult:
        tool_request=ToolRequest(name=name,arguments=arguments)
        message=JSONRPCRequest(id=self.id,method=Method.TOOLS_CALL,params=tool_request.model_dump())
        response=await self.transport.send_request(request=message)
        return ToolResult.model_validate(response.result)

    async def disconnect(self)->None:
        await self.transport.disconnect()