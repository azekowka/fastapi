from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
 ]

@app.get("/", summary="Root endpoint", tags=["General documentation"])
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/books", summary="Get all books", tags=["Books"])
def get_books():
    return books

@app.get("/books/{book_id}", summary="Get a book by ID", tags=["Books"])
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return {"error": "Book not found"}, 404

class NewBook(BaseModel):
    title: str
    author: str
    id: int

@app.post("/books", summary="Add a new book", tags=["Books"])
def add_book(new_book: NewBook):
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author
    })
    return {"message": "Book added successfully", "book": new_book}

if __name__ == "__main__":
    uvicorn.run(app, reload=True)