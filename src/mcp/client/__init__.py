from src.mcp.client.utils import create_transport_from_server_config
from src.mcp.session import Session
from typing import Any
import json

class Client:
    def __init__(self,config:dict[str,dict[str,Any]]={})->None:
        self.config=config
        self.sessions:dict[str,Session]={}
        if self.config.get("mcpServers") is None:
            self.config["mcpServers"]={}
        
    @classmethod
    def from_config(cls,config:dict[str,dict[str,Any]])->'Client':
        return cls(config=config)
    
    @classmethod
    def from_config_file(cls,config_file_path:str)->'Client':
        with open(config_file_path) as f:
            config=json.load(f)
        return cls(config=config)
    
    def get_server_names(self)->list[str]:
        return list(self.config.get("mcpServers").keys())
    
    def add_server(self,name:str,server_config:dict[str,Any])->None:
        if self.config.get("mcpServers") is None:
            self.config["mcpServers"]={}
        self.config["mcpServers"][name]=server_config

    def remove_server(self,name:str)->None:
        if name in self.get_server_names():
            del self.config["mcpServers"][name]
        if name in self.sessions.keys():
            del self.sessions[name]
    
    def save_config(self,config_file_path:str)->None:
        with open(config_file_path,"w") as f:
            json.dump(self.config,f,indent=4)

    async def create_session(self,name:str)->Session:
        servers:dict[str,dict[str,Any]]=self.config.get("mcpServers")
        if not servers:
            raise Exception("No MCP servers configured")
        if name not in servers:
            raise ValueError(f"Server {name} not found in config")
        
        server_config=servers.get(name)
        transport=create_transport_from_server_config(server_config=server_config)
        session=Session(transport=transport)
        await session.connect()
        await session.initialize()
        self.sessions[name]=session
        return session
    
    def get_session(self,name:str)->Session|None:
        if name not in self.sessions:
            raise ValueError(f"Session {name} not found")
        return self.sessions.get(name)
    
    async def close_session(self,name:str)->None:
        if name not in self.sessions:
            raise ValueError(f"Session {name} not found")
        session=self.sessions.get(name)
        await session.disconnect()
        del self.sessions[name]

    async def create_all_sessions(self)->None:
        servers:dict[str,dict[str,Any]]=self.config.get("mcpServers")
        if not servers:
            raise Exception("No MCP servers configured")
        for name in servers:
            await self.create_session(name=name)

    async def close_all_sessions(self)->None:
        for name in list(self.sessions.keys()):
            await self.close_session(name=name)
    

        

