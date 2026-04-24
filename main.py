import os
import sys
import json
import asyncio
from dotenv import load_dotenv
from rich import print as rprint
from rich.progress import track

from agents.plot_agent import run_plot_agent
from agents.chapter_agent import run_chapter_agent
from models.schemas import FinalBook, BookRequest


def safe_input(prompt: str) -> str:
    sys.stdout.write(prompt)
    sys.stdout.flush()
    raw = sys.stdin.buffer.readline().rstrip(b'\r\n')
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('cp1251')

load_dotenv()

def save_book(book: FinalBook):
    os.makedirs("output", exist_ok=True)
    path = "output/book.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {book.plot.title}\n\n")
        f.write(f"**Жанр:** {book.request.genre}\n\n")
        f.write(f"**Синопсис:** {book.plot.synopsis}\n\n")
        f.write(f"**Персонажі:** {', '.join(book.plot.characters)}\n\n")
        f.write("---\n\n")
        for chapter in book.chapters:
            f.write(f"## Розділ {chapter.number}: {chapter.title}\n\n")
            f.write(f"{chapter.content}\n\n")
    rprint(f"[bold green]Книжку збережено:[/bold green] {path}")


async def main():
    rprint("[bold cyan]Ласкаво просимо до Book Agents! 📚[/bold cyan]")
    topic = safe_input("Введіть тему книжки: ")
    genre = safe_input("Введіть жанр (фантастика, детектив, пригоди...): ")
    num_chapters = int(safe_input("Кількість розділів (1-5): "))

    request = BookRequest(
        topic=topic,
        genre=genre,
        num_chapters=num_chapters
    )

    rprint("[bold cyan]Крок 1: Створюю сюжет...[/bold cyan]")
    plot = await run_plot_agent(request.topic, request.genre)
    rprint(f"[green]✓ Назва:[/green] {plot.title}")
    rprint(f"[green]✓ Персонажі:[/green] {', '.join(plot.characters)}")

    chapters = []
    rprint("\n[bold cyan]Крок 2: Пишу розділи...[/bold cyan]")
    tasks = []
    for i, chapter_title in enumerate(plot.chapters_plan[:request.num_chapters], 1):
        tasks.append(run_chapter_agent(plot, chapter_title, i))
        rprint(f"[yellow]→ Пишу розділи {i}: {chapter_title}[/yellow]")

    chapters = await asyncio.gather(*tasks)
    rprint(f"[green]✓ Всі {len(chapters)} розділи готові[/green]")

    book = FinalBook(request=request, plot=plot, chapters=chapters)


    rprint("\n[bold cyan]Крок 3: Зберігаю книжку...[/bold cyan]")
    save_book(book)

    rprint("\n[bold magenta]🎉 Книжка готова![/bold magenta]")
    rprint(f"[bold]Розділів написано:[/bold] {len(chapters)}")


if __name__ == "__main__":
    asyncio.run(main())