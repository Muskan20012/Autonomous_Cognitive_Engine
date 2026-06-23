from langchain_community.tools.tavily_search import TavilySearchResults
from src.core.config import config

# Initialize Tavily search tool if API key is present
# Otherwise, we create a dummy tool to avoid import errors
if config.TAVILY_API_KEY:
    web_search = TavilySearchResults(max_results=3)
else:
    from langchain_core.tools import tool
    @tool
    def web_search(query: str) -> str:
        """Search the web."""
        return "TAVILY_API_KEY not configured. Web search unavailable."
