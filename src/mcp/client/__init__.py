from src.mcp.client.utils import create_transport_from_server_config
from src.mcp.types.info import ClientInfo
from src.mcp.client.session import Session
from typing import Any
import json

class MCPClient:
    client_info=ClientInfo(name="MCP Client",version="0.1.0")
    def __init__(self,config:dict[str,dict[str,Any]]={})->None:
        self.servers=config.get("mcpServers",{})
        self.sessions:dict[str,Session]={}
        
    @classmethod
    def from_config(cls,config:dict[str,dict[str,Any]])->'MCPClient':
        return cls(config=config)
    
    @classmethod
    def from_config_file(cls,config_file_path:str)->'MCPClient':
        with open(config_file_path) as f:
            config=json.load(f)
        return cls(config=config)
    
    def get_server_names(self)->list[str]:
        return list(self.servers.keys())
    
    def get_servers_metadata(self)->list[dict[str,bool]]:
        return [{
            'name':name,
            'description':config.get("description",""),
            'status':self.is_connected(name)
        } for name,config in self.servers.items()]

    def to_config_file(self,config_file_path:str)->None:
        with open(config_file_path,"w") as f:
            json.dump(self.to_config(),f,indent=4)

    def to_config(self)->dict[str,dict[str,Any]]:
        return {"mcpServers":self.servers}

    def add_server(self,name:str,config:dict[str,Any],auto_connect:bool=False)->None:
        self.servers[name]=config
        if auto_connect:
            self.create_session(name)

    def remove_server(self,name:str)->None:
        if self.get_session(name):
            self.close_session(name)
        del self.servers[name]

    async def create_session(self,name:str)->Session:
        if not self.servers:
            raise Exception("No MCP servers available")
        if name not in self.servers:
            raise ValueError(f"{name} not found")
        server_config=self.servers.get(name)
        transport=create_transport_from_server_config(server_config=server_config)
        session=Session(transport=transport,client_info=self.client_info)
        await session.connect()
        await session.initialize()
        self.sessions[name]=session
        return session
    
    def is_connected(self,server_name:str)->bool:
        return server_name in self.sessions
    
    def get_session(self,name:str)->Session|None:
        if not self.is_connected(name):
            raise ValueError(f"Session {name} not found")
        return self.sessions.get(name)
    
    async def close_session(self,name:str)->None:
        if not self.is_connected(name):
            raise ValueError(f"Session {name} not found")
        session=self.sessions.get(name)
        await session.shutdown()
        del self.sessions[name]

    async def create_all_sessions(self)->None:
        for name in self.servers:
            await self.create_session(name=name)

    async def close_all_sessions(self)->None:
        for name in list(self.sessions.keys()):
            await self.close_session(name=name)
    

        

