from pydantic import BaseModel

class ClientInfo(BaseModel):
    name: str
    version: str

class ServerInfo(BaseModel):
    name: str
    version: str