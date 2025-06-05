from src.types.resources import Resource, ResourceTemplate, ResourceContent
from src.types.json_rpc import JSONRPCMessage, Method
from src.transport.base import BaseTransport
from typing import Optional
from uuid import uuid4

async def send_resources_list(transport:BaseTransport,cursor:Optional[str]=None)->list[Resource]:
    message=JSONRPCMessage(id=str(uuid4()),method=Method.RESOURCES_LIST,params={"cursor":cursor} if cursor else {})
    response=await transport.send_message(message=message)
    return [Resource.model_validate(resource) for resource in response.result.get("resources")]

async def send_resources_read(transport:BaseTransport,uri:str)->ResourceContent:
    message=JSONRPCMessage(id=str(uuid4()),method=Method.RESOURCES_READ,params={"uri":uri})
    response=await transport.send_message(message=message)
    return [ResourceContent.model_validate(resource) for resource in response.result.get("contents")]

async def send_resources_templates_list(transport:BaseTransport)->list[ResourceTemplate]:
    message=JSONRPCMessage(id=str(uuid4()),method=Method.RESOURCES_TEMPLATES_LIST)
    response=await transport.send_message(message=message)
    return [ResourceTemplate.model_validate(template) for template in response.result.get("resourceTemplates")]