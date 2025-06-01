from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Annotated

from ..models import User
from ..auth.utils import get_current_user

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
]

class NewBook(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=100, description="The title of the book")
    author: str = Field(..., min_length=1, max_length=100, description="The author of the book")

    @field_validator('title')
    def title_must_be_valid(cls, v):
        if v.strip() == "":
            raise ValueError('Title cannot be empty or only whitespace')
        return v.strip()

    @field_validator('author')
    def author_must_be_valid(cls, v):
        if v.strip() == "":
            raise ValueError('Author cannot be empty or only whitespace')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger"
            }
        }

@router.get("/", summary="Get all books")
async def get_books(current_user: Annotated[User, Depends(get_current_user)]):
    return books

@router.get("/{book_id}", summary="Get a book by ID")
async def get_book(
    book_id: int,
    current_user: Annotated[User, Depends(get_current_user)]
):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.post("/", summary="Add a new book")
async def add_book(
    new_book: NewBook,
    current_user: Annotated[User, Depends(get_current_user)]
):
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author
    })
    return {"message": "Book added successfully", "book": new_book} 