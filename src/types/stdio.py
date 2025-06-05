from pydantic import BaseModel,Field
from typing import Optional

class StdioServerParams(BaseModel):
    command: str
    args: list[str]=Field(default_factory=list)
    env: Optional[dict[str,str]]=None