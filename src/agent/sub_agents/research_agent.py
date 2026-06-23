from langgraph.graph import StateGraph, END
from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from src.core.llm import get_llm
from src.tools.web_search import web_search
from langgraph.prebuilt import ToolNode

class SubAgentState(TypedDict):
    task: str
    messages: Annotated[List[BaseMessage], add_messages]

def research_node(state: SubAgentState) -> dict:
    llm = get_llm()
    agent_llm = llm.bind_tools([web_search])
    
    if not state.get("messages"):
        messages = [
            SystemMessage(content=f"You are a research sub-agent. Your task is: {state['task']}"),
            HumanMessage(content="Please perform the research and summarize the findings.")
        ]
    else:
        messages = state["messages"]
        
    response = agent_llm.invoke(messages)
    return {"messages": [response]}

def router(state: SubAgentState):
    messages = state.get("messages", [])
    last_message = messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

def build_research_graph():
    workflow = StateGraph(SubAgentState)
    workflow.add_node("agent", research_node)
    workflow.add_node("tools", ToolNode([web_search]))
    
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", router, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

research_graph = build_research_graph()
