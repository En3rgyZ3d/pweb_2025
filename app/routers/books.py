from fastapi import APIRouter, Path, HTTPException, Query
from pydantic import ValidationError

from ..models.book import Book
from ..models.review import Review
from ..data.books import books
from typing import Annotated


router = APIRouter(prefix="/books")

@router.get("/")
def get_all_books(
        sort: Annotated[bool, Query(description="Whether to sort the books by review")] = False # Query parameter

) -> list[Book]: # -> list[Book] è un'annotazione per indicare che restituirà una lista utilizzato da pydantic come controllo del typing
    '''Returns the list of available books.'''

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
        id: Annotated[int, Path(description="The ID of the book to get")]
        )-> Book:
    '''Returns the book with the given id.'''
    try:
        return books[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")

@router.post("/{id}/review") #L'ordine dei parametri non conta, è FastAPI che riconosce dove va messo cosa
def post_review(
        id: Annotated[int, Path(description="The ID of the book to review")],
        review: Review
        ):
    '''Adds a review to the book with the given id.'''
    try:
        books[id].review = review.review
        return "Review added successfully"
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")
    # Non serve aggiungere altri except, in quanto utilizzando Pydantic, se la richiesta non è valida avremo già un errore
    # Se c'è un errore di validazione di pydantic, non si arriva nemmeno a eseguire questa parte di codice
    # In quanto nell'inizializzazione dei vincoli della classe Review, si ha un errore
    # Non è possibile rispettare le specifiche con l'errore (sovrascrivere con errore 400 non è di interesse al momento)


@router.post("/")
def add_book(book: Book):
    '''Adds a new book.'''
    if book.id in books:
        raise HTTPException(status_code=403, detail="Book ID already exists")
    books[book.id] = book # si ricorda che books è un dizionario
    return "Book added successfully"

@router.put("/{id}")
def update_book(
        id: Annotated[int, Path(description="The ID of the book to update")],
        book: Book
        ):
    '''Updates the book with the given id.'''

    if book.id != id:
        raise HTTPException(status_code=403, detail="Book ID does not match")
    try:
        books[id] = book
        return "Book updated successfully"
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/")
def delete_all_books():
    '''Deletes all books.'''
    books.clear()
    return "All books deleted successfully"

@router.delete("/{id}")
def delete_book_by_id(
        id: Annotated[int, Path(description="The ID of the book to delete")]
        ):
    '''Deletes the book with the given id.'''
    try:
        del books[id]
        return "Book deleted successfully"
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")