from langchain_core.tools import tool
import json
from models.schemas import PlotOutline
from agents.chapter_agent import run_chapter_agent
from agents.plot_agent import run_plot_agent

@tool
def generate_book_title(topic: str, genre: str) -> str:
    """Генерує назву книжки на основі теми та жанру."""
    return f"Book about {topic} in {genre}"


@tool
def create_plot(topic: str, genre: str) -> str:
    """Створює детальний сюжет книжки з персонажами та планом розділів."""
    plot = run_plot_agent(topic, genre)
    return plot.model_dump_json()


@tool
def create_chapter(plot_json: str, chapter_title: str, chapter_number: int) -> str:
    """Пише текст одного розділу книжки на основі сюжету та назви розділу."""
    plot_data = json.loads(plot_json)
    plot = PlotOutline(**plot_data)

    chapter = run_chapter_agent(plot, chapter_title, chapter_number)
    return chapter.model_dump_json()