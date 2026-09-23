# Week 1, Day 1

This lesson sends a prompt to Groq using the `hello_llm.py` script.

## Setup

```powershell
uv sync
Copy-Item .env.example .env
```

Add your `GROQ_API_KEY` to `.env`, then run:

```powershell
uv run python hello_llm.py
```

The local `.env` file and `.venv` directory are ignored by Git.
