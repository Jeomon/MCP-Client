from pydantic import BaseModel,ConfigDict
from typing import Optional

class Root(BaseModel):
    uri:str
    name:Optional[str]=None
    model_config=ConfigDict(extra='allow')

class ListRootsRequest(BaseModel):
    model_config=ConfigDict(extra='allow')

class ListRootsResult(BaseModel):
    roots:list[Root]
    model_config=ConfigDict(extra='allow')