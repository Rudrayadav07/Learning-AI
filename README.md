# AI Learning

Practice projects and notes organized by week.

## Structure

```text
week1/
  day1/
    hello_llm.py
    pyproject.toml
    uv.lock
    src/day1/
week2/
week3/
week4/
week5/
week6/
week7/
week8/
```

Each day can contain its own Python project and dependencies. Local virtual environments and API keys are ignored by Git.

## Start a lesson

```powershell
cd week1/day1
uv sync
uv run python hello_llm.py
```

Copy `.env.example` to `.env` and add your API key before running a lesson that uses an external API. Never commit `.env`.
.
