from pydantic import BaseModel
from typing import List


class BookRequest(BaseModel):
    topic: str
    genre: str
    num_chapters: int
    language: str = "ukrainian"


class PlotOutline(BaseModel):
    title: str
    synopsis: str
    characters: List[str]
    chapters_plan: List[str]


class Chapter(BaseModel):
    number: int
    title: str
    content: str


class FinalBook(BaseModel):
    request: BookRequest
    plot: PlotOutline
    chapter: List[Chapter]


if __name__ == "__main__":
    test = BookRequest(topic="space", genre="fantasy", num_chapters=3)
    print(test)