from src.types.tools import Tool,ToolRequest,ToolResult
from src.types.json_rpc import JSONRPCRequest, Method
from src.transport.base import BaseTransport
from typing import Optional,Any
from uuid import uuid4

async def send_tools_list(transport:BaseTransport,cursor:Optional[str]=None)->list[Tool]:
    message=JSONRPCRequest(id=str(uuid4()),method=Method.TOOLS_LIST,params={"cursor":cursor} if cursor else {})
    response=await transport.send_request(request=message)
    return [Tool.model_validate(tool) for tool in response.result.get("tools")]

async def send_tools_call(transport:BaseTransport,tool_request:ToolRequest)->ToolRequest:
    message=JSONRPCRequest(id=str(uuid4()),method=Method.TOOLS_CALL,params=tool_request.model_dump())
    response=await transport.send_request(request=message)
    return ToolResult.model_validate(response.result)