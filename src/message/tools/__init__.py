from src.types.tools import Tool,ToolRequest,ToolResult
from src.types.message import JSONRPCMessage, Method
from src.transport.base import BaseTransport
from typing import Optional,Any
from uuid import uuid4

async def send_tools_list(transport:BaseTransport,cursor:Optional[str]=None)->list[Tool]:
    message=JSONRPCMessage(id=str(uuid4()),method=Method.TOOLS_LIST,params={"cursor":cursor} if cursor else {})
    response=await transport.send_message(message=message)
    return [Tool.model_validate(tool) for tool in response.result.get("tools")]

async def send_tools_call(transport:BaseTransport,tool_request:ToolRequest)->dict[str,Any]:
    message=JSONRPCMessage(id=str(uuid4()),method=Method.TOOLS_CALL,params=tool_request.model_dump())
    response=await transport.send_message(message=message)
    return ToolResult.model_validate(response.result)