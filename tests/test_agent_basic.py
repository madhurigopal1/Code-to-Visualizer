import os
from agent.agent import load_repo_files, code_search


def test_load_repo_files_returns_dict(tmp_path):
    # create dummy files
    d = tmp_path / "repo"
    d.mkdir()
    f = d / "test.md"
    f.write_text("This repo has visualization code and examples.")

    files = load_repo_files(str(d))
    assert isinstance(files, dict)
    assert "test.md" in files


def test_code_search_matches(tmp_path):
    d = tmp_path / "repo"
    d.mkdir()
    f = d / "viz.py"
    f.write_text("function draw() { /* visualization */ }")

    results = code_search("visualization", base_path=str(d))
    assert isinstance(results, list)
    assert len(results) >= 1
