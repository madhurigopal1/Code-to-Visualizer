# Agent module for repo-level code search + LangChain agent
import os
from pathlib import Path
from typing import Dict, List

try:
    from langchain.llms import OpenAI
    from langchain.agents import Tool, initialize_agent, AgentType
except Exception:
    # Imports may fail in environments without langchain installed; allow functions below to be imported for tests that don't require LLMS
    OpenAI = None
    Tool = None
    initialize_agent = None
    AgentType = None


def load_repo_files(base_path: str = ".") -> Dict[str, str]:
    """Load text files from the repository path. Returns mapping path -> content."""
    base = Path(base_path)
    files = {}
    for p in base.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".py", ".md", ".txt", ".html", ".js", ".ts", ".json", ".yaml", ".yml"}:
            try:
                files[str(p.relative_to(base))] = p.read_text(encoding="utf-8")
            except Exception:
                # skip binary or unreadable files
                continue
    return files


def code_search(query: str, base_path: str = ".", max_results: int = 5) -> List[str]:
    """Naive code search across repository files. Returns matched file paths and snippets."""
    files = load_repo_files(base_path)
    results = []
    q = query.lower()
    for path, content in files.items():
        if q in content.lower() or q in path.lower():
            snippet = content[:500].replace("\n", " ")
            results.append(f"{path}: {snippet}")
            if len(results) >= max_results:
                break
    return results


def make_agent(base_path: str = "."):
    """Create and return a LangChain agent wired with repo tools. Requires langchain and an LLM API key in env."""
    if OpenAI is None or Tool is None or initialize_agent is None:
        raise RuntimeError("langchain is not installed or imports failed. Install requirements before creating the agent.")

    # LLM from environment (e.g., OPENAI_API_KEY)
    llm = OpenAI(temperature=0)

    # Wrap tools
    def _code_search_tool(q: str) -> str:
        matches = code_search(q, base_path=base_path, max_results=5)
        return "\n---\n".join(matches) if matches else "No matches found."

    tools = [
        Tool(name="code_search", func=_code_search_tool, description="Search repository files for a query and return snippets.")
    ]

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a simple LangChain agent on this repository (CLI)")
    parser.add_argument("--query", "-q", required=True, help="Question or search query for the agent")
    parser.add_argument("--path", "-p", default=".", help="Repository base path")
    args = parser.parse_args()

    # Basic CLI fallback: if langchain isn't available, run local search
    if OpenAI is None:
        print("langchain not installed; running local code search fallback\n")
        for r in code_search(args.query, base_path=args.path):
            print(r)
    else:
        # Create agent and run
        agent = make_agent(base_path=args.path)
        resp = agent.run(args.query)
        print(resp)
