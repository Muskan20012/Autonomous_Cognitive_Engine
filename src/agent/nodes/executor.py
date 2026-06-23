from langchain_core.messages import SystemMessage
from src.core.llm import get_llm
from src.agent.state import AgentState
from src.tools.file_system import read_file, write_file, edit_file, ls
from src.tools.web_search import web_search
from src.tools.delegation import delegate_task

def executor_node(state: AgentState) -> dict:
    """Executes the current TODO."""
    llm = get_llm()
    tools = [read_file, write_file, edit_file, ls, web_search, delegate_task]
    agent_llm = llm.bind_tools(tools)
    
    current_todo = state.get("current_todo")
    
    system_msg = SystemMessage(
        content=f"You are an executor agent. Your current task is: {current_todo}\n\n"
                f"You have access to file system tools (ls, read_file, write_file, edit_file) "
                f"to save and retrieve context. You can also search the web or delegate complex tasks."
    )
    
    messages = [system_msg] + state["messages"]
    response = agent_llm.invoke(messages)
    
    return {"messages": [response]}
