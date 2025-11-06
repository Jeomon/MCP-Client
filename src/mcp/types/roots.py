from pydantic import BaseModel,ConfigDict
from src.mcp.types.json_rpc import Error
from typing import Optional,Protocol

class ListRootsFn(Protocol):
    def __call__(self,params:'ListRootsRequest') -> 'ListRootsResult'|Error:
        ...

class Root(BaseModel):
    uri:str
    name:Optional[str]=None
    model_config=ConfigDict(extra='allow')

class ListRootsRequest(BaseModel):
    model_config=ConfigDict(extra='allow')

class ListRootsResult(BaseModel):
    roots:list[Root]
    model_config=ConfigDict(extra='allow')