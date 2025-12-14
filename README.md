# Explore MCP

This repo runs a local MCP (Model Context Protocol) server, verifies tool connectivity with a client, and demonstrates OpenAI tool-calling integration.

## Prerequisites
- Python 3.13 (per `pyproject.toml`).
- Linux/macOS shell (commands shown for bash).
- An OpenAI API key.
- Dependencies listed in `pyproject.toml`.

## Install dependencies
You can use uv, poetry, or pip. Pick one approach.

### Option A: uv (fast, recommended)
```bash
# If uv is not installed, see https://docs.astral.sh/uv/getting-started/
uv sync
```

### Option B: poetry
```bash
poetry install
poetry shell
```

### Option C: pip + venv
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt .
```

## Set OpenAI API key
The script `utils/helpers.py` expects your key in a file at:

- `~/.llm_secrets` with content like:

```text
OPENAI_API_KEY=sk-...
```

Alternatively, you can set the environment variable directly in your shell before running the OpenAI test:

```bash
export OPENAI_API_KEY=sk-...
```

Note: `call_my_mcp2.py` imports `get_api_key()` and sets `os.environ["OPENAI_API_KEY"]` internally using the `~/.llm_secrets` file. If that file is missing, set the env var as shown above or create the file.

## Start the MCP server
This launches the FastAPI app serving the MCP endpoint at `http://127.0.0.1:8000/mcp`.

```bash
python mcp_server.py
```

Expected log: uvicorn starts and listens on port 8000.

## Health check: MCP client
In a separate terminal (while the server is running), verify connectivity and tool discovery.

```bash
python mcp_client_check.py
```

Expected output: A tools list including `ping`, `add`, and `subtract`.

## OpenAI integration test
With the server running and your OpenAI key available, run the LLM orchestration demo:

```bash
python mcp_llm_mode2.py
```

What it does:
- Discovers MCP tools from the server.
- Provides those tools to the OpenAI Chat Completions API.
- Lets the model call `add` and returns the final answer.

Expected: The printed result of adding two numbers (e.g., `68` for 23 + 45).

### Notes
- The script uses model `gpt-5`. If this model is not available on your account, change it inside `call_my_mcp2.py` to a model you have access to (e.g., `gpt-4.1-mini` or another supported tools-capable model).
- Ensure the server URL in `call_my_mcp2.py` and `mcp_client_check.py` matches `http://127.0.0.1:8000/mcp`.
- If port 8000 is in use, edit `mcp_server.py` to run uvicorn on a different port and update the client scripts accordingly.

## Files
- `mcp_server.py`: FastAPI + FastMCP server exposing tools: `ping`, `add`, `subtract`.
- `mcp_client_check.py`: Async client that pings the server and lists tools.
- `call_my_mcp2.py`: Orchestrates an OpenAI chat with MCP tools.
- `utils/helpers.py`: Utility to load the OpenAI API key from `~/.llm_secrets` or set env vars from a JSON file.

