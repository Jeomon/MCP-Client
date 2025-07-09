from pydantic import BaseModel,ConfigDict,Field
from typing import Optional

class ServerCapabilities(BaseModel):
    prompts: Optional['PromptCapability'] = None
    logging: Optional['LoggingCapability'] = None
    resources: Optional['ResourceCapability'] = None
    completion: Optional['CompletionCapability'] = None
    tools: Optional['ToolCapability'] = None
    experimental: Optional[dict] = None
    model_config=ConfigDict(extra='allow')

class ToolCapability(BaseModel):
    listChanged:Optional[bool]=None
    model_config=ConfigDict(extra='allow')

class CompletionCapability(BaseModel):
    model_config=ConfigDict(extra='allow')

class LoggingCapability(BaseModel):
    model_config=ConfigDict(extra='allow')

class PromptCapability(BaseModel):
    listChanged:Optional[bool]=None
    model_config=ConfigDict(extra='allow')

class ResourceCapability(BaseModel):
    listChanged:Optional[bool]=None
    subscribe:Optional[bool]=None
    model_config=ConfigDict(extra='allow')

class SamplingCapability(BaseModel):
    model_config=ConfigDict(extra='allow')

class ElicitationCapability(BaseModel):
    model_config=ConfigDict(extra='allow')

class RootCapability(BaseModel):
    listChanged:Optional[bool]=None
    model_config=ConfigDict(extra='allow')

class ClientCapabilities(BaseModel):
    experimental: Optional[dict] = Field(default_factory=dict)
    roots: Optional['RootCapability'] = Field(default_factory=lambda: RootCapability(listChanged=True))
    sampling: Optional['SamplingCapability'] = None
    elicitation: Optional['ElicitationCapability'] = None
    model_config=ConfigDict(extra='allow')