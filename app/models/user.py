from sqlmodel import SQLModel, Field

from datetime import date

class BaseUser(SQLModel):
    name: str
    birth_date: date
    city: str

class User(BaseUser, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Come valore di default, racchiudiamo tutto in Field così che
    # possiamo specificare il metadato che id è primary key.


class UserPublic(BaseUser):
    pass
