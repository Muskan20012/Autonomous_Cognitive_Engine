from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import Literal

from src.agent.state import AgentState
from src.agent.nodes.planner import planner_node
from src.agent.nodes.executor import executor_node
from src.agent.nodes.synthesizer import synthesizer_node

from src.tools.file_system import read_file, write_file, edit_file, ls
from src.tools.web_search import web_search
from src.tools.delegation import delegate_task

# Tool node for executor
executor_tools = [read_file, write_file, edit_file, ls, web_search, delegate_task]
executor_tool_node = ToolNode(executor_tools)

# Tool node for synthesizer
synthesizer_tools = [read_file, ls]
synthesizer_tool_node = ToolNode(synthesizer_tools)

def router(state: AgentState) -> Literal["executor", "synthesizer", "executor_tools", "synthesizer_tools", "next_todo", "__end__"]:
    """Routes the agent based on the state."""
    messages = state.get("messages", [])
    if not messages:
        return END

    last_message = messages[-1]

    # If the last message is a tool call
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        if state.get("current_todo"):
            return "executor_tools"
        else:
            return "synthesizer_tools"

    # If we just finished a tool call from executor, go back
    if last_message.type == "tool":
        if state.get("current_todo"):
            return "executor"
        else:
            return "synthesizer"

    # If no tool calls and we are in executor, move to next todo
    if state.get("current_todo"):
        return "next_todo"
    
    # If in synthesizer and no tool calls, we are done
    return END

def next_todo_node(state: AgentState) -> dict:
    """Updates the state with the next TODO."""
    todos = state.get("todos", [])
    completed_todos = state.get("completed_todos", [])
    current_todo = state.get("current_todo")
    
    if current_todo and current_todo not in completed_todos:
        completed_todos.append(current_todo)
        
    pending_todos = [t for t in todos if t not in completed_todos]
    
    if pending_todos:
        next_todo = pending_todos[0]
        return {"completed_todos": completed_todos, "current_todo": next_todo}
    else:
        return {"completed_todos": completed_todos, "current_todo": None}

def main_router(state: AgentState) -> Literal["executor", "synthesizer"]:
    """Routes after next_todo_node."""
    if state.get("current_todo"):
        return "executor"
    return "synthesizer"

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", planner_node)
    # workflow.add_node("next_todo", next_todo_node)
    # workflow.add_node("executor", executor_node)
    # workflow.add_node("executor_tools", executor_tool_node)
    # workflow.add_node("synthesizer", synthesizer_node)
    # workflow.add_node("synthesizer_tools", synthesizer_tool_node)
    
    workflow.set_entry_point("planner")
    
    # Temporarily end after planning for Milestone 1
    workflow.add_edge("planner", END)
    
    # workflow.add_edge("planner", "next_todo")
    # workflow.add_conditional_edges(
    #     "next_todo",
    #     main_router,
    #     {
    #         "executor": "executor",
    #         "synthesizer": "synthesizer"
    #     }
    # )
    # workflow.add_conditional_edges(
    #     "executor",
    #     router,
    #     {
    #         "executor_tools": "executor_tools",
    #         "next_todo": "next_todo",
    #         END: END
    #     }
    # )
    # workflow.add_edge("executor_tools", "executor")
    # workflow.add_conditional_edges(
    #     "synthesizer",
    #     router,
    #     {
    #         "synthesizer_tools": "synthesizer_tools",
    #         END: END
    #     }
    # )
    # workflow.add_edge("synthesizer_tools", "synthesizer")
    
    return workflow.compile()

main_graph = build_graph()
