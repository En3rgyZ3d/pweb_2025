from typing import Annotated, Optional
from sqlmodel import SQLModel, Field




class BookBase(SQLModel):
    title: str
    author: str
    review: Annotated[Optional[int], Field(ge=1, le=5)] = None #int oppure None come tipo, usiamo come default None ; ge -> greater or equal, le-> less or equal
    # Non è possibile usare la richiesta POST senza il campo review, in quanto non verranno incontrate le condizioni
    # dettate da Field(). In questi casi, si omette il campo Field e si fa la validazione successivamente.


class Book(BookBase, table=True):
    id:int = Field(default=None, primary_key=True)

class BookCreate(BookBase): # schema per creare un nuovo libro
    pass
class BookPublic(BookBase): # schema per restituire le info di un libro
    id:int