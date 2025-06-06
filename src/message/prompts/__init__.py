from src.types.json_rpc import JSONRPCRequest, JSONRPCResponse ,Method
from src.types.prompts import Prompt,PromptContent
from src.transport.base import BaseTransport
from uuid import uuid4

async def send_prompts_list(transport:BaseTransport)->list[Prompt]:
    request=JSONRPCRequest(id=str(uuid4()),method=Method.PROMPTS_LIST)
    response=await transport.send_request(request=request)
    return [Prompt.model_validate(prompt) for prompt in response.result.get("prompts")]

async def send_prompts_get(transport:BaseTransport,name:str)->PromptContent:
    request=JSONRPCRequest(id=str(uuid4()),method=Method.PROMPTS_GET,params={"name":name})
    response=await transport.send_request(request=request)
    return PromptContent.model_validate(response.result)