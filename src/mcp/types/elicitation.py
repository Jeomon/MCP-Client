from pydantic import BaseModel,ConfigDict,Field
from typing import Optional, Literal


class ElicitResult(BaseModel):
    action:Literal["accept","decline","cancel"]
    content:dict[str, str|int|float|bool|None]|None=None