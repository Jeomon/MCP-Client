from src.mcp.types.resources import BinaryContent as ResourceBinaryContent, TextContent as ResourceTextContent
from pydantic import BaseModel,ConfigDict

class Prompt(BaseModel):
    name: str
    title: str
    description: str
    arguments: list['Argument']

class Argument(BaseModel):
    name: str
    description: str
    required: bool

    model_config=ConfigDict(extra='allow')

class PromptResult(BaseModel):
    description: str
    messages: list['Message']


class TextContent(BaseModel):
    type: str = 'text'
    text: str

class ImageContent(BaseModel):
    type: str = 'image'
    data: str
    mimeType: str

class AudioContent(BaseModel):
    type: str = 'audio'
    data: str
    mimeType: str

class EmbeddedResource(BaseModel):
    type:str= 'resource'
    resource: ResourceTextContent | ResourceBinaryContent

class Message(BaseModel):
    role: str
    content: TextContent | ImageContent | AudioContent | EmbeddedResource

    model_config=ConfigDict(extra='allow')