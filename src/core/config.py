import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

    # If keys are missing (common on Streamlit Cloud), attempt fallback to st.secrets
    if not GROQ_API_KEY:
        try:
            import streamlit as st
            GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
            TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY")
            LANGCHAIN_API_KEY = st.secrets.get("LANGCHAIN_API_KEY")
            
            # LangSmith strictly looks for these variables in os.environ
            for key in ["LANGCHAIN_API_KEY", "LANGCHAIN_TRACING_V2", "LANGCHAIN_PROJECT"]:
                if key in st.secrets:
                    os.environ[key] = str(st.secrets[key])
        except Exception:
            pass

config = Config()

