from langchain_groq import ChatGroq
from src.core.config import config

def get_llm(model_name: str = "llama-3.1-8b-instant", temperature: float = 0):
    """Returns an instance of the Groq LLM."""
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    
    return ChatGroq(
        api_key=config.GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature
    )
