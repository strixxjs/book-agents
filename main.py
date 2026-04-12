import os
from dotenv import load_dotenv
from agents.orchestrator import run_orchestrator
from rich import print as rprint

load_dotenv()

def main():
    result = run_orchestrator("Придумай назву для книжки про космічних козаків")
    rprint(f"[bold green][Результат]:[/bold green] {result}")

if __name__ == "__main__":
    main()
