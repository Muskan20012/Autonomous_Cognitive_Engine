# Autonomous Cognitive Engine

A stateful LangGraph-based AI agent capable of deep research and long-horizon tasks through memory, planning, and multi-agent collaboration.

## Features
- **Structured Task Planning**: Decomposes requests into sub-tasks (TODOs).
- **Context Management**: Virtual file system (`workspace` folder) for reading/writing intermediate notes.
- **Sub-Agent Delegation**: Supervisor delegates specific tasks to specialized sub-agents.
- **Stateful Architecture**: Uses LangGraph's StateGraph to manage workflow.
- **UI**: Streamlit application.

## Setup
1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your API keys (Groq, Tavily, LangSmith).
3. Run the application:
   ```bash
   python main.py
   ```
