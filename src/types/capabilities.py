from pydantic import BaseModel,Field
from typing import Optional

class ServerCapabilities(BaseModel):
    prompts: Optional[dict] = None
    resources: Optional[dict] = None
    tools: Optional[dict] = None
    experimental: Optional[dict] = None

class ClientCapabilities(BaseModel):
    roots: dict = Field(default_factory=lambda: {"listChanged": True})
    sampling: dict = Field(default_factory=dict)
    experimental: dict = Field(default_factory=dict)