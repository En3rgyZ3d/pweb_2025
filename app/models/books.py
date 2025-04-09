from pydantic import BaseModel,Field
from typing import Annotated


class Book(BaseModel):
    id : int
    title: str
    author: str
    review: Annotated[int | None, Field(ge=1, le=5)] = None #int oppure None come tipo, usiamo come default None ; ge -> greater or equal, le-> less or equal



book = Book(id=1, title="Titolo", author= "Autore", review=4)
print(book)