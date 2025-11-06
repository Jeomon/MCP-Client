from pydantic import BaseModel,ConfigDict,Field
from typing import Optional, Literal, Any

class ElicitRequest(BaseModel):
    message:str
    requestedSchema:dict[str, Any]
    model_config=ConfigDict(extra='allow')

class ElicitResult(BaseModel):
    action:Literal["accept","decline","cancel"]
    content:dict[str, str|int|float|bool|None]|None=None