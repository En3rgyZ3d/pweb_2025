from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles

from .routers import books, frontend
app = FastAPI()
app.include_router(books.router, tags=["books"]) #il campo tags riporta il nome dell'endpoint (serve per la docs)

app.include_router(frontend.router, tags=["frontend"])
app.mount("/static", StaticFiles(directory="static"), name="static")
# il primo parametro è l'url della web app dove possono essere recuperate le risorse
# il secondo è il percorso della cartella dove si possono recuperare i file
# il terzo è un tag identificativo