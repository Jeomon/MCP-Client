from pydantic import BaseModel,Field,ConfigDict
from typing import Optional

class Resource(BaseModel):
    uri: str
    name: str
    description: Optional[str]=None
    mimeType: Optional[str]=None
    size: Optional[int]=None

    model_config = ConfigDict(extra="allow")

class ResourceTemplate(BaseModel):
    uriTemplate: str
    name: str
    description: Optional[str]=None
    mimeType: Optional[str]=None

    model_config = ConfigDict(extra="allow")

class ResourceResult(BaseModel):
    uri: str
    mimeType: Optional[str]=None
    text: Optional[str]=None
    blob: Optional[str]=None # base64 encoded binary data

