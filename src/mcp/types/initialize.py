from src.mcp.types.capabilities import ClientCapabilities,ServerCapabilities
from src.mcp.types.info import ClientInfo,ServerInfo
from pydantic import BaseModel
from typing import Optional

class InitializeParams(BaseModel):
    protocolVersion: str
    capabilities: ClientCapabilities
    clientInfo: ClientInfo

class InitializeResult(BaseModel):
    protocolVersion: str
    capabilities: ServerCapabilities
    serverInfo: ServerInfo
    instructions: Optional[str]=None