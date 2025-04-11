from typing import Annotated
from pydantic import BaseModel, Field


class Review(BaseModel):
    review: Annotated[int, Field(ge=1, le=5)]
    # Non specifico valore di default perché voglio forzare chi utilizza
    # questa API a mettere un valore per il libro
    # Se viene fatta una richiesta post senza campo review, viene restituito un errore
    # I modelli di Pydantic sono automaticamente convertiti in JSON, in quanto FastAPI tratta tutti i dati come file JSON
    # Legge le richieste in HTTP, li converte in tipi di dato Python, e poi per elaborare le risposte
    # effettua il meccanismo opposto, ovvero prende i tipi di dato di Python e li converte in JSON.