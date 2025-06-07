from pydantic import BaseModel,Field,ConfigDict
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
    model_config=ConfigDict(extra='allow')

class ClientCapabilities(BaseModel):
    roots: dict = Field(default_factory=lambda: {"listChanged": True})
    sampling: dict = Field(default_factory=dict)
    experimental: dict = Field(default_factory=dict)