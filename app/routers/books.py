from fastapi import APIRouter, Path, HTTPException, Query, Form
#from pydantic import ValidationError

from ..models.book import Book, BookCreate, BookPublic
from ..models.review import Review
from typing import Annotated
from ..data.db import SessionDep
from sqlmodel import select,delete

router = APIRouter(prefix="/books")

@router.get("/")
def get_all_books(
        session: SessionDep,
        sort: Annotated[bool, Query(description="Sort books by their review")] = False
    ) -> list[BookPublic]:
    """Returns the list of available books."""
    books = session.exec(select(Book)).all()
    # Restituiamo una lista dei valori perché restituire solamente i valori senza convertire in una lista rende
    # impossibile la trasformazione a json, in quanto l'oggetto restituito sarebbe dict_values (che FastAPI non può
    # serializzare).
    # In alternativa si può restituire il dizionario stesso
    if sort:
        return sorted(list(books.values()), key=lambda book: book.review) # Se vero, restituiamo una lista ordinata per book review
    else:
        return list(books.values())

@router.get("/{id}")
def get_book_by_id(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to get")]
    ) -> BookPublic:
    """Returns the book with the given ID."""
    book = session.get(Book, id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.post("/{id}/review")
def add_review(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to which add the review")],
    review: Review
    ):
    """Adds a review to the book with the given ID."""
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    book.review = review.review
    session.commit()
    return "Review successfully added"

@router.post("/")
def add_book(session: SessionDep, book: BookCreate):
    """Adds a new book."""
    session.add(Book.model_validate(book))
    session.commit()
    return "Book successfully added"

@router.put("/{id}")
def update_book(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to update")],
    new_book: BookCreate
    ):
    """Updates the book with the given ID."""
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404,detail="Booknotfound")
    book.title = new_book.title
    book.author = new_book.author
    book.review = new_book.review
    session.add(book)
    session.commit()
    return "Book successfully updated"

@router.delete("/")
def delete_all_books(session: SessionDep):
    """Deletes all the stored books."""
    session.exec(delete(Book))
    session.commit()
    return "All books successfully deleted"
@router.delete("/{id}")
def delete_book(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to delete")]
    ):
    """Deletes the book with the given ID."""
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return "Book successfully deleted"

@router.post("_form/")
def add_book_from_form(
    session: SessionDep,
    book: Annotated[BookCreate, Form()]
    ):
    """Adds a new book."""
    session.add(Book.model_validate(book))
    session.commit()
    return "Book successfully added"