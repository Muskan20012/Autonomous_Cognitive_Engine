from typing import Annotated, TypedDict, List, Dict, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    todos: List[str]
    completed_todos: List[str]
    current_todo: Optional[str]
    virtual_fs: Dict[str, str]
