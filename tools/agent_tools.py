from langchain_core.tools import tool
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