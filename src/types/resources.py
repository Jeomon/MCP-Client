from typing import Optional
from pydantic import BaseModel,Field

class Resource(BaseModel):
    uri: str
    name: str
    description: Optional[str]=None
    mimeType: Optional[str]=None
    size: Optional[int]=None

class ResourceTemplate(BaseModel):
    uriTemplate: str
    name: str
    description: Optional[str]=None
    mimeType: Optional[str]=None

class ResourceContent(BaseModel):
    uri: str
    mimeType: Optional[str]=None
    text: Optional[str]=None
    blob: Optional[str]=None # base64 encoded binary data