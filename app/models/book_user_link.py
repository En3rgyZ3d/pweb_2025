from sqlmodel import SQLModel, Field

class BookUserLink(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id",primary_key=True)
    user_id: int = Field(foreign_key="user.id",primary_key=True)

    # Salvando entrambi come primary key, sto dicendo che ogni riga è univoca
    # (composta dalla combinazione di due valori)

    # Creiamo questa tabella che contiene tutti gli id che sono in prestito a qualcuno (normalizzazione dei db)
