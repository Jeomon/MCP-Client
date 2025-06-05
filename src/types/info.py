from pydantic import BaseModel,Field

class ClientInfo(BaseModel):
    name: str='MCP Client'
    version: str='0.1'

class ServerInfo(BaseModel):
    name: str
    version: str