from pydantic import BaseModel,ConfigDict
from typing import Callable,Type

class Function(BaseModel):
    name:str
    description:str
    params:Type[BaseModel]|None
    function:Callable|None
    model_config=ConfigDict(arbitrary_types_allowed=True)

class ToolResult(BaseModel):
    name: str
    content:str