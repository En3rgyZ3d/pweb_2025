from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .routers import books

app = FastAPI()
app.include_router(books.router, tags=["books"]) #il campo tags riporta il nome dell'endpoint (serve per la docs)

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse, tags=["HTML Responses"])
def home(request: Request): # Aggiungiamo il parametro alla funzione in modo che la funzione riceva la richiesta http
    '''Returns the home page.'''


    # Ovviamente lavorare con python in stringhe è abominevole, quindi si restituiscono i file HTML nella cartella templates.
    return templates.TemplateResponse(
        name = "home.html", request =request
    ) #TODO: Comprendere perché è così 💀
