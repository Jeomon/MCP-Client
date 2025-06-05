from src.transport.base import BaseTransport
from src.types.json_rpc import JSONRPCMessage,Method
from uuid import uuid4

async def send_ping(transport:BaseTransport)->bool:
    message=JSONRPCMessage(id=str(uuid4()),method=Method.PING)
    response=await transport.send_message(message=message)
    return response is not None