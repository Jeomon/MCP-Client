from pydantic import BaseModel,Field,ConfigDict
from typing import Literal,Optional,Any

class Prompt(BaseModel):
    name: str
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


class Message(BaseModel):
    role: str
    content: dict[str,Any]

    model_config=ConfigDict(extra='allow')