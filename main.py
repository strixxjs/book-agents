import os
from dotenv import load_dotenv
from agents.orchestrator import run_orchestrator
from rich import print as rprint

load_dotenv()

def main():
    query = "Використай інструмент create_plot з topic='космічні козаки' та genre='фантастика' і покажи повний результат"

    result = run_orchestrator(query)

    rprint("\n[bold cyan]=== Сюжет вашої майбутньої книги ===[/bold cyan]")
    print(result)

if __name__ == "__main__":
    main()
