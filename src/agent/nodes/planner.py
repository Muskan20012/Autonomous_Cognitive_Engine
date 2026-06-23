from langchain_core.messages import SystemMessage
from src.core.llm import get_llm
from src.agent.state import AgentState
from src.tools.planning import write_todos

def planner_node(state: AgentState) -> dict:
    """Analyzes the request and generates a list of TODOs."""
    llm = get_llm()
    planner_llm = llm.bind_tools([write_todos])
    
    system_msg = SystemMessage(
        content=(
            "You are a planning agent for a deep research and long-horizon task framework. "
            "Your sole objective is to analyze the user's request and break it down into a detailed, sequential, "
            "and logical plan consisting of actionable sub-tasks (TODOs). You must use the 'write_todos' tool to submit this plan.\n\n"
            "Guidelines for a good plan:\n"
            "1. Break the user's complex request into a clear sequence of steps (e.g., gathering information, analyzing findings, drafting sections, compiling the final output).\n"
            "2. Keep each sub-task focused, atomic, and easy for an execution agent to understand.\n"
            "3. Do not try to perform the task or answer the question yourself. Focus strictly on structuring the work.\n"
            "4. Ensure that completing all listed TODOs will fully and accurately address the user's request."
        )
    )
    
    messages = [system_msg] + state["messages"]
    
    response = planner_llm.invoke(messages)
    
    # Extract the TODOs from the tool call
    todos = []
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "write_todos":
                todos = tool_call["args"].get("todos", [])
                
    if not todos:
        # Fallback if the LLM didn't use the tool properly
        todos = ["Process the user request directly."]
        
    return {"todos": todos, "completed_todos": [], "messages": [response]}
