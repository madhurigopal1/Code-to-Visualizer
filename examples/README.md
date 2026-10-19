# Examples for running the agent

1) CLI (no LLM required):
   python agent/agent.py -q "find visualization code"

2) Run server (with langchain + OPENAI_API_KEY set):
   uvicorn agent.server:app --reload --port 8000

3) Example query using curl:
   curl -s -X POST http://localhost:8000/ask -H 'Content-Type: application/json' -d '{"query":"Where is the visualization HTML?"}' | jq
