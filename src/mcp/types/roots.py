from pydantic import BaseModel,ConfigDict
from typing import Optional

class Root(BaseModel):
    uri:str
    name:Optional[str]=None
    model_config=ConfigDict(extra='allow')