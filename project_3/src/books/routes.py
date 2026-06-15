from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.books.schemas import Book, BookUpdateModel
from src.books.book_data import books

app = APIRouter(
    prefix="/books",
    tags=["Books"]
)



@app.get("/", response_model=List[Book])
async def get_all_books():
    return books


@app.post("/", status_code=201)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book


@app.get("/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")

  

@app.put("/{book_id}")
async def update_book(book_id: int,book_update_data:BookUpdateModel) -> dict:

    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/{book_id}",status_code=204)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(status_code=404, detail="Book not found")