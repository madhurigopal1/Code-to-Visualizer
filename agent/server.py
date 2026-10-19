from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from agent.agent import make_agent, code_search

app = FastAPI(title="Repo Agent API")

class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
async def ask(req: QueryRequest):
    # If langchain isn't installed, fall back to code search
    try:
        agent = make_agent()
    except Exception as e:
        # fallback
        return {"answer": "langchain not available; returning code search results.", "results": code_search(req.query)}

    try:
        answer = agent.run(req.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
