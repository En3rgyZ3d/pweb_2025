from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional


class Book(BaseModel):
    id : int
    title: str
    author: str
    review: Annotated[Optional[int], Field(ge=1, le=5)] = None #int oppure None come tipo, usiamo come default None ; ge -> greater or equal, le-> less or equal
    # Non è possibile usare la richiesta POST senza il campo review, in quanto non verranno incontrate le condizioni
    # dettate da Field(). In questi casi, si omette il campo Field e si fa la validazione successivamente.