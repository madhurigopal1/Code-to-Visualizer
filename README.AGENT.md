# Agent integration README

This branch adds a lightweight LangChain-based agent and a Langraph graph example to help interact with the repository contents.

Files added
- agent/agent.py - a simple LangChain agent wrapper + local fallback search
- agent/server.py - FastAPI app exposing POST /ask
- langraph/graph.yaml - minimal Langraph-style graph schema
- requirements.txt - dependencies for the agent demo
- .env.example - environment variable placeholders
- README.AGENT.md - this file

Quick start (local)
1. Create a virtualenv and install requirements:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Copy .env.example to .env and set OPENAI_API_KEY (if you want real LLMs).

3. Run the FastAPI server for the agent:
   uvicorn agent.server:app --reload --port 8000

4. POST a query:
   curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"query":"how does this repo visualize data"}'

Notes
- If langchain or an LLM key isn't available, the server will return results from a local code search fallback.
- The agent is intentionally simple: it demonstrates how to wire repo-aware tools into LangChain and how to expose a demo API.

Security
- Do not commit API keys. Use .env and environment variables for secrets.
- The agent uses only a read-only code search tool by default and does not execute arbitrary shell commands.

