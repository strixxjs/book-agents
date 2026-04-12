import os
from models.schemas import BookRequest, PlotOutline, Chapter, FinalBook
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from rich import print as rprint

from tools.agent_tools import generate_book_title

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature = 0.7,
    groq_api_key = GROQ_API_KEY
)


llm_with_tools = llm.bind_tools([generate_book_title])

def main():
    messages = [
        SystemMessage(content="Ти творчий письменник. Відповідай українською мовою."),
        HumanMessage(content="Придумай назву для книжки про космічних козаків")
    ]
    try:
        response = llm_with_tools.invoke(messages)

        if response.tool_calls:
            tool_call = response.tool_calls[0]
            result = generate_book_title.invoke(tool_call["args"])
            rprint(f"[bold yellow][Tool result]:[/bold yellow] {result}")

        rprint(f"[Tool calls]: {response.tool_calls}")
        answer = response.content
        rprint(f"\n[bold green][LLM відповів]:[/bold green] [italic]{answer}[/italic]\n")
    except Exception as e:
        print(f"[bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    main()
