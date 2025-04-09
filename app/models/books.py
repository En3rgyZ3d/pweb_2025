from pydantic import BaseModel,Field
from typing import Annotated


class Book(BaseModel):
    id : int
    title: str
    author: str
    review: Annotated[str, Field(ge=1, le=5)]



book = Book(id=1, title="Titolo", author= "Autore", review=4)
print(book)