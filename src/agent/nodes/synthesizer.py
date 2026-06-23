from langchain_core.messages import SystemMessage
from src.core.llm import get_llm
from src.agent.state import AgentState
from src.tools.file_system import read_file, ls

def synthesizer_node(state: AgentState) -> dict:
    """Generates the final comprehensive output."""
    llm = get_llm()
    
    system_msg = SystemMessage(
        content="You are a synthesizer agent. Your task is to look at the completed TODOs and "
                "any files in the virtual file system to generate a final comprehensive output for the user. "
                "If you need to read files to get the full context, use the read_file tool. Then output the final response."
    )
    
    synthesizer_llm = llm.bind_tools([read_file, ls])
    
    messages = [system_msg] + state["messages"]
    response = synthesizer_llm.invoke(messages)
    
    return {"messages": [response]}
