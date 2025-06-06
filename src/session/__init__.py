from src.types.json_rpc import JSONRPCRequest, JSONRPCResponse, JSONRPCNotification, Method
from src.types.initialize import InitializeResult,InitializeParams
from src.types.capabilities import ClientCapabilities
from src.transport.base import BaseTransport
from src.types.tools import Tool, ToolRequest, ToolResult
from src.types.prompts import Prompt, PromptContent
from src.types.resources import Resource, ResourceContent, ResourceTemplate
from src.types.info import ClientInfo
from typing import Optional

from uuid import uuid4

class Session:
    def __init__(self,transport:BaseTransport)->None:
        self.id=str(uuid4())
        self.transport=transport

    async def connect(self)->None:
        await self.transport.connect()

    async def initialize(self)->InitializeResult:
        client_version="2024-11-05"
        initialize_params=InitializeParams(clientInfo=ClientInfo(),capabilities=ClientCapabilities(),protocolVersion=client_version)

        request=JSONRPCRequest(id=self.id,method=Method.INITIALIZE,params=initialize_params.model_dump())
        response=await self.transport.send_request(request=request)

        json_rpc_notification=JSONRPCNotification(method=Method.NOTIFICATION_INITIALIZED)
        await self.transport.send_notification(json_rpc_notification)

        return InitializeResult.model_validate(response.result)
    
    async def ping(self)->bool:
        request=JSONRPCRequest(id=self.id,method=Method.PING)
        response=await self.transport.send_request(request=request)
        return response is not None

    async def send_prompts_list(self)->list[Prompt]:
        request=JSONRPCRequest(id=self.id,method=Method.PROMPTS_LIST)
        response=await self.transport.send_request(request=request)
        return [Prompt.model_validate(prompt) for prompt in response.result.get("prompts")]
    
    async def send_prompts_get(self,name:str)->PromptContent:
        request=JSONRPCRequest(id=self.id,method=Method.PROMPTS_GET,params={"name":name})
        response=await self.transport.send_request(request=request)
        return PromptContent.model_validate(response.result)
    
    async def send_resources_list(self,cursor:Optional[str]=None)->list[Resource]:
        request=JSONRPCRequest(id=self.id,method=Method.RESOURCES_LIST,params={"cursor":cursor} if cursor else {})
        response=await self.transport.send_request(request=request)
        return [Resource.model_validate(resource) for resource in response.result.get("resources")]
    
    async def send_resources_read(self,uri:str)->ResourceContent:
        request=JSONRPCRequest(id=self.id,method=Method.RESOURCES_READ,params={"uri":uri})
        response=await self.transport.send_request(request=request)
        return [ResourceContent.model_validate(resource) for resource in response.result.get("contents")]
    
    async def send_resources_templates_list(self)->list[ResourceTemplate]:
        request=JSONRPCRequest(id=self.id,method=Method.RESOURCES_TEMPLATES_LIST)
        response=await self.transport.send_request(request=request)
        return [ResourceTemplate.model_validate(template) for template in response.result.get("resourceTemplates")]
    
    async def send_tools_list(self,cursor:Optional[str]=None)->list[Tool]:
        message=JSONRPCRequest(id=self.id,method=Method.TOOLS_LIST,params={"cursor":cursor} if cursor else {})
        response=await self.transport.send_request(request=message)
        return [Tool.model_validate(tool) for tool in response.result.get("tools")]
    
    async def send_tools_call(self,tool_request:ToolRequest)->ToolRequest:
        message=JSONRPCRequest(id=self.id,method=Method.TOOLS_CALL,params=tool_request.model_dump())
        response=await self.transport.send_request(request=message)
        return ToolResult.model_validate(response.result)

    async def disconnect(self)->None:
        await self.transport.disconnect()