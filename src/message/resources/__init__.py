from src.types.resources import Resource, ResourceTemplate, ResourceContent
from src.types.json_rpc import JSONRPCRequest, Method
from src.transport.base import BaseTransport
from typing import Optional
from uuid import uuid4

async def send_resources_list(transport:BaseTransport,cursor:Optional[str]=None)->list[Resource]:
    request=JSONRPCRequest(id=str(uuid4()),method=Method.RESOURCES_LIST,params={"cursor":cursor} if cursor else {})
    response=await transport.send_request(request=request)
    return [Resource.model_validate(resource) for resource in response.result.get("resources")]

async def send_resources_read(transport:BaseTransport,uri:str)->ResourceContent:
    request=JSONRPCRequest(id=str(uuid4()),method=Method.RESOURCES_READ,params={"uri":uri})
    response=await transport.send_request(request=request)
    return [ResourceContent.model_validate(resource) for resource in response.result.get("contents")]

async def send_resources_templates_list(transport:BaseTransport)->list[ResourceTemplate]:
    request=JSONRPCRequest(id=str(uuid4()),method=Method.RESOURCES_TEMPLATES_LIST)
    response=await transport.send_request(request=request)
    return [ResourceTemplate.model_validate(template) for template in response.result.get("resourceTemplates")]