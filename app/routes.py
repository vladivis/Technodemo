from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Book
from pydantic import BaseModel

#from .producer import send_event

router = APIRouter()

class BookRequest(BaseModel):
    title: str
    author: str

@router.post("/books/")
def create_book(book_request: BookRequest, db: Session = Depends(get_db)):
    book = Book(title=book_request.title, author=book_request.author)
    db.add(book)
    db.commit()
    db.refresh(book)
    #send_event({"action": "create_book", "book": {"id": book.id, "title": book.title, "author": book.author}})
    return book

@router.get("/books/")
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
