from pydantic import BaseModel,ConfigDict
from typing import Optional

class ServerCapabilities(BaseModel):
    prompts: Optional['PromptCapability'] = None
    resources: Optional['ResourceCapability'] = None
    tools: Optional['ToolCapability'] = None
    experimental: Optional[dict] = None

class ToolCapability(BaseModel):
    listChanged:bool
    model_config=ConfigDict(extra='allow')

class PromptCapability(BaseModel):
    listChanged:bool
    model_config=ConfigDict(extra='allow')

class ResourceCapability(BaseModel):
    listChanged:bool
    subscribe:bool
    model_config=ConfigDict(extra='allow')

class SamplingCapability(BaseModel):
    model_config=ConfigDict(extra='allow')

class ElicitationCapability(BaseModel):
    model_config=ConfigDict(extra='allow')

class RootCapability(BaseModel):
    listChanged:bool
    model_config=ConfigDict(extra='allow')

class ClientCapabilities(BaseModel):
    roots: Optional['RootCapability'] = None
    sampling: Optional['SamplingCapability'] = None
    elicitation: Optional['ElicitationCapability'] = None
    model_config=ConfigDict(extra='allow')