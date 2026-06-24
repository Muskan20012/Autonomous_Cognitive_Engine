import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.agent.graph import main_graph
from langchain_core.messages import HumanMessage

def run_app():
    st.set_page_config(page_title="Deep Cognitive Agent", layout="wide")

    st.title("Autonomous Cognitive Engine")

    st.markdown("""
    This is a demonstration of the LangGraph-based deep cognitive agent.
    It features task planning, a virtual file system for context offloading, and sub-agent delegation.
    """)

    user_query = st.text_area("Enter your complex task:", height=150)

    if st.button("Run Agent") and user_query:
        with st.spinner("Agent is running..."):
            initial_state = {
                "messages": [HumanMessage(content=user_query)],
                "todos": [],
                "completed_todos": [],
                "current_todo": None,
                "virtual_fs": {}
            }
            
            final_response = None
            
            # Display agent progress
            st.markdown("### Agent Progress")
            
            for event in main_graph.stream(initial_state, stream_mode="updates"):
                for node, state_update in event.items():
                    with st.expander(f"Step completed by: {node}", expanded=False):
                        if "current_todo" in state_update:
                            st.write(f"**Current TODO:** {state_update['current_todo']}")
                        if "todos" in state_update:
                            st.write(f"**Plan:** {state_update['todos']}")
                        if "messages" in state_update and state_update["messages"]:
                            msg = state_update["messages"][-1]
                            if hasattr(msg, "content") and msg.content:
                                st.write(msg.content)
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                st.write("🔧 Tool Calls:", msg.tool_calls)
                            
                            if node == "synthesizer":
                                final_response = msg.content
                                
            if final_response:
                st.markdown("### Final Output")
                st.markdown(final_response)

if __name__ == "__main__":
    run_app()
