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

class TextContent(BaseModel):
    uri: str
    name: str
    title: Optional[str]=None
    mimeType: Optional[str]=None
    text: str

class BinaryContent(BaseModel):
    uri: str
    name: str
    title: Optional[str]=None
    mimeType: Optional[str]=None
    blob: str

class ResourceResult(BaseModel):
    contents: list[TextContent | BinaryContent]