from langchain_core.tools import tool

@tool
def generate_book_title(topic: str, genre: str) -> str:
    """Генерує назву книжки на основі теми та жанру."""
    return f"Book about {topic} in {genre}"