from src.types.initialize import InitializeParams, InitializeResult
from src.types.capabilities import ClientCapabilities
from src.types.message import JSONRPCMessage, JSONRPCNotification, Method
from src.transport.base import BaseTransport
from src.types.info import ClientInfo
from uuid import uuid4

async def send_initialize(transport:BaseTransport,supported_versions:list[str]=["2024-11-05"])->InitializeResult:
    client_version=supported_versions[0]
    initialize_params=InitializeParams(clientInfo=ClientInfo(),capabilities=ClientCapabilities(),protocolVersion=client_version)
    
    json_rpc_message=JSONRPCMessage(id=str(uuid4()),method=Method.INITIALIZE,params=initialize_params.model_dump())
    response=await transport.send_message(json_rpc_message)

    json_rpc_notification=JSONRPCNotification(method=Method.NOTIFICATION_INITIALIZED)
    await transport.send_notification(json_rpc_notification)

    return InitializeResult.model_validate(response.result)