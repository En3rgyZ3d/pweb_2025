from fastapi import FastAPI
from .models.books import Book
from .data.books import books
app = FastAPI()
@app.get ("/books")
def get_all_books() -> list[Book]: # -> list[Book] è un'annotazione per indicare che restituirà una lista utilizzato da pydantic come controllo del typing
    '''Returns the list of available books.'''

    # Restituiamo una lista dei valori perché restituire solamente i valori senza convertire in una lista rende
    # impossibile la trasformazione a json, in quanto l'oggetto restituito sarebbe dict_values (che FastAPI non può
    # serializzare).

    return list(books.values())

