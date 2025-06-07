from pydantic import BaseModel,Field
from typing import Optional,Any

class ToolInputSchema(BaseModel):
    type: str
    properties: dict[str,Any]
    required: Optional[list[str]]=None

class Tool(BaseModel):
    name: str
    description: str
    inputSchema: ToolInputSchema
    annotations: Optional['Annotations']=None 

class ToolRequest(BaseModel):
    name: str
    arguments: dict[str,Any]

class ToolResult(BaseModel):
    content: list[dict[str,Any]]
    isError: bool=False

class Annotations(BaseModel):
    title: Optional[str]=None
    readOnlyHint: Optional[bool]=None
    destructiveHint: Optional[bool]=None
    idempotentHint: Optional[bool]=None
    openWorldHint: Optional[bool]=None