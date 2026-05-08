import asyncio
from models.schemas import BookRequest, FinalBook
from agents.plot_agent import run_plot_agent
from agents.chapter_agent import run_chapter_agent
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

books = []

class Book(BaseModel):
    title: str
    author: str

@app.get("/api/books")
def get_books():
    return books


@app.post("/api/books", status_code = 201)
def create_book(book: Book):
    books.append(book.dict())
    return book

@app.get("/api/books/{book_id}")
def get_book(book_id: int):
    if book_id >= len(books):
        raise HTTPException(status_code=404)
    return books[book_id]


@app.put("/api/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id >= len(books):
        raise HTTPException(status_code=404)
    books[book_id] = book.dict()
    return books[book_id]


@app.delete("/api/books/{book_id}", status_code = 204)
def delete_book(book_id: int):
    if book_id >= len(books):
        raise HTTPException(status_code=404)
    books.pop(book_id)


@app.post("/generate", status_code = 201)
async def generate(request: BookRequest):
    plot = await run_plot_agent(request.topic, request.genre)

    tasks = []
    for i, chapter_title in enumerate(plot.chapters_plan[:request.num_chapters], 1):
        tasks.append(run_chapter_agent(plot, chapter_title, i))
    chapters = await asyncio.gather(*tasks)

    return FinalBook(request=request, plot=plot, chapters=chapters)