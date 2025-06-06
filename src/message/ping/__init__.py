from src.transport.base import BaseTransport
from src.types.json_rpc import JSONRPCRequest,Method
from uuid import uuid4

async def send_ping(transport:BaseTransport)->bool:
    request=JSONRPCRequest(id=str(uuid4()),method=Method.PING)
    response=await transport.send_request(request=request)
    return response is not None