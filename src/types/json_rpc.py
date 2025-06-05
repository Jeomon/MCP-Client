from pydantic import BaseModel,Field,ConfigDict
from typing import Optional,Any
from enum import Enum

class JSONRPCMessage(BaseModel):
    jsonrpc: str=Field(default="2.0")
    id: Optional[str]=None
    method: Optional['Method']=None
    params: Optional[dict[str,Any]]=None
    result: Optional[dict[str,Any]]=None
    error: Optional[dict[str,Any]]=None

    model_config=ConfigDict(extra='allow')

class JSONRPCNotification(BaseModel):
    jsonrpc: str=Field(default="2.0")
    method: Optional['Method']=None
    params: Optional[dict[str,Any]]=None

class Method(str,Enum):
    # Ping
    PING = "ping"

    # Initialize
    INITIALIZE = "initialize"

    # Resource methods
    RESOURCES_LIST = "resources/list"
    RESOURCES_READ = "resources/read"
    RESOURCES_SUBSCRIBE = "resources/subscribe"
    RESOURCES_TEMPLATES_LIST = "resources/templates/list"

    # Tool methods
    TOOLS_LIST = "tools/list"
    TOOLS_CALL = "tools/call"

    # Prompt methods
    PROMPTS_LIST = "prompts/list"
    PROMPTS_GET = "prompts/get"

    # Notification methods
    NOTIFICATION_PROMPTS_LIST_CHANGED = "notifications/prompts/list_changed"
    NOTIFICATION_INITIALIZED = "notifications/initialized"
    