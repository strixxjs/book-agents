import asyncio

from models.schemas import BookRequest, FinalBook
from agents.plot_agent import run_plot_agent
from agents.chapter_agent import run_chapter_agent
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token, decode_access_token
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

books = []

class Book(BaseModel):
    title: str
    author: str


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(401, "Invalid or expired token")
    else:
        return payload


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form.username, form.password)
    if user is None:
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


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
async def generate(request: BookRequest, current_user: dict = Depends(get_current_user)):
    plot = await run_plot_agent(request.topic, request.genre)

    tasks = []
    for i, chapter_title in enumerate(plot.chapters_plan[:request.num_chapters], 1):
        tasks.append(run_chapter_agent(plot, chapter_title, i))
    chapters = await asyncio.gather(*tasks)

    return FinalBook(request=request, plot=plot, chapters=chapters)