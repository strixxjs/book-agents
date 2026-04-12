# 📚 Book Agents — Agent within Agents

A learning project for building multi-agent systems in Python. Generates a full book using a hierarchy of AI agents.

## How it works

```
OrchestratorAgent
    └── PlotAgent      — creates plot, characters and chapter plan
    └── ChapterAgent   — writes the text for each chapter
```

The result is saved to `output/book.md`.

## Tech Stack

- Python 3.11+
- LangChain + LangGraph
- Groq API (free tier)
- Pydantic

## Getting Started

```bash
git clone https://github.com/strixxjs/book-agents
cd book-agents

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_api_key_here
```

Run:
```bash
python main.py
```

## Project Structure

```
book-agents/
├── agents/
│   ├── orchestrator.py   # main agent
│   ├── plot_agent.py     # plot agent
│   └── chapter_agent.py  # chapter writing agent
├── models/
│   └── schemas.py        # Pydantic models
├── tools/
│   └── agent_tools.py    # tools for agents
├── output/               # generated books
└── main.py               # entry point
```
