**LPGIC — Multi-Tool College Assistant**

A compact Python project that routes user queries to deterministic utility tools (attendance, results, fee balance, library fine, hostel fee, student lookup) and can optionally use a Groq-based LLM to decide which tool to call.

**Prerequisites:**

- Python 3.10+ installed
- A virtual environment (recommended)
- A valid `GROQ_API_KEY` stored in a `.env` file at the project root

**Files of interest:**

- **`src.py`**: Consolidated single-file implementation (tools, schemas, Groq client, agent, demo runner).
- **`agents/multi_tool_agent.py`**: Project agent that uses the Groq client and tool-calling schema.
- **`tools/`**: Individual tool implementations used by the agent (attendance, result, fee balance, library fine, hostel fee, student info).
- **`utils/groq_client.py`**: Groq client initializer — the project expects `GROQ_API_KEY` in `.env`.
- **`demos/multi_tool.py`**: Simple runner that calls `agents.multi_tool_agent.multi_tool_agent` for a set of test queries.

**Quick setup:**

1. Create and activate a virtual env (Windows example):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# or
.\.venv\Scripts\activate.bat   # cmd
```

2. Install dependencies (adjust if you use `requirements.txt`):

```
pip install python-dotenv groq
```

3. Create a `.env` in the project root with:

```
GROQ_API_KEY=your_key_here
```

**Run the demo:**

- Using the consolidated file:

```
python src.py
```

- Using the demo runner (calls `agents/multi_tool_agent`):

```
python -m demos.multi_tool
```

**Notes & tips:**

- The Groq-driven agent returns deterministic JSON-like tool outputs (tools always return a `status` field).
- If you prefer a pure deterministic, dependency-free path, use `src.py` which bundles everything.
- `agents/multi_tool_agent.py` is wired to use `utils/groq_client.py` and the `multi_tool_schema` for function-style tool calls.
- `.gitignore` now includes common virtualenv and `__pycache__` patterns.

If you want, I can:

- Run the demo and paste the output here.
- Convert `agents/multi_tool_agent.py` to use LangChain's `create_tool_calling_agent()` and `AgentExecutor` with `@tool` wrappers — only if you request it.
