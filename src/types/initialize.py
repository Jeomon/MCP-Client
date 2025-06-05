from src.types.capabilities import ClientCapabilities,ServerCapabilities
from src.types.info import ClientInfo,ServerInfo
from pydantic import BaseModel

class InitializeParams(BaseModel):
    protocolVersion: str
    capabilities: ClientCapabilities
    clientInfo: ClientInfo

class InitializeResult(BaseModel):
    protocolVersion: str
    capabilities: ServerCapabilities
    serverInfo: ServerInfo
