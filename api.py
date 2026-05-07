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