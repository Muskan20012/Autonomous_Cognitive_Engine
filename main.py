import os
import sys
import subprocess
import streamlit as st

def main():
    # If running inside Streamlit, render the app UI
    if st.runtime.exists():
        from src.ui.app import run_app
        run_app()
    else:
        # If running via normal python, bootstrap Streamlit
        print("Bootstrapping Streamlit UI...")
        subprocess.run(["streamlit", "run", __file__])

if __name__ == "__main__":
    main()
