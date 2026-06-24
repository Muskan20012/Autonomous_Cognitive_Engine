import os
import sys
import subprocess
import streamlit as st

def main():
    # If running inside Streamlit, render the app UI
    if st.runtime.exists():
        # Inject LangSmith secrets into os.environ BEFORE importing any LangChain modules
        try:
            for key in ["LANGCHAIN_API_KEY", "LANGCHAIN_TRACING_V2", "LANGCHAIN_PROJECT"]:
                if key in st.secrets:
                    os.environ[key] = str(st.secrets[key])
        except Exception:
            pass

        from src.ui.app import run_app
        run_app()
    else:
        # If running via normal python, bootstrap Streamlit
        print("Bootstrapping Streamlit UI...")
        subprocess.run(["streamlit", "run", __file__])

if __name__ == "__main__":
    main()
