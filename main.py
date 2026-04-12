import os
from dotenv import load_dotenv
from agents.orchestrator import run_orchestrator
from rich import print as rprint

load_dotenv()


def main():
    query = """
    Створи сюжет для книжки про космічних козаків у жанрі фантастика.
    Потім напиши перший розділ цієї книжки.
    """

    result = run_orchestrator(query)

    rprint("\n[bold magenta]=== Результат виконання ===[/bold magenta]")

    try:
        data = json.loads(result)
        if "content" in data:
            rprint(f"[bold yellow]Розділ {data.get('number')}: {data.get('title')}[/bold yellow]")
            rprint(data.get("content"))
        else:
            rprint(data)
    except:
        rprint(result)


if __name__ == "__main__":
    main()