from langchain_core.tools import tool

@tool
def delegate_task(task_description: str) -> str:
    """Delegates a specific sub-task to the research sub-agent."""
    from src.agent.sub_agents.research_agent import research_graph
    try:
        # Invoke the sub-agent graph
        result = research_graph.invoke({"task": task_description})
        if "messages" in result and result["messages"]:
            return f"Sub-agent result: {result['messages'][-1].content}"
        return "Sub-agent finished but returned no specific messages."
    except Exception as e:
        return f"Error delegating task: {str(e)}"
